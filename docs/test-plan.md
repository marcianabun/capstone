# Plan de pruebas - ShelfVision AI

Verifica que cada etapa ya construida cumple lo que promete: qué
requisito cubre, cómo se prueba, qué resultado se exige y qué resultado
dio la última vez. Ítem #19 de `PROGRESS.md`.

**Cuándo se ejecuta completo:**

1. Al mergear el ítem #6 (disponibilidad, PR #16).
2. Cuando exista el detector entrenado (`best.pt`, ítem #5).
3. Antes de cada entrega académica (Fase 2 y Fase 3).

Cada ejecución se anota en el [registro](#registro-de-ejecuciones) al
final.

## Tipos de prueba

| Tipo | Qué asegura | Cómo se corre |
| --- | --- | --- |
| **Unitaria** | El contrato de cada función: formato de bbox, coordenadas, errores ante entradas inválidas | `pytest tests/` (también en el CI de cada PR) |
| **Métrica** | Que el método funciona sobre datos reales, con un número comparable entre versiones | Scripts de `scripts/` sobre los datasets de `data/raw/` |
| **Integración** | Que cada caso de uso funciona en la app web con su base de datos y sus permisos por perfil | `tests/test_web.py` (sección 8) |
| **Visual** | Lo que un número no muestra: repisas mal puestas, cajas corridas | Láminas generadas por los visores, revisadas con la lista de cada sección |
| **Trazabilidad** | Que cada requisito del README (RF01-RF06) y cada regla de `CLAUDE.md` tiene al menos una prueba | Tablas de las secciones 9 y 10 |

Los criterios marcados **(por acordar)** no estaban definidos en el
proyecto: son una propuesta basada en lo ya medido y se confirman en la
revisión de este plan.

## Cómo ejecutarlo

Desde la raíz del repo, con el `.venv` activo y los datasets descargados
(ver `docs/datasets.md`):

```bash
pytest tests/                                          # unitarias
python scripts/download_datasets.py --check            # DAT-01
python scripts/prepare_datasets.py                     # DAT-04 (sin --dataset, ver DAT-04)
python scripts/evaluate_shard.py --split holdout       # SEG-02
python scripts/visualize_segmentation.py               # SEG-03 y SEG-04
python scripts/evaluate_availability.py                # AV-02 y AV-03
python scripts/train_detector.py val --weights <best.pt> --split test   # DET-04 (con el modelo entrenado)
```

## 1. Datos (ítems #10, #11, #12, #16)

| ID | Qué se verifica | Cómo | Criterio | Último resultado |
| --- | --- | --- | --- | --- |
| DAT-01 | Los 6 datasets están completos en `data/raw/` | `download_datasets.py --check` | Los 6 en OK | OK (2026-09-29) |
| DAT-02 | Los conversores llevan cada formato (COCO, CSV, XML, Supervisely) a `[x_min, y_min, x_max, y_max]` en píxeles | `tests/test_dataset_converters.py` | Pasan | Pasan |
| DAT-03 | La descarga es reproducible y segura (versiones fijas, sin rutas que escapan de la carpeta) | `tests/test_dataset_sources.py` | Pasan | Pasan |
| DAT-04 | Las anotaciones combinadas están completas | `prepare_datasets.py`; revisar el total | 1,760,633 anotaciones de 5 datasets | 1,760,633 (#11). **Problema conocido:** con `--dataset X`, `all_annotations.csv` queda solo con ese dataset; correrlo sin `--dataset` |
| DAT-05 | El dataset YOLO es correcto (cajas normalizadas y ruta local) | `tests/test_dataset_converters.py` (`xyxy_to_yolo`) y `prepare_yolo_dataset.py --limit 16` | Pasan; `data.yaml` apunta a la carpeta del repo | OK (2026-09-30, regenerado tras mover el repo) |

## 2. Corrección de imagen (ítem #3)

| ID | Qué se verifica | Cómo | Criterio | Último resultado |
| --- | --- | --- | --- | --- |
| COR-01 | CLAHE mejora el detalle en sombras sin alterar colores | `tests/test_image_correction.py` | Pasan | Pasan |
| COR-02 | El dewarping endereza una repisa curvada (distorsión sintética) y `to_original()` vuelve a la imagen original | `tests/test_image_correction.py` | Pasan | Pasan |
| COR-03 | Sin calibración solo se aplica CLAHE y las coordenadas no cambian | `tests/test_image_correction.py` | Pasan | Pasan |
| COR-05 | Cámara defectuosa (CU01, excepción 1a, #87): una foto toda verde o toda magenta no se analiza; una góndola real, aun casi de un solo color, sí | `tests/test_camera_check.py` y `tests/test_web.py`; `camera_fault()` sobre 2.808 fotos reales (Kaggle, SHARD, Roboflow, UniDataPro y SKU-110K) y las 45 de Kaggle teñidas de verde y de magenta | Ninguna foto real rechazada; todas las teñidas detectadas | **Cumple** (2026-11-16): 0 de 2.808 reales rechazadas; 45 de 45 verdes y 45 de 45 magenta detectadas. En 4.800 fotos reales el tinte llega a 1,16 (verde) y 1,42 (magenta); el umbral es 2,0 |
| COR-04 | El dewarping funciona con una cámara real | Parámetros de calibración que entregue Walmart (calibrando ellos con un tablero de ajedrez; no comparten imágenes de sus cámaras, #21) | Repisas rectas a ojo; error de reproyección < 1 px **(por acordar)** | **No probado**: no hay calibración real |

## 3. Segmentación de góndola y repisas (ítems #4, #15)

| ID | Qué se verifica | Cómo | Criterio | Último resultado |
| --- | --- | --- | --- | --- |
| SEG-01 | Repisas, niveles y ROI en imágenes sintéticas (incluidas repisas inclinadas y el caso sin repisas) | `tests/test_gondola_segmentation.py` y `tests/test_shelf_evaluation.py` | Pasan | Pasan |
| SEG-02 | Las repisas detectadas coinciden con las anotadas en SHARD (tolerancia 3% del alto) | `evaluate_shard.py --split holdout` | F1 >= 0.80 **(por acordar)**; no bajar de la última medición | P 0.796 / R 0.851 / F1 0.823 (2026-09-30; igual que en #15) |
| SEG-03 | La ROI contiene los productos | `visualize_segmentation.py` (`metrics.csv`, `annotations_inside_roi`) | >= 0.99 en cada dataset | 0.99-1.00 (2026-09-30) |
| SEG-04 | Revisión visual de 30 láminas por dataset | `visualize_segmentation.py` | Las líneas rojas caen sobre bordes de repisa reales; sin diagonales; la ROI cubre los productos. Anotar los casos que fallan | Hecho en #15; limitaciones en #17 |
| SEG-05 | Funciona con vista de cámara de sala (alta, oblicua, fisheye) | Imágenes tipo CCTV (#14) | Por definir con #14 | **Parcial** (#22): con giro de cámara la segmentación sola pierde repisas; los niveles de la disponibilidad salen de `shelf_levels()` (AV-06). Sin probar: fisheye y cámaras reales |

## 4. Recorte de ROI (ítems #1, #2)

| ID | Qué se verifica | Cómo | Criterio | Último resultado |
| --- | --- | --- | --- | --- |
| ROI-01 | Recorte exacto; ROI parcialmente fuera se recorta; ROI totalmente fuera, imagen `None` o vacía -> `ValueError` | `tests/test_preprocessing.py` | Pasan | Pasan |
| ROI-02 | Una caja del recorte vuelve a su lugar en la imagen original (`RoiCrop.to_original()`) | `tests/test_preprocessing.py` y `tests/test_detector.py` | Pasan | Pasan |

## 5. Detector YOLO26 (ítem #5)

| ID | Qué se verifica | Cómo | Criterio | Último resultado |
| --- | --- | --- | --- | --- |
| DET-01 | Contrato de inferencia: `ultralytics>=8.4.0`, cabeza sin NMS (`nms=False`), sin tope de 300 cajas, rechazo de modelos que no son YOLO26 | `tests/test_models.py` y `tests/test_detector.py` | Pasan | Pasan |
| DET-02 | El entrenamiento corre de punta a punta y se reanuda | Prueba corta de `docs/training.md` (16 fotos, 1 época) | Termina y deja `best.pt` y `metrics.json` | OK en CPU (2026-09-29) |
| DET-03 | Comparación de `yolo26s` y `yolo26s-p2` en `val` | `train_detector.py val` para cada una | Se elige por `map50_95` y luego `recall` (ver `docs/training.md`) | `yolo26s` 0.606 contra 0.596 de `yolo26s-p2`: gana `yolo26s` (2026-10-07, #5) |
| DET-04 | La variante ganadora en `test` (una sola vez) | `train_detector.py val --split test` | Recall >= 0.90 con `conf=0.25` **(por acordar)**: la tasa de falsas alertas de AV-02 (4%) se midió con recall 0.9, y con 0.8 sube a 11.7%. `map50_95` se informa | R 0.885, mAP50 0.950, mAP50-95 0.610 (2026-10-07): **bajo el criterio** por poco |
| DET-06 | El detector fuera de SKU-110K (#33): fotos que no se usaron para entrenar | `train_detector.py val --data` con las 45 fotos de Kaggle en formato YOLO; `run_pipeline.py --annotations` para P y R por foto | mAP50 >= 0.70 (si no, fine-tuning; #33) | mAP50 0.713, mAP50-95 0.423, P 0.843, R 0.644 (2026-10-20, #34): cumple por poco; recall muy bajo el de DET-04 |
| DET-05 | Revisión visual de las detecciones | Láminas de la vista anotada de los 10 mejores y 10 peores casos (`docs/analisis-resultados.md`, #34) | Cajas ajustadas a cada producto, sin cajas sobre carteles ni pilares | **Hecho** (2026-10-20, #34): cajas ajustadas en los mejores casos; los errores se concentran en frutas y verduras sueltas (fuera del alcance) y refrigeradores con vidrio (#46) |
| DET-07 | Fine-tuning con Kaggle CC0 y vistas giradas (#33): mejora fuera de dominio sin olvidar SKU-110K | `prepare_finetune_dataset.py` + `train_detector.py finetune`, y `val` en `data/processed/yolo/finetune/data-{f,y20,y35}.yaml` (12 fotos de Kaggle, de frente y giradas) y `--split test` de SKU-110K | Mejora mAP50 en las 3 vistas; mAP50 en SKU-110K `test` no baja más de 0.02 **(por acordar)**; mAP50-95 se informa | `yolo26s-finetune` (2026-10-21): mAP50 0.809 -> 0.854 / 0.778 -> 0.837 / 0.701 -> 0.818; SKU-110K `test` mAP50 0.950 -> 0.940, mAP50-95 0.610 -> 0.533 (informado). 2.ª corrida (1500 fotos SKU, lr0 0.0005): 0.834 / 0.823 / 0.805 y 0.943 / 0.548, descartada |
| DET-08 | El detector con ruido de cámara de sala (#55, #76): las 12 fotos de prueba de Kaggle degradadas con `degrade()` (sensor, poca luz, contraluz, JPEG fuerte, baja resolución, desenfoque, reflejos; mezcla al azar, semilla fija). Las cajas que una persona u objeto tapa más del 80 % se descartan (no se pueden detectar). La validación se reparte en **óptico** (23 imágenes sin nada que tape) y **oclusión** (13 con persona u objeto) | `prepare_finetune_dataset.py` (arma `val-*-optico`, `val-*-oclusion` y `data-{ruido,optico,oclusion}.yaml`), `train_detector.py finetune --name yolo26s-finetune-ruido-v2` con una copia con ruido por vista de entrenamiento, y `val` en esos YAML | mAP50 >= 0.70 con ruido (RNF02); el modelo con ruido no empeora al anterior, ni en fotos limpias ni en SKU-110K `test` | mAP50 (limpias / con ruido / óptico / oclusión): `yolo26s-finetune` 0.836 / 0.792 / 0.815 / 0.746; `yolo26s-finetune-ruido-v2` (2026-11-15, 30 épocas) 0.839 / 0.804 / 0.823 / 0.763. Por vista con ruido (de frente / 20° / 35°): 0.804 / 0.795 / 0.777 contra 0.816 / 0.807 / 0.787. SKU-110K `test` mAP50 0.939 y mAP50-95 0.537 contra 0.940 y 0.533. **Cumple**: la mejora (+0.012 con ruido) es chica y sale de 12 fotos, así que no justifica reemplazar a `yolo26s-finetune`, que sigue siendo el modelo versionado. De la caída de recall con ruido (0.744 a 0.685, medido a conf 0.25 con IoU 0.5), las cajas tapadas explican 1.2 puntos y el resto es degradación real. La 1.ª versión (`yolo26s-finetune-ruido`, que entrenaba con las cajas tapadas) acertaba 34 % de las cajas tapadas más del 80 % contra 14 % del modelo base: aprendía a marcar productos que no se ven; la v2 acierta 11 %. Con el desenfoque más fuerte de #79 estas cifras cambian (ver DET-10). Por tipo de ruido: DET-09 |
| DET-09 | El detector por tipo y nivel de ruido (#78), un efecto a la vez, en las 36 vistas de prueba de Kaggle (12 fotos, de frente y giradas) | `prepare_finetune_dataset.py` y `scripts/measure_noise.py` (ruido del sensor, JPEG, baja resolución, desenfoque de foco y de movimiento, poca y mucha luz, y una columna que tapa 5, 10 y 20 % del ancho, sin las cajas tapadas más del 80 %) | mAP50 >= 0.70 en cada nivel (RNF02) | `yolo26s-finetune`, mAP50 en nivel bajo / medio / alto (limpias 0.836): sensor (sigma 5/10/20) 0.837 / 0.833 / 0.804; JPEG (calidad 50/30/15) 0.835 / 0.833 / 0.813; baja resolución (escala 0.5/0.35/0.2) 0.828 / 0.816 / 0.785; poca luz (ganancia 0.6/0.4/0.25) 0.836 / 0.831 / 0.819; mucha luz (1.5/2.0/2.5) 0.824 / 0.799 / 0.777; desenfoque de foco (sigma 1.5/3/5) 0.814 / 0.774 / 0.712; desenfoque de movimiento (largo 7/15/31) 0.814 / 0.760 / **0.577**; oclusión (5/10/20 %) 0.800 / 0.801 / 0.799. **Parcial**: solo el desenfoque de movimiento de 31 píxeles baja de 0.70, y el de foco de sigma 5 queda al borde (0.712). El sensor, el JPEG, la poca luz y la baja resolución casi no lo afectan. La oclusión cuesta ~0.035 aunque tape poco, porque deja cajas medio tapadas. Una semilla, 12 fotos y efectos sintéticos: sirven para ordenar los riesgos, no como medida de una cámara real |
| DET-10 | Fine-tuning con desenfoque más fuerte (#79): `degrade()` sube el desenfoque de foco de sigma 3 a 5 y el de movimiento de 14 a 31 px, y se reentrena con 2 copias con ruido por vista | `prepare_finetune_dataset.py --ruido 2`, `train_detector.py finetune --name yolo26s-finetune-ruido-v3`, `scripts/measure_noise.py --weights ...` y `val` en `data-{ruido,optico,oclusion}.yaml` | mAP50 >= 0.70 en cada nivel de DET-09; sin bajar en fotos limpias ni en SKU-110K `test` más de 0.02 | `yolo26s-finetune-ruido-v3` (2026-11-15, 30 épocas) contra `yolo26s-finetune`, mAP50: desenfoque de foco (sigma 1.5/3/5) 0.830 / 0.802 / 0.756 contra 0.814 / 0.774 / 0.712; de movimiento (7/15/31 px) 0.832 / 0.792 / **0.647** contra 0.814 / 0.760 / 0.577; sensor, JPEG, baja resolución, luz y oclusión suben 0.002 a 0.04 en todos los niveles. Limpias 0.844 contra 0.836; SKU-110K `test` mAP50 0.935 contra 0.940 y mAP50-95 0.535 contra 0.533. Validación con ruido de DET-08 (con el nuevo `degrade()`; la base se recalculó: 0.780 / óptico 0.802 / oclusión 0.728): v3 0.801 / 0.820 / 0.759 y v2 0.795 / 0.815 / 0.750. **Cumple** salvo el desenfoque de movimiento de 31 px, que sigue bajo 0.70 (0.647) aunque mejora 0.07. Es el mejor modelo en todas las filas, sobre 12 fotos y una semilla |
| DET-11 | Desenfoque de movimiento más frecuente y fuerte (#82): `degrade()` lo aplica aparte en el 30 % de las fotos y hasta 41 px, y se reentrena | `train_detector.py finetune --name yolo26s-finetune-ruido-v4`, `scripts/measure_noise.py` y `val` en `data-{ruido,optico,oclusion}.yaml`; además, realce (unsharp mask) antes de detectar | mAP50 >= 0.70 con movimiento de 31 px | **No cumple, sin mejora real**: `yolo26s-finetune-ruido-v4` (2026-11-15) da 0.652 con movimiento de 31 px contra 0.647 de la v3 y 0.577 del modelo anterior (foco sigma 5: 0.745 contra 0.756; limpias 0.841 contra 0.844; SKU-110K `test` 0.937 contra 0.935; con ruido de DET-08 0.797 contra 0.795). El realce antes de detectar sirve poco con desenfoque de foco (sigma 5: 0.756 a 0.773) y empeora el de movimiento (31 px: 0.647 a 0.622). Un desenfoque de 31 px es 1.2 % del ancho de la foto: la información ya no está en la imagen, así que no se arregla con más aumentación. Se acepta como límite y no se reemplaza el modelo versionado (v3) |

## 6. Disponibilidad y alerta (ítems #6 y #22)

| ID | Qué se verifica | Cómo | Criterio | Último resultado |
| --- | --- | --- | --- | --- |
| AV-01 | Huecos, acotado a los productos, niveles (bbox y franjas inclinadas), umbral inclusivo de 30%, volumen con 25 cm. La alerta es solo de la góndola completa: una repisa sobre el umbral no alerta si la góndola no lo alcanza (#40) | `tests/test_availability.py` | Pasan | Pasan (29 tests, 2026-10-19) |
| AV-02 | Falsas alertas con la góndola llena (anotaciones de SKU-110K como detector, recall simulado 0.9) | `evaluate_availability.py` | <= 5% **(por acordar)** | 4.0% (2026-09-30). Con los niveles de `shelf_levels()` (variante `hibrido`, #22): 6% en las mismas 300 fotos y en 288 de control (2026-10-01), **sobre el criterio** |
| AV-03 | Detección de un quiebre simulado de 40% del frente en el interior | `evaluate_availability.py` | >= 95% **(por acordar)** | 99.7% (2026-09-30); `hibrido`: 100% (2026-10-01) |
| AV-04 | AV-02 y AV-03 con las detecciones del modelo entrenado en vez de las anotaciones | `run_pipeline.py --annotations` sobre fotos anotadas (sistema completo con el detector); `evaluate_availability.py` no tiene la opción de detector | Mismos criterios | **Parcial** (2026-10-20): con el detector, alerta correcta en 84% de 44 fotos de Kaggle y 92% en las 36 de envasados (registro de esa fecha); no se repitió el quiebre simulado de AV-03 |
| AV-05 | Niveles desde filas de productos: repisas inclinadas, repisa vacía aportada por la segmentación, pilas, diagonales, recorte a la ROI; vistas sintéticas en ángulo | `tests/test_shelf_levels.py`, `tests/test_synthetic_views.py` | Pasan | Pasan (18 + 6 tests, 2026-10-01) |
| AV-06 | AV-02 y AV-03 con la cámara girada (vistas sintéticas de Kaggle, 45 fotos, giro 20° y 35° y 15° hacia abajo) | `evaluate_availability.py --dataset kaggle --yaw 0 20 35 --pitch -15` | Mismos criterios **(por acordar)** | `hibrido`, recall 0.9: falsas alertas 2% / 2% (20° / 35°); quiebre de 40% detectado 96% / 91% (2026-10-01) |
| AV-07 | Oclusión por personas (#77): lo que tapa una persona se mide como frente no visible, no como espacio libre | `tests/test_availability.py` y `tests/test_pipeline.py` (cajas de oclusión), `PersonDetector` (`src/models/people.py`, pesos de COCO) en 45 fotos de Kaggle y en `bus.jpg` y `zidane.jpg` de Ultralytics | El hueco tapado no cuenta como libre; con más de 50 % del frente tapado, `inconclusive` y sin alerta; ningún falso positivo en las 45 fotos de góndola | **Parcial** (2026-11-15): la medición está probada con cajas sintéticas. El detector de personas sin filtro marca como persona las caras impresas en cajas de remedios y cereales (4 de 45 fotos, hasta 26 por foto, todas de menos de 15 % del alto); con el filtro de persona alta (>= 40 % del alto, ancho <= alto) quedan 0 de 45, y en fotos con personas reales encuentra 5 de 6 (la que falta sale cortada). **Falta** validar con fotos de góndola con clientes (Walmart no las comparte) (ya va activo por defecto con `weights/yolo26n.pt` versionado) |

## 7. Integración entre etapas

| ID | Qué se verifica | Cómo | Criterio | Último resultado |
| --- | --- | --- | --- | --- |
| INT-01 | Una detección sobre el recorte vuelve a la imagen original | `tests/test_detector.py` | Pasa | Pasa |
| INT-02 | El pipeline completo corre sobre una imagen: `correct_image()` -> `segment_gondola()` -> `crop_roi()` -> `detect()` -> `to_original()` -> `compute_availability()` | `tests/test_pipeline.py`: góndola sintética con un detector falso por color (`tests/pipeline_fixtures.py`); `tests/test_run_pipeline_cli.py` para el CLI | Pasa; resultado igual al de las etapas por separado | Pasa (2026-10-10): igual a las etapas encadenadas a mano; vaciar dos repisas crea sus huecos y la alerta |
| INT-03 | Sistema de coordenadas: la disponibilidad se calcula en la imagen corregida (donde se segmentaron las repisas) y el reporte usa la original | `tests/test_pipeline.py`: la góndola sintética distorsionada con `LensCalibration.approximate(k1=-0.25)` | Los huecos coinciden con los de la imagen corregida | Pasa (2026-10-10): cajas y esquinas de repisa iguales a las calculadas en la imagen corregida y llevadas a la original; bordes densificados (curvos con lente) |

## 8. Aplicación web y casos de uso (ítems #28, #43 a #45, #84 a #87, #94, #96)

Pruebas de integración de la app Django con su base de datos, en
`tests/test_web.py` (67 pruebas) y `tests/test_report_export.py`. El
análisis usa un detector falso para no depender de los pesos ni de la
GPU, igual que en el CI.

| ID | Qué se verifica | Cómo | Criterio | Último resultado |
| --- | --- | --- | --- | --- |
| WEB-01 | **CU00 Autenticar**: el login con RUT o correo lleva a la vista de su perfil; 5 intentos fallidos bloquean 15 minutos sin desactivar la cuenta; el Administrador desbloquea; cada perfil ve solo lo suyo | `test_login_*`, `test_bloquea_15_minutos_tras_5_intentos_sin_desactivar_la_cuenta`, `test_el_admin_desbloquea_antes_de_tiempo`, `test_cada_perfil_ve_solo_lo_suyo` | Pasan | Pasan (2026-11-18) |
| WEB-02 | **CU01 Analizar una foto**: abre la alerta con ubicación; normaliza pasillo y góndola; rechaza archivos que no son imagen, fotos de más de 20 MB o 50 megapíxeles, fotos sin productos, góndolas tapadas por una persona (#77) y fotos de cámara defectuosa (#87), sin tocar la alerta abierta; si falla el guardado, la alerta abierta no se cierra | `test_analisis_de_foto_abre_alerta_con_ubicacion_y_franjas`, `test_foto_*`, `test_archivo_que_no_es_imagen_se_rechaza`, `test_gondola_tapada_*`, `test_si_falla_el_guardado_*` | Pasan | Pasan (2026-11-18) |
| WEB-03 | **CU02 Alertas**: el Reponedor toma y completa la alerta; una foto nueva la reemplaza o confirma la reposición; tomar una alerta ya reemplazada no la reabre; no se informa % ni alerta por repisa (#40). La notificación push quedó fuera del alcance (#88) | `test_reponedor_toma_y_completa_la_alerta`, `test_foto_nueva_reemplaza_la_alerta_o_confirma_la_reposicion`, `test_tomar_una_alerta_ya_reemplazada_no_la_reabre`, `test_no_informa_porcentaje_ni_quiebre_por_repisa` | Pasan | Pasan (2026-11-18) |
| WEB-04 | **CU03 Dashboard**: estado de la última foto de cada góndola (amarillo desde la mitad del umbral; sin datos si no hay foto reciente); detalle con historial; índice por góndola y fecha (#85) | `test_dashboard_*`, `test_amarillo_desde_la_mitad_del_umbral`, `test_sin_foto_reciente_o_camara_sin_fotos_es_sin_datos`, `test_detalle_de_gondola_con_su_historial` | Pasan | Pasan (2026-11-18) |
| WEB-05 | **CU04 Reportes** (RF05): CSV con una fila por análisis, % libre y alerta; Excel y PDF; filtro por góndola; sin datos avisa y no genera archivo; rechaza un período invertido; el Reponedor no exporta; no carga el JSON del resultado (#85) | `test_reporte_*`, `test_reponedor_no_exporta_reportes`, `tests/test_report_export.py` | Pasan | Pasan (2026-11-18) |
| WEB-06 | **CU05 Configurar**: el umbral rige para las fotos siguientes y uno fuera de rango se rechaza; la calibración de la cámara se usa al analizar su góndola, se conserva al editar sin archivo y se rechaza si es inválida; una cámara por góndola; solo el Administrador configura | `test_admin_cambia_el_umbral_*`, `test_umbral_fuera_de_rango_*`, `test_*calibracion*`, `test_una_gondola_tiene_una_sola_camara`, `test_solo_el_admin_configura` | Pasan | Pasan (2026-11-18) |
| WEB-07 | **CU06 Cuentas y roles** (#84): el Administrador crea el usuario y ve en pantalla su enlace de un solo uso para definir la contraseña (sin correo); genera uno nuevo si no la definió; solo el Administrador lo hace; RUT con dígito verificador válido; el Administrador no se desactiva a sí mismo; desactivar cierra la sesión abierta | `test_admin_crea_usuario_y_ve_en_pantalla_su_enlace_de_un_uso`, `test_admin_genera_un_enlace_nuevo_*`, `test_solo_el_admin_genera_el_enlace`, `test_*rut*`, `test_admin_no_puede_desactivarse_a_si_mismo`, `test_desactivar_cierra_la_sesion_abierta` | Pasan | Pasan (2026-11-18) |
| WEB-08 | **CU07 Evaluar un lote** (RF06): `run_pipeline.py --annotations` deja la vista, el JSON y las métricas IoU por foto y por lote | `tests/test_run_pipeline_cli.py`, `tests/test_detection_metrics.py` | Pasan | Pasan (2026-11-18) |
| WEB-09 | **Navegación, privacidad y cámara simulada**: «Últimos análisis» se pagina de a 25 (#96); Anterior y Siguiente recorren la misma góndola o las alertas abiertas (#94); borrar las fotos antiguas conserva el análisis (RNF05, #45); la cámara de sala simulada registra la cámara y analiza fotos degradadas (#58) | `test_ultimos_analisis_se_paginan_de_a_25`, `test_botones_*`, `test_las_alertas_abren_la_foto_en_modo_alertas_*`, `test_borrar_fotos_*`, `test_simular_camara_*` | Pasan | Pasan (2026-11-18) |
| WEB-10 | **Analizar por ruta** (#95): una foto o una carpeta dentro de `SHELFVISION_PHOTOS_DIR` se analiza con el pasillo y la góndola del formulario; se rechazan rutas fuera de la carpeta (con `..` o absolutas), inexistentes, más de 20 fotos y el caso de elegir foto y ruta a la vez o ninguna; una foto mala no frena a las demás | `test_ruta_*`, `test_hay_que_elegir_una_foto_o_una_ruta_*`, `test_carpeta_con_demasiadas_fotos_*`, `test_una_foto_mala_de_la_carpeta_*` | Pasan | Pasan (2026-11-22) |

## 9. Trazabilidad con los requisitos (README)

| Requisito | Cubierto por | Estado |
| --- | --- | --- |
| RF01 Ingesta de imágenes, 2 a 5 s por imagen | INT-02; tiempo por etapa de `scripts/run_pipeline.py` | **Cumple en CPU**: mediana 0.51 s por foto (45 fotos de Kaggle de 5616 x 3744, i5-13400F, 4 hilos, 2026-10-20; antes 0.70 s con 6 fotos). Falta medir en el hardware final |
| RF02 Espacios vacíos dentro de la ROI | SEG-03, AV-01, AV-02 | Cubierto con anotaciones; falta con el detector (AV-04) |
| RF03 Disponibilidad en % o cm, profundidad fija de 25 cm | AV-01 (% y volumen) | % cubierto. Para cm falta la escala cm/px de cada cámara, que hoy no tiene fuente |
| RF04 Alertas de quiebre | AV-01 a AV-03 (la decisión de alertar, una por góndola completa); `tests/test_pipeline.py` y `tests/test_annotate.py` (el JSON y la vista no traen % ni alerta por repisa, #40); WEB-03 (ciclo de la alerta en la app); COR-05 (cámara defectuosa, #87) | **Cumple**: la alerta se ve y se atiende en la app. La notificación push al teléfono quedó fuera del alcance del MVP (#88) |
| RF05 Reportes Excel, CSV y PDF | WEB-05 | **Cumple** (#7) |
| RF06 Evaluación por lotes | WEB-08; registro del 2026-10-20 (44 fotos de Kaggle con `--annotations`) | **Cumple** |

## 10. Reglas de `CLAUDE.md`

| Regla | Cómo se verifica | Estado |
| --- | --- | --- |
| Bounding boxes `[x_min, y_min, x_max, y_max]` en píxeles | DAT-02, ROI-02, DET-01 | Cubierta |
| Orden híbrido: corrección -> segmentación -> recorte -> YOLO26 | INT-02 (el detector recibe la imagen corregida recortada a la ROI) | Cubierta |
| ROI automática, sin configuración por cámara | Revisión de código: ninguna función lee una ROI de configuración | Cubierta por diseño |
| Profundidad constante de 25 cm | AV-01 (`GONDOLA_DEPTH_CM`) | Cubierta |
| YOLO26 con `nms=False`, `max_det >= 1000`, `imgsz=1280` | DET-01 | Cubierta |
| Etapas sin importar detalles internos de otras | Test que revise los `import` de cada paquete de `src/` **(por agregar)** | **Sin test** |
| Alerta con espacio libre >= 30% | AV-01 | Cubierta |

## 11. Lo que aún no se puede probar

- **Dataset oculto de Walmart**: se reserva para la evaluación ciega
  final; nunca se usa para ajustar. Walmart no comparte imágenes de sus
  cámaras (privacidad, #21): la evaluación solo puede correrla Walmart en
  sus instalaciones, con nuestra imagen Docker, y entregar las métricas.
- **Cámaras reales de sala**: Walmart no comparte fotogramas y la
  calibración está por confirmar (COR-04, SEG-05). Mientras tanto,
  imágenes sintéticas tipo CCTV (#14) desde datasets cuya licencia lo
  permite (no SKU-110K).
- **Escala en centímetros** (RF03 en cm): depende de cada cámara.
- **Tiempo en el hardware final** (RF01): no se conoce el equipo donde
  correrá el sistema.
- **Oclusión con clientes reales** (AV-07): falta validarla con fotos
  de góndolas con personas.

## Registro de ejecuciones

| Fecha | Commit | Quién | Resultado | Observaciones |
| --- | --- | --- | --- | --- |
| 2026-09-30 | `main` 4848c64 + PR #16 | Francisco | `pytest`: 131 passed. AV-02 y AV-03 cumplen. SEG-02 y SEG-03 tomados de #15 (2026-09-28) | Línea base del plan. DET-03 a DET-05, AV-04, INT-02, INT-03 y RF01 pendientes |
| 2026-09-30 | `main` 9cd8286 (PR #16 mergeado) | Francisco | `pytest`: 131 passed. DAT-01 6/6 OK; DAT-04 1,760,633; DAT-05 OK. SEG-02 F1 0.823 (P 0.796 / R 0.851); SEG-03 0.99-1.00. AV-02 4.0%; AV-03 99.7%. Todo cumple | Primera ejecución tras mergear #6. SEG-04: lámina de SKU-110K revisada, sin casos nuevos (diagonales en una foto oblicua de refrigeradores, ya en #17). Sin imports entre etapas en `src/` (revisión manual; sigue sin test). DET-02 no se repitió (OK 2026-09-29) |
| 2026-10-10 | `feat/run-pipeline` (#8) | Francisco | `pytest`: 192 passed. INT-02 e INT-03 pasan. RF01: mediana 0.70 s por foto en CPU (corrección 0.31, segmentación 0.06, detección 0.34, disponibilidad 0.02). Evaluación por lotes (CU07) con la anotación de Kaggle, IoU >= 0.5: P 0.797, R 0.425, IoU medio 0.785, alerta correcta 5/6, error de % libre 7.8% | 6 fotos de Kaggle (001, 010, 020, 030, 039, 045), `yolo26s`. Prueba de humo, no la medición del #33. Hallazgos para #33: el recall bajo viene de la 030, un puesto de verduras sueltas (fuera del alcance de no perecibles; Kaggle anota cada verdura): 21 detectados de 546; sin ella, R 0.70. Y una falsa alerta en 020 (refrigeradores llenos, 34% libre): los marcos entre puertas, letreros y el vidrio borroso cuentan como huecos |
| 2026-10-19 | `feat/gondola-alert` (#40, sobre e9c6381) | Francisco | `pytest`: 195 passed. AV-01 pasa (29 tests): la alerta es solo de la góndola completa. El JSON y la vista ya no traen % ni alerta por repisa (`test_pipeline.py`, `test_annotate.py`). Pipeline real en CPU sobre 3 fotos de Kaggle: mediana 0.55 s por foto (corrección 0.25, segmentación 0.04, detección 0.29, disponibilidad 0.01) | `yolo26s`, fotos 003, 017 y 031. Vista revisada a ojo: huecos en rojo, contorno de repisas y cartel de la góndola, sin etiquetas por repisa. 017 (0%) y 031 (5%) sin alerta, correcto. 003 da una falsa alerta (41% libre): refrigerador con la fila de abajo y la columna izquierda llenas marcadas como hueco; la medición no cambió en #40, queda como caso para #34/#33 |
| 2026-10-20 | `main` 07a5981 (#34) | Francisco | DET-06: mAP50 0.713, mAP50-95 0.423, P 0.843, R 0.644 (45 fotos de Kaggle). Sistema completo con `--annotations` (44 fotos únicas): P 0.889, R 0.555, IoU medio 0.82, alerta correcta 84%, error de % libre 9.6 pts; envasados (36): R 0.713, alerta 92%, 6.2 pts. RF01: mediana 0.51 s por foto en CPU | `yolo26s`. Detalle, 10 mejores y 10 peores casos en `docs/analisis-resultados.md`. 6 falsas alertas (4 en frutas y verduras sueltas, fuera del alcance; 020 y 003, refrigeradores, #46) y 1 alerta perdida (011, pocos productos). La 035 repite la 004. Solo 1 foto tiene un quiebre real: el set mide falsas alertas, no quiebres detectados |
| 2026-10-20 | `main` 1e63b64 (#33, pasos 2 y 3) | Francisco | Paso 2, Kaggle girado con `oblique_view()` (44 fotos únicas, `yolo26s`, `nms=False`, `max_det=1000`, `imgsz=1280`): de frente mAP50 0.704 / mAP50-95 0.411 / R 0.632; 20° y 15° hacia abajo, 0.688 / 0.302 / 0.621; 35° y 15° hacia abajo, **0.637** / 0.211 / 0.586. Paso 3, Roboflow con `run_image()` (huecos contra espacios vacíos anotados, píxeles): Out Of Stock (200 fotos al azar) IoU 0.106, alerta correcta 88%, 24 falsas alertas, 2 quiebres (≥ 30% del frente) y 2 detectados; Empty Shelf (60 fotos) IoU 0.162, alerta correcta 95%, 3 falsas alertas, 0 quiebres | La caída con el giro está en la localización, no en encontrar productos: el mAP50-95 baja de 0.41 a 0.21 y el mAP75 de 0.42 a 0.07, mientras el recall baja poco (0.63 a 0.59). Con 35° queda bajo 0.70: se cumple el criterio para reentrenar. Roboflow anota espacios vacíos chicos (casi ninguna foto llega a 30% del frente): el IoU bajo mezcla criterios distintos (nosotros exigimos huecos de al menos un ancho de producto), así que no es un error de detección comparable; sí confirma falsas alertas (24 de 200). Scripts de medición sin versionar |
| 2026-11-18 | `main` 0372661 | Mariana | `pytest`: 314 passed (67 de la app web). WEB-01 a WEB-09 pasan. Detector final `yolo26s-finetune-ruido-v3`: DET-08 a DET-11 (2026-11-15); COR-05 (2026-11-16) | Ejecución para la entrega final de la Fase 2. Se agrega la sección 8 (app web y C.U) y se ponen al día DET-05, AV-04 y la trazabilidad de RF04 a RF06. Sin cambios en SEG, AV-02 y AV-03 desde sus últimas mediciones |
