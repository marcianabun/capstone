# Python 3.13: 3.10 termina su soporte en octubre de 2026 y Django 6.1 (app
# web) exige 3.12 o superior.
FROM python:3.13-slim-trixie

# Librerias de sistema que necesita opencv-python (lo exige ultralytics; ver
# requirements.txt). Nombres de paquete de Debian 13 (trixie): la base se fija
# a trixie porque en otras versiones de Debian cambian (ej. libglib2.0-0t64).
# apt-get upgrade aplica los parches de seguridad que la imagen base aun no trae
# (ej. zlib1g, CVE-2026-85091; Trivy del CI, #57).
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0t64 \
    libsm6 \
    libice6 \
    libxext6 \
    libx11-6 \
    && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# PyTorch solo CPU: desde PyPI, pip instala en Linux la variante CUDA
# (~0.5 GB de torch mas varios GB de toolkit CUDA/cuDNN) aunque no haya GPU.
# Se actualiza pip antes: el 23.0.1 de la imagen base rechaza wheels del
# indice de PyTorch (ej. typing_extensions) por la normalizacion del nombre
# e intenta compilarlos desde fuente, sin las dependencias de build.
# setuptools y wheel tambien: los de la imagen base tienen avisos de seguridad
# (Trivy del CI, #57), con el jaraco.context que setuptools trae adentro.
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY scripts/ ./scripts/
COPY web/ ./web/
COPY manage.py pytest.ini ./
COPY weights/yolo26s-finetune-ruido-v3.pt weights/yolo26n.pt ./weights/

# Sin privilegios: la app no necesita root. Solo /data (el volumen) es escribible;
# -m crea un HOME donde ultralytics guarda su configuracion.
RUN useradd -m -u 10001 app && mkdir /data && chown app /data
USER app

# App web (item #28). /data es el volumen con la base de datos y las fotos
# analizadas (los pesos ya vienen en la imagen, en /app/weights; para otros,
# SHELFVISION_WEIGHTS): sin volumen se pierden al recrear el
# contenedor (con un volumen del host, `chown 10001` a esa carpeta).
# DJANGO_SECRET_KEY y DJANGO_ALLOWED_HOSTS se pasan con -e; la app exige HTTPS
# (DJANGO_HTTPS=0 solo para probar sin TLS).
# El pipeline por lotes sigue disponible: docker run ... python scripts/run_pipeline.py
ENV DJANGO_DEBUG=0 \
    SHELFVISION_DATA_DIR=/data
EXPOSE 8000
# Un solo worker: cada uno cargaria su propia copia de YOLO26 en memoria.
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn web.wsgi --bind 0.0.0.0:8000 --workers 1 --threads 4 --timeout 120"]
