# Sprint Backlog

Los sprints se miden contra los hitos del curso y de Walmart (ver [Metodología ágil](Metodologia%20Agil.md)). Los ítems **#N** son los de [Product Backlog](Product%20Backlog.md) y `PROGRESS.md`; **PR #N** es el Pull Request de GitHub. Fechas y estados salen de la [Carta Gantt](Carta%20Gantt%20Fase%202.xlsx) y del historial de git.

El detalle semana a semana (sprints 0 a 9, semanas 37 a 47) está en la [Documentación SCRUM](Documentacion%20SCRUM.docx). Equivalencia aproximada: el Sprint 1 de este documento son los sprints semanales 1 a 5, y el Sprint 2, los sprints 6 a 9; los cortes difieren unos días porque las semanas van de lunes a domingo.

## Sprint 0: arranque y Fase 1 (2026-09-07 a 2026-09-26)

Objetivo: dejar en el repositorio los documentos de la Fase 1. No hay ítems numerados: era carga de documentos (casos de uso, diagramas, mockups, autoevaluaciones; ver la sección "Fase 1" de la [Carta Gantt](Carta%20Gantt%20Fase%202.xlsx)).

## Sprint 1: pipeline, detector y app web (2026-09-27 a 2026-10-28)

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
| Pendiente al cierre | Video de demostración (#36), ruido de cámara de sala (#55, planificado del 2026-10-29 al 2026-11-06), servidor del CITT (#39, descartado el 2026-11-15) | Pasa al Sprint 2 |

## Sprint 2: documentación final y entrega (2026-10-29 a 2026-11-20, en curso)

Objetivo: GitHub al día para la revisión de Walmart (2026-11-16), entrega del MVP y entrega final de la Fase 2 (2026-11-20, 12:00).

| Ítem | Descripción | Dueño | Estado (2026-11-15) |
| --- | --- | --- | --- |
| #59 | Mejor modelo del detector en el repositorio | Francisco | Hecho (PR #86) |
| #60 | Manuales de usuario por perfil y manual de instalación | Mariana | En curso: manuales de usuario hechos (PR #83), falta el de instalación |
| #66 | Orden de carpetas según el profesor | Mariana | Hecho (PR #85) |
| #55, #58, #68 | Ruido de cámara de sala: PR de las ramas y métricas | Francisco | Hecho (PR #90 y #91) |
| #76 | Corrección del ruido: cajas tapadas fuera y validación óptico/oclusión | Francisco | Hecho (PR #92) |
| #77 | Falsa alarma por oclusión en el pipeline | Francisco | En curso: medición del frente visible y detector de personas listos (opt-in); falta validar con personas reales |
| #78 | Detector por tipo y nivel de ruido | Francisco | Hecho (PR #95) |
| #79 | Reentrenamiento con desenfoque más fuerte | Francisco | Hecho (PR #96) |
| #80 | Modelo versionado: `yolo26s-finetune-ruido-v3` | Francisco | Hecho (PR #97) |
| #82 | Desenfoque de movimiento fuerte: v4 sin mejora real (límite aceptado) | Francisco | Hecho |
| #61 a #65, #67 | Video tutorial, script SQL, SCRUM, diagramas de actividad, informe final y presentación, hojas semanales del Excel | Sin asignar | Pendiente |
| #70 a #75 | Hallazgos de la auditoría N.º 4 (README, metodología, RNF, UML, docker-compose, innovación) | Francisco | Hecho (PR #88) |
| #69 | Evidencias individuales que faltan (autoevaluación 1.3 y diario 2.1 de Francisco) y presentación | Francisco | En curso: borradores en el PR #89; la presentación llega con #65 |
| #81 | Revisión de los documentos de la auditoría N.º 4 contra el repositorio | Mariana | Hecho |
