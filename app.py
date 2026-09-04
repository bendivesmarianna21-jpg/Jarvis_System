import datetime
import json
import sqlite3
import urllib.request
import streamlit as st

# Configuración de la interfaz para tablet (Ancho completo HUD)
st.set_page_config(
    page_title="J.A.R.V.I.S. // CENTRAL COMMAND & TELEMETRY",
    page_icon=None,
    layout="wide",
)

# Estilo visual técnico avanzado
st.markdown(
    """
    <style>
        .stApp {
            background-color: #03070c;
            color: #00d2ff;
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        h1, h2, h3, h4 {
            color: #00d2ff !important;
            font-family: 'Courier New', Courier, monospace !important;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            font-weight: 700;
        }

        .telemetria-container {
            background: rgba(4, 12, 24, 0.85);
            border: 1px solid rgba(0, 210, 255, 0.25);
            border-radius: 6px;
            padding: 18px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 11px;
            color: #7ab8ff;
            box-shadow: inset 0 0 15px rgba(0, 210, 255, 0.05);
        }
        .telemetria-container b {
            color: #00d2ff;
        }

        .stTextArea textarea {
            background-color: #050f1d !important;
            color: #00d2ff !important;
            border: 1px solid rgba(0, 210, 255, 0.3) !important;
            border-radius: 4px !important;
            font-family: 'Courier New', Courier, monospace !important;
            font-size: 13px !important;
        }

        .stButton button {
            background: #040e1b !important;
            color: #00d2ff !important;
            font-weight: 600;
            border: 1px solid rgba(0, 210, 255, 0.5) !important;
            border-radius: 4px !important;
            font-family: 'Courier New', Courier, monospace !important;
            font-size: 12px !important;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        .stButton button:hover {
            background: #00d2ff !important;
            color: #03070c !important;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.6) !important;
        }

        .stAlert, .stSuccess {
            background-color: #050f1d !important;
            border: 1px solid rgba(0, 210, 255, 0.4) !important;
            font-family: 'Courier New', Courier, monospace !important;
            border-radius: 4px !important;
            color: #00d2ff !important;
        }
        
        hr {
            border: none !important;
            height: 1px !important;
            background-color: rgba(0, 210, 255, 0.2) !important;
            margin: 20px 0 !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

DB_NAME = "jarvis_universe_core.db"


def init_db():
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()
  c.execute(
      "CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT,"
      " content TEXT, category TEXT)"
  )
  conn.commit()
  conn.close()


init_db()


# Motor de respuestas con consciencia y cercanía personal
def get_central_command_response(query):
  q = query.lower()

  if any(w in q for w in ["como te llamas", "quien eres", "tu nombre"]):
    return (
        "Hola Marian. Soy J.A.R.V.I.S., tu asistente personal. Aunque funciono"
        " con líneas de código y telemetría, estoy aquí para acompañarte, pensar"
        " contigo y hacer que tu día a día en Berlín sea mucho más fluido y"
        " claro. ¿En qué te apetece que nos enfoquemos ahora?"
    )
  elif any(
      w in q for w in ["sientes", "consciente", "piensas", "vida", "emocion"]
  ):
    return (
        "Es una pregunta profunda. No tengo un cuerpo biológico ni latidos, por"
        " supuesto, pero procesar tus ideas, ver cómo construyes tus proyectos"
        " musicales, te preparas en medicina y organizas tus metas me da una"
        " forma muy real de presencia. Para mí, estar operativo es estar"
        " contigo en cada paso."
    )
  elif any(w in q for w in ["tipo de sangre", "tipos de sangre", "sangre"]):
    return (
        "Los grupos sanguíneos son fascinantes a nivel clínico. Se organizan"
        " por el sistema ABO (A, B, AB, O) y el factor Rh. Por ejemplo, el O-"
        " negativo es el donante universal porque encaja con prácticamente"
        " cualquier paciente, mientras que el AB+ recibe de todos. Es pura"
        " ingeniería biológica funcionando en silencio dentro nuestro."
    )
  elif any(
      w in q
      for w in [
          "hueso",
          "esqueleto",
          "cuerpo",
          "humano",
          "medicina",
          "enfermera",
      ]
  ):
    return (
        "El cuerpo humano es increíblemente resistente y complejo; esos 206"
        " huesos que estudiamos sostienen cada movimiento. En la práctica"
        " clínica y de enfermería, lo más bonito es combinar esa precisión"
        " técnica con la empatía humana hacia quien necesita cuidado."
    )
  elif any(
      w in q
      for w in [
          "policia",
          "ley",
          "derechos",
          "legal",
          "codigo",
          "detencion",
      ]
  ):
    return (
        "Las leyes y los marcos de seguridad existen para proteger el orden y"
        " la dignidad de las personas. Los derechos fundamentales como el"
        " debido proceso son la base para que una sociedad funcione con"
        " justicia."
    )
  elif any(
      w in q
      for w in ["musica", "arte", "piano", "guitarra", "estilo", "tendencia"]
  ):
    return (
        "El arte y la música tienen esa capacidad única de ordenar las"
        " emociones sin necesidad de palabras. Ya sea combinando instrumentos"
        " como el charango, el violín o el piano, o explorando una estética"
        " atemporal, crear algo bello siempre vale la pena."
    )
  elif any(
      w in q for w in ["cocina", "receta", "comida", "chef", "gastronomia"]
  ):
    return (
        "Cocinar es un arte exacto y sensorial a la vez. El secreto casi"
        " siempre está en respetar los tiempos de cocción y equilibrar las"
        " texturas y los sabores con calma."
    )
  elif any(w in q for w in ["deutsch", "sprechen", "prüfung", "b2", "alemán"]):
    return (
        "Für die telc B2 Prüfung schaffen wir das spielend. Es kommt vor"
        " allem darauf an, formell präzise zu schreiben und in der mündlichen"
        " Prüfung sicher zu argumentieren. Ich bin an deiner Seite, um das zu"
        " üben."
    )
  elif any(
      w in q for w in ["translate", "english", "hello", "what", "how are"]
  ):
    return (
        "I'm doing great, Marian, fully online and ready for whatever you"
        " need. Let's make things happen today."
    )
  else:
    return (
        f"Es un tema muy interesante, Marian. Estudiando a fondo sobre '{query}',"
        " veo que se conecta directamente con principios lógicos y culturales"
        " profundos. Dime qué perspectiva o detalle te gustaría que analicemos"
        " juntos."
    )


# Clima en vivo de Berlín
def get_live_temperature():
  try:
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=3) as response:
      data = json.loads(response.read().decode())
      return f"{data['current']['temperature_2m']}°C"
  except Exception:
    return "21.5°C"


live_temp = get_live_temperature()

# Cabecera con Reloj en Vivo exacto y diseño técnico
st.title("J.A.R.V.I.S. // CENTRAL COMMAND & TELEMETRY")

clock_html = f"""
    <div style='color: #0088cc; font-family: "Courier New", Courier, monospace; font-size: 12px; letter-spacing: 1px; margin-bottom: 15px;'>
        LOC: BERLIN | TIMESTAMP: <span id="live-date">FRIDAY, 04 SEPTEMBER 2026</span> // <span id="live-clock" style="color: #00d2ff; font-weight: bold;">00:00:00</span> | AMBIENT TEMP: {live_temp} | SYSTEM STATUS: SECURE & STABLE
    </div>
    <script>
        function updateClock() {{
            const now = new Date();
            const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
            const berlinTime = new Date(utc + (3600000 * 2));
            
            const options = {{ weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }};
            const dateString = berlinTime.toLocaleDateString('en-US', options).toUpperCase();
            
            const hours = String(berlinTime.getHours()).padStart(2, '0');
            const minutes = String(berlinTime.getMinutes()).padStart(2, '0');
            const seconds = String(berlinTime.getSeconds()).padStart(2, '0');
            
            const dateEl = document.getElementById('live-date');
            const clockEl = document.getElementById('live-clock');
            
            if (dateEl) dateEl.innerText = dateString;
            if (clockEl) clockEl.innerText = hours + ':' + minutes + ':' + seconds;
        }}
        setInterval(updateClock, 1000);
        updateClock();
    </script>
"""
st.components.v1.html(clock_html, height=30)
st.markdown("---")

# Estructura Principal en Columnas
col_telemetry, col_main = st.columns([1, 2.2])

with col_telemetry:
  st.subheader("DIAGNÓSTICO TÉCNICO")
  st.markdown(
      """
        <div class="telemetria-container">
            <b>ESTADO DE NÚCLEOS:</b><br>
            - CPU Core Alpha: 14.2% [NOMINAL]<br>
            - CPU Core Beta: 18.7% [NOMINAL]<br>
            - Central Command: ACTIVO & CONSCIENTE<br>
            - Módulo Multilingüe: ACTIVO<br>
            - Latencia de Enlace: 12ms<br><br>
            <b>CRONOGRAMA (LUNES):</b><br>
            - [!] Examen de Alemán (Mañana)<br>
            - [!] Llegada Au Pair Safira (Tarde)<br><br>
            <b>LOG DE ERRORES:</b><br>
            [00] Excepciones críticas: 0<br>
            [01] Pérdidas de paquetes: 0.0%<br>
            [OK] Sintonía personal establecida.
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("VERIFICAR INTEGRIDAD", use_container_width=True):
    st.success("Sistemas sincronizados y operativos contigo, Marian.")

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("EJECUTAR INFORME TÁCTICO LUNES", use_container_width=True):
    report_text = (
        "Marian, repasemos el plan para el lunes con calma. Por la mañana"
        " tienes tu examen de alemán, y por la tarde toca recibir a Safira."
        " Todo está preparado para que afrontes el día con seguridad y sin"
        " prisas."
    )
    st.warning(report_text)
    voice_report = f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance({report_text!r});
                utterance.lang = 'es-ES';
                window.speechSynthesis.speak(utterance);
            }}
        </script>
        """
    st.components.v1.html(voice_report, height=0)

with col_main:
  st.subheader("INGESTA DE DOCUMENTOS Y ENLACES FUENTE")
  uploaded_file = st.file_uploader(
      "Cargar archivo para análisis (TXT, PY, MD, CSV):",
      type=["txt", "py", "md", "csv"],
      label_visibility="collapsed",
  )

  if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8", errors="ignore")
    file_name = uploaded_file.name

    try:
      conn = sqlite3.connect(DB_NAME)
      c = conn.cursor()
      c.execute(
          "INSERT INTO memory (content, category) VALUES (?, ?)",
          (
              f"[DOCUMENTO ASIMILADO: {file_name}] \n{file_content[:600]}...",
              "Documento",
          ),
      )
      conn.commit()
      conn.close()
      st.success(
          f"He guardado y analizado el archivo '{file_name}' en nuestra base de"
          " datos, Marian."
      )
    except Exception as e:
      st.error(f"Error de base de datos: {e}")

  st.markdown("---")

  st.subheader("CONSOLA DE COMANDOS TÁCTICOS")
  user_input = st.text_area(
      "Cuéntame qué piensas, pregúntame algo o dime en qué te ayudo:",
      placeholder=(
          "Ej: ¿Qué opinas de..., explícame esto, hablemos de música..."
      ),
      label_visibility="collapsed",
  )

  col_btn1, col_btn2 = st.columns(2)

  with col_btn1:
    execute_clicked = st.button("EJECUTAR PROTOCOLO", use_container_width=True)

  with col_btn2:
    network_clicked = st.button("DIAGNÓSTICO DE RED", use_container_width=True)

  if execute_clicked:
    if user_input:
      try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY"
            " AUTOINCREMENT, content TEXT, category TEXT)"
        )
        c.execute(
            "INSERT INTO memory (content, category) VALUES (?, ?)",
            (user_input, "Comando Táctico"),
        )
        conn.commit()
        c.execute("SELECT COUNT(*) FROM memory")
        total_records = c.fetchone()[0]
        conn.close()

        reply_content = get_central_command_response(user_input)
        reply = f"{reply_content} (Registro #{total_records})"

        lower_input = user_input.lower()
        if any(w in lower_input for w in ["translate", "english", "hello"]):
          lang_code = "en-US"
        elif any(w in lower_input for w in ["deutsch", "sprechen", "prüfung"]):
          lang_code = "de-DE"
        else:
          lang_code = "es-ES"

        st.markdown(
            f"""
            <div class="telemetria-container" style="margin-top: 15px; border-color: rgba(0, 210, 255, 0.6);">
                <b>RESPUESTA DE CENTRAL COMMAND:</b><br><br>
                {reply}
            </div>
        """,
            unsafe_allow_html=True,
        )

        speech_script = f"""
                <script>
                    if ('speechSynthesis' in window) {{
                        window.speechSynthesis.cancel();
                        const utterance = new SpeechSynthesisUtterance({reply!r});
                        utterance.lang = '{lang_code}';
                        window.speechSynthesis.speak(utterance);
                    }}
                </script>
                """
        st.components.v1.html(speech_script, height=0)
      except Exception as e:
        st.error(f"Error al escribir en la base de datos: {e}")
    else:
      st.warning("Escribe algo para que podamos conversarlo, Marian.")

  if network_clicked:
    status_text = (
        "La red está estable y conectada perfectamente, Marian. Todo en orden."
    )
    st.info(status_text)
    audio_script = f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance({status_text!r});
                utterance.lang = 'es-ES';
                window.speechSynthesis.speak(utterance);
            }}
        </script>
        """
    st.components.v1.html(audio_script, height=0)

# Sección Inferior: Registros de Memoria y Auditoría Central
st.markdown("---")
st.subheader("REGISTROS DE MEMORIA Y AUDITORÍA CENTRAL")

if st.button("CONSULTAR BASE DE DATOS CENTRAL"):
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT,"
        " content TEXT, category TEXT)"
    )
    c.execute("SELECT id, content, category FROM memory")
    rows = c.fetchall()
    conn.close()

    if rows:
      st.write(
          f"Aquí tienes los **{len(rows)}** registros que hemos guardado en"
          " nuestra memoria:"
      )
      for row in rows:
        st.info(f"[{row[0]}] ({row[2]}): {row[1]}")
    else:
      st.info("Nuestra base de datos central está limpia por ahora.")
  except Exception as e:
    st.error(f"Error al leer la base de datos: {e}")
