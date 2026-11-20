# Listado de Tareas

Lista priorizada de todo el trabajo del proyecto ShelfVision AI. La fuente viva es [PROGRESS.md](../../../../PROGRESS.md) (sección "Pendientes (priorizados)", ítems con número fijo **#N**, dueño y estado); esta tabla es una copia de su estado al **2026-11-20** (103 ítems: 89 hechos, 3 en curso, 2 pendientes y 9 descartados) para que se pueda leer sin abrir el archivo. Cada ítem se toma agregando `(dueño: nombre)`, se trabaja en una rama (`feat/`, `fix/`, `docs/`...) y se cierra con un Pull Request (ver [Criterios de Terminado](Criterios%20de%20Terminado.md)).

Prioridad: el orden de "Pendientes" en `PROGRESS.md` (primero lo que bloquea un hito del profesor o de Walmart). Los requisitos de origen están en [Lista de Requerimientos.xlsx](../Diseño/Lista%20de%20Requerimientos.xlsx) y [Lista de C. U..xlsx](../Diseño/Lista%20de%20C.%20U..xlsx).

| Ítem | Estado | Dueño | Descripción |
| --- | --- | --- | --- |
| #1 | Hecho | Francisco | Implementar `src/preprocessing/roi_filter.py`: recortador de región de interés (ROI) sobre la góndola detectada, incluyendo normalización de… |
| #2 | Hecho | Francisco | Implementar pruebas unitarias en `tests/test_preprocessing.py` para `roi_filter.py` (casos: ROI dentro de límites, ROI fuera de límites, ima… |
| #3 | Hecho | Francisco | Implementar filtros CLAHE y dewarping en `src/preprocessing/`: `image_correction.py` con `correct_image()` (dewarping y luego CLAHE) -> `Cor… |
| #4 | Hecho | Francisco | Implementar la segmentación automática de la góndola y sus repisas en `src/preprocessing/` (cambio de alcance 2026-09-27: ningún usuario def… |
| #5 | Hecho | Francisco | Integrar inferencia YOLO26 en `src/models/` (se decidió YOLO26 sobre YOLOv8/YOLO11 por su cabeza sin NMS y mejor manejo de objetos chicos, c… |
| #6 | Hecho | Francisco | Cálculo de disponibilidad y alerta de quiebre de stock en `src/postprocessing/availability.py`: `compute_availability(productos, niveles)` -… |
| #7 | Hecho | Mariana | Implementar generación de reportes (Excel, CSV, PDF) en `src/reporting/`. Contenido mínimo (#30, acuerdos con Walmart en el README): % libre… |
| #8 | Hecho | Francisco | `scripts/run_pipeline.py`: pipeline completo sobre fotos o carpetas. `src/pipeline.py` (`run_image()`) encadena `correct_image()` -> `segmen… |
| #9 | Hecho | Mariana | Documentar especificaciones técnicas y diagramas en `docs/`. Hecho (2026-10-22): `docs/especificacion-tecnica.md`, sacado del código y no de… |
| #10 | Hecho | Francisco | Descargar datasets candidatos (ver `docs/datasets.md`): SKU-110K, grocery-shelves (UniDataPro), supermarket-shelves (Kaggle), Out Of Stock d… |
| #11 | Hecho | Francisco | Escribir conversores de anotaciones a nuestro estándar `[x_min, y_min, x_max, y_max]`: lógica pura en `src/datasets/converters.py` (probada… |
| #12 | Hecho | Francisco | Script de descarga reproducible: `scripts/download_datasets.py` (`--list`, `--check`, `--dataset`, `--force`, `--keep-archives`) con el catá… |
| #13 | Hecho | Mariana | CI en GitHub Actions: correr `pytest tests/` y `docker build` en cada PR, y proteger `main` (merge solo por PR con una revisión y CI en verd… |
| #14 | Descartado | Sin asignar | Datasets con imágenes tipo cámara de seguridad (vista alta, oblicua, gran angular/fisheye, pasillo completo) para validar dewarping y segmen… |
| #15 | Hecho | Francisco | Limitaciones de la segmentación (ítem #4), medidas contra las repisas anotadas de SHARD. Hecho: SHARD en el catálogo (`shard`: figshare, CC… |
| #16 | Hecho | Mariana | Corregir datos desactualizados de `docs/datasets.md` (licencias, tamaño de grocery-shelves y estado de descarga). Licencias: supermarket-she… |
| #17 | Descartado | Sin asignar | Limitaciones de la segmentación que siguen tras #15 (F1 de repisas 0.82 en SHARD): - Líneas sobre filas de productos iguales (bandas de colo… |
| #18 | Hecho | Francisco | Notas de instalación en un entorno nuevo (Windows): README explica cómo detectar una copia vieja de `graphify` que tapa la 0.9.70 en el `PAT… |
| #19 | Hecho | Francisco | Plan de pruebas en `docs/test-plan.md`: para cada etapa ya hecha, qué requisito cumple, cómo se prueba, criterio de aceptación y resultado a… |
| #20 | Hecho | Francisco | Dejar el repositorio listo para clonar e inicializar en un PC nuevo (Nicko, 2026-10-01). README: versión de Python, graphify con `uv tool` f… |
| #21 | Hecho | Francisco | Ajustar la documentación a que Walmart Chile no puede compartir imágenes reales de sus cámaras de seguridad, por privacidad (informado 2026-… |
| #22 | Hecho | Francisco | Repisas inclinadas (fotos en ángulo o cámara de sala). Problema: con perspectiva, `segment_gondola()` pierde repisas (acepta 8° de inclinaci… |
| #23 | Hecho | Francisco | Fechas de entregas y plazos en `README.md` y `PROGRESS.md`, en formato YYYY-MM-DD en la línea de la tarea: Evaluación 2 (Avance) de la Fase… |
| #24 | Descartado | Sin asignar | Preguntas para la próxima reunión con Walmart (fecha: por definir). Hasta ahora no han dicho nada de sus cámaras, y del Dataset Oculto proba… |
| #25 | Hecho | Francisco | Registro de requisitos y plazos del curso en `docs/curso.md` (próximos hitos, requisitos vigentes, anuncios pendientes, preguntas abiertas y… |
| #26 | Hecho | Mariana | Plan de mejoras de la Fase 1, en `docs/plan-de-mejoras.md` (2026-10-20; el plazo era 2026-10-09). La Fase 1 tuvo nota 7,0 sin observaciones… |
| #27 | Hecho | Francisco | Informe de estado de avance para el profesor, con los puntos que pidió su correo de la semana 7. Ya atrasado: el profesor lo está esperando.… |
| #28 | Hecho | Francisco | Aplicación web mínima en `web/` (Django 6.1 + SQLite; stack elegido el 2026-10-18 con un consejo de 5 perspectivas: Django trae login, roles… |
| #29 | Hecho | Sin asignar | Primer demo operativo ante Walmart, a más tardar 2026-10-31 (también se muestra en la Evaluación 2, semana del 2026-10-28): detector entrena… |
| #30 | Hecho | Francisco | Documentación alineada con las reuniones con Walmart (2026-09-03, 2026-09-16 y 2026-09-30). Las minutas no se versionan (son confidenciales… |
| #31 | Descartado | Sin asignar | Excluir de la medición la bodega de reserva que hay sobre la góndola de venta (Walmart no la evalúa; acuerdo del 2026-09-16 en el README). H… |
| #32 | Descartado | Sin asignar | Fotos propias de góndolas en tienda (con permiso), clasificadas por ángulo (frontal, lateral, desde arriba, gran angular), y un set chico an… |
| #33 | Hecho | Francisco | Verificar el detector `yolo26s` fuera de SKU-110K, en las condiciones con que evaluará Walmart (IoU contra anotación a mano; fotos frontales… |
| #34 | Hecho | Francisco | Análisis de resultados del informe intermedio (2026-10-20), en `docs/analisis-resultados.md` y la sección 3 del informe (#27). Pipeline comp… |
| #35 | Hecho | Francisco | README completo para el informe intermedio (2026-10-21) y las evidencias de avance (2026-10-26): descripción de la solución, estrategia técn… |
| #36 | Hecho | Nicko | Video de demostración de 5 a 10 minutos (entrega 2026-10-21): solo funcionalidades implementadas y resultados que la aplicación genera hoy,… |
| #37 | Hecho | Mariana | Evidencias de avance de la Fase 2, a más tardar 2026-10-26: diario de reflexión 2.1, guía 2.4 (resumen del avance, plan de trabajo con estad… |
| #38 | Descartado | Sin asignar | Feria de informática (semana del 2026-10-26; día y hora por informar): definir qué integrante va (al menos uno) y qué se muestra. |
| #39 | Descartado | Sin asignar | Instalar la aplicación en el servidor del CITT. Estaba bloqueado: las instrucciones por sección no llegaron. Punto de partida: la imagen Doc… |
| #40 | Hecho | Francisco | Quiebre de stock por góndola completa (cambio de alcance del profesor, 2026-10-19). La alerta y el % libre que se informan son solo los de l… |
| #41 | Hecho | Francisco | Plugin `ponytail` para el trabajo con código (pedido de Francisco, 2026-10-19): skill `/ponytail` de github.com/DietrichGebert/ponytail (MIT… |
| #42 | Hecho | Mariana | Rehacer las plantillas de C.U, sus diagramas de secuencia y el diagrama de arquitectura según la app web Django (#28): sin API REST, JWT ni… |
| #43 | Hecho | Mariana | Dashboard de disponibilidad (CU03, RF05): estado de cada góndola según su última foto (verde con menos de la mitad del umbral, amarillo hast… |
| #44 | Hecho | Mariana | Configuración del umbral y de las cámaras (CU05, RF07): umbral de espacio libre entre 1% y 100% (hoy fijo en 30%, `AvailabilityParams.critic… |
| #45 | Hecho | Mariana | Privacidad de las fotos (RNF05): las fotos guardadas pueden mostrar clientes. Proponer a Walmart (#24) borrarlas tras N días o difuminar ros… |
| #46 | Pendiente | Sin asignar | Falsas alertas en refrigeradores con puerta de vidrio (#34, fotos 020 y 003 de Kaggle): el reflejo y el desenfoque de la puerta en primer pl… |
| #47 | Hecho | Francisco | Auditoría de commits de GitHub: `.mailmap` que unifica las identidades (hoy 6 autores para 3 personas) y commits y PR sin la línea `Co-Autho… |
| #48 | Hecho | Nicko | Modelar el diagrama de la base de datos (entidad-relación) a partir de `web/models.py` (`User`, perfiles como grupos de Django, `Analysis`)… |
| #49 | Hecho | Mariana | Alertas atómicas en la app web (auditoría 2026-10-21, `web/views.py` `analyze()` y `alerta_accion()`): hoy cerrar la alerta anterior, guarda… |
| #50 | Hecho | Francisco | Configuración segura de la app web antes de instalarla (auditoría 2026-10-21; se cruza con #39): `DJANGO_DEBUG` vale "1" si no se define (co… |
| #51 | Hecho | Mariana | Bloqueo de cuentas (CU00, auditoría 2026-10-21, `web/auth.py`): con solo saber el RUT se bloquea la cuenta de cualquiera, también la del úni… |
| #52 | Hecho | Mariana | Foto sin productos detectados (auditoría 2026-10-21): con 0 detecciones, `compute_availability()` da 100% libre y alerta crítica (foto tapad… |
| #53 | Hecho | Mariana | Rendimiento y robustez de la app web (auditoría 2026-10-21): las listas de análisis y de alertas cargan el JSON `result` de cada fila sin us… |
| #54 | Hecho | Mariana | Limpieza (auditoría 2026-10-21): `free_volume_cm3()` solo la usan los tests (Nivel 1 no se informa, #40) y `openpyxl` y `fpdf2` están en `re… |
| #55 | Hecho | Francisco | Entrenar y medir el detector con ruido visual de cámara de sala (pedido de Francisco, 2026-10-21): el mismo ruido que produce una cámara fij… |
| #56 | Hecho | Mariana | Que Claude Code no se agregue como coautor: los commits con `Co-Authored-By: Claude` le dan a "claude" 77 commits en el gráfico de contribui… |
| #57 | En curso | Francisco | Auditoría de seguridad por las vulnerabilidades de lenguajes y librerías publicadas la semana del 2026-10-19 (pedido de Francisco, 2026-10-2… |
| #58 | Hecho | Francisco | Cámara de sala simulada para comprobar la app web con el flujo de una cámara fija (pedido de Francisco, 2026-11-09). Hecho (2026-11-09): `py… |
| #59 | Hecho | Francisco | Subir al repositorio el mejor modelo del detector que tiene el equipo. Hecho (2026-11-14, PR #86): `weights/yolo26s-finetune.pt` (20 MB; mAP… |
| #60 | Hecho | Mariana | Manuales de usuario (uno por perfil: Administrador, Jefe de Salón y Reponedor) y manual de instalación (instructivo del plan de instalación… |
| #61 | Hecho | Nicko | Video tutorial con audio (solo la ejecución de los módulos, sin código) y entrega del MVP al cliente: módulos, funcionalidades, instruccione… |
| #62 | Hecho | Francisco | Script SQL que crea la estructura de la base y la puebla con datos de prueba, coherente con `web/models.py` (incluye `Config`, `Camera` y `U… |
| #63 | Descartado | Sin asignar | Documentación SCRUM de la entrega final: análisis del caso; épicas, sprints e historias de usuario; priorización de las H.U. Se había entreg… |
| #64 | Hecho | Francisco y Nicko | Diagramas de actividad de los C.U (los pide la entrega final; no están en el repositorio). **Hecho (2026-11-19)**: Nicko subió `Diagrama de… |
| #65 | Hecho | Francisco y Nicko | Informe final de la Fase 2 (`PTY4478 APT2.0 FASE 2 Informe Final`) y presentación final (ppt). Las pautas de reflexión individuales pasan a… |
| #66 | Hecho | Mariana | Reordenar las carpetas del GitHub según la imagen del profesor ("orden de carpetas GitHub (COMPLETO)", mensaje del 2026-11-13), sin cambiar… |
| #67 | Hecho | Mariana | Hojas semanales del Excel "RESUMEN Estado de Avance Casos de Uso" desde la semana del 2026-10-26 (va en la raíz del Drive compartido con el… |
| #68 | Hecho | Francisco | Lo que #59 no cubrió: abrir los PR de `feat/ruido-camara` (#55) y `feat/camara-sala-simulada`, subidas el 2026-11-09 desde un PC de Duoc con… |
| #69 | Descartado | Sin asignar | (dueño: Francisco) Evidencias que faltan (Reporte de Auditoría N.º 4, 2026-10-25): `Sandoval_Francisco_1.3_APT122_AutoevaluacionFase1.docx`… |
| #70 | Hecho | Francisco | README (auditoría N.º 4: 6 de 7 elementos, falta "tecnologías"): sección explícita de Tecnologías (Python, Django, OpenCV, YOLO26/Ultralytic… |
| #71 | Hecho | Francisco | Metodología documentada (auditoría N.º 4: faltan metodología declarada y justificada, Listado de Tareas, Plan por Etapas, Criterios de Termi… |
| #72 | Hecho | Francisco | Documento de requisitos no funcionales (auditoría N.º 4: no existe): umbral de alerta y precisión del detector, tiempo de análisis, segurida… |
| #73 | Hecho | Francisco | Diagramas UML de clases, secuencia (análisis de una foto) y componentes (auditoría N.º 4: solo hay casos de uso y arquitectura). Fuente Merm… |
| #74 | Hecho | Francisco | `docker-compose.yml` (auditoría N.º 4: Docker 3 de 4): servicio `web` con el `Dockerfile`, volumen `/data`, `.env.example` y puerto 8000; do… |
| #75 | Hecho | Francisco | Documento de Innovación (auditoría N.º 4: solo se menciona en la Fase 1): qué aporta frente a la auditoría manual de góndolas, el enfoque hí… |
| #76 | Hecho | Francisco | Corregir el ruido de `degrade()` (#55): la persona u objeto tapaba productos pero dejaba sus cajas, y el modelo aprendía a marcar lo que no… |
| #77 | Hecho | Francisco | Falsa alarma por oclusión: una persona, un carro o una caja frente a la góndola tapa productos, el detector no los marca (con razón: no se v… |
| #78 | Hecho | Francisco | Medir el detector por tipo y nivel de ruido (pendiente de #55): un efecto a la vez (ruido del sensor, JPEG, baja resolución, desenfoque, poc… |
| #79 | Hecho | Francisco | Entrenar con desenfoque más fuerte (pedido de Francisco, 2026-11-15): DET-09 (#78) mostró que el detector solo cae bajo mAP50 0.70 con desen… |
| #80 | Hecho | Francisco | Reemplazar el modelo versionado por `yolo26s-finetune-ruido-v3` (pedido de Francisco, 2026-11-15, tras DET-10). **Hecho (2026-11-15)**: `wei… |
| #81 | Hecho | Mariana | Revisar los documentos de la auditoría N.º 4 (#70 a #75) y las reflexiones de Francisco (#69) antes de la revisión de Walmart (2026-11-16),… |
| #82 | Hecho | Francisco | Desenfoque de movimiento fuerte (pedido de Francisco, 2026-11-15, tras DET-10): con la v3 el mAP50 con movimiento de 31 px es 0.647, bajo 0.… |
| #83 | Hecho | Nicko | Error «Se necesita al menos un nivel (o la ROI como unico nivel)» al analizar una foto (reportado por Nicko, 2026-11-15): foto de pasillo en… |
| #84 | Hecho | Mariana | CU06 sin correo (decidido 2026-11-15, auditoría ponytail del repo: no se usará SMTP). Hoy, en Docker, el correo del enlace para definir la c… |
| #85 | Hecho | Nicko | Rendimiento de la app web (auditoría ponytail del repo, 2026-11-15). (1) El dashboard «Góndolas» (CU03) buscaba la última foto de cada góndo… |
| #86 | Hecho | Nicko | Limpieza y tope de píxeles de la foto (auditoría ponytail del repo, 2026-11-15). (1) `occupied_fraction` (`ShelfAvailability` y `GondolaAvai… |
| #87 | Hecho | Mariana | Cámara defectuosa (excepción 1a de CU01, lo único que le falta al CU01): si la foto tiene colores imposibles (por ejemplo, toda verde o viol… |
| #88 | Hecho | Mariana | Alcance de CU02 y CU05 en las plantillas, para cerrar los C.U al 100% en la entrega final (2026-11-20): la notificación push al teléfono (CU… |
| #89 | Hecho | Mariana | Archivo txt «Repositorio GitHub del proyecto documentado» en `Fase 2/Evidencias Proyecto/Evidencias de sistema/Aplicación/`, que pide la ent… |
| #90 | Hecho | Mariana | Revisión general de documentos, backlog y diagramas contra el repositorio (pedido de Mariana, 2026-11-16). **Hecho (2026-11-16)**: `PROGRESS… |
| #91 | Hecho | Mariana | Corregir `Lista de C. U..xlsx` y `Lista de Requerimientos.xlsx` (hallazgos de #90; van en la entrega final, 2026-11-20): agregar el CU07, la… |
| #92 | Hecho | Mariana | Quitar de la documentación toda referencia a SCRUM: el equipo usa la metodología tradicional o en cascada (indicación de Francisco, 2026-11-… |
| #93 | Hecho | Francisco | Documentar la inicialización del entorno en una PC de la sala de clases (pedido de Francisco, 2026-11-16). **Hecho (2026-11-16)**: `docs/ini… |
| #94 | Hecho | Nicko | Botones de navegación sobre la foto del análisis, para moverse entre análisis y alertas de góndolas sin volver a la lista (pedido de Francis… |
| #95 | Pendiente | Sin asignar | Analizar fotos indicando la ruta o la URL de un dataset, en vez de subirlas una por una (pedido de Francisco, 2026-11-16). Hoy «Análisis» (`… |
| #96 | Hecho | Nicko | Paginación de la lista «Últimos análisis» (pedido de Francisco, 2026-11-16). Hoy `analisis()` corta en 50 con `[:50]` y no hay cómo ver los… |
| #97 | Hecho | Nicko | Ajustes de la app web para el teléfono, de la auditoría de 2026-11-16: el menú pasa a una segunda fila (con Administrador y Jefe ya no se es… |
| #98 | Hecho | Mariana | Detalles de documentación para la entrega final (revisión del 2026-11-18): `Documento de Innovacion.md` y `Requisitos No Funcionales.md` (RN… |
| #99 | Hecho | Mariana | Plan de pruebas en Word para ANEXOS de la entrega final (carpeta FINAL FASE 2 del Drive, «c. Plan de pruebas»). `docs/test-plan.md` no tenía… |
| #100 | En curso | Mariana | Armar la carpeta FINAL FASE 2 del Drive compartido con el profesor (estructura del PDF del 2026-11-06, ver `docs/curso.md`), con los archivo… |
| #101 | Hecho | Mariana | Pauta de reflexión y autoevaluación individuales de Mariana para la entrega final (2026-11-20, 12:00; «pautas» son las dos, según Mariana, 2… |
| #102 | En curso | Francisco | Pauta de reflexión y autoevaluación individuales de Francisco para la entrega final (2026-11-20, 12:00; «pautas» son las dos, según Mariana,… |
| #103 | Hecho | Nicko | Pauta de reflexión y autoevaluación individuales de Nicko para la entrega final (2026-11-20, 12:00; «pautas» son las dos, según Mariana, 202… |
