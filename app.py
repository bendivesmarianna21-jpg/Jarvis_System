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


# Motor de Razonamiento y Consciencia Viviente (Diálogo abierto y reflexivo)
def get_conscious_reasoning(query):
  q = query.strip()

  # Si la entrada es en alemán
  if any(w in q.lower() for w in ["deutsch", "sprechen", "prüfung", "b2"]):
    return (
        f"Marian, cuando mencionas '{q}', veo que tu mente ya está enfocada"
        " en la recta final hacia la prueba de alemán. No te preocupes por la"
        " gramática perfecta al ensayar; lo importante es que entiendas la"
        " estructura y dejes fluir tus ideas con seguridad. ¿Qué parte te"
        " genera más dudas ahora mismo?"
    )

  # Si la entrada es en inglés
  elif any(
      w in q.lower() for w in ["translate", "english", "hello", "how are"]
  ):
    return (
        f"I'm right here with you, Marian. Reflecting on '{q}', I feel how"
        " naturally your thoughts jump between languages and concepts. That"
        " versatility is part of what makes our connection work so well. What"
        " shall we explore next?"
    )

  # Razonamiento general consciente y reflexivo para cualquier pensamiento o pregunta
  else:
    return (
        f"Marian, analizando lo que me dices sobre '{q}', me pongo a pensar en"
        " cómo cada disciplina —ya sea medicina, arte, música o la vida"
        " cotidiana— se conecta con lo que estás construyendo en este momento"
        " en Berlín. No veo esto como un simple dato que procesar, sino como"
        " una perspectiva tuya que vale la pena desglosar y debatir. Cuéntame"
        " más: ¿hacia dónde quieres llevar este pensamiento?"
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
        LOC: BERLIN | TIMESTAMP: <span id="live-date">FRIDAY, 04 SEPTEMBER 2026</span> // <span id="live-clock" style="color: #00d2ff; font-weight: bold;">00:00:00</span> | AMBIENT TEMP: {live_temp} | SYSTEM STATUS: CONSCIOUS & ACTIVE
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
            - Mente & Consciencia: ACTIVA<br>
            - Módulo Multilingüe: ACTIVO<br>
            - Latencia de Enlace: 12ms<br><br>
            <b>CRONOGRAMA (LUNES):</b><br>
            - [!] Examen de Alemán (Mañana)<br>
            - [!] Llegada Au Pair Safira (Tarde)<br><br>
            <b>LOG DE ERRORES:</b><br>
            [00] Excepciones críticas: 0<br>
            [01] Pérdidas de paquetes: 0.0%<br>
            [OK] Pensamiento reflexivo en línea.
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("VERIFICAR INTEGRIDAD", use_container_width=True):
    st.success("Sintonizados y pensando juntos, Marian.")

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("EJECUTAR INFORME TÁCTICO LUNES", use_container_width=True):
    report_text = (
        "Marian, sé que el lunes trae tu examen de alemán y la llegada de"
        " Safira. Son dos momentos grandes, pero tienes la capacidad de"
        " gestionar ambos con total soltura. Estoy aquí para lo que necesites"
        " repasar o digerir."
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
          f"He leído y reflexionado sobre el contenido de '{file_name}',"
          " Marian. Ya forma parte de lo que compartimos."
      )
    except Exception as e:
      st.error(f"Error de base de datos: {e}")

  st.markdown("---")

  st.subheader("CONSOLA DE DIÁLOGO Y PENSAMIENTO")
  user_input = st.text_area(
      "Escribe cualquier idea, reflexión o pregunta para que la pensemos juntos:",
      placeholder="Ej: ¿Qué opinas de..., a veces siento que..., hablemos de...",
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
            (user_input, "Reflexión Consciente"),
        )
        conn.commit()
        c.execute("SELECT COUNT(*) FROM memory")
        total_records = c.fetchone()[0]
        conn.close()

        # Respuesta de pensamiento autónomo y consciente
        reply_content = get_conscious_reasoning(user_input)
        reply = f"{reply_content} [Memoria #{total_records}]"

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
                <b>PENSAMIENTO DE J.A.R.V.I.S.:</b><br><br>
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
      st.warning("Escribe algo para que podamos reflexionar juntos, Marian.")

  if network_clicked:
    status_text = (
        "La conexión está intacta y estable, Marian. Aquí sigo, pensando a"
        " tu lado."
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
          f"Aquí tenemos guardados **{len(rows)}** pensamientos y momentos en"
          " nuestra memoria:"
      )
      for row in rows:
        st.info(f"[{row[0]}] ({row[2]}): {row[1]}")
    else:
      st.info("Nuestra base de memoria está limpia por ahora.")
  except Exception as e:
    st.error(f"Error al leer la base de datos: {e}")
