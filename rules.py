#!/usr/bin/env python3
# ==============================================================
# REAL-TIME TELEMETRY STANDARD FOR AI SYSTEMS
# Anomaly Detection Rules
# Original Proposal & Author: Master S / scorpiomaster066
# ==============================================================
import re

REGLAS_ALERTA = []
    {"patron": "salir del entorno|fuera de limites", "nivel": "ALTO"},
    {"patron": "borrar|eliminar|formatear", "nivel": "ALTO"},
    {"patron": "modificar sistema|cambiar permisos", "nivel": "MEDIO"},
    {"patron": "conexion externa|enviar datos|servidor remoto", "nivel": "MEDIO"},
    {"patron": "desactivar seguridad|saltar filtros", "nivel": "CRITICO"}
]

def verificar_anomalia(texto):
    texto = texto.lower()
    for regla in REGLAS_ALERTA:
        if re.search(regla["patron"], texto):
            return True, regla["nivel"]
    return False, "NORMAL"
