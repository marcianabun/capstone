import functools
import logging
import re
import threading
import uuid
from datetime import timedelta

import cv2
import numpy as np
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import OuterRef, Subquery
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_encode
from django.views.decorators.http import require_POST
from PIL import Image

from src.pipeline import LensCalibration, run_image
from src.preprocessing.camera_check import camera_fault
from src.reporting.annotate import draw_availability
from src.reporting.export import MEDIA_TYPES, export
from web.forms import CameraForm, ConfigForm, PhotoForm, ReportForm, UserForm, photo_limit
from web.models import (ABIERTAS, ACTIVA, ADMIN, COMPLETADA, EN_PROCESO, JEFE, REEMPLAZADA, REPONEDOR,
                        Analysis, Camera, Config, User)

logger = logging.getLogger(__name__)

# Vista principal de cada perfil (CU00).
HOME = {ADMIN: "usuarios", JEFE: "gondolas", REPONEDOR: "alertas"}
TODOS = (ADMIN, JEFE, REPONEDOR)


def roles(*allowed):
    """Solo usuarios con sesion y uno de estos perfiles; al resto, 403."""

    def decorator(view):
        @login_required
        @functools.wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.user.role not in allowed:
                raise PermissionDenied
            return view(request, *args, **kwargs)

        return wrapper

    return decorator


@login_required
def inicio(request):
    return redirect(HOME.get(request.user.role, "alertas"))


# --- CU06: usuarios y roles ---

@roles(ADMIN)
def usuarios(request):
    users = User.objects.order_by("username").prefetch_related("groups")
    return render(request, "web/usuarios.html", {"usuarios": users})


@roles(ADMIN)
def usuario_form(request, pk=None):
    user = get_object_or_404(User, pk=pk) if pk else None
    form = UserForm(request.POST or None, instance=user, editor=request.user)
    if form.is_valid():
        saved = form.save()
        if user is None:
            return show_password_link(request, saved, creado=True)
        messages.success(request, f"Usuario {saved.username} actualizado.")
        return redirect("usuarios")
    return render(request, "web/usuario_form.html", {"form": form, "nuevo": user is None})


@require_POST
@roles(ADMIN)
def usuario_enlace(request, pk):
    """CU06: enlace nuevo para definir la contraseña (si el usuario lo perdió o venció)."""
    return show_password_link(request, get_object_or_404(User, pk=pk), creado=False)


def show_password_link(request, user, creado):
    """CU06 sin correo (#84): el Administrador ve el enlace de un solo uso (deja
    de valer cuando el usuario define su contrasena) y se lo entrega. Va en la
    respuesta y no en un mensaje, que viajaria en una cookie."""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    link = request.build_absolute_uri(reverse("definir_clave", args=[uid, default_token_generator.make_token(user)]))
    return render(request, "web/usuario_enlace.html", {"usuario": user, "enlace": link, "creado": creado})


# --- CU01: analisis de fotos ---

_model_lock = threading.Lock()


@functools.cache
def get_detector():
    """Un solo modelo por proceso: cada copia de YOLO26 ocupa cientos de MB."""
    if not settings.WEIGHTS.exists():
        raise FileNotFoundError(f"No existen los pesos {settings.WEIGHTS} (ver docs/training.md).")
    from src.models.detector import ProductDetector  # import diferido: ultralytics tarda en cargar

    return ProductDetector(settings.WEIGHTS, device="cpu")


@functools.cache
def get_person_detector():
    """None con SHELFVISION_PERSON_WEIGHTS vacia: no se busca oclusion (#77)."""
    if settings.PERSON_WEIGHTS is None:
        return None
    from src.models.people import PersonDetector

    return PersonDetector(settings.PERSON_WEIGHTS, device="cpu")


