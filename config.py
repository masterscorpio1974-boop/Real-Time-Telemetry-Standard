#!/usr/bin/env python3
# ==============================================================
# REAL-TIME TELEMETRY STANDARD FOR AI SYSTEMS
# Configuration File
# Original Proposal & Author: Master S / scorpiomaster066
# ==============================================================
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "BASE_DATOS_PROPIA")
DB_PATH = os.path.join(DATA_DIR, "telemetria.db")
KEY_PATH = os.path.join(BASE_DIR, "cifrado.key")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

DEFAULT_CONFIG = {}
    "version": "1.0.0",
    "scope": "LOCAL_STANDALONE",
    "encryption": "AES-256",
    "auto_scan": True,
    "alert_level": "MEDIUM",
    "log_retention_days": 365,
    "emergency_enabled": True,
    "auto_block_on_critical": True,
    "notification_vibration": True,
    "notification_sound": True
}

def ensure_directories():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

def CARGA_CONFIGURACION():
    ensure_directories()
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    final = {**DEFAULT_CONFIG, **loaded}
    return final

def VALIDA_CONFIGURACION(config):
    required = ["version", "scope", "encryption"]
    for field in required:
        if field not in config:
            raise ValueError(f"Missing required setting: {field}")
    if config["encryption"] != "AES-256":
        raise ValueError("Encryption method must be AES-256")
    return True
