# Retrospectivas

**Cómo se hicieron:** el equipo no registró retrospectivas en el momento. Estas se **reconstruyeron el 2026-11-14 desde el historial** (git, Pull Requests, `PROGRESS.md` y la [Carta Gantt](Carta%20Gantt%20Fase%202.xlsx)). Cada afirmación cita su evidencia y donde no hay evidencia se escribe "sin evidencia". No incluyen opiniones que nadie haya expresado.

Las acciones marcadas **(por confirmar)** son propuestas que el equipo debe aceptar o descartar.

## Sprint 0 (2026-09-07 a 2026-09-26)

- **Qué pasó:** 21 commits (Nicko 14, que figura como "Mateo" en git; Mariana 4; Francisco 3), todos subidas de documentos de la Fase 1 por la web de GitHub, sin ramas ni Pull Requests.
- **Qué funcionó:** los documentos de la Fase 1 quedaron en el repositorio.
- **Qué no funcionó:** el historial muestra archivos de prueba creados y borrados (`a.txt`, `jj.txt`) y carpetas borradas y vueltas a subir entre el 2026-09-10 y el 2026-09-12.
- **Acción tomada:** el 2026-09-27 se definió el flujo de trabajo en equipo (ramas por ítem, Pull Request, CI), base de la [Definition of Done](Definition%20of%20Done.md).

## Sprint 1 (2026-09-27 a 2026-10-28)

- **Qué pasó:** Pull Requests #3 a #81 integrados y 157 commits entre el 2026-09-27 y el 2026-10-24 (Francisco 83, Mariana 66, Nicko 8; por tipo: 90 `docs`, 27 `feat`, 14 `fix`, 7 `chore`, 3 `ci`, 2 `build`, 1 `refactor`, 13 sin prefijo). Pruebas: 233 el 2026-10-21 (`PROGRESS.md`), 264 el 2026-11-14 y 276 el 2026-11-15.
- **Qué funcionó:** pipeline completo; detector `yolo26s` con mAP50-95 0.610 en `test` de SKU-110K y fine-tuning que sube el mAP50 fuera de dominio de 0.713 a 0.854; app web con login, roles, dashboard, reportes y configuración; informe intermedio entregado el 2026-10-21.
- **Qué no funcionó:**
  - El entrenamiento de `yolo26s-p2` se atascó por memoria de video y porque Windows mandaba el proceso a núcleos de bajo consumo; hubo que arreglarlo (PR #18, `fix/train-vram`) y reanudarlo por tramos (registro del ítem #5).
  - La segunda corrida de fine-tuning (`yolo26s-finetune2`) quedó peor que la primera y se descartó (`docs/test-plan.md`, DET-07).
  - La auditoría del 2026-10-21 encontró problemas en la app web (foto sin productos que daba falsa alerta, alertas no atómicas, configuración insegura, bloqueo de cuenta): siete PR de corrección entre el 2026-10-22 y el 2026-10-23 (PR #69, #70, #75, #76, #79, #80, #81).
  - El cambio de alcance del 2026-10-19 (alerta por góndola completa) llegó a mitad del sprint y obligó a rehacer parte de la alerta y de la documentación (ítem #40).
  - Los ítems #36 (video) y #55 (ruido de cámara) pasaron sin terminar al sprint siguiente.
- **Acciones:** auditar antes de entregar (ítems #49 a #54 y #57) y fijar por commit las acciones del CI (#54).

## Sprint 2 (2026-10-29 a 2026-11-20, parcial al 2026-11-15)

- **Qué pasó:** entre el 2026-10-24 y el 2026-11-13 **no hay commits en `main`**: sin evidencia de trabajo integrado en esas tres semanas. Las ramas `feat/ruido-camara` y `feat/camara-sala-simulada` se subieron el 2026-11-09 sin Pull Request; sus PR (#90 y #91) se abrieron e integraron el 2026-11-15. El 2026-11-14 se integraron siete PR (#82 a #88): mensajes del profesor, manuales de usuario, orden de carpetas, registro de la imagen del profesor, el modelo del detector y los faltantes de la auditoría N.º 4. El 2026-11-15, siete más (#89 a #93, #95 y #96): reflexiones de Francisco, ruido de cámara de sala y su corrección (#55, #58, #68, #76), medición por tipo de ruido (#78) y reentrenamiento con desenfoque más fuerte (#79).
- **Qué funcionó:** el orden de carpetas y los manuales de usuario se resolvieron el mismo día de la instrucción del profesor.
- **Qué no funcionó:** la auditoría N.º 4 (2026-10-25) marcó como faltantes metodología ágil, requisitos no funcionales, innovación, UML, `docker-compose.yml` y la sección Tecnologías del README; hasta el 2026-11-14 no tenían ítem en el backlog. El ítem #55 (planificado del 2026-10-29 al 2026-11-06) se cerró recién el 2026-11-15, nueve días tarde.
- **Acciones:** ítems #68 a #75 con plazo antes de la revisión del 2026-11-16. **(por confirmar)** Revisar cada auditoría el mismo día que llega y no dejar semanas sin Pull Requests.
