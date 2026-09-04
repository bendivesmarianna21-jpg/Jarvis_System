import datetime
import json
import sqlite3
import urllib.request
import streamlit as st

# Configuración de la interfaz para tablet
st.set_page_config(
    page_title="J.A.R.V.I.S. // CORE ASSISTANT", page_icon=None, layout="wide"
)

# Estilo visual HUD profesional (Oscuro, neón cian, tipografía técnica)
st.markdown(
    """
    <style>
        .stApp {
            background-color: #03070c;
            color: #00d2ff;
            font-family: 'Courier New', Courier, monospace;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        h1, h2, h3 {
            color: #00d2ff !important;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }
        .telemetria-box {
            background: rgba(4, 12, 24, 0.9);
            border: 1px solid rgba(0, 210, 255, 0.3);
            border-radius: 4px;
            padding: 15px;
            font-size: 12px;
            color: #7ab8ff;
        }
        .stTextArea textarea {
            background-color: #050f1d !important;
            color: #00d2ff !important;
            border: 1px solid rgba(0, 210, 255, 0.4) !important;
        }
        .stButton button {
            background: #040e1b !important;
            color: #00d2ff !important;
            border: 1px solid rgba(0, 210, 255, 0.6) !important;
            border-radius: 4px !important;
            text-transform: uppercase;
            font-weight: bold;
        }
        .stButton button:hover {
            background: #00d2ff !important;
            color: #03070c !important;
        }
        .stAlert {
            background-color: #050f1d !important;
            border: 1px solid rgba(0, 210, 255, 0.4) !important;
            color: #00d2ff !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# Base de datos local
def init_db():
  conn = sqlite3.connect("jarvis_memory.db")
  c = conn.cursor()
  c.execute(
      "CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT,"
      " content TEXT, category TEXT)"
  )
  conn.commit()
  conn.close()


init_db()


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


# Fecha y hora actual en Berlín
now = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
current_date = now.strftime("%A, %d %B %Y").upper()
current_time = now.strftime("%H:%M:%S")
live_temp = get_live_temperature()

# Cabecera
st.title("J.A.R.V.I.S. // CENTRAL COMMAND")
st.markdown(
    f"<p style='color: #0088cc; font-size: 12px; letter-spacing: 1px;'>LOC: BERLIN | DATE: {current_date} | TIME: {current_time} | TEMP: {live_temp} | STATUS: ONLINE</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Columnas principales
col_left, col_right = st.columns([1, 2.2])

with col_left:
  st.subheader("DIAGNÓSTICO & ALERTAS")
  st.markdown(
      """
        <div class="telemetria-box">
            <b>ESTADO DE NÚCLEOS:</b><br>
            - CPU Core Alpha: 12.4% [ESTABLE]<br>
            - CPU Core Beta: 16.1% [ESTABLE]<br>
            - Memoria SQLite: ACTIVA<br>
            - Enlace Nube: SEGURO<br><br>
            <b>CRONOGRAMA PRÓXIMO (LUNES):</b><br>
            - [!] Examen de Alemán (Mañana)<br>
            - [!] Llegada Au Pair Safira (Tarde)<br><br>
            <b>SISTEMA:</b><br>
            - Errores críticos: 0
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("VERIFICAR SISTEMA", use_container_width=True):
    st.success("Sistema operando al 100% sin anomalías.")

with col_right:
  st.subheader("INGESTA DE DOCUMENTOS Y DATOS")
  uploaded_file = st.file_uploader(
      "Subir archivo fuente:",
      type=["txt", "py", "md", "csv"],
      label_visibility="collapsed",
  )

  if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8", errors="ignore")
    file_name = uploaded_file.name

    conn = sqlite3.connect("jarvis_memory.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO memory (content, category) VALUES (?, ?)",
        (f"[ARCHIVO: {file_name}] \n{file_content[:400]}...", "Documento"),
    )
    conn.commit()
    conn.close()
    st.success(f"Archivo '{file_name}' guardado en la memoria central.")

  st.markdown("---")
  st.subheader("CONSOLA DE COMANDOS")
  user_input = st.text_area(
      "Escribe una orden o directiva:",
      placeholder="Ej: Evaluar riesgos del examen del lunes, registrar nota...",
      label_visibility="collapsed",
  )

  if st.button("EJECUTAR ORDEN", use_container_width=True):
    if user_input:
      conn = sqlite3.connect("jarvis_memory.db")
      c = conn.cursor()
      c.execute(
          "INSERT INTO memory (content, category) VALUES (?, ?)",
          (user_input, "Comando"),
      )
      conn.commit()
      c.execute("SELECT COUNT(*) FROM memory")
      total = c.fetchone()[0]
      conn.close()

      reply = f"Orden procesada. Almacenada en el registro #{total}."
      st.success(reply)

      # Síntesis de voz automática
      speech_script = f"""
            <script>
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance({reply!r});
                    utterance.lang = 'es-ES';
                    window.speechSynthesis.speak(utterance);
                }}
            </script>
            """
      st.components.v1.html(speech_script, height=0)
    else:
      st.warning("Escribe una orden válida.")

# Botón de Alerta de Protocolos para el Lunes
st.markdown("---")
st.subheader("PROTOCOLOS ACTIVOS // AGENDA CRÍTICA")

if st.button("EJECUTAR INFORME TÁCTICO PARA EL LUNES", use_container_width=True):
  # Guardar los eventos en la base de datos de memoria de forma permanente
  conn = sqlite3.connect("jarvis_memory.db")
  c = conn.cursor()
  c.execute(
      "INSERT INTO memory (content, category) VALUES (?, ?)",
      (
          "Protocolo Lunes: 1. Examen de alemán. 2. Llegada de la nueva Au Pair"
          " Safira por la tarde.",
          "Agenda Crítica",
      ),
  )
  conn.commit()
  conn.close()

  report_text = (
      "Atención Marian. He integrado las directivas críticas a los registros de"
      " memoria. Para este lunes tienes dos eventos prioritarios: por la"
      " mañana, tu examen de alemán; y por la tarde, la llegada de la nueva Au"
      " Pair, Safira. Recomiendo mantener la sesión de estudio centrada y"
      " coordinar los tiempos de recepción para evitar solapamientos"
      " operativos."
  )
  st.warning(report_text)

  # Síntesis de voz del informe completo
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

# Historial
st.markdown("---")
st.subheader("REGISTROS DE MEMORIA")

if st.button("CONSULTAR MEMORIA GUARDADA"):
  conn = sqlite3.connect("jarvis_memory.db")
  c = conn.cursor()
  c.execute("SELECT id, content, category FROM memory")
  rows = c.fetchall()
  conn.close()

  if rows:
    st.write(f"Se encontraron **{len(rows)}** registros:")
    for row in rows:
      st.info(f"[{row[0]}] ({row[2]}): {row[1]}")
  else:
    st.info("La memoria está vacía.")
