import mysql.connector

from flask import current_app


# =========================================================
# CONEXIÓN A MYSQL
# FITZONE STORE - SEMANA 13
# =========================================================

def obtener_conexion():

    conexion = mysql.connector.connect(

        host=current_app.config["MYSQL_HOST"],

        port=current_app.config["MYSQL_PORT"],

        user=current_app.config["MYSQL_USER"],

        password=current_app.config["MYSQL_PASSWORD"],

        database=current_app.config["MYSQL_DATABASE"]

    )

    return conexion