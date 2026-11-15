"""Script SQL de la base (#62): crea la misma estructura que `manage.py migrate`
y la puebla con datos de prueba ficticios."""

import json
import re
import sqlite3
from pathlib import Path

import pytest
from django.db import connection

from web.auth import valid_rut
from web.models import ROLES

pytestmark = pytest.mark.django_db
SCRIPT = Path(__file__).parent.parent / "Fase 2/Evidencias Proyecto/Evidencias de sistema/Base de datos/shelfvision.sql"


@pytest.fixture
def script_db():
    db = sqlite3.connect(":memory:")
    db.executescript(SCRIPT.read_text(encoding="utf-8"))
    return db


def schema(rows):
    """Tablas e indices sin los espacios (el script va indentado para leerse)."""
    return sorted((kind, name, table, re.sub(r"\s+", "", sql)) for kind, name, table, sql in rows if sql)


def test_script_schema_equals_migrate(script_db):
    query = "SELECT type, name, tbl_name, sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"
    with connection.cursor() as cursor:
        migrated = cursor.execute(query).fetchall()
    assert schema(script_db.execute(query)) == schema(migrated)


def test_script_marks_the_migrations_as_applied(script_db):
    with connection.cursor() as cursor:
        applied = set(cursor.execute("SELECT app, name FROM django_migrations").fetchall())
    assert set(script_db.execute("SELECT app, name FROM django_migrations")) == applied


def test_sample_data_is_consistent(script_db):
    script_db.execute("PRAGMA foreign_keys = ON")
    assert script_db.execute("PRAGMA foreign_key_check").fetchall() == []
    assert {name for (name,) in script_db.execute("SELECT name FROM auth_group")} == set(ROLES)
    assert script_db.execute("SELECT COUNT(*) FROM web_config").fetchone() == (1,)
    ruts = [rut for (rut,) in script_db.execute("SELECT username FROM web_user")]
    assert len(ruts) >= 3 and all(valid_rut(rut) for rut in ruts)
    roles = {role for (role,) in script_db.execute(
        "SELECT g.name FROM web_user_groups ug JOIN auth_group g ON g.id = ug.group_id")}
    assert roles == set(ROLES)


def test_sample_analyses_follow_the_app_rules(script_db):
    rows = script_db.execute("SELECT pasillo, gondola, critical, estado, result FROM web_analysis").fetchall()
    assert rows
    for _, _, critical, estado, result in rows:
        assert json.loads(result)["shelves"]  # Analysis.strips lo necesita
        assert bool(estado) == bool(critical)  # un analisis sin quiebre no tiene estado
    open_alerts = [(p, g) for p, g, _, estado, _ in rows if estado in ("activa", "en_proceso")]
    assert len(open_alerts) == len(set(open_alerts))  # CU02: una alerta abierta por gondola
    assert {estado for *_, estado, _ in rows} >= {"", "activa", "completada"}
