import csv
import os
import random
import re
import contextlib
import pyttsx3 

with contextlib.redirect_stdout(None):
    import pygame

class GestorAgenda:
    def __init__(self, ruta_csv):
        self.ruta_csv = ruta_csv
        self.contactos = {}
        self.cargar_agenda()

    def cargar_agenda(self):
        if os.path.exists(self.ruta_csv):
            try:
                with open(self.ruta_csv, mode='r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) >= 2:
                            self.contactos[row[0].strip()] = row[1].strip()
                print(f"✅ Agenda cargada: {len(self.contactos)} contactos.")
            except Exception as e:
                print(f"⚠️ Error en agenda: {e}")

    def obtener_nombre(self, interno, nombre_sip=None):
        if not interno: return "Desconocido"
        nombre_csv = self.contactos.get(interno)
        if nombre_csv: return nombre_csv
        if nombre_sip:
            nombre_sip = nombre_sip.strip()
            if nombre_sip.isdigit() or nombre_sip == interno: return "Desconocido"
            return nombre_sip
        return "Desconocido"

def iniciar_sistema_audio():
    try:
        pygame.mixer.init()
    except: pass

def reproducir_random(carpeta_tonos):
    try:
        if os.path.exists(carpeta_tonos):
            archivos = [f for f in os.listdir(carpeta_tonos) if f.endswith('.mp3')]
            if archivos:
                elegido = random.choice(archivos)
                pygame.mixer.music.load(os.path.join(carpeta_tonos, elegido))
                pygame.mixer.music.set_volume(0.8) 
                pygame.mixer.music.play()
    except: pass

def anunciar_voz(nombre):
    """Habla sobre la música bajando el volumen (Ducking)"""
    try:
        if pygame.mixer.music.get_busy(): pygame.mixer.music.set_volume(0.2)
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        engine.say(f"Llamada de {nombre}")
        engine.runAndWait()
        engine.stop()
        del engine
        if pygame.mixer.music.get_busy(): pygame.mixer.music.set_volume(0.8)
    except: pass

def detener_audio():
    """Detiene la música inmediatamente"""
    try: pygame.mixer.music.stop()
    except: pass

def obtener_call_id(mensaje):
    """Extrae SOLO el Call-ID de cualquier mensaje SIP"""
    match_callid = re.search(r'Call-ID:\s*([^\r\n]+)', mensaje, re.IGNORECASE)
    if match_callid:
        return match_callid.group(1).strip()
    return None

def extraer_datos_sip(mensaje):
    # Usamos la función auxiliar para el ID
    call_id = obtener_call_id(mensaje) or "sin_id"

    match_contact = re.search(r'Contact:\s*<sip:(\d+)@', mensaje)
    if match_contact:
        interno_origen = match_contact.group(1)
    else:
        match_from_num = re.search(r'From:.*<sip:(\d+)@', mensaje)
        interno_origen = match_from_num.group(1) if match_from_num else None

    match_nom = re.search(r'From:\s*"([^"]+)"', mensaje)
    nombre_sip = match_nom.group(1).strip() if match_nom else None

    match_dest = re.search(r'INVITE sip:(\d+)', mensaje)
    destino = match_dest.group(1) if match_dest else "Línea"

    return interno_origen, nombre_sip, destino, call_id