# Metodología en cascada

**Metodología declarada: tradicional o en cascada, por fases.** El proyecto avanza por fases secuenciales del curso (análisis y diseño, construcción, pruebas y entrega), cada una con entregables y fechas fijas que cierran un hito del curso o de Walmart. Se planifica con Carta Gantt, Matriz RACI y matriz de riesgo.

## Por qué cascada

- **Fases y entregables definidos por el curso (APT122):** la Fase 1 (análisis, levantamiento de requisitos y arquitectura) se entregó y evaluó antes de empezar la Fase 2 (construcción, pruebas y entrega); la Fase 3 cierra con ajustes finales y la exposición. Ver `docs/curso.md`.
- **Hitos con fecha fija:** informe intermedio 2026-10-21, Evaluación 2 (semana del 2026-10-28), revisión de Walmart 2026-11-16 y entrega final 2026-11-20.
- **Documentación como parte de cada fase:** casos de uso, requisitos, diagramas, plan de pruebas y manuales se entregan y evalúan por separado del código.

## Fases del proyecto

| Fase | Período | Qué se hace | Cierra con |
| --- | --- | --- | --- |
| Fase 1: análisis y diseño | 2026-09-07 a 2026-09-26 | Levantamiento de requisitos con Walmart, casos de uso, diagramas, mockups y arquitectura | Entregables de `Fase 1/` (ya evaluados, no se modifican) |
| Fase 2, etapa 1: construcción | 2026-09-27 a 2026-10-28 | Pipeline de visión, detector, app web y su documentación técnica | Informe intermedio (2026-10-21) y Evaluación 2 |
| Fase 2, etapa 2: pruebas, documentación final y entrega | 2026-10-29 a 2026-11-20 | Pruebas con ruido de cámara de sala, manuales, base de datos, informe final | Revisión de Walmart (2026-11-16) y entrega final (2026-11-20) |
| Fase 3: ajustes finales | Semanas 17 y 18 | Ajustes, manuales y exposición | Exposición ante la comisión |

El detalle por etapa está en el [Plan por Etapas](Plan%20por%20Etapas.md).

## Cómo se trabaja (lo que de verdad se hace)

| Elemento | Cómo se materializa aquí |
| --- | --- |
| Lista de trabajo | [Listado de Tareas](Listado%20de%20Tareas.md): copia legible de `PROGRESS.md` (ítems **#N** con dueño y estado) |
| Plan | [Plan por Etapas](Plan%20por%20Etapas.md) y la Carta Gantt (`Carta Gantt Fase 2.xlsx`, estados Cumplido / En curso / Pendiente / Atrasado / Bloqueado) |
| Responsables | Quien toma un ítem se lo asigna en `PROGRESS.md`; lo ejecuta en una rama propia (`feat/`, `fix/`, `docs/`, `chore/`) |
| Control de calidad | Pull Request contra `main` con CI en verde; desde el 2026-10-19 `main` no exige aprobación de otro integrante |
| Criterios de aceptación | [Criterios de Terminado](Criterios%20de%20Terminado.md) |
| Cierre de cada etapa | [Lecciones Aprendidas](Lecciones%20Aprendidas.md), reconstruidas desde el historial de git |
| Cambios de requisitos | Los fija el cliente (Walmart Chile) o el profesor; se registran como ítem nuevo y actualizan los documentos afectados |
| Alcance del MVP | [Alcance MVP](Alcance%20MVP.md) |

Dentro de la Fase 2, el código se integra ítem por ítem mediante Pull Requests para que tres personas trabajen en paralelo sin pisarse; eso es una práctica de control de versiones, no un cambio de metodología.

## Roles

Los tres integrantes comparten el desarrollo y se reparten los ítems. El cliente (Walmart Chile) y el profesor revisan y aprueban los entregables. La asignación por ítem y por actividad está en la [Matriz RACI](Matriz%20RACI.xlsx).

## Cambios de requisitos

El alcance cambió durante la Fase 2 (de "por repisa" a "góndola completa", 2026-10-19, indicación del profesor). Se trató como un cambio de requisitos: se registró como ítem (#40), se rehízo la alerta y se actualizaron los documentos afectados. Es un costo propio de la cascada y queda anotado en las [Lecciones Aprendidas](Lecciones%20Aprendidas.md).
