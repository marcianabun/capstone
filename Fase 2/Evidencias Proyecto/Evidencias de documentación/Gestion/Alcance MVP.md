# Alcance del MVP

El MVP es la **solución de Nivel 2** del README ("Objetivos y Niveles de Solución"), ampliada con la aplicación web que pidió el curso. Vigente desde el 2026-10-19 (cambio de alcance indicado por el profesor: quiebre por **góndola completa**).

## Qué entrega el MVP

| Capacidad | Detalle | Casos de uso |
| --- | --- | --- |
| Analizar una foto de góndola | Corrección de imagen (dewarping y CLAHE) -> segmentación automática de la góndola -> recorte de ROI -> detección de productos con YOLO26 (`yolo26s-finetune`) -> disponibilidad | CU01 |
| Alerta de quiebre de stock | Se alerta cuando el espacio libre de la góndola completa es **>= 30%** (umbral configurable) | CU01, CU02 |
| Alertas y dashboard | Lista de alertas abiertas, estado de las góndolas y estado de los análisis | CU02, CU03 |
| Reportes | Excel, CSV y PDF por período, pasillo o góndola | CU04 |
| Configuración | Umbral de alerta y cámaras | CU05 |
| Usuarios y roles | Login, CRUD de usuarios y perfiles Reponedor, Jefe de Salón y Administrador, con bloqueo de cuenta tras intentos fallidos | CU00, CU06 |
| Despliegue | Docker y Docker Compose; instalación en el servidor del CITT pendiente de instrucciones | - |

## Qué queda fuera del MVP

- **Medición volumétrica exacta (Nivel 1):** el MVP informa el porcentaje de espacio libre en 2D sobre la vista frontal; la profundidad es una constante de 25 cm y no se estima.
- **Alerta o porcentaje por repisa:** las repisas son solo el método interno de medición.
- **Cámaras en vivo:** se analizan fotos subidas por los usuarios (las cámaras de Walmart no se comparten con el equipo).
- **Estimación de profundidad o visión estéreo.**
- **Bodega de reserva sobre la góndola** (ítem #31) y falsas alertas en puertas de vidrio (ítem #46): conocidos y pendientes.

Referencias: [Lista de C. U..xlsx](../Diseño/Lista%20de%20C.%20U..xlsx), [Lista de Requerimientos.xlsx](../Diseño/Lista%20de%20Requerimientos.xlsx) y los acuerdos con el cliente en el [README](../../../../README.md).
