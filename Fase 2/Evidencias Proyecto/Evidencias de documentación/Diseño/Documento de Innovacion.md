# Documento de innovación

Qué aporta ShelfVision AI y qué lo distingue de las alternativas obvias. Cada afirmación remite a una decisión del [README](../../../../README.md) o a una medición de [docs/analisis-resultados.md](../../../../docs/analisis-resultados.md) y [docs/test-plan.md](../../../../docs/test-plan.md). Lo que no se midió se dice.

## El problema y la alternativa de hoy

Detectar quiebres de stock en góndola exige que una persona recorra el pasillo. El sistema analiza una foto de una cámara de sala y responde una pregunta: ¿el espacio libre de la góndola completa es mayor o igual al 30% del frente? La respuesta sale como alerta (sí/no), porcentaje libre y foto anotada con los huecos.

Quedan fuera del documento comparaciones con la operación real de Walmart (frecuencia de recorridos, costo) porque el equipo no tiene esos datos.

## Qué se hizo distinto

| Innovación | Qué la distingue | Evidencia |
| --- | --- | --- |
| **Mide el espacio vacío, no cuenta productos** | Una sola clase ("producto"): no necesita catálogo, SKU ni planograma, y funciona con cualquier categoría de no perecibles | README, "Una sola clase de producto" |
| **Enfoque híbrido: visión clásica antes del modelo** | OpenCV corrige la imagen (dewarping y CLAHE), segmenta la góndola y recorta la ROI **antes** de YOLO26. Ningún usuario dibuja zonas por cámara | README, "OpenCV antes de YOLO26" y "Segmentación automática de ROI" |
| **Detector sin NMS para góndolas apiladas** | YOLO26 con cabeza sin NMS y hasta 1000 cajas por foto: no suprime productos vecinos que se tocan ni trunca góndolas llenas | README, "YOLO26 con cabeza sin NMS" |
| **Niveles de repisa híbridos** | Las filas de productos detectados marcan la repisa aunque esté inclinada; las líneas de la segmentación aportan las repisas vacías. Funciona con cámara en ángulo | README, "Niveles de repisa híbridos"; DET y AV en `docs/test-plan.md` |
| **Huecos medidos como cobertura a lo largo de la repisa** | Un hueco cuenta solo si cabe al menos un ancho de producto (no se puede reponer menos); el espacio vertical sobre un producto no cuenta (respuesta a "la trampa del apilamiento") | README, "Fachada visible, sin apilamiento" |
| **Una alerta por góndola completa** | El % y la alerta que se informan son de la góndola entera; las repisas son solo el método interno de medición | README, cambio de alcance del 2026-10-19 |
| **Fine-tuning fuera de dominio con datos que se pueden modificar** | El detector entrenado con SKU-110K se ajustó con fotos de Kaggle (CC0) y vistas giradas, cumpliendo la licencia de SKU-110K | `docs/datasets.md`, DET-07 |
| **Reproducible y explicable** | Docker y Docker Compose, 276 pruebas sin datos, pesos ni GPU, etapas desacopladas; Walmart prefiere un modelo que el equipo pueda explicar | README, [Requisitos no funcionales](Requisitos%20No%20Funcionales.md) |

## Resultados medidos que respaldan el aporte

- Detector `yolo26s` en el conjunto de prueba de SKU-110K: mAP50 0,950 y mAP50-95 0,610.
- Fuera de dominio (45 fotos de Kaggle): mAP50 0,713 y recall 0,644; con el fine-tuning (`yolo26s-finetune`, 12 fotos de prueba) el mAP50 sube a 0,854 y el recall a 0,809 (DET-06 y DET-07).
- Sistema completo: acierta la alerta en 92% de las fotos de productos envasados (33 de 36), según el README y `docs/analisis-resultados.md`.
- Tiempo: mediana de 0,51 s por foto en CPU en un lote (objetivo de 2 a 5 s).

## Límites (lo que no se afirma)

- El sistema no estima profundidad: usa 25 cm constantes y el análisis es 2D sobre la vista frontal.
- Frutas a granel, vidrio y reflejos son puntos débiles conocidos (ítem #46). El ruido de cámara de sala se midió solo simulado sobre 12 fotos (DET-08 a DET-10): cumple mAP50 >= 0,70 salvo con desenfoque de movimiento fuerte; con una cámara real no se ha medido.
- Si una persona o un carro tapa la góndola, el hueco tapado se mide como espacio libre y puede dar una falsa alerta (ítem #77, pendiente).
- No se ha probado con fotos ni cámaras de Walmart: no las comparte.
