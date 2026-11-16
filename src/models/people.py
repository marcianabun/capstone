"""Deteccion de personas (YOLO26 con pesos de COCO) para saber que parte de la
gondola tapa un cliente (item #77 de PROGRESS.md).

Solo cuenta a la persona alta y angosta, la que tapa la gondola: en las fotos
de gondola las caras impresas en cajas de remedios y cereales salen como
"persona" (45 fotos de Kaggle: 4 con falsos positivos, todos de menos de 15%
del alto). Las cajas van en pixeles absolutos de la imagen recibida.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from ultralytics import YOLO

from src.models.detector import IMGSZ, Detection

BBox = tuple[float, float, float, float]

PERSON_CLASS = 0  # COCO
MIN_HEIGHT_FRACTION = 0.40  # alto minimo de la persona, sobre el alto de la imagen
MAX_ASPECT = 1.0  # ancho / alto maximo: mas ancho que alto no es una persona de pie
DEFAULT_CONF = 0.4


def is_tall_person(bbox: BBox, image_height: int) -> bool:
    x_min, y_min, x_max, y_max = bbox
    height = y_max - y_min
    return height >= MIN_HEIGHT_FRACTION * image_height and (x_max - x_min) <= MAX_ASPECT * height


class PersonDetector:
    """Misma interfaz que ProductDetector.detect(), con `.bbox`."""

    def __init__(self, weights: str | Path, device: str | None = None, conf: float = DEFAULT_CONF) -> None:
        self._model = YOLO(str(weights))
        self._device = device
        self._conf = conf

    def detect(self, image: np.ndarray | None, *args, **kwargs) -> list[Detection]:
        if image is None or image.size == 0:
            raise ValueError("La imagen a detectar es None o esta vacia")
        result = self._model.predict(
            image, imgsz=IMGSZ, conf=self._conf, classes=[PERSON_CLASS], device=self._device, verbose=False
        )[0]
        boxes = result.boxes
        return [
            Detection(bbox=(x_min, y_min, x_max, y_max), score=score, class_id=int(class_id),
                      class_name=result.names[int(class_id)])
            for (x_min, y_min, x_max, y_max), score, class_id in zip(
                boxes.xyxy.tolist(), boxes.conf.tolist(), boxes.cls.tolist()
            )
            if is_tall_person((x_min, y_min, x_max, y_max), image.shape[0])
        ]
