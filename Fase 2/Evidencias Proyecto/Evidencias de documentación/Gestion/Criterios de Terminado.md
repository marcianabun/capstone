# Criterios de Terminado

Un ítem del listado de tareas está **terminado** solo si cumple todo lo siguiente. Son las reglas de trabajo en equipo del repositorio (`CLAUDE.md`, "Trabajo en equipo") y se verifican en cada Pull Request.

1. **Rama propia** por ítem (`feat/`, `fix/`, `docs/`, `build/` o `chore/`); nunca commits directos a `main`.
2. **Pruebas:** `pytest tests/` pasa completo antes de cada commit (303 pruebas al 2026-11-16). En código nuevo, la prueba se escribe primero (TDD).
3. **Docker:** si se tocó `Dockerfile`, `docker-compose.yml` o `requirements.txt`, también `docker build`.
4. **Pull Request a `main`** en español, con qué cambia y cómo se verificó; el **CI de GitHub Actions** (pruebas y `docker build`) debe quedar en verde.
5. **Convenciones del código:** solo scripts `.py`, bounding boxes `[x_min, y_min, x_max, y_max]` en píxeles absolutos, preprocesamiento (OpenCV) antes del modelo (YOLO26), etapas del pipeline sin importar detalles internos de otras.
6. **Commits** en estilo Conventional Commits (tipo en inglés, texto en español) que explican qué cambió y por qué; la historia publicada no se reescribe.
7. **Documentación al día:** el ítem se marca `[x]` en `PROGRESS.md` (solo sus líneas), la Carta Gantt refleja su estado y fecha real, y el README o `docs/` cambian si el comportamiento cambió.
8. **Licencias de datos** respetadas (SKU-110K solo para entrenar y evaluar; nunca para generar imágenes ni demos ante terceros).
9. **Sin secretos** en archivos versionados (las claves van en `.env`, que no se versiona).
