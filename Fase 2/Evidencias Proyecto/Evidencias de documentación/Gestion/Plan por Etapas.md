# Plan por Etapas

Las etapas se miden contra los hitos del curso y de Walmart (ver [Metodología en cascada](Metodologia%20Cascada.md)). Los ítems **#N** son los de [Listado de Tareas](Listado%20de%20Tareas.md) y `PROGRESS.md`; **PR #N** es el Pull Request de GitHub. Fechas y estados salen de la [Carta Gantt](Carta%20Gantt%20Fase%202.xlsx) y del historial de git.

## Etapa 0: arranque y Fase 1 (2026-09-07 a 2026-09-26)

Objetivo: dejar en el repositorio los documentos de la Fase 1. No hay ítems numerados: era carga de documentos (casos de uso, diagramas, mockups, autoevaluaciones; ver la sección "Fase 1" de la [Carta Gantt](Carta%20Gantt%20Fase%202.xlsx)).

## Etapa 1: pipeline, detector y app web (2026-09-27 a 2026-10-28)

Objetivo: primer demo operativo con el 50% de los C.U resueltos (Evaluación 2) e informe intermedio (2026-10-21).

| Área | Ítems y Pull Requests | Estado al cierre |
| --- | --- | --- |
| Equipo y CI | Flujo de ramas y PR, plugins compartidos, CI con GitHub Actions (PR #6, #8, #11) | Hecho |
| Datasets | Descarga reproducible y evaluación en SHARD (PR #10, #13) | Hecho |
| Visión artificial | Corrección de imagen, segmentación y ROI (PR #3, #7); detector YOLO26 (PR #15, #18, #19); repisas inclinadas (PR #22); detector fuera de SKU-110K y fine-tuning (PR #40, #41, #55) | Hecho (ítems #1 a #6, #33, #34) |
| Pipeline | `run_pipeline.py` completo con vista anotada y métricas (PR #28, #30) | Hecho (ítem #8) |
| Alerta | Disponibilidad y quiebre por góndola completa (PR #16, #32) | Hecho (ítems #6, #40) |
| App web | Login, usuarios y roles (PR #35); reportes (PR #54); configuración y cámaras (PR #71); dashboard (PR #72); privacidad de fotos (PR #74) | Hecho (ítems #7, #28, #43 a #45) |
| Auditoría 2026-10-21 | Seguridad, robustez, alertas atómicas, bloqueo de cuenta y limpieza (PR #69, #70, #75, #76, #79, #80, #81) | Hecho (ítems #49 a #54; #57 en curso) |
| Documentación | Informe intermedio, README, especificación técnica, plan de pruebas, análisis de resultados (PR #17, #34 a #39, #46, #63, #77) | Hecho |
| Pendiente al cierre | Video de demostración (#36), ruido de cámara de sala (#55, planificado del 2026-10-29 al 2026-11-06), servidor del CITT (#39, descartado el 2026-11-15) | Pasa a la Etapa 2 |

## Etapa 2: documentación final y entrega (2026-10-29 a 2026-11-20, en curso)

Objetivo: GitHub al día para la revisión de Walmart (2026-11-16), entrega del MVP y entrega final de la Fase 2 (2026-11-20, 12:00).

| Ítem | Descripción | Dueño | Estado (2026-11-19) |
| --- | --- | --- | --- |
| #59 | Mejor modelo del detector en el repositorio | Francisco | Hecho (PR #86) |
| #60 | Manuales de usuario por perfil y manual de instalación | Mariana | Hecho (PR #83 y el de #60) |
| #66 | Orden de carpetas según el profesor | Mariana | Hecho (PR #85) |
| #55, #58, #68 | Ruido de cámara de sala: PR de las ramas y métricas | Francisco | Hecho (PR #90 y #91) |
| #76 | Corrección del ruido: cajas tapadas fuera y validación óptico/oclusión | Francisco | Hecho (PR #92) |
| #77 | Falsa alarma por oclusión en el pipeline | Francisco | Hecho (PR #99 y #101); medir con clientes reales queda como límite |
| #78 | Detector por tipo y nivel de ruido | Francisco | Hecho (PR #95) |
| #79 | Reentrenamiento con desenfoque más fuerte | Francisco | Hecho (PR #96) |
| #80 | Modelo versionado: `yolo26s-finetune-ruido-v3` | Francisco | Hecho (PR #97) |
| #82 | Desenfoque de movimiento fuerte: v4 sin mejora real (límite aceptado) | Francisco | Hecho |
| #61 | Video tutorial y entrega del MVP a Walmart (por mensaje de AVA al profesor, que se la hace llegar) | Nicko | En curso |
| #62 | Script SQL que crea y puebla la base | Francisco | Hecho (PR #102) |
| #63 | Documentación SCRUM | Francisco | Descartado (2026-11-16): no aplica, el equipo usa cascada |
| #64, #65 | Diagramas de actividad, informe final y presentación | Francisco y Nicko | En curso: informe final subido (PR #122) |
| #67 | Hojas semanales del Excel de avance de C.U | Mariana | En curso (PR #110): hojas 5 a 8 hechas |
| #83 | Error de niveles con una sola repisa | Nicko | Hecho (PR #104) |
| #84 | CU06 sin correo: el enlace de contraseña se muestra en pantalla | Mariana | Hecho (PR #111) |
| #85, #86 | Rendimiento de la app web y tope de píxeles de la foto | Nicko | Hecho (PR #108 y #109) |
| #87 | Cámara defectuosa (excepción 1a de CU01) | Mariana | Hecho |
| #88 | Alcance de CU02 (push) y CU05 (tolerancia) en las plantillas | Mariana | Hecho |
| #89 | txt del repositorio GitHub documentado | Mariana | Hecho |
| #90 | Revisión general de documentos, backlog y diagramas contra el repositorio | Mariana | Hecho |
| #91 | Lista de C.U (agrega CU07) y lista de requerimientos al día | Mariana | Hecho |
| #92 | Quitar SCRUM de la documentación: metodología en cascada | Mariana (lo empezó Francisco) | Hecho (PR #117 y el de la Carta Gantt) |
| #93 | Inicialización del entorno en una PC de la sala de clases | Francisco | Hecho (PR #116) |
| #94, #96 | Anterior/Siguiente en la foto del análisis y paginación de «Últimos análisis» | Nicko | Hecho (PR #120) |
| #95 | Analizar fotos por ruta o URL de un dataset | Sin asignar | Pendiente |
| #97 | Ajustes de la app web para el teléfono | Nicko | Hecho (PR #121) |
| #98 | Detalles de documentación para la entrega final (pruebas, README, APK y NoSQL) | Mariana | Hecho (PR #125) |
| #99 | Plan de pruebas en Word para ANEXOS, con la app web y los C.U | Mariana | Hecho (PR #126) |
| #100 | Carpeta FINAL FASE 2 del Drive ordenada según el profesor | Mariana | En curso: estructura lista; faltan pautas, evaluación formativa, diagramas de actividad y video |
| #101, #102, #103 | Pauta de reflexión individual de cada integrante | Mariana, Francisco y Nicko | En curso |
| #70 a #75 | Hallazgos de la auditoría N.º 4 (README, metodología, RNF, UML, docker-compose, innovación) | Francisco | Hecho (PR #88) |
| #69 | Evidencias individuales que faltan (autoevaluación 1.3 y diario 2.1 de Francisco) y presentación | Francisco | Descartado (2026-11-19): es la pauta de reflexión de Francisco, sigue en el #102 |
| #81 | Revisión de los documentos de la auditoría N.º 4 contra el repositorio | Mariana | Hecho |
