"""Excepcion 1a de CU01 (#87): una camara defectuosa entrega fotos con colores
imposibles (toda verde o toda magenta, por ejemplo un sensor o un cable con
un canal cortado). Esas fotos no se analizan."""

import cv2
import numpy as np

from src.preprocessing._validation import check_image

# Medido el 2026-11-16 en 4.800 fotos reales de gondolas (Kaggle, SHARD,
# Roboflow, UniDataPro y SKU-110K): verde / max(rojo, azul) llega a 1,16 y
# min(rojo, azul) / verde a 1,42, aun con gondolas casi de un solo color.
MAX_COLOR_CAST = 2.0


def camera_fault(image: np.ndarray) -> str | None:
    """Motivo ("imagen verde" o "imagen magenta") si la foto BGR parece de una
    camara defectuosa; None si se puede analizar."""
    check_image(image)
    if image.ndim == 2:
        return None
    small = cv2.resize(image, (160, 120), interpolation=cv2.INTER_AREA)
    blue, green, red = small.reshape(-1, 3).mean(axis=0) + 1  # +1: una foto negra no divide por cero
    if green / max(red, blue) > MAX_COLOR_CAST:
        return "imagen verde"
    if min(red, blue) / green > MAX_COLOR_CAST:
        return "imagen magenta"
    return None
