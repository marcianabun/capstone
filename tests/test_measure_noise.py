import importlib.util
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def measure():
    spec = importlib.util.spec_from_file_location("measure_noise", ROOT / "scripts" / "measure_noise.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def photo():
    return np.random.default_rng(1).integers(40, 200, (200, 300, 3), dtype=np.uint8)


def test_every_effect_changes_the_photo_at_every_level_and_keeps_its_shape(measure):
    for name, (apply, levels) in measure.EFFECTS.items():
        assert len(levels) == 3, name
        for level in levels:
            out, hidden = apply(photo(), level, np.random.default_rng(0))
            assert out.shape == (200, 300, 3) and out.dtype == np.uint8, (name, level)
            assert hidden.shape == (200, 300) and hidden.dtype == bool, (name, level)
            assert not np.array_equal(out, photo()), (name, level)


def test_a_stronger_level_degrades_more(measure):
    for name in ("sensor", "jpeg", "lowres", "blur", "motion", "dark", "bright"):
        apply, levels = measure.EFFECTS[name]
        error = [np.abs(apply(photo(), v, np.random.default_rng(0))[0].astype(int) - photo()).mean() for v in levels]
        assert error == sorted(error), (name, error)


def test_occlusion_hides_more_of_the_photo_at_higher_levels_and_only_it_hides(measure):
    apply, levels = measure.EFFECTS["occlusion"]
    shares = [apply(photo(), v, np.random.default_rng(0))[1].mean() for v in levels]
    assert shares == sorted(shares) and 0 < shares[0] and shares[-1] <= 0.25
    assert not any(measure.EFFECTS[n][0](photo(), measure.EFFECTS[n][1][2], np.random.default_rng(0))[1].any() for n in ("sensor", "blur", "dark"))
