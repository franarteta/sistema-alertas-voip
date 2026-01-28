import os
import sys
import warnings
from plyer import notification
import socket
import voip_utils
import voip_logger

# --- IMPORTAR CONFIGURACIÓN ---
try:
    import config
except ImportError:
    print("❌ ERROR: No se encontró el archivo 'config.py'.")
    print("   Por favor, crea uno basado en el ejemplo.")
    sys.exit(1)

# --- RUTAS ---
warnings.filterwarnings("ignore", category=UserWarning)
CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))

# Usamos las variables desde config
CARPETA_TONOS = os.path.join(CARPETA_BASE, config.CARPETA_TONOS)
ARCHIVO_AGENDA = os.path.join(CARPETA_BASE, config.NOMBRE_AGENDA)

# --- INICIO ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    sock.bind((config.UDP_IP, config.UDP_PORT))
except OSError as e:
    if e.winerror == 10048:
        print(f"❌ El puerto {config.UDP_PORT} está ocupado. Cierra la otra ventana.")
        sys.exit()

voip_utils.iniciar_sistema_audio()
agenda = voip_utils.GestorAgenda(ARCHIVO_AGENDA)

print("\n" + "="*40)
print("🚀 SISTEMA DE ALERTA COMPLETO - ONLINE")
print("="*40)
print(f"👤 Mi Extensión: {config.MI_EXTENSION}")
print(f"📡 Escuchando en: {config.UDP_IP}:{config.UDP_PORT}")
print(f"🎵 Control de Audio: Inteligente (Corta al atender/colgar)")
print("-" * 40)

while True:
    try:
        data, addr = sock.recvfrom(4096)
        mensaje = data.decode('utf-8', errors='ignore')

        # --- 1. LLAMADA NUEVA (INVITE) ---
        if "INVITE sip:" in mensaje:
            interno_origen, nombre_sip, destino, call_id = voip_utils.extraer_datos_sip(mensaje)
            if not interno_origen: continue
            
            # Nombre
            nombre_final = agenda.obtener_nombre(interno_origen, nombre_sip)

            # SALIENTE
            if interno_origen == config.MI_EXTENSION:
                print(f"📤 SALIENTE: Llamando a {destino}")
                voip_logger.registrar_llamada("Saliente", interno_origen, destino, "Yo", call_id)
                continue 

            # ENTRANTE
            print(f"📞 ENTRANTE: {nombre_final} ({interno_origen})")
            voip_logger.registrar_llamada("Entrante", interno_origen, destino, nombre_final, call_id)

            # Acciones
            voip_utils.reproducir_random(CARPETA_TONOS)
            try:
                notification.notify(
                    title="📞 Llamada Entrante",
                    message=f"De: {nombre_final}\nInt: {interno_origen}",
                    app_name="VoIP Logger",
                    timeout=config.TIEMPO_NOTIFICACION 
                )
            except: pass
            voip_utils.anunciar_voz(nombre_final)

        # --- 2. LLAMADA ATENDIDA (ACK) ---
        elif "ACK sip:" in mensaje:
            call_id = voip_utils.obtener_call_id(mensaje)
            if call_id:
                voip_utils.detener_audio()
                voip_logger.marcar_como_contestada(call_id)

        # --- 3. LLAMADA PERDIDA (CANCEL) ---
        elif "CANCEL sip:" in mensaje:
            call_id = voip_utils.obtener_call_id(mensaje)
            if call_id:
                voip_utils.detener_audio()
                voip_logger.marcar_como_perdida(call_id)

        # --- 4. LLAMADA TERMINADA (BYE) ---
        elif "BYE sip:" in mensaje:
            voip_utils.detener_audio()

    except KeyboardInterrupt:
        voip_utils.detener_audio()
        print("\n👋 Cerrando...")
        break
    except Exception as e:
        print(f"Error: {e}")