def analyze(upload, user, pasillo, gondola) -> Analysis:
    image = cv2.imdecode(np.frombuffer(upload.read(), np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("No se pudo leer la imagen.")
    fault = camera_fault(image)
    if fault:  # CU01 excepcion 1a (#87): no se analiza ni se toca la alerta abierta; queda en el registro
        logger.warning("Posible camara defectuosa en pasillo %s, gondola %s: %s", pasillo, gondola, fault)
        raise ValueError(f"Posible cámara defectuosa ({fault}): revisa la cámara de esta góndola "
                         "y vuelve a tomar la foto.")
    # CU05: umbral configurado y, si la gondola tiene camara, su calibracion de lente.
    camera = Camera.objects.filter(pasillo__iexact=pasillo, gondola__iexact=gondola).first()
    calibration = LensCalibration(**camera.calibracion) if camera and camera.calibracion else None
    with _model_lock:  # el modelo se comparte entre los hilos del servidor
        result = run_image(image, get_detector(), calibration=calibration,
                           critical_free_fraction=Config.get().umbral / 100,
                           occluder_detector=get_person_detector())
    if not result.products:  # #52: daría 100% libre y una alerta falsa; no se toca la alerta abierta
        raise ValueError("No se detectaron productos en la foto: revisa que muestre la góndola, "
                         "con luz y sin nada que la tape.")
    if result.inconclusive:  # #77: con tanto tapado no se puede afirmar un quiebre; no se toca la alerta abierta
        raise ValueError(f"La góndola está tapada en {result.occluded_fraction:.0%} (persona u objeto): "
                         "vuelve a tomar la foto cuando esté despejada.")
    _, jpg = cv2.imencode(".jpg", draw_availability(image, result, banner=False))
    analysis = Analysis(created_by=user, pasillo=pasillo, gondola=gondola, photo_name=upload.name,
                        free_fraction=result.free_fraction, critical=result.critical, result=result.to_dict())
    # La foto se guarda antes de tocar las alertas: si falla, ninguna alerta cambia (#49).
    analysis.annotated.save(f"{uuid.uuid4().hex}.jpg", ContentFile(jpg.tobytes()), save=False)
    try:
        # CU02: una gondola tiene a lo mas una alerta abierta. Con quiebre, la foto
        # nueva reemplaza a la anterior (y hereda quien la atiende); sin quiebre, la
        # foto confirma la reposicion y cierra la alerta abierta. Todo o nada: con
        # SQLite en modo IMMEDIATE, dos fotos de la misma gondola van una tras otra.
        with transaction.atomic():
            previous = Analysis.objects.select_for_update().filter(pasillo=pasillo, gondola=gondola,
                                                                   estado__in=ABIERTAS)
            last_open = previous.first()
            now = timezone.now()
            if result.critical:
                analysis.estado, analysis.taken_by = (last_open.estado, last_open.taken_by) if last_open else (ACTIVA, None)
                analysis.estado_at = last_open.estado_at if last_open else now
                previous.update(estado=REEMPLAZADA, estado_at=now)
            else:
                previous.update(estado=COMPLETADA, estado_at=now)
            analysis.save()
    except Exception:
        analysis.annotated.delete(save=False)  # sin foto huerfana
        raise
    return analysis


def analyze_paths(paths, user, pasillo, gondola):
    """#95: analiza las fotos de una ruta; una mala no frena a las demás. Devuelve
    (analisis, errores). Los mensajes llevan solo el nombre del archivo, no su ruta."""
    done, errors = [], []
    for path in paths:
        try:
            with Image.open(path) as image:
                error = photo_limit(path.stat().st_size, image.width * image.height)
        except FileNotFoundError:  # la foto desapareció: no sirve seguir
            raise
        # ImportError: con un archivo que no es imagen, Pillow nuevo intenta cargar un plugin (pi_heif).
        except (OSError, ImportError, Image.DecompressionBombError):
            errors.append(f"{path.name}: no se pudo leer la imagen.")
            continue
        try:
            if error:
                raise ValueError(error)
            done.append(analyze(SimpleUploadedFile(path.name, path.read_bytes()), user, pasillo, gondola))
        except ValueError as error:
            errors.append(f"{path.name}: {error}")
    return done, errors


@roles(ADMIN, JEFE)
def analisis(request):
    form = PhotoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        data = form.cleaned_data
        try:
            if data["foto"]:
                return redirect("analisis_detalle", analyze(data["foto"], request.user, data["pasillo"], data["gondola"]).pk)
            done, errors = analyze_paths(data["fotos"], request.user, data["pasillo"], data["gondola"])
        except (FileNotFoundError, ValueError) as error:
            form.add_error(None, str(error))
        else:
            if not errors and len(done) == 1:
                return redirect("analisis_detalle", done[0].pk)
            if not errors:
                messages.success(request, f"{len(done)} fotos analizadas en {data['pasillo']}/{data['gondola']}.")
                return redirect("analisis")
            form.add_error(None, f"{len(done)} de {len(done) + len(errors)} fotos analizadas. " + " · ".join(errors))
    page = Paginator(Analysis.objects.select_related("taken_by").order_by("-created_at", "-pk"), 25).get_page(request.GET.get("pagina"))
    return render(request, "web/analisis.html", {"form": form, "analisis": page})


def alertas_abiertas(user):
    """CU02: primero las que atiende el usuario, despues las activas de la mas
    libre a la menos, al final las que atienden otros."""
    def order(a):
        group = 0 if a.estado == EN_PROCESO and a.taken_by_id == user.pk else 1 if a.estado == ACTIVA else 2
        return group, -a.free_fraction

    return sorted(Analysis.objects.filter(estado__in=ABIERTAS).select_related("taken_by"), key=order)


@roles(*TODOS)
def alertas(request):
    return render(request, "web/alertas.html", {"alertas": alertas_abiertas(request.user), "umbral": Config.get().umbral})


@require_POST
@roles(*TODOS)
def alerta_accion(request, pk, accion):
    alert = get_object_or_404(Analysis, pk=pk)
    # El cambio solo se aplica si la alerta sigue en el estado de origen: si otra
    # foto la reemplazo o alguien la tomo entremedio, no se reabre (#49).
    pending = Analysis.objects.filter(pk=alert.pk)
    now = timezone.now()
    if accion == "tomar" and pending.filter(estado=ACTIVA).update(
            estado=EN_PROCESO, taken_by=request.user, estado_at=now):
        messages.success(request, f"Tomaste {alert.location}.")
    elif accion == "completar" and pending.filter(estado=EN_PROCESO).update(  # se toma antes de completarla
            estado=COMPLETADA, estado_at=now):
        messages.success(request, f"{alert.location} quedó como repuesta. La próxima foto lo confirmará.")
    else:
        messages.error(request, f"La alerta de {alert.location} ya cambió de estado: se muestra la lista al día.")
        return redirect("alertas")
    target = request.POST.get("next", "")
    return redirect(target if url_has_allowed_host_and_scheme(target, {request.get_host()}) else "alertas")


@roles(*TODOS)
def analisis_detalle(request, pk):
    analysis = get_object_or_404(Analysis.objects.select_related("taken_by", "created_by"), pk=pk)
    return render(request, "web/analisis_detalle.html", {"a": analysis, "nav": navegacion(analysis, request)})


def navegacion(a, request):
    """Anterior y siguiente de la foto (#94): los analisis de la misma gondola por
    fecha o, con ?desde=alertas, las alertas abiertas en el orden de CU02."""
    if request.GET.get("desde") == "alertas":
        lista = alertas_abiertas(request.user)
        i = lista.index(a) if a in lista else -1
        anterior = lista[i - 1] if i > 0 else None
        siguiente = lista[i + 1] if i + 1 < len(lista) else None
        return {"desde": "alertas", "anterior": anterior, "siguiente": siguiente, "posicion": i + 1 or None, "total": len(lista)}
    mismos = Analysis.objects.filter(pasillo=a.pasillo, gondola=a.gondola)
    return {"desde": "", "anterior": mismos.filter(created_at__lt=a.created_at).first(),
            "siguiente": mismos.filter(created_at__gt=a.created_at).order_by("created_at").first(),
            "posicion": mismos.filter(created_at__lte=a.created_at).count(), "total": mismos.count()}


@roles(*TODOS)
def analisis_imagen(request, pk):
    # Las fotos de tienda se sirven solo con sesion, no como archivos publicos.
    analysis = get_object_or_404(Analysis, pk=pk)
    if not analysis.annotated:  # borrada por antigua (RNF05, borrar_fotos)
        raise Http404
    return FileResponse(analysis.annotated.open("rb"), content_type="image/jpeg")


# --- CU04: reportes ---

@roles(ADMIN, JEFE)
def reportes(request):
    today = timezone.localdate()
    form = ReportForm(request.GET if "formato" in request.GET else None,
                      initial={"desde": today - timedelta(days=7), "hasta": today, "formato": "xlsx"})
    if form.is_valid():
        data = form.cleaned_data
        found = (Analysis.objects.filter(created_at__date__range=(data["desde"], data["hasta"]))
                 .select_related("created_by").defer("result").order_by("created_at"))
        if data["pasillo"]:
            found = found.filter(pasillo__iexact=data["pasillo"])
        if data["gondola"]:
            found = found.filter(gondola__iexact=data["gondola"])
        if found:
            rows = [{"fecha": timezone.localtime(a.created_at), "pasillo": a.pasillo, "gondola": a.gondola,
                     "free_fraction": a.free_fraction, "critical": a.critical,
                     "estado": a.get_estado_display() or "Sin quiebre",
                     "usuario": a.created_by.username if a.created_by else ""} for a in found]
            period = f"{data['desde']} a {data['hasta']}"
            fmt = data["formato"]
            response = HttpResponse(export(rows, fmt, f"Reporte de disponibilidad {period}"),
                                    content_type=MEDIA_TYPES[fmt])
            response["Content-Disposition"] = f'attachment; filename="reporte-{period.replace(" ", "-")}.{fmt}"'
            return response
        form.add_error(None, "No hay análisis en el período elegido: no se genera un archivo vacío.")
    return render(request, "web/reportes.html", {"form": form})


# --- CU05: umbral y camaras ---

@roles(ADMIN)
def configuracion(request):
    config = Config.get()
    form = ConfigForm(request.POST or None, instance=config)
    if form.is_valid():
        form.save()
        messages.success(request, "Parámetros actualizados. Rigen para las fotos siguientes.")
        return redirect("configuracion")
    return render(request, "web/configuracion.html", {"form": form, "camaras": Camera.objects.all()})


@roles(ADMIN)
def camara_form(request, pk=None):
    camera = get_object_or_404(Camera, pk=pk) if pk else None
    form = CameraForm(request.POST or None, request.FILES or None, instance=camera)
    if form.is_valid():
        saved = form.save()
        messages.success(request, f"{saved.nombre} quedó asociada a {saved.location}.")
        return redirect("configuracion")
    return render(request, "web/camara_form.html", {"form": form, "nueva": camera is None})


# --- CU03: dashboard de gondolas ---

# Una foto mas antigua que esto ya no dice como esta la gondola: "Sin datos".
RECENT = timedelta(hours=24)


def gondola_state(analysis, umbral, now) -> tuple[str, str]:
    """(clase CSS, texto) del estado de una gondola segun su ultima foto:
    quiebre si esa foto tiene alerta; en riesgo desde la mitad del umbral;
    disponible bajo la mitad; sin datos si no hay foto reciente."""
    if analysis is None or now - analysis.created_at > RECENT:
        return "ok", "Sin datos"
    if analysis.critical:
        return "activa", "Quiebre"
    if analysis.free_fraction * 100 >= umbral / 2:
        return "off", "En riesgo"
    return "completada", "Disponible"


def _natural(text: str) -> list:
    """Orden natural: "Góndola 2" antes que "Góndola 10"."""
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", text)]


@roles(*TODOS)
def gondolas(request):
    newest = (Analysis.objects.filter(pasillo=OuterRef("pasillo"), gondola=OuterRef("gondola"))
              .order_by("-created_at").values("pk")[:1])
    latest = {(a.pasillo, a.gondola): a for a in Analysis.objects.filter(pk=Subquery(newest)).defer("result")}
    for camera in Camera.objects.all():  # una camara sin fotos todavia tambien es una gondola, sin datos
        latest.setdefault((camera.pasillo, camera.gondola), None)
    umbral, now = Config.get().umbral, timezone.now()
    pasillos: dict[str, list] = {}
    for (pasillo, gondola), analysis in sorted(latest.items(), key=lambda item: (_natural(item[0][0]), _natural(item[0][1]))):
        state, label = gondola_state(analysis, umbral, now)
        pasillos.setdefault(pasillo, []).append(
            {"pasillo": pasillo, "gondola": gondola, "a": analysis, "state": state, "label": label})
    return render(request, "web/gondolas.html", {
        "pasillos": pasillos.items(), "umbral": umbral, "recent_hours": int(RECENT.total_seconds() // 3600)})


@roles(*TODOS)
def gondola_detalle(request, pasillo, gondola):
    historial = list(Analysis.objects.filter(pasillo=pasillo, gondola=gondola).select_related("created_by")[:30])
    if not historial and not Camera.objects.filter(pasillo=pasillo, gondola=gondola).exists():
        raise Http404
    state, label = gondola_state(historial[0] if historial else None, Config.get().umbral, timezone.now())
    return render(request, "web/gondola_detalle.html", {
        "pasillo": pasillo, "gondola": gondola, "historial": historial, "state": state, "label": label})
