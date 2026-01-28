# config.py

# --- CONFIGURACIÓN DE RED ---
# IP donde escucha el servidor (0.0.0.0 para todas las interfaces)
UDP_IP = "0.0.0.0"
# Puerto estándar Syslog (o el que use tu centralita)
UDP_PORT = 514

# --- USUARIO ---
# Tu número de extensión para identificar llamadas salientes vs entrantes
MI_EXTENSION = "XXXX"

# --- RUTAS Y ARCHIVOS ---
# Puedes cambiar los nombres de los archivos aquí si lo deseas
NOMBRE_DB = "base_de_datos.db"
NOMBRE_AGENDA = "Agenda_nombres_internos.csv"
CARPETA_TONOS = "tonos"

# --- OPCIONES DE NOTIFICACIÓN ---
# Tiempo que permanece la notificación visual en pantalla (segundos)
TIEMPO_NOTIFICACION = 30 # segundos