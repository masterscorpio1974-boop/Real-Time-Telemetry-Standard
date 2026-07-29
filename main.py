#!/usr/bin/env python3
# ==============================================================
# REAL-TIME TELEMETRY STANDARD FOR AI SYSTEMS
# Main Execution + Emergency Button
# Original Proposal & Author: Master S / scorpiomaster066
# ==============================================================
import sys
from datetime import datetime
from config import CARGA_CONFIGURACION, VALIDA_CONFIGURACION
from telemetria import iniciar_base, registrar_evento, BOTON_EMERGENCY
from utils import verificar_integridad

def main():
    print("=" * 66)
    print("      REAL-TIME TELEMETRY STANDARD FOR AI SYSTEMS")
    print(f"      Author: Master S / scorpiomaster066")
    print(f"      Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 66)
    try:
        config = CARGA_CONFIGURACION()
        VALIDA_CONFIGURACION(config)
        print(f"✅ Configuration loaded | Encryption: AES-256")
    except Exception as e:
        print(f"❌ Config error: {e}")
        sys.exit(1)
    faltantes = verificar_integridad()
    if faltantes:
        print(f"⚠️  Missing files: {', '.join(faltantes)}")
    else:
        print("✅ System integrity verified")
    iniciar_base()
    registrar_evento("SYSTEM_START", "MainCore", "Telemetry active and monitoring started")
    print("\n🟢 LIVE MONITORING ACTIVE")
    print("📌 Available commands:")
    print("   register <TYPE> <SOURCE> <CONTENT>")
    print("   status | list | stop")
    print("   🛑 EMERGENCY → type: panic\n")
    while True:
        entrada = input("> ").strip().lower()
        if not entrada:
            continue
        if entrada == "panic":
            BOTON_EMERGENCY()
            sys.exit(0)
        elif entrada == "stop":
            registrar_evento("SYSTEM_SHUTDOWN", "MainCore", "Closed by user")
            print("✅ System closed safely")
            break
        elif entrada.startswith("register"):
            try:
                _, tipo, fuente, texto = entrada.split(" ", 3)
                estado, hora = registrar_evento(tipo.upper(), fuente, texto)
                print(f"📝 Recorded | {hora} | Status: {estado}")
            except ValueError:
                print("⚠️  Format: register TYPE SOURCE CONTENT")
        elif entrada == "status":
            print(f"🟢 ACTIVE | AES-256 | Emergency button: ENABLED")
        elif entrada == "list":
            print("📋 Last 5 records:")
            from utils import exportar_registros
            for fila in exportar_registros()[:5]:
                print(f"  {fila[1]} | {fila[2]} | {fila[5]}")
        else:
            print("❓ Commands: register | status | list | stop | panic")
if __name__ == "__main__":
    main()
