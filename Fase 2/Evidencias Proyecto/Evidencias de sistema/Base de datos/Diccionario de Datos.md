# Diccionario de datos - ShelfVision AI

Detalle de cada tabla y columna de la base de datos de la aplicación web
(Django + SQLite): tipo, nulidad, llaves, valor por defecto y significado. Se
lee junto con el [Modelo Lógico](Modelo%20Logico.md) y el
[Modelo Relacional](Modelo%20Relacional.md).

- **Corte**: 2026-11-15, `main` después del PR #103.
- **Fuente de verdad**: `web/models.py`, las migraciones `web/migrations/0001` a
  `0006` y el esquema real que crea `migrate`. Reemplaza al
  `Diccionario de Datos.docx` anterior, que describía solo `web_user`,
  `auth_group`, `web_user_groups` y `web_analysis` y tenía datos que ya no
  valen (ítem #48): el bloqueo por 5 intentos ya no desactiva la cuenta,
  `critical` ya no depende de un 0,30 fijo y faltaban `web_config`, `web_camera`
  y `web_user.locked_until`.

**Cómo leerlo**: *Tipo* es el declarado en SQLite. *Nulo* dice si la columna
admite `NULL`. *Clave* usa `PK`, `FK` y `UK` (única). *Por defecto* es el valor
que pone **Django al crear la fila**: la base no declara `DEFAULT`, así que un
`INSERT` directo debe dar todos los valores `NOT NULL`.

## Índice de tablas

| Tabla | Propósito | Sección |
| --- | --- | --- |
| `web_user` | Cuentas de usuario | 1 |
| `auth_group` | Los tres perfiles | 2 |
| `web_user_groups` | Perfil de cada usuario | 3 |
| `web_analysis` | Foto analizada y su alerta | 4 |
| `web_camera` | Cámaras de sala por pasillo y góndola | 5 |
| `web_config` | Umbral de la tienda (fila única) | 6 |
| `web_user_user_permissions`, `auth_permission`, `auth_group_permissions`, `django_content_type` | Permisos de Django (la aplicación no los usa) | 7 |
| `django_session`, `django_migrations` | Soporte de Django | 8 |

---

## 1. `web_user`

Cuenta de usuario (`web.models.User`, que extiende `AbstractUser`). CU00 y CU06.

| Columna | Tipo | Nulo | Clave | Por defecto | Descripción y valores permitidos |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | No | PK | autoincremental | Identificador |
| `password` | varchar(128) | No | - | - | Hash de la contraseña. El primero de `PASSWORD_HASHERS` es `BCryptSHA256PasswordHasher` (formato `bcrypt_sha256$...`); también acepta PBKDF2. Nunca texto plano |
| `last_login` | datetime | **Sí** | - | `NULL` | Último ingreso exitoso. `NULL` si nunca entró |
| `is_superuser` | bool | No | - | `0` | `1` implica perfil **Administrador** sin importar el grupo |
| `username` | varchar(150) | No | **UK** | - | RUT normalizado, sin puntos y con la `K` en mayúscula (`12345678-5`). Es una credencial de ingreso. Los formularios exigen un RUT con dígito verificador válido; una cuenta creada por `createsuperuser` o desde el shell puede usar otro texto |
| `first_name` | varchar(150) | No | - | `''` | Nombre. Vacío permitido |
| `last_name` | varchar(150) | No | - | `''` | Apellido. Vacío permitido |
| `is_staff` | bool | No | - | `0` | Acceso al admin de Django (que esta aplicación no instala). Sin uso práctico |
| `is_active` | bool | No | - | `1` | `0` = cuenta dada de baja por el Administrador (baja lógica). **No** significa «bloqueada»: el bloqueo por intentos fallidos es `locked_until`. Una cuenta inactiva no puede entrar y sus sesiones abiertas dejan de valer (el backend de login rechaza cuentas inactivas o bloqueadas); la fila de `django_session` queda hasta que vence |
| `date_joined` | datetime | No | - | ahora | Creación de la cuenta |
| `email` | varchar(254) | No | **UK** | - | Correo. Único porque también sirve para entrar (CU00) y para el enlace de definir la contraseña (CU06) |
| `failed_logins` | smallint unsigned | No | - | `0` | Intentos fallidos seguidos, de 0 a 4 en reposo. Al llegar a 5 se pone en 0 y se fija `locked_until`. Se suma en la base (`F()`), así que intentos en paralelo no se pierden. Vuelve a 0 al ingresar bien. `CHECK (failed_logins >= 0)` |
| `locked_until` | datetime | **Sí** | - | `NULL` | Fin del bloqueo temporal (#51): 15 minutos después del quinto intento fallido. Con `locked_until` en el futuro no se puede ingresar; pasado ese momento la cuenta se desbloquea sola. El Administrador lo borra al guardar la cuenta en «Editar». Los intentos durante el bloqueo no lo alargan |

**Perfil derivado** (`User.role`, no se guarda): `Administrador` si
`is_superuser = 1`; si no, el nombre del primer grupo del usuario; vacío si no
tiene ninguno.

---

## 2. `auth_group`

Los tres perfiles del sistema. Las filas las crea la migración `0002_roles`.

| Columna | Tipo | Nulo | Clave | Por defecto | Descripción y valores permitidos |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | No | PK | autoincremental | Identificador |
| `name` | varchar(150) | No | **UK** | - | `Reponedor`, `Jefe de Salón` o `Administrador` |

| Perfil | Entra a | Puede |
| --- | --- | --- |
| Administrador | Usuarios | Todo: usuarios (CU06), configuración (CU05), análisis, alertas, dashboard y reportes |
| Jefe de Salón | Góndolas | Subir fotos y ver análisis (CU01), dashboard (CU03), alertas y reportes (CU04) |
| Reponedor | Alertas | Ver alertas, tomarlas y completarlas (CU02); ver el dashboard |

---

## 3. `web_user_groups`

Tabla intermedia usuario - perfil. La aplicación asigna **un** perfil por
usuario, aunque la tabla permitiría varios.

| Columna | Tipo | Nulo | Clave | Por defecto | Descripción y valores permitidos |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | No | PK | autoincremental | Identificador |
| `user_id` | bigint | No | **FK**, UK* | - | → `web_user(id)`. *Único junto con `group_id` |
| `group_id` | integer | No | **FK**, UK* | - | → `auth_group(id)` |

---

## 4. `web_analysis`

Una foto de góndola analizada con el pipeline (CU01) y, si hay quiebre, su
alerta (CU02). Orden por defecto: `-created_at` (la más nueva primero).

| Columna | Tipo | Nulo | Clave | Por defecto | Descripción y valores permitidos |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | No | PK | autoincremental | Identificador |
| `created_at` | datetime | No | - | ahora | Momento del análisis (`auto_now_add`) |
| `created_by_id` | bigint | **Sí** | **FK** | - | → `web_user(id)`, `SET_NULL`. Quién subió la foto. `NULL` si la subió la cámara simulada (`simular_camara`) |
| `pasillo` | varchar(20) | No | - | - | Pasillo de la góndola, sin espacios y en mayúsculas (`A1`). Junto con `gondola` es la ubicación |
| `gondola` | varchar(20) | No | - | - | Góndola, sin espacios y en mayúsculas. No hay tabla de góndolas |
| `photo_name` | varchar(255) | No | - | - | Nombre original del archivo subido. No es una ruta |
| `annotated` | varchar(100) | No | - | - | Ruta, relativa a `MEDIA_ROOT`, de la foto anotada (huecos en rojo), en la carpeta `analisis/` y con nombre al azar (`<uuid>.jpg`). **Vacío** después de `borrar_fotos`: el análisis se conserva sin la imagen |
| `free_fraction` | real | No | - | - | Espacio libre de la **góndola completa**, de 0,0 a 1,0 (#40). No hay valor por repisa |
| `critical` | bool | No | - | - | `1` si `free_fraction` >= umbral vigente al analizar (`Config.umbral / 100`, 30 % por defecto). Es la alerta de quiebre de la góndola |
| `result` | text (JSON) | No | - | - | `PipelineResult.to_dict()`: resultado completo del pipeline (ver sección 9). `CHECK (JSON_VALID(result) OR result IS NULL)`. De aquí salen las franjas del fleje (`Analysis.strips`) |
| `estado` | varchar(12) | No | - | `''` | Estado de la alerta. `''` = análisis sin quiebre (nunca `NULL`). Con quiebre: `activa`, `en_proceso`, `completada` o `reemplazada` (ver tabla abajo) |
| `taken_by_id` | bigint | **Sí** | **FK** | `NULL` | → `web_user(id)`, `SET_NULL`. Reponedor que tomó la alerta. `NULL` mientras está activa o si no hay alerta |
| `estado_at` | datetime | **Sí** | - | `NULL` | Último cambio de `estado`. `NULL` si el análisis nunca tuvo alerta |

**Valores de `estado`**

| Valor | Etiqueta | Significado |
| --- | --- | --- |
| `''` | - | Análisis sin quiebre; no tiene alerta |
| `activa` | Activa | Quiebre sin atender |
| `en_proceso` | En proceso | Un Reponedor la tomó (`taken_by_id`) |
| `completada` | Completada | El Reponedor la marcó repuesta, o llegó una foto sin quiebre que lo confirmó |
| `reemplazada` | Reemplazada por una foto más nueva | Llegó otra foto con quiebre de la misma góndola; la alerta pasó al análisis nuevo |

Una góndola (pasillo + góndola) tiene a lo más **una** alerta abierta
(`activa` o `en_proceso`). Las transiciones están en el
[Modelo Lógico](Modelo%20Logico.md#ciclo-de-vida-de-la-alerta-análisisestado).

---

## 5. `web_camera`

Cámara de sala asociada a un pasillo y una góndola (CU05). Orden por defecto:
`pasillo`, `gondola`.

| Columna | Tipo | Nulo | Clave | Por defecto | Descripción y valores permitidos |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | No | PK | autoincremental | Identificador |
| `nombre` | varchar(60) | No | **UK** | - | Nombre de la cámara (por ejemplo `Cámara A1-1`) |
| `pasillo` | varchar(20) | No | UK* | - | Pasillo, sin espacios y en mayúsculas. *Único junto con `gondola` |
| `gondola` | varchar(20) | No | UK* | - | Góndola, sin espacios y en mayúsculas |
| `calibracion` | text (JSON) | **Sí** | - | `NULL` | Calibración de lente en el formato de OpenCV (sección 10). Si existe, se aplica a las fotos de esa góndola; si es `NULL`, solo se corrige el contraste (CLAHE). `CHECK (JSON_VALID(calibracion) OR calibracion IS NULL)` |

Restricción `una_camara_por_gondola`: `UNIQUE (pasillo, gondola)`; mensaje «Esa
góndola ya tiene una cámara». La unión con `web_analysis` es por texto
(`pasillo`, `gondola`), sin llave foránea y sin distinguir mayúsculas.

---

## 6. `web_config`

Parámetros de la tienda que fija el Administrador (CU05). **Una sola fila**
(`id = 1`), que `Config.get()` crea si no existe.

| Columna | Tipo | Nulo | Clave | Por defecto | Descripción y valores permitidos |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | No | PK | `1` | Siempre 1 |
| `umbral` | smallint unsigned | No | - | `30` | Espacio libre (%) desde el que se alerta. La aplicación acepta de 1 a 100; la base solo exige `>= 0` (`CHECK (umbral >= 0)`). El 30 por defecto viene de `CRITICAL_FREE_FRACTION` (`src/pipeline.py`). Un cambio rige para las fotos siguientes |

---

## 7. Permisos de Django

La aplicación **no usa** permisos de Django: el acceso se decide por el perfil
(`@roles(...)` en `web/views.py`). Las tablas existen porque `AbstractUser` y
`django.contrib.auth` las crean.

### `web_user_user_permissions`

| Columna | Tipo | Nulo | Clave | Descripción |
| --- | --- | --- | --- | --- |
| `id` | integer | No | PK | Identificador |
| `user_id` | bigint | No | **FK**, UK* | → `web_user(id)`. *Único junto con `permission_id` |
| `permission_id` | integer | No | **FK**, UK* | → `auth_permission(id)` |

### `auth_group_permissions`

| Columna | Tipo | Nulo | Clave | Descripción |
| --- | --- | --- | --- | --- |
| `id` | integer | No | PK | Identificador |
| `group_id` | integer | No | **FK**, UK* | → `auth_group(id)`. *Único junto con `permission_id` |
| `permission_id` | integer | No | **FK**, UK* | → `auth_permission(id)` |

### `auth_permission`

| Columna | Tipo | Nulo | Clave | Descripción |
| --- | --- | --- | --- | --- |
| `id` | integer | No | PK | Identificador |
| `content_type_id` | integer | No | **FK**, UK* | → `django_content_type(id)`. *Único junto con `codename` |
| `codename` | varchar(100) | No | UK* | Código del permiso (`add_analysis`, `view_camera`...) |
| `name` | varchar(255) | No | - | Nombre legible (`Can add analysis`) |

### `django_content_type`

| Columna | Tipo | Nulo | Clave | Descripción |
| --- | --- | --- | --- | --- |
| `id` | integer | No | PK | Identificador |
| `app_label` | varchar(100) | No | UK* | Aplicación (`web`, `auth`...). *Único junto con `model` |
| `model` | varchar(100) | No | UK* | Modelo (`user`, `analysis`, `camera`, `config`...) |

---

## 8. Soporte de Django

### `django_session`

Sesiones de inicio de sesión. Una cookie firmada (`HttpOnly`) apunta a la fila;
la sesión expira tras **2 horas sin uso** (`SESSION_COOKIE_AGE`, renovada en
cada petición). Las sesiones de un usuario dado de baja o bloqueado dejan de valer
en la siguiente petición, aunque su fila siga hasta vencer.

| Columna | Tipo | Nulo | Clave | Descripción |
| --- | --- | --- | --- | --- |
| `session_key` | varchar(40) | No | PK | Clave de la sesión (la que viaja en la cookie) |
| `session_data` | text | No | - | Datos de la sesión, firmados y codificados (incluyen el id del usuario) |
| `expire_date` | datetime | No | índice | Cuándo vence. Indexada para limpiar las vencidas |

### `django_migrations`

Registro de las migraciones aplicadas (de `auth`, `contenttypes`, `sessions` y
`web`).

| Columna | Tipo | Nulo | Clave | Descripción |
| --- | --- | --- | --- | --- |
| `id` | integer | No | PK | Identificador |
| `app` | varchar(255) | No | - | Aplicación (`web`, `auth`...) |
| `name` | varchar(255) | No | - | Nombre de la migración (`0006_bloqueo_por_tiempo`) |
| `applied` | datetime | No | - | Cuándo se aplicó |

---

## 9. Estructura del JSON `web_analysis.result`

Es `PipelineResult.to_dict()` (`src/pipeline.py`). Todas las coordenadas están
en **píxeles de la foto original** que subió el usuario, con cajas
`[x_min, y_min, x_max, y_max]`.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `image_size` | `[ancho, alto]` | Tamaño de la foto original |
| `roi` | caja | Góndola segmentada automáticamente |
| `products` | lista de cajas | Productos detectados por YOLO26 (una sola clase) |
| `shelves` | lista de objetos | Una por nivel medido; solo geometría, **sin % ni alerta** (#40) |
| `shelves[].level_index` | entero | Número del nivel, de arriba hacia abajo |
| `shelves[].polygon` | lista de puntos `[x, y]` | Contorno del nivel (9 puntos por borde, para seguir la curva de un lente) |
| `shelves[].gaps` | lista de polígonos | Un polígono por hueco libre del nivel |
| `shelves[].product_count` | entero | Productos del nivel |
| `free_fraction` | decimal, 0 a 1 | Espacio libre de la góndola completa (igual a la columna) |
| `critical` | bool | Alerta de la góndola completa (igual a la columna) |
| `segmentation_found` | bool | `false` si no se encontraron repisas y la góndola se midió como un solo nivel |
| `times` | objeto | Segundos por etapa: `correction`, `segmentation`, `detection`, `availability` y `total` |
| `occluders` | lista de cajas | Lo que tapa la góndola (personas, #77). Vacío si no se buscó |
| `occluded_fraction` | decimal, 0 a 1 | Parte del frente tapada. Se mide solo el frente visible |
| `inconclusive` | bool | `true` si lo tapado pasa de 50 %. Esos análisis **no se guardan**: la aplicación los rechaza, así que en la base siempre es `false` |

Los análisis creados antes del ítem #77 no traen `occluders`,
`occluded_fraction` ni `inconclusive`. La aplicación lee de `result` solo
`shelves` (para dibujar el fleje), `segmentation_found` y la cantidad de
`products` (detalle del análisis).

## 10. Estructura del JSON `web_camera.calibracion`

Formato de la calibración de OpenCV (`LensCalibration`, `src/preprocessing/`).
El formulario de CU05 recibe un archivo JSON de hasta 100 KB, lo valida con
`LensCalibration` y guarda siempre las tres claves, ya normalizadas.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `camera_matrix` | matriz 3x3 | Matriz intrínseca de la cámara |
| `dist_coeffs` | lista de 4, 5, 8, 12 o 14 decimales (pinhole), o 4 (fisheye) | Coeficientes de distorsión |
| `fisheye` | bool | `true` si el lente es ojo de pez. En el archivo subido es opcional (`false` si falta); en la base siempre está |

Ejemplo:

```json
{"camera_matrix": [[1000.0, 0.0, 960.0], [0.0, 1000.0, 540.0], [0.0, 0.0, 1.0]],
 "dist_coeffs": [-0.28, 0.07, 0.0, 0.0, 0.0], "fisheye": false}
```

## 11. Dominios y constantes

| Dominio | Valores | Dónde se define |
| --- | --- | --- |
| Perfiles | `Reponedor`, `Jefe de Salón`, `Administrador` | `web/models.py` (`ROLES`) |
| Estados de la alerta | `activa`, `en_proceso`, `completada`, `reemplazada` (y `''`) | `web/models.py` (`ESTADOS`) |
| Intentos fallidos para bloquear | 5 | `web/auth.py` (`MAX_FAILED_LOGINS`) |
| Duración del bloqueo | 15 minutos | `web/auth.py` (`LOCK_TIME`) |
| Umbral por defecto | 30 % de espacio libre | `src/pipeline.py` (`CRITICAL_FREE_FRACTION`) |
| Rango del umbral | 1 a 100 % | `web/models.py` (`Config.umbral`) |
| Vigencia de «Sin datos» en el dashboard | 24 horas | `web/views.py` (`RECENT`) |
| Duración de la sesión | 2 horas sin uso | `web/settings.py` (`SESSION_COOKIE_AGE`) |
| Tamaño máximo de la foto subida | 20 MB y 50 megapíxeles (JPG o PNG) | `web/forms.py` (`MAX_PHOTO_MB`, `MAX_PHOTO_MEGAPIXELS`) |
| Antigüedad para borrar fotos | 30 días (propuesta, #24) | `borrar_fotos --dias` |

## 12. Datos derivados que no se guardan

| Dato | Cómo se obtiene |
| --- | --- |
| Perfil del usuario | `is_superuser` o el nombre de su primer grupo (`User.role`) |
| Ubicación como texto | `Pasillo {pasillo} · Góndola {gondola}` (`location`) |
| Franjas del fleje | Se calculan desde `result.shelves` (`Analysis.strips`) |
| Estado de una góndola en el dashboard (Disponible, En riesgo, Quiebre, Sin datos) | Último análisis de la góndola, umbral y hora actual (`gondola_state`) |
| Sesión abierta o cuenta bloqueada | `django_session` y `locked_until` contra la hora actual |
