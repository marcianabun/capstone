"""Mide el detector por tipo y nivel de ruido, un efecto a la vez (item #78).

Aplica cada efecto, en 3 niveles, a las 36 vistas de prueba (12 fotos de Kaggle
de frente y giradas, de `prepare_finetune_dataset.py`) y mide el mAP50 con
`val`. En la oclusion se descartan las cajas tapadas mas de MAX_HIDDEN (#76).

Uso:
    python scripts/prepare_finetune_dataset.py
    python scripts/measure_noise.py [--weights weights/yolo26s-finetune-ruido-v3.pt]
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.datasets.synthetic import hidden_fraction  # noqa: E402
from src.models.detector import IMGSZ, MAX_DET  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FINETUNE = ROOT / "data" / "processed" / "yolo" / "finetune"
OUT = ROOT / "data" / "processed" / "yolo" / "noise-type"
MAX_HIDDEN = 0.8


def _u8(image: np.ndarray) -> np.ndarray:
    return np.clip(image, 0, 255).astype(np.uint8)


def _jpeg(image: np.ndarray, quality: int) -> np.ndarray:
    return cv2.imdecode(cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality])[1], cv2.IMREAD_COLOR)


def _lowres(image: np.ndarray, scale: float) -> np.ndarray:
    small = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    return cv2.resize(small, image.shape[1::-1], interpolation=cv2.INTER_LINEAR)


def _motion(image: np.ndarray, size: int) -> np.ndarray:
    kernel = np.zeros((size, size), np.float32)
    kernel[size // 2] = 1 / size
    return cv2.filter2D(image, -1, kernel)


def _occlusion(image: np.ndarray, share: float) -> tuple[np.ndarray, np.ndarray]:
    """Una columna oscura de alto completo (una persona) que tapa `share` del ancho."""
    hidden = np.zeros(image.shape[:2], bool)
    left = int(0.4 * image.shape[1])
    hidden[:, left:left + int(share * image.shape[1])] = True
    out = image.copy()
    out[hidden] = 60
    return out, hidden


def _only_pixels(function):
    """Efecto que solo cambia los pixeles: no tapa nada."""
    return lambda image, level, rng: (function(image, level, rng), np.zeros(image.shape[:2], bool))


# nombre -> (efecto(foto, nivel, rng) -> (foto, mascara de lo que tapa), 3 niveles de menos a mas)
EFFECTS = {
    "sensor": (_only_pixels(lambda im, v, rng: _u8(im + rng.normal(0, v, im.shape))), (5, 10, 20)),  # sigma
    "jpeg": (_only_pixels(lambda im, v, rng: _jpeg(im, v)), (50, 30, 15)),  # calidad
    "lowres": (_only_pixels(lambda im, v, rng: _lowres(im, v)), (0.5, 0.35, 0.2)),  # escala
    "blur": (_only_pixels(lambda im, v, rng: cv2.GaussianBlur(im, (0, 0), v)), (1.5, 3, 5)),  # foco, sigma
    "motion": (_only_pixels(lambda im, v, rng: _motion(im, v)), (7, 15, 31)),  # movimiento, largo
    "dark": (_only_pixels(lambda im, v, rng: _u8(im * v)), (0.6, 0.4, 0.25)),  # poca luz, ganancia
    "bright": (_only_pixels(lambda im, v, rng: _u8(im * v)), (1.5, 2.0, 2.5)),  # contraluz, ganancia
    "occlusion": (lambda im, v, rng: _occlusion(im, v), (0.05, 0.10, 0.20)),  # ancho tapado
}


def build(name: str, level, apply, seed: int = 0) -> Path:
    """Arma `OUT/<efecto>-<nivel>` con las vistas de prueba degradadas; devuelve su data.yaml."""
    root = OUT / f"{name}-{level}"
    (root / "images" / "val").mkdir(parents=True)
    (root / "labels" / "val").mkdir(parents=True)
    rng = np.random.default_rng(seed)
    for view in ("f", "y20", "y35"):
        for image_path in sorted((FINETUNE / "images" / f"val-{view}").glob("*.jpg")):
            image = cv2.imread(str(image_path))
            noisy, hidden = apply(image, level, rng)
            rows = (FINETUNE / "labels" / f"val-{view}" / f"{image_path.stem}.txt").read_text().split("\n")
            rows = [r for r in rows if r.strip()]
            boxes = np.array([[float(v) for v in r.split()[1:]] for r in rows]).reshape(-1, 4)
            h, w = image.shape[:2]
            xyxy = np.column_stack([(boxes[:, 0] - boxes[:, 2] / 2) * w, (boxes[:, 1] - boxes[:, 3] / 2) * h,
                                    (boxes[:, 0] + boxes[:, 2] / 2) * w, (boxes[:, 1] + boxes[:, 3] / 2) * h])
            keep = hidden_fraction(xyxy, hidden) <= MAX_HIDDEN
            stem = f"{view}_{image_path.stem}"
            cv2.imwrite(str(root / "images" / "val" / f"{stem}.jpg"), noisy, [cv2.IMWRITE_JPEG_QUALITY, 95])
            (root / "labels" / "val" / f"{stem}.txt").write_text("\n".join(r for r, k in zip(rows, keep) if k) + "\n")
    yaml = root / "data.yaml"
    yaml.write_text(f"path: {root.as_posix()}\ntrain: images/val\nval: images/val\nnames:\n  0: product\n", encoding="utf-8")
    return yaml


def main() -> None:
    from ultralytics import YOLO

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--weights", default=str(ROOT / "weights" / "yolo26s-finetune-ruido-v3.pt"))
    parser.add_argument("--device", default="0")
    args = parser.parse_args()

    shutil.rmtree(OUT, ignore_errors=True)
    model = YOLO(args.weights)
    print("| Efecto | Nivel | mAP50 | Recall |\n| --- | --- | --- | --- |")
    for name, level, apply in [("limpia", 0, lambda im, v, rng: (im, np.zeros(im.shape[:2], bool)))] + [
        (n, v, apply) for n, (apply, levels) in EFFECTS.items() for v in levels
    ]:
        metrics = model.val(data=str(build(name, level, apply)), imgsz=IMGSZ, batch=2, device=args.device, workers=2,
                            nms=False, max_det=MAX_DET, plots=False, verbose=False)
        print(f"| {name} | {level} | {metrics.box.map50:.3f} | {metrics.box.mr:.3f} |", flush=True)


if __name__ == "__main__":
    main()
