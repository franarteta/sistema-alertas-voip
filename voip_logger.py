import sqlite3
from datetime import datetime
import os
try:
    import config
    DB_FILENAME = config.NOMBRE_DB
except ImportError:
    DB_FILENAME = "registro_llamadas.db" # Fallback por si acaso

CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(CARPETA_BASE, DB_FILENAME)

def inicializar_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS llamadas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                hora TEXT,
                tipo TEXT,        -- Entrante, Saliente, Perdida, Contestada
                estado TEXT,      
                origen TEXT,
                destino TEXT,
                nombre TEXT,
                call_id TEXT      
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Error base de datos: {e}")

def registrar_llamada(tipo, origen, destino, nombre, call_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        ahora = datetime.now()
        fecha = ahora.strftime("%Y-%m-%d")
        hora = ahora.strftime("%H:%M:%S")
        
        # Guardamos inicialmente como "Entrante"
        estado_inicial = "Entrante" if tipo == "Entrante" else "Saliente"
        
        cursor.execute('''
            INSERT INTO llamadas (fecha, hora, tipo, estado, origen, destino, nombre, call_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (fecha, hora, tipo, estado_inicial, origen, destino, nombre, call_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Error log: {e}")

def actualizar_estado(call_id, nuevo_estado):
    """Actualiza el estado de una llamada (Perdida o Contestada)"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Actualizamos tanto el campo 'estado' como 'tipo' para que sea facil de leer
        cursor.execute('''
            UPDATE llamadas 
            SET estado = ?, tipo = ?
            WHERE call_id = ? AND tipo = 'Entrante'
        ''', (nuevo_estado, nuevo_estado, call_id))
        
        if cursor.rowcount > 0:
            print(f"🔄 Llamada {call_id} -> {nuevo_estado}")
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Error actualizando: {e}")

# Helpers rápidos
def marcar_como_perdida(call_id):
    actualizar_estado(call_id, "Perdida")

def marcar_como_contestada(call_id):
    actualizar_estado(call_id, "Contestada")

inicializar_db()