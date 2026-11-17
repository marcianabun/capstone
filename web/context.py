from pathlib import Path

from web.models import ABIERTAS, Analysis

CSS = Path(__file__).parent / "static/web/app.css"


def open_alerts(request):
    """Alertas abiertas para el contador de la barra superior, y la versión del CSS
    (su fecha) para que el navegador no use una copia vieja al cambiar los estilos."""
    context = {"css_version": int(CSS.stat().st_mtime)}
    if getattr(request, "user", None) and request.user.is_authenticated:
        context["open_alerts"] = Analysis.objects.filter(estado__in=ABIERTAS).count()
    return context
