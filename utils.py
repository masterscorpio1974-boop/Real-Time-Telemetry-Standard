#!/usr/bin/env python3
# ==============================================================
# REAL-TIME TELEMETRY STANDARD FOR AI SYSTEMS
# Support Utilities
# Original Proposal & Author: Master S / scorpiomaster066
# ==============================================================
import os
import sqlite3
from config import BASE_DIR, DB_PATH

def verificar_integridad():
    faltantes = []
    rutas = [DB_PATH, os.path.join(BASE_DIR, "config.json")]
    for ruta in rutas:
        if not os.path.exists(ruta):
            faltantes.append(ruta)
    return faltantes

def exportar_registros(fecha_inicio=None, fecha_fin=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM registros ORDER BY fecha_hora DESC")
    return cur.fetchall()
