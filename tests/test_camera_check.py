"""Excepcion 1a de CU01 (#87): una camara defectuosa entrega fotos con
colores imposibles (toda verde o toda magenta) y no se analizan."""

import numpy as np
import pytest

from src.preprocessing.camera_check import camera_fault
from tests.pipeline_fixtures import gondola


def tinted(image, keep_green):
    """La misma foto como la entrega un sensor fallado: su brillo queda solo en
    el verde, o solo en el rojo y el azul (magenta)."""
    gray = image.mean(axis=2).astype(np.uint8)
    out = np.zeros_like(image)
    if keep_green:
        out[..., 1] = gray
    else:
        out[..., 0] = out[..., 2] = gray
    return out


def test_una_gondola_normal_se_analiza():
    image, _ = gondola()
    assert camera_fault(image) is None


def test_una_gondola_con_mucho_envase_verde_se_analiza():
    # Una góndola real puede ser casi toda de un color: no es una falla.
    image, _ = gondola()
    image[..., 1] = np.maximum(image[..., 1], 150)
    assert camera_fault(image) is None


@pytest.mark.parametrize("keep_green, motivo", [(True, "verde"), (False, "magenta")])
def test_una_foto_toda_verde_o_magenta_es_camara_defectuosa(keep_green, motivo):
    image, _ = gondola()
    assert motivo in camera_fault(tinted(image, keep_green))


def test_una_foto_negra_no_es_camara_defectuosa():
    # Negra o tapada sigue el camino de "sin productos" (#52), no este.
    assert camera_fault(np.zeros((120, 160, 3), np.uint8)) is None
