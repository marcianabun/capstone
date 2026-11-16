# Aplicación

El código de ShelfVision AI está en la raíz del repositorio, no en esta
carpeta, porque la aplicación y sus pruebas se ejecutan desde ahí:

| Carpeta o archivo | Qué contiene |
|---|---|
| `src/` | Pipeline de visión: corrección de imagen y segmentación (OpenCV), detector YOLO26, cálculo de disponibilidad y reportes |
| `web/` | Aplicación web Django: login por perfil, usuarios, análisis, góndolas, alertas, reportes y configuración |
| `scripts/` | Línea de comandos del pipeline, entrenamiento y evaluación |
| `tests/` | Pruebas automáticas (`pytest tests/`) |
| `Dockerfile` | Imagen para instalar la aplicación |

Las instrucciones de instalación y ejecución están en el `README.md` de la
raíz, en el [Instructivo del plan de instalación](<../../Evidencias de documentación/Manual de instalación/Instructivo plan de instalación - ShelfVision AI.docx>)
(servidor, con Docker) y en `Implementación ambiente de desarrollo - ShelfVision AI.pdf`
(computador de desarrollo), en esta carpeta. `Video Modelo.mp4` (unos 5 minutos, del 2026-10-21) muestra las
pruebas y la app web funcionando: el análisis de una foto con quiebre y la
gestión de usuarios.
