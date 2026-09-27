import os

import psycopg
from psycopg.rows import dict_row


# =========================================================
# CONEXIÓN A POSTGRESQL
# FITZONE STORE - SEMANA 15
# =========================================================

def obtener_conexion():

    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "Debe definir la variable de entorno DATABASE_URL."
        )

    conexion = psycopg.connect(
        database_url,
        row_factory=dict_row
    )

    return conexion