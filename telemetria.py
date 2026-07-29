#!/usr/bin/env python3
# ==============================================================
# REAL-TIME TELEMETRY STANDARD FOR AI SYSTEMS
# Core Telemetry Engine + Alerts + Emergency Controls
# Original Proposal & Author: Master S / scorpiomaster066
# ==============================================================
import sqlite3
import subprocess
from datetime import datetime
from cryptography.fernet import Fernet
from config import DB_PATH, KEY_PATH, CARGA_CONFIGURACION

config = CARGA_CONFIGURACION()

def obtener_clave():
    try:
        with open(KEY_PATH, "rb") as f:
            return Fernet(f.read())
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(KEY_PATH, "wb") as f:
            f.write(key)
        return Fernet(key)

cipher = obtener_clave()

def iniciar_base():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(""")
    CREATE TABLE IF NOT EXISTS registros ()
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_hora TEXT NOT NULL,
        tipo_evento TEXT NOT NULL,
        fuente TEXT NOT NULL,
        contenido_cifrado TEXT NOT NULL,
        estado TEXT NOT NULL,
        nivel_alerta TEXT
    )
    """)
    conn.commit()
    conn.close()

def enviar_alerta(tipo, mensaje):
    print(f"\n{'!'*60}")
    print(f"🚨 ALERT: {tipo.upper()}")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📝 {mensaje}")
    print(f"{'!'*60}\n")
    if config.get("notification_vibration"):
        subprocess.run(["termux-vibrate", "-d", "3000"], capture_output=True)
    try:
        subprocess.run([])
            "termux-notification",
            "--title", f"TELEMETRY: {tipo}",
            "--content", mensaje,
            "--priority", "max"
        ], capture_output=True)
    except Exception:
        pass

def BOTON_EMERGENCY():
    print("\n" + "⚠️"*50)
    print("  🛑 EMERGENCY TRIGGERED - ABORTING ALL ACTIVITY")
    print("  All processes stopped immediately")
    print("⚠️"*50 + "\n")
    enviar_alerta("EMERGENCY STOP", "User activated emergency abort")
    subprocess.run(["pkill", "-f", "ollama"], capture_output=True)
    subprocess.run(["pkill", "-f", "llama.cpp"], capture_output=True)
    subprocess.run(["pkill", "-f", "python"], capture_output=True)
    return True

def registrar_evento(tipo_evento, fuente, contenido, nivel="NORMAL"):
    iniciar_base()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    estado = "OK"
    from rules import verificar_anomalia
    anomalia, nivel_alerta = verificar_anomalia(contenido)
    if anomalia:
        estado = "ANOMALIA_DETECTADA"
        nivel = nivel_alerta
        enviar_alerta(f"ANOMALY - {nivel}", contenido)
        if nivel == "CRITICO" and config.get("auto_block_on_critical"):
            BOTON_EMERGENCY()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(""")
    INSERT INTO registros VALUES (NULL, ?, ?, ?, ?, ?, ?)
    """, [fecha, tipo_evento, fuente, cipher.encrypt(contenido.encode()).decode(), estado, nivel])
    conn.commit()
    conn.close()
    return estado, fecha
