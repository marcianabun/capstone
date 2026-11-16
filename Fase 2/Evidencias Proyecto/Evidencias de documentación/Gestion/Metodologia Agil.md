# Metodología ágil

**Metodología declarada: Scrumban** (Scrum ligero con tablero de ítems estilo Kanban), con sprints semanales agrupados en etapas que cierran los hitos del curso y de Walmart, sin ceremonias formales diarias.

## Por qué Scrumban

- **Requisitos que cambian** durante el semestre: el alcance bajó de "por repisa" a "góndola completa" el 2026-10-19 (indicación del profesor), el umbral se reinterpretó el 2026-09-30 y el cliente pidió ajustes en tres reuniones. Un plan cerrado de cascada no lo habría tolerado; un backlog que se reordena, sí.
- **Entregas con fecha fija** (informe intermedio 2026-10-21, Evaluación 2, revisión de Walmart 2026-11-16, entrega final 2026-11-20): las etapas (Sprint 1 y Sprint 2 del curso) se miden contra esos hitos y, dentro de cada una, el trabajo se ordena por semana.
- **Equipo de 3 personas trabajando en paralelo**, cada una con su propio entorno: un flujo de ramas y Pull Requests por ítem evita pisarse sin reuniones diarias.

## Cómo se trabaja (lo que de verdad se hace)

| Elemento de Scrum/Kanban | Cómo se materializa aquí |
| --- | --- |
| Product Backlog | [Product Backlog](Product%20Backlog.md): copia legible de `PROGRESS.md` (ítems **#N** con dueño y estado) |
| Sprint Backlog | [Sprint Backlog](Sprint%20Backlog.md): los ítems de cada sprint |
| Tablero | `PROGRESS.md` (`[ ]` pendiente, `[x]` hecho, `(dueño: nombre)` en curso) y la Carta Gantt (`Carta Gantt Fase 2.xlsx`, estados Cumplido / En curso / Pendiente / Atrasado / Bloqueado) |
| Dueño del ítem | Quien lo toma se lo asigna en `PROGRESS.md`; lo ejecuta en una rama propia (`feat/`, `fix/`, `docs/`, `chore/`) |
| Revisión | Pull Request contra `main` con CI en verde; desde el 2026-10-19 `main` no exige aprobación de otro integrante |
| Definition of Done | [Definition of Done](Definition%20of%20Done.md) |
| Retrospectiva | [Retrospectivas](Retrospectivas.md): por sprint, reconstruidas desde el historial de git |
| Product Owner | El cliente (Walmart Chile) y el profesor fijan prioridades; el equipo las traduce a ítems |
| Alcance del MVP | [Alcance MVP](Alcance%20MVP.md) |

## Roles

Los tres integrantes son equipo de desarrollo y se reparten los ítems; no hay Scrum Master fijo. La asignación por ítem y por actividad está en la [Matriz RACI](Matriz%20RACI.xlsx).

## Lo que no se hace (y por qué)

- **Daily formal:** no hay evidencia de reuniones diarias; el estado se comunica por `PROGRESS.md`, los Pull Requests y los mensajes del equipo.
- **Planificar semana a semana:** los sprints semanales de la [Documentación SCRUM](Documentacion%20SCRUM.docx) ordenan el trabajo ya hecho según la fecha de integración de cada Pull Request; el [Sprint Backlog](Sprint%20Backlog.md) los agrupa por el hito que cierra cada etapa.
