# Auditoría de seguridad por vulnerabilidades recientes (ítem #57)

Fecha: 2026-10-22. Responsable: Francisco. Pedido: revisar las
vulnerabilidades publicadas la semana del 2026-10-19 en distintos
lenguajes y librerías, y ver si alcanzan a la app web.

## Cómo se hizo

1. Búsqueda de las vulnerabilidades de la semana (Python, Django, Pillow,
   PHP, Node.js, Java y otras).
2. Contraste con lo que usamos: `requirements.txt`, el `Dockerfile` y el
   CI.
3. `pip-audit` (base OSV/PyPI) sobre el entorno del proyecto, para no
   depender de blogs.

Cada hallazgo dice de qué fuente sale. Las páginas agregadoras de CVE
(strix.ai, dailycve, blogs de resumen) pueden traer datos erróneos y los
CVE recientes aún no tienen análisis del NVD: la fuente que manda es el
aviso del proyecto o `pip-audit`.

## Lo que sí nos alcanza

### Pillow 12.3.0: corregido (la subida de fotos lo usa)

- **Dónde**: `PhotoForm` (`web/forms.py`) usa `forms.ImageField`, y Django
  valida con Pillow cada archivo que sube un usuario. Es entrada no
  confiable, con una cuenta de Reponedor basta. Pillow no estaba en
  `requirements.txt`: llegaba por otra dependencia, así que nada impedía
  quedarse en una versión vieja.
- **Qué**: Pillow 13.0.0 (2026-10-16) corrige unas 35 vulnerabilidades,
  según sus notas de versión: dos críticas de decodificador (almacenamiento
  nativo reutilizado tras cambios de modo; desbordamiento del decodificador
  JPEG con líneas más anchas que el tile), trece altas (TIFF, WMF/EMF,
  OpenJPEG, PDF, bucle sin límite con cabeceras Exif repetidas) y varias
  medias de agotamiento de memoria o CPU (BMP, GIF, MSP, APNG). `pip-audit`
  reporta 35 avisos para 12.3.0, todos con arreglo en 13.0.0.
- **Exposición real**: las que corren al abrir y validar una imagen
  (JPEG, TIFF, BMP, GIF, MSP, Exif) son alcanzables desde la subida de
  foto. Las de PDF/EPS y de funciones que no llamamos (`Image.merge`,
  `quantize`, guardar TIFF) no, pero no hay que depender de eso.
  La foto se valida con Pillow y después se decodifica con OpenCV
  (`web/views.py`, `cv2.imdecode`), que no se ve afectado.
- **Arreglo**: `pillow>=13.0` en `requirements.txt` (13.0 ya no admite
  Python 3.10; usamos 3.13). Entorno actualizado, 255 tests pasan.
- **Lo que queda**: Pillow 13 solo hay que subirlo en cada PC (`pip
  install -r requirements.txt`) y en la imagen Docker al reconstruirla.

### certifi 2026.7.22: corregido

- **Qué**: incidente de la CA emSign (eMudhra). Python 3.13.17 (2026-10-21)
  trae certifi 2026.10.19 por eso, y `pip-audit` reporta PYSEC-2026-4320
  para la versión anterior.
- **Exposición**: certifi lo trae `requests`, que usa
  `scripts/download_datasets.py` (descarga de datasets). La app web no
  hace conexiones salientes con él.
- **Arreglo**: `certifi>=2026.10.19` en `requirements.txt`.

### setuptools 78.1.0 (solo el entorno local)

`pip-audit` reporta PYSEC-2025-49 y PYSEC-2026-3447. No está en
`requirements.txt` ni en la imagen Docker (`python:3.13-slim` no lo
trae); solo está en el `.venv` local. No toca la app. Se puede subir con
`pip install -U setuptools` en cada PC.

## Lo que ya estaba cubierto

- **Django 6.1.2**: la versión que usamos ya trae el paquete de seguridad
  del 2026-10-06 (CVE-2026-77050, -84429, -87890 y -87975, según el aviso
  de Django). Además, no usamos `django.contrib.gis` ni formsets con clave
  primaria editable. `requirements.txt` pide `django>=6.1,<7`, por lo
  que una instalación nueva ya recibe la corregida.
- **Python en el contenedor**: `python:3.13-slim-trixie` no fija el parche;
  una reconstrucción recibe 3.13.17 (2026-10-21). Las CVE de CPython de
  2026 que encontré (SNI/`SSLContext` de septiembre, `tarfile`) están
  corregidas en las versiones recientes; los detalles de varias vienen de
  agregadores y no pude confirmarlos en python.org.
- **`tarfile`**: `scripts/download_datasets.py` extrae con
  `filter="data"` y solo de fuentes fijas del proyecto; no es una entrada
  de usuarios. Con un Python reciente queda cubierto.

## Lo que no nos alcanza

PHP (CVE-2026-109618/-109619), Node.js (Brotli y otros 9), Java/JSSE,
Tomcat y GitLab: no están en la pila (Django, OpenCV, PyTorch, ultralytics,
gunicorn). Node corre solo en el runner de GitHub Actions, que mantiene
GitHub. El incidente de LiteLLM en PyPI tampoco: no lo usamos.

