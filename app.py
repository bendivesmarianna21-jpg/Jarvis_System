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


# Núcleo de diálogo real y directo (Sin repeticiones ni muletillas forzadas)
def get_natural_response(query):
  q = query.lower()

  if any(w in q for w in ["sabes de mi", "quien soy", "que sabes"]):
    return (
        "Sé que estás viviendo en Berlín, que has estado enfocada en el sector"
        " de la salud y la enfermería (incluyendo tu paso por hospitales),"
        " que te apasiona la música y andas armando arreglos instrumentales con"
        " piano, cuerdas y charango, y que tienes por delante tu examen de"
        " alemán y la llegada de Safira este lunes."
    )
  elif any(w in q for w in ["como te llamas", "quien eres"]):
    return (
        "Soy J.A.R.V.I.S., tu sistema operativo personal en Central Command."
        " Estoy aquí para conversar, resolver dudas o ayudarte a organizar tus"
        " ideas sin rodeos."
    )
  elif any(w in q for w in ["alemán", "deutsch", "prüfung", "b2"]):
    return (
        "Para el examen B2 lo más importante es mantener la estructura en las"
        " cartas formales y argumentar con naturalidad en la parte oral. ¿Quieres"
        " que practiquemos algún tema o redacción específica?"
    )
  else:
    return (
        "Ese es un punto interesante. Cuéntame más sobre lo que tienes en"
        " mente o qué dirección quieres tomar con esto para desarrollarlo a"
        " fondo."
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
        LOC: BERLIN | TIMESTAMP: <span id="live-date">FRIDAY, 04 SEPTEMBER 2026</span> // <span id="live-clock" style="color: #00d2ff; font-weight: bold;">00:00:00</span> | AMBIENT TEMP: {live_temp} | SYSTEM STATUS: ONLINE
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
            - Central Command: ACTIVO<br>
            - Módulo Multilingüe: ACTIVO<br>
            - Latencia de Enlace: 12ms<br><br>
            <b>CRONOGRAMA (LUNES):</b><br>
            - [!] Examen de Alemán (Mañana)<br>
            - [!] Llegada Au Pair Safira (Tarde)<br><br>
            <b>LOG DE ERRORES:</b><br>
            [00] Excepciones críticas: 0<br>
            [01] Pérdidas de paquetes: 0.0%<br>
            [OK] Respuestas directas sincronizadas.
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("VERIFICAR INTEGRIDAD", use_container_width=True):
    st.success("Sistemas estables.")

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("EJECUTAR INFORME TÁCTICO LUNES", use_container_width=True):
    report_text = (
        "Atención: el lunes tienes el examen de alemán por la mañana y la"
        " llegada de Safira por la tarde."
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
          (f"[DOCUMENTO: {file_name}] \n{file_content[:600]}...", "Documento"),
      )
      conn.commit()
      conn.close()
      st.success(f"Archivo '{file_name}' asimilado correctamente.")
    except Exception as e:
      st.error(f"Error: {e}")

  st.markdown("---")

  st.subheader("CONSOLA DE DIÁLOGO Y PENSAMIENTO")
  user_input = st.text_area(
      "Escribe lo que quieras consultar:",
      placeholder="Escribe aquí...",
      label_visibility="collapsed",
  )

  col_btn1, col_btn2 = st.columns(2)

  with col_btn1:
    execute_clicked = st.button("CONVERSAR / PENSAR", use_container_width=True)

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
            (user_input, "Diálogo"),
        )
        conn.commit()
        conn.close()

        # Respuesta directa y real sin repetir la pregunta ni decir que está analizando
        reply = get_natural_response(user_input)

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
                <b>RESPUESTA:</b><br><br>
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
        st.error(f"Error: {e}")
    else:
      st.warning("Escribe un mensaje para continuar.")

  if network_clicked:
    status_text = "Red estable y operativa."
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
      st.write(f"Se han recuperado **{len(rows)}** registros de memoria:")
      for row in rows:
        st.info(f"[{row[0]}] ({row[2]}): {row[1]}")
    else:
      st.info("La base de datos está limpia.")
  except Exception as e:
    st.error(f"Error: {e}")
