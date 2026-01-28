# VoIP Monitor & Alerter

Un script en Python que escucha el tráfico de red de mi teléfono IP y me avisa en la PC cuando entra una llamada.

Lo hice porque quería tener un registro propio de llamadas y notificaciones con sonido en la compu (estilo retro/gamer) sin depender de la pantalla del teléfono.

### ¿Qué hace?
Básicamente levanta un socket UDP en el puerto 514 (Syslog) y "escucha" los mensajes SIP:

* **Detecta llamadas:** Filtra los paquetes `INVITE`, `CANCEL`, `ACK` y `BYE`.
* **Notifica:** Tira una alerta nativa en Windows y una voz te lee quién llama.
* **Audio:** Reproduce un MP3 aleatorio de una carpeta (yo uso temas de juegos viejos) mientras suena el teléfono.
* **Log:** Guarda todo en una base de datos SQLite local (`registro_llamadas.db`).

### Stack
* **Python 3**
* **Librerías:** `socket` (nativo), `pygame` (audio), `plyer` (notificaciones), `pyttsx3` (texto a voz).

### Cómo usarlo

1.  **Clonar:**
    ```bash
    git clone [https://github.com/franarteta/sistema-alertas-voip.git](https://github.com/franarteta/sistema-alertas-voip.git)
    cd sistema-alertas-voip
    ```

2.  **Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar:**
    * Renombrá `config.example.py` a `config.py`.
    * Poné tu número de interno y el puerto donde tu teléfono manda el syslog.
    * *(Opcional)* Cargá tu `agenda.csv` con nombres y números para que identifique los contactos.

4.  **Correr:**
    ```bash
    python alerta_voip.py
    ```

### Nota
El código está armado para mi configuración de red, pero modificando el `config.py` debería andar en cualquier setup que tire logs SIP por UDP.