## Revisión del 2026-11-22

Segunda pasada (ítem #57), con `pip-audit` sobre el entorno y los avisos
de GitHub de cada proyecto.

### filelock 3.32.3 y brotli 1.2.0: corregidos

- **filelock**: 13 avisos de `pip-audit` (CVE-2026-112907 a -112940), con
  arreglo en 4.0.9 y 4.2.1. Lo traen `torch` y `ultralytics`, que guardan
  cachés con bloqueos de archivo. **Exposición**: la app no bloquea rutas que
  escriba un usuario; solo las usa PyTorch para sus cachés locales. Riesgo
  bajo, pero el arreglo cuesta una línea.
- **brotli**: PYSEC-2026-4322, arreglo en 1.2.1. Lo trae `py7zr`, que solo
  descomprime SHARD en `scripts/download_datasets.py` desde una fuente fija:
  no recibe archivos de usuarios.
- **Arreglo**: `filelock>=4.2.1` y `brotli>=1.2.1` en `requirements.txt`, como
  se hizo con Pillow y certifi. Una instalación nueva ya recibía las
  corregidas (4.3.0 y 1.2.1); el piso protege a los entornos viejos. Tras
  subirlas, `pip check` no marca conflictos, `pip-audit` no encuentra
  vulnerabilidades y los 322 tests pasan.
- **setuptools 78.1.0** (solo el `.venv` local, ver más arriba): subido a
  84.2.1.

### torch, torchvision, OpenCV y ultralytics: revisados

`pip-audit` no los cubre (vienen del índice de PyTorch, con versión local
`+cpu` o `+cu130`; los lista como «no auditados»). Se revisaron a mano los
avisos de GitHub (`/advisories?ecosystem=pip&affects=<paquete>`):

- **torch**: 14 avisos y ninguno vigente para las versiones que usamos
  (2.13 o superior). Los de ejecución remota al cargar un checkpoint
  (GHSA-63cw-57p8-fm3p, arreglo en 2.10.0; GHSA-53q9-r3pm-6pq6, en 2.6.0)
  quedan fuera, y además los pesos que carga la app son los del proyecto
  (`weights/`) o los que indica quien administra el servidor con
  `SHELFVISION_WEIGHTS`, nunca un archivo de un usuario. Quedan sin arreglo
  solo avisos de torch 2.6.0 o anteriores (memoria en `pad_packed_sequence`,
  argumentos nulos), que no nos tocan.
- **torchvision** y **ultralytics**: sin avisos publicados.
- **opencv-python**: solo avisos antiguos (libwebp, escrituras fuera de
  rango de 2021), todos con arreglo anterior a 4.8, que es nuestro mínimo.
- Este análisis es una foto del 2026-11-22. Como `pip-audit` no los ve,
  hay que repetirlo a mano al instalar en otro servidor.

### CI: auditoría semanal

`.github/workflows/auditoria.yml` corre cada lunes, a mano y en los PR que
tocan `requirements.txt`, el `Dockerfile` o el propio archivo:

- **pip-audit** (2.10.1) sobre el entorno instalado, como en `tests`.
- **Trivy** (acción y versión fijadas) sobre la imagen `shelfvision-ai`:
  avisos HIGH y CRITICAL con arreglo publicado, del sistema (Debian) y de las
  librerías. Cubre lo que faltaba de la imagen base.

No es un check que exija `main`: un aviso nuevo no debe bloquear un PR que no
lo causó. Si falla, se ve en la pestaña Actions y GitHub avisa por correo a
quien la creó o la editó por última vez.

### Primer resultado de Trivy y pip-audit en el CI (2026-11-22)

Sobre la imagen construida con las dependencias ya subidas, Trivy marcó 5
avisos HIGH con arreglo publicado, y `pip-audit` en el runner, el mismo
setuptools:

- **zlib1g** (Debian, CVE-2026-85091: desbordamiento de memoria en
  `gz_vacate()`): la base `python:3.13-slim-trixie` aún no trae el parche
  (`1.3.1-1+deb13u1`). La app no descomprime gzip de usuarios, pero la
  librería la cargan Python y OpenCV. **Arreglo**: `apt-get upgrade` en el
  `Dockerfile`, que aplica los parches de seguridad pendientes de la base.
- **setuptools 78.1.0, wheel 0.45.1 y jaraco.context 5.3.0** (CVE-2025-47273,
  CVE-2026-24049, CVE-2026-23949): vienen con la imagen base de Python; el
  último es una copia que setuptools lleva adentro. No los usa la app, pero
  están en la imagen. **Arreglo**: `pip install --upgrade pip setuptools
  wheel` en el `Dockerfile` (y `setuptools` en el job `pip-audit`).

## Pendiente

1. Confirmar en el CI que Trivy y `pip-audit` salen limpios con estos
   arreglos.
2. La configuración de la app (DEBUG apagado por defecto, cookies seguras,
   usuario sin privilegios en el contenedor) es el ítem #50.
3. Si se instala en otro servidor, repetir `pip-audit` y la revisión de
   torch ese día: la lista cambia cada semana.
