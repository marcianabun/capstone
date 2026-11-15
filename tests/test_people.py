from types import SimpleNamespace

import numpy as np
import pytest

from src.models.people import PersonDetector, is_tall_person


def test_tall_person_is_kept_and_small_faces_on_packaging_are_not():
    # Imagen de 1000 px de alto: una persona cerca de la camara ocupa casi todo el alto.
    assert is_tall_person((100, 100, 400, 950), 1000)
    assert not is_tall_person((100, 100, 160, 170), 1000)  # cara impresa en una caja (Kaggle 021, 042, 043)
    assert not is_tall_person((100, 500, 900, 950), 1000)  # tan ancha como alta: un carro o una pila, no una persona


class FakeModel:
    def __init__(self, boxes, scores, classes):
        self.result = SimpleNamespace(
            boxes=SimpleNamespace(xyxy=SimpleNamespace(tolist=lambda: boxes),
                                  conf=SimpleNamespace(tolist=lambda: scores),
                                  cls=SimpleNamespace(tolist=lambda: classes)),
            names={0: "person"},
        )
        self.kwargs = None

    def predict(self, image, **kwargs):
        self.kwargs = kwargs
        return [self.result]


def test_detector_returns_only_tall_people_and_asks_for_the_person_class_only():
    detector = object.__new__(PersonDetector)
    detector._model = FakeModel([[100, 100, 400, 950], [100, 100, 160, 170]], [0.9, 0.8], [0, 0])
    detector._device, detector._conf = "cpu", 0.4
    found = detector.detect(np.zeros((1000, 1500, 3), np.uint8))
    assert [d.bbox for d in found] == [(100, 100, 400, 950)]
    assert found[0].class_name == "person" and found[0].score == pytest.approx(0.9)
    assert detector._model.kwargs["classes"] == [0] and detector._model.kwargs["conf"] == 0.4


def test_detector_rejects_an_empty_image():
    detector = object.__new__(PersonDetector)
    with pytest.raises(ValueError):
        detector.detect(None)
