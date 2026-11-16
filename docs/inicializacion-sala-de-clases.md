# Inicialización del entorno: PC de la Sala de Clases

Registro de la inicialización del 2026-11-16 en una PC de la sala de
clases (Windows 11 Enterprise, usuario sin permisos de administrador).
Complementa "Configuración de un entorno nuevo" del README con los
problemas reales que aparecieron.

## Resultado

Entorno listo: `pytest tests/` da **309 passed** (40 s) con Python
3.13.18, Django 6.1.3, torch 2.15.0+cpu, OpenCV 4.14.0 y ultralytics
8.4.215. Sin GPU: el entrenamiento no es posible en esta PC.

## Estado inicial de la PC

- Git y rama `main` al día.
- Python: **solo 3.15.0a3** (alfa) en `C:\Program Files\Python315`. No
  había `py -3.13`, ni `uv`, ni `graphify`, ni `gh`.
- Disponibles: `winget` y Node.js.
- Sin `.venv`, `CLAUDE.local.md` ni `db.sqlite3` (entorno nuevo).

## Problema 1: Python 3.15 alfa no sirve para el proyecto

`pip install -r requirements.txt` en un venv de Python 3.15.0a3 falló:
`py7zr` depende de `inflate64`, `pybcj` y `pyppmd`, que no tienen wheels
para 3.15 y se intentan compilar:

```
error: Microsoft Visual C++ 14.0 or greater is required.
Failed to build inflate64 pybcj pyppmd
```

No se instalaron las Build Tools (varios GB, piden administrador). El
README dice 3.12 o superior (el CI usa 3.13), y una alfa además no tiene
wheels de torch ni numpy.

**Solución:** Python 3.13 en el usuario con `uv`, sin admin y sin tocar
el Python del sistema.

## Descargas realizadas

| Qué | De dónde | Cómo |
|---|---|---|
| `uv` 0.13.8 | PyPI: https://pypi.org/project/uv/ | `python -m pip install --user uv` |
| CPython 3.13.18 (21,3 MiB) | python-build-standalone: https://github.com/astral-sh/python-build-standalone (lo descarga uv) | `python -m uv venv --python 3.13 .venv` |
| 64 paquetes de `requirements.txt` (torch, ultralytics, django, etc.) | PyPI: https://pypi.org | `python -m uv pip install --python .venv\Scripts\python.exe -r requirements.txt` |

No se descargaron datasets ni pesos (`pytest` no los necesita). `uv` se
instaló en el Python global del usuario (`--user`), no en el venv.

## Comandos que funcionaron

```powershell
git switch main; git pull
python -m pip install --user uv
python -m uv venv --python 3.13 .venv
python -m uv pip install --python .venv\Scripts\python.exe -r requirements.txt
.venv\Scripts\python.exe -m pytest tests/
```

## Otros hallazgos

- **El venv de `uv` no trae `pip`**: instalar con `uv pip install
  --python .venv\Scripts\python.exe ...`, o agregar pip con
  `.venv\Scripts\python.exe -m ensurepip`.
- **No se puede borrar `.venv` mientras un `pip` lo usa** ("Acceso
  denegado" en `python.exe`): esperar a que termine el proceso. Un
  comando de PowerShell que pasa a segundo plano no muestra progreso si
  se filtra con `Select-Object -Last`; mejor redirigir a un archivo de log.
- **PowerShell marca como `NativeCommandError`** el texto que `uv` y
  `pip` escriben por stderr (avisos de actualización, "Using CPython");
  no es un error real. Se mira el código de salida.
- **`.venv\Scripts\activate`**: no se probó la activación; se invocó
  `.venv\Scripts\python.exe` directo. Si PowerShell bloquea la activación:
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Pendiente en esta PC

- Paso 6 (levantar el servidor): `migrate`, `createsuperuser`, `runserver`.
- `CLAUDE.local.md` con `Integrante: <nombre>`.
- `graphify` (`uv tool install graphifyy==0.9.70`; `uv` ya está) y
  `graphify update .`. Sin él, los hooks de `.claude/settings.json` fallan.
- Ponytail y su `ledger` en falso; `gh auth login` para los PR.
