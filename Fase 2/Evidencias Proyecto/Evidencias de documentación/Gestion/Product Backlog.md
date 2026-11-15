# Product Backlog

Lista priorizada de todo el trabajo del proyecto ShelfVision AI. La fuente viva es [PROGRESS.md](../../../../PROGRESS.md) (sección "Pendientes (priorizados)", ítems con número fijo **#N**, dueño y estado); esta tabla es una copia de su estado al **2026-11-14** (66 ítems, 44 hechos) para que se pueda leer sin abrir el archivo. Cada ítem se toma agregando `(dueño: nombre)`, se trabaja en una rama (`feat/`, `fix/`, `docs/`...) y se cierra con un Pull Request (ver [Definition of Done](Definition%20of%20Done.md)).

Prioridad: el orden de "Pendientes" en `PROGRESS.md` (primero lo que bloquea un hito del profesor o de Walmart). Los requisitos de origen están en [Lista de Requerimientos.xlsx](../Diseño/Lista%20de%20Requerimientos.xlsx) y [Lista de C. U..xlsx](../Diseño/Lista%20de%20C.%20U..xlsx).

| Ítem | Estado | Dueño | Descripción |
| --- | --- | --- | --- |
| #1 | Hecho | Francisco | Implementar `src/preprocessing/roi_filter.py`: recortador de región de interés (ROI) sobre la góndola detectada, incluyendo normalización de… |
| #2 | Hecho | Francisco | Implementar pruebas unitarias en `tests/test_preprocessing.py` para `roi_filter.py` (casos: ROI dentro de límites, ROI fuera de límites, imagen… |
| #3 | Hecho | Francisco | Implementar filtros CLAHE y dewarping en `src/preprocessing/`: `image_correction.py` con `correct_image()` (dewarping y luego CLAHE) ->… |
| #4 | Hecho | Francisco | Implementar la segmentación automática de la góndola y sus repisas en `src/preprocessing/` (cambio de alcance 2026-09-27: ningún usuario define la… |
| #5 | Hecho | Francisco | Integrar inferencia YOLO26 en `src/models/` (se decidió YOLO26 sobre YOLOv8/YOLO11 por su cabeza sin NMS y mejor manejo de objetos chicos, clave en… |
| #6 | Hecho | Francisco | Cálculo de disponibilidad y alerta de quiebre de stock en `src/postprocessing/availability.py`: `compute_availability(productos, niveles)` ->… |
| #7 | Hecho | Mariana | Implementar generación de reportes (Excel, CSV, PDF) en `src/reporting/` |
| #8 | Hecho | Francisco | `scripts/run_pipeline.py`: pipeline completo sobre fotos o carpetas |
| #9 | Hecho | Mariana | Documentar especificaciones técnicas y diagramas en `docs/` |
| #10 | Hecho | Francisco | Descargar datasets candidatos (ver `docs/datasets.md`): SKU-110K, grocery-shelves (UniDataPro), supermarket-shelves (Kaggle), Out Of Stock detection… |
| #11 | Hecho | Francisco | Escribir conversores de anotaciones a nuestro estándar `[x_min, y_min, x_max, y_max]`: lógica pura en `src/datasets/converters.py` (probada en… |
| #12 | Hecho | Francisco | Script de descarga reproducible: `scripts/download_datasets.py` (`--list`, `--check`, `--dataset`, `--force`, `--keep-archives`) con el catálogo en… |
| #13 | Hecho | Mariana | CI en GitHub Actions: correr `pytest tests/` y `docker build` en cada PR, y proteger `main` (merge solo por PR con una revisión y CI en verde) |
| #14 | Pendiente | Sin asignar | Datasets con imágenes tipo cámara de seguridad (vista alta, oblicua, gran angular/fisheye, pasillo completo) para validar dewarping y segmentación en… |
| #15 | Hecho | Francisco | Limitaciones de la segmentación (ítem #4), medidas contra las repisas anotadas de SHARD. Hecho: SHARD en el catálogo (`shard`: figshare, CC BY 4.0,… |
| #16 | Hecho | Mariana | Corregir datos desactualizados de `docs/datasets.md` (licencias, tamaño de grocery-shelves y estado de descarga) |
| #17 | Pendiente | Sin asignar | Limitaciones de la segmentación que siguen tras #15 (F1 de repisas 0.82 en SHARD): - Líneas sobre filas de productos iguales (bandas de color o… |
| #18 | Hecho | Francisco | Notas de instalación en un entorno nuevo (Windows): README explica cómo detectar una copia vieja de `graphify` que tapa la 0.9.70 en el `PATH`, y que… |
| #19 | Hecho | Francisco | Plan de pruebas en `docs/test-plan.md`: para cada etapa ya hecha, qué requisito cumple, cómo se prueba, criterio de aceptación y resultado actual;… |
| #20 | Hecho | Francisco | Dejar el repositorio listo para clonar e inicializar en un PC nuevo (Nicko, 2026-10-01) |
| #21 | Hecho | Francisco | Ajustar la documentación a que Walmart Chile no puede compartir imágenes reales de sus cámaras de seguridad, por privacidad (informado 2026-10-01) |
| #22 | Hecho | Francisco | Repisas inclinadas (fotos en ángulo o cámara de sala) |
| #23 | Hecho | Francisco | Fechas de entregas y plazos en `README.md` y `PROGRESS.md`, en formato YYYY-MM-DD en la línea de la tarea: Evaluación 2 (Avance) de la Fase 2 y… |
| #24 | Pendiente | Sin asignar | Preguntas para la próxima reunión con Walmart (fecha: por definir) |
| #25 | Hecho | Francisco | Registro de requisitos y plazos del curso en `docs/curso.md` (próximos hitos, requisitos vigentes, anuncios pendientes, preguntas abiertas y registro… |
| #26 | Hecho | Mariana | Plan de mejoras de la Fase 1, en `docs/plan-de-mejoras.md` (2026-10-20; el plazo era 2026-10-09) |
| #27 | Hecho | Francisco | Informe de estado de avance para el profesor, con los puntos que pidió su correo de la semana 7. Ya atrasado: el profesor lo está esperando |
| #28 | Hecho | Francisco | Aplicación web mínima en `web/` (Django 6.1 + SQLite; stack elegido el 2026-10-18 con un consejo de 5 perspectivas: Django trae login, roles, bcrypt,… |
| #29 | Pendiente | Sin asignar | Primer demo operativo ante Walmart, a más tardar 2026-10-31 (también se muestra en la Evaluación 2, semana del 2026-10-28): detector entrenado (#5),… |
| #30 | Hecho | Francisco | Documentación alineada con las reuniones con Walmart (2026-09-03, 2026-09-16 y 2026-09-30) |
| #31 | Pendiente | Sin asignar | Excluir de la medición la bodega de reserva que hay sobre la góndola de venta (Walmart no la evalúa; acuerdo del 2026-09-16 en el README) |
| #32 | Pendiente | Sin asignar | Fotos propias de góndolas en tienda (con permiso), clasificadas por ángulo (frontal, lateral, desde arriba, gran angular), y un set chico anotado a… |
| #33 | Hecho | Francisco | Verificar el detector `yolo26s` fuera de SKU-110K, en las condiciones con que evaluará Walmart (IoU contra anotación a mano; fotos frontales, en… |
| #34 | Hecho | Francisco | Análisis de resultados del informe intermedio (2026-10-20), en `docs/analisis-resultados.md` y la sección 3 del informe (#27) |
| #35 | Hecho | Francisco | README completo para el informe intermedio (2026-10-21) y las evidencias de avance (2026-10-26): descripción de la solución, estrategia técnica y… |
| #36 | Pendiente | Sin asignar | Video de demostración de 5 a 10 minutos (entrega 2026-10-21): solo funcionalidades implementadas y resultados que la aplicación genera hoy, con fotos… |
| #37 | Pendiente | Mariana | Evidencias de avance de la Fase 2, a más tardar 2026-10-26: diario de reflexión 2.1, guía 2.4 (resumen del avance, plan de trabajo con estado y… |
| #38 | Pendiente | Sin asignar | Feria de informática (semana del 2026-10-26; día y hora por informar): definir qué integrante va (al menos uno) y qué se muestra |
| #39 | Hecho | Sin asignar | Instalar la aplicación en el servidor del CITT. Bloqueado: las instrucciones por sección llegan en los próximos días |
| #40 | Hecho | Francisco | Quiebre de stock por góndola completa (cambio de alcance del profesor, 2026-10-19) |
| #41 | Hecho | Francisco | Plugin `ponytail` para el trabajo con código (pedido de Francisco, 2026-10-19): skill `/ponytail` de github.com/DietrichGebert/ponytail (MIT),… |
| #42 | Hecho | Mariana | Rehacer las plantillas de C.U, sus diagramas de secuencia y el diagrama de arquitectura según la app web Django (#28): sin API REST, JWT ni React;… |
| #43 | Hecho | Mariana | Dashboard de disponibilidad (CU03, RF05): estado de cada góndola según su última foto (verde con menos de la mitad del umbral, amarillo hasta el… |
| #44 | Hecho | Mariana | Configuración del umbral y de las cámaras (CU05, RF07): umbral de espacio libre entre 1% y 100% (hoy fijo en 30%,… |
| #45 | Hecho | Mariana | Privacidad de las fotos (RNF05): las fotos guardadas pueden mostrar clientes |
| #46 | Pendiente | Sin asignar | Falsas alertas en refrigeradores con puerta de vidrio (#34, fotos 020 y 003 de Kaggle): el reflejo y el desenfoque de la puerta en primer plano, los… |
| #47 | Hecho | Francisco | Auditoría de commits de GitHub: `.mailmap` que unifica las identidades (hoy 6 autores para 3 personas) y commits y PR sin la línea `Co-Authored-By`… |
| #48 | Pendiente | Nicko | Modelar el diagrama de la base de datos (entidad-relación) a partir de `web/models.py` (`User`, perfiles como grupos de Django, `Analysis`) y dejarlo… |
| #49 | Hecho | Mariana | Alertas atómicas en la app web (auditoría 2026-10-21, `web/views.py` `analyze()` y `alerta_accion()`): hoy cerrar la alerta anterior, guardar la foto… |
| #50 | Hecho | Francisco | Configuración segura de la app web antes de instalarla (auditoría 2026-10-21; se cruza con #39): `DJANGO_DEBUG` vale "1" si no se define (con la… |
| #51 | Hecho | Mariana | Bloqueo de cuentas (CU00, auditoría 2026-10-21, `web/auth.py`): con solo saber el RUT se bloquea la cuenta de cualquiera, también la del único… |
| #52 | Hecho | Mariana | Foto sin productos detectados (auditoría 2026-10-21): con 0 detecciones, `compute_availability()` da 100% libre y alerta crítica (foto tapada, oscura… |
| #53 | Hecho | Mariana | Rendimiento y robustez de la app web (auditoría 2026-10-21): las listas de análisis y de alertas cargan el JSON `result` de cada fila sin usarlo… |
| #54 | Hecho | Mariana | Limpieza (auditoría 2026-10-21): `free_volume_cm3()` solo la usan los tests (Nivel 1 no se informa, #40) y `openpyxl` y `fpdf2` están en… |
| #55 | Hecho | Francisco | Entrenar y medir el detector con ruido visual de cámara de sala (pedido de Francisco, 2026-10-21): el mismo ruido que produce una cámara fija… |
| #56 | Hecho | Mariana | Que Claude Code no se agregue como coautor: los commits con `Co-Authored-By: Claude` le dan a "claude" 77 commits en el gráfico de contribuidores de… |
| #57 | Pendiente | Francisco | Auditoría de seguridad por las vulnerabilidades de lenguajes y librerías publicadas la semana del 2026-10-19 (pedido de Francisco, 2026-10-22) |
| #58 | Hecho | Francisco | Cámara de sala simulada para comprobar la app web con el flujo de una cámara fija (pedido de Francisco, 2026-11-09). Hecho (2026-11-09): `py… |
| #59 | Hecho | Francisco | Subir la versión del detector con mejor precisión que tiene en su PC: compartir los pesos por Drive (no se versionan), registrar sus métricas en… |
| #60 | Pendiente | Mariana | Manuales de usuario (uno por perfil: Administrador, Jefe de Salón y Reponedor) y manual de instalación (instructivo del plan de instalación y PDF de… |
| #61 | Pendiente | Sin asignar | Video tutorial con audio (solo la ejecución de los módulos, sin código) y correo de entrega del MVP al cliente: módulos, funcionalidades,… |
| #62 | Pendiente | Sin asignar | Script SQL que crea la estructura de la base y la puebla con datos de prueba, coherente con `web/models.py` (incluye `Config`, `Camera` y… |
| #63 | Pendiente | Sin asignar | Documentación SCRUM de la entrega final: análisis del caso; épicas, sprints e historias de usuario; priorización de las H.U. Salen del backlog… |
| #64 | Pendiente | Sin asignar | Diagramas de actividad de los C.U (los pide la entrega final; no están en el repositorio) |
| #65 | Pendiente | Sin asignar | Informe final de la Fase 2 (`PTY4478 APT2.0 FASE 2 Informe Final`, guía 2.6 en `Fase 2/Evidencias Grupales/`), presentación final (ppt) y la pauta de… |
| #66 | Hecho | Mariana | Reordenar las carpetas del GitHub según la imagen del profesor ("orden de carpetas GitHub (COMPLETO)", mensaje del 2026-11-13), sin cambiar nombres… |
| #67 | Pendiente | Sin asignar | Hojas semanales del Excel "RESUMEN Estado de Avance Casos de Uso" desde la semana del 2026-10-26 (va en la raíz del Drive compartido con el profesor)… |
| #68 | Hecho | Francisco | Lo que #59 no cubrió: abrir los PR de `feat/ruido-camara` (#55) y `feat/camara-sala-simulada`, subidas el 2026-11-09 desde un PC de Duoc con… |
| #69 | Pendiente | Francisco | Evidencias que faltan (Reporte de Auditoría N.º 4, 2026-10-25): `Sandoval_Francisco_1.3_APT122_AutoevaluacionFase1.docx` (Fase 1, individual… |
| #70 | Hecho | Francisco | README (auditoría N.º 4: 6 de 7 elementos, falta "tecnologías"): sección explícita de Tecnologías (Python, Django, OpenCV, YOLO26/Ultralytic… |
| #71 | Hecho | Francisco | Metodología ágil documentada (auditoría N.º 4: faltan metodología declarada y justificada, Product Backlog, Sprint Backlog, Definition of Do… |
| #72 | Hecho | Francisco | Documento de requisitos no funcionales (auditoría N.º 4: no existe): umbral de alerta y precisión del detector, tiempo de análisis, segurida… |
| #73 | Hecho | Francisco | Diagramas UML de clases, secuencia (análisis de una foto) y componentes (auditoría N.º 4: solo hay casos de uso y arquitectura). Fuente Merm… |
| #74 | Hecho | Francisco | `docker-compose.yml` (auditoría N.º 4: Docker 3 de 4): servicio `web` con el `Dockerfile`, volumen `/data`, `.env.example` y puerto 8000; do… |
| #75 | Hecho | Francisco | Documento de Innovación (auditoría N.º 4: solo se menciona en la Fase 1): qué aporta frente a la auditoría manual de góndolas, el enfoque hí… |
| #76 | Hecho | Francisco | Corregir el ruido de `degrade()` (#55): la persona u objeto tapaba productos pero dejaba sus cajas, y el modelo aprendía a marcar lo que no … |
| #77 | Pendiente | Sin asignar | Falsa alarma por oclusión: una persona, un carro o una caja frente a la góndola tapa productos, el detector no los marca (con razón: no se v… |
| #78 | Pendiente | Francisco | Medir el detector por tipo y nivel de ruido (pendiente de #55): un efecto a la vez (ruido del sensor, JPEG, baja resolución, desenfoque, poc… |
