import numpy as np
import pytest

from src.datasets.synthetic import oblique_view


def test_no_rotation_keeps_image_and_boxes():
    image = np.random.default_rng(0).integers(0, 255, (300, 400, 3), dtype=np.uint8)
    boxes = [(10, 20, 60, 90), (200, 100, 250, 180)]
    warped, moved = oblique_view(image, boxes, yaw_deg=0)
    assert warped.shape == image.shape
    np.testing.assert_allclose(moved, boxes, atol=1e-6)


def test_boxes_follow_the_warped_pixels():
    image = np.zeros((400, 600, 3), dtype=np.uint8)
    box = (380, 250, 460, 330)
    image[250:330, 380:460] = 255
    warped, moved = oblique_view(image, [box], yaw_deg=25, pitch_deg=10)
    ys, xs = np.nonzero(warped[..., 0] > 127)
    x_min, y_min, x_max, y_max = moved[0]
    assert xs.min() >= x_min - 2 and xs.max() <= x_max + 2
    assert ys.min() >= y_min - 2 and ys.max() <= y_max + 2
    # El rectangulo envuelve bien al producto (no es mucho mas grande).
    assert (x_max - x_min) <= 1.2 * (xs.max() - xs.min() + 1)


def test_yaw_tilts_horizontal_shelves():
    # Dos productos sobre la misma repisa horizontal: con la camara girada
    # hacia un lado, sus bases quedan a distinta altura.
    image = np.full((400, 600, 3), 128, dtype=np.uint8)
    boxes = [(50, 200, 100, 300), (500, 200, 550, 300)]
    _, moved = oblique_view(image, boxes, yaw_deg=30, pitch_deg=-15)
    assert len(moved) == 2
    assert abs(moved[0][3] - moved[1][3]) > 10


def test_crop_has_no_black_borders():
    image = np.full((300, 400, 3), 128, dtype=np.uint8)
    warped, _ = oblique_view(image, [], yaw_deg=35, pitch_deg=-20)
    assert warped.max(axis=2).min() > 0
    assert max(warped.shape[:2]) == 400


def test_drops_boxes_left_out_of_the_crop():
    image = np.full((300, 400, 3), 128, dtype=np.uint8)
    corner = (0, 0, 30, 30)  # la esquina queda fuera del recorte
    center = (180, 130, 220, 170)
    _, moved = oblique_view(image, [corner, center], yaw_deg=35, pitch_deg=-20)
    assert len(moved) == 1


def test_rejects_rotation_out_of_view():
    image = np.full((300, 400, 3), 128, dtype=np.uint8)
    with pytest.raises(ValueError):
        oblique_view(image, [], yaw_deg=80)


def test_degrade_changes_the_image_but_not_its_shape_and_is_reproducible():
    from src.datasets.synthetic import degrade

    image = np.random.default_rng(1).integers(0, 255, (300, 400, 3), dtype=np.uint8)
    first, _ = degrade(image, np.random.default_rng(7))
    assert first.shape == image.shape and first.dtype == np.uint8
    assert not np.array_equal(first, image)
    np.testing.assert_array_equal(first, degrade(image, np.random.default_rng(7))[0])
    assert not np.array_equal(first, degrade(image, np.random.default_rng(8))[0])


def test_degrade_varies_the_brightness_across_seeds():
    from src.datasets.synthetic import degrade

    image = np.full((300, 400, 3), 128, dtype=np.uint8)
    means = [degrade(image, np.random.default_rng(seed))[0].mean() for seed in range(30)]
    assert min(means) < 100 and max(means) > 140  # de noche y de contraluz


def test_degrade_returns_the_mask_of_what_hides_the_shelf():
    from src.datasets.synthetic import degrade

    image = np.full((300, 400, 3), 128, dtype=np.uint8)
    masks = [degrade(image, np.random.default_rng(seed))[1] for seed in range(30)]
    assert all(m.shape == (300, 400) and m.dtype == bool for m in masks)
    assert any(m.any() for m in masks) and not all(m.any() for m in masks)  # no a todas les toca


def test_hidden_fraction_is_the_share_of_each_box_under_the_mask():
    from src.datasets.synthetic import hidden_fraction

    hidden = np.zeros((100, 200), bool)
    hidden[:, :100] = True  # mitad izquierda tapada
    boxes = np.array([[10.0, 10.0, 50.0, 50.0], [80.0, 10.0, 120.0, 50.0], [150.0, 10.0, 190.0, 50.0]])
    np.testing.assert_allclose(hidden_fraction(boxes, hidden), [1.0, 0.5, 0.0])



def test_degrade_blurs_as_hard_as_the_detector_needs_to_learn(monkeypatch):
    """DET-09 (#78): el mAP50 baja de 0.70 con desenfoque de foco sigma 5 y de movimiento largo 31."""
    import cv2

    from src.datasets import synthetic

    sigmas, sizes = [], []
    gaussian_blur, filter2d = cv2.GaussianBlur, cv2.filter2D

    def spy_blur(src, ksize, sigma, *args, **kwargs):
        if src.ndim == 3:  # el desenfoque de foco; la mancha desenfoca una mascara 2D
            sigmas.append(sigma)
        return gaussian_blur(src, ksize, sigma, *args, **kwargs)

    def spy_filter(src, ddepth, kernel, *args, **kwargs):
        sizes.append(len(kernel))
        return filter2d(src, ddepth, kernel, *args, **kwargs)

    monkeypatch.setattr(synthetic.cv2, "GaussianBlur", spy_blur)
    monkeypatch.setattr(synthetic.cv2, "filter2D", spy_filter)
    image = np.full((60, 80, 3), 128, dtype=np.uint8)
    for seed in range(300):
        synthetic.degrade(image, np.random.default_rng(seed))
    assert min(sigmas) >= 1 and max(sigmas) >= 4.5
    assert min(sizes) >= 5 and max(sizes) >= 38
    assert len(sizes) >= 60  # al menos 1 de cada 5 fotos con desenfoque de movimiento (DET-09: es la mayor debilidad)
