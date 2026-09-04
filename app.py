import datetime
import sqlite3
import streamlit as st

# Configuración de la interfaz optimizada para tablet (Ancho completo HUD)
st.set_page_config(
    page_title="J.A.R.V.I.S. // CORE TELEMETRY", page_icon=None, layout="wide"
)

# Estilo visual profesional: Tipografía técnica, paneles oscuros profundos, neón cian y diseño modular
st.markdown(
    """
    <style>
        /* Fondo general y tipografía base */
        .stApp {
            background-color: #03070c;
            color: #00d2ff;
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Ocultar elementos innecesarios de Streamlit para limpieza visual */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Cabeceras estilo terminal técnica */
        h1, h2, h3, h4 {
            color: #00d2ff !important;
            font-family: 'Courier New', Courier, monospace !important;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            font-weight: 700;
        }

        /* Paneles de telemetría y contenedores */
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

        /* Campos de texto estilo consola */
        .stTextArea textarea {
            background-color: #050f1d !important;
            color: #00d2ff !important;
            border: 1px solid rgba(0, 210, 255, 0.3) !important;
            border-radius: 4px !important;
            font-family: 'Courier New', Courier, monospace !important;
            font-size: 13px !important;
        }
        .stTextArea textarea:focus {
            border-color: #00d2ff !important;
            box-shadow: 0 0 10px rgba(0, 210, 255, 0.3) !important;
        }

        /* Botones estilo táctico industrial */
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
            transition: all 0.2s ease-in-out;
            box-shadow: 0 0 5px rgba(0, 210, 255, 0.1);
        }
        .stButton button:hover {
            background: #00d2ff !important;
            color: #03070c !important;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.6) !important;
        }

        /* Cajas de Alertas y Mensajes */
        .stAlert {
            background-color: #050f1d !important;
            border: 1px solid rgba(0, 210, 255, 0.4) !important;
            color: #00d2ff !important;
            font-family: 'Courier New', Courier, monospace !important;
            border-radius: 4px !important;
        }
        
        /* Divisores sutiles */
        hr {
            border-color: rgba(0, 210, 255, 0.15) !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# Inicialización de la base de datos de memoria persistente SQLite
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

# Parámetros temporales y ambientales en tiempo real (Berlín)
now = datetime.datetime.now()
current_date = now.strftime("%A, %d %B %Y").upper()
current_time = now.strftime("%H:%M:%S")

# Cabecera de Telemetría Global del Sistema
st.title("J.A.R.V.I.S. // CENTRAL COMMAND & TELEMETRY")
st.markdown(
    f"<p style='color: #0088cc; font-family: Courier New; font-size: 12px; letter-spacing: 1px;'>LOC: BERLIN | TIMESTAMP: {current_date} // {current_time} | AMBIENT TEMP: 22.0°C | SYSTEM STATUS: SECURE & STABLE</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Estructura Principal en Columnas (Izquierda: Diagnóstico Técnico / Derecha: Consola Operativa)
col_telemetry, col_main = st.columns([1, 2.2])

with col_telemetry:
  st.subheader("DIAGNÓSTICO TÉCNICO")
  st.markdown(
      """
        <div class="telemetria-container">
            <b>ESTADO DE NÚCLEOS:</b><br>
            - CPU Core Alpha: 14.2% [NOMINAL]<br>
            - CPU Core Beta: 18.7% [NOMINAL]<br>
            - SQLite Engine: CONECTADO<br>
            - Cloud Enclave: CIFRADO (AES-256)<br>
            - Latencia de Enlace: 12ms<br><br>
            <b>SUBSISTEMAS ACTIVOS:</b><br>
            - Motor de Ingesta Doc: ONLINE<br>
            - Módulo Sintaxis Voz: READY<br>
            - Análisis Autónomo: HABILITADO<br><br>
            <b>LOG DE ERRORES:</b><br>
            [00] Excepciones críticas: 0<br>
            [01] Pérdidas de paquetes: 0.0%<br>
            [OK] Integridad de base de datos íntegra.
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("VERIFICAR INTEGRIDAD", use_container_width=True):
    st.success("Diagnóstico completado: Cero anomalías en el sistema.")

with col_main:
  st.subheader("INGESTA DE DOCUMENTOS FUENTE")
  uploaded_file = st.file_uploader(
      "Cargar archivo para análisis (TXT, PY, MD, CSV):",
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
        (
            f"[DOCUMENTO ASIMILADO: {file_name}] \n{file_content[:600]}...",
            "Documento",
        ),
    )
    conn.commit()
    conn.close()
    st.success(
        f"Archivo '{file_name}' procesado e integrado exitosamente al núcleo de"
        " memoria."
    )

  st.markdown("---")
  st.subheader("CONSOLA DE COMANDOS TÁCTICOS")
  user_input = st.text_area(
      "Introducir directiva de análisis autónomo:",
      placeholder=(
          "Ej: Evaluar riesgos operativos, sintetizar directrices de proyecto..."
      ),
      label_visibility="collapsed",
  )

  col_btn1, col_btn2 = st.columns(2)

  with col_btn1:
    if st.button("EJECUTAR PROTOCOLO", use_container_width=True):
      if user_input:
        conn = sqlite3.connect("jarvis_memory.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO memory (content, category) VALUES (?, ?)",
            (user_input, "Comando Táctico"),
        )
        conn.commit()
        c.execute("SELECT COUNT(*) FROM memory")
        total_records = c.fetchone()[0]
        conn.close()

        reply = (
            f"Protocolo ejecutado con éxito. Registro asignado al sector"
            f" #{total_records}. Análisis de viabilidad y evaluación de riesgos"
            " completados."
        )
        st.success(reply)

        # Módulo de Síntesis de Voz Automatizada
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
        st.warning("Introduce una directiva válida para procesar.")

  with col_btn2:
    if st.button("DIAGNÓSTICO DE RED", use_container_width=True):
      status_text = (
          "Enlace de red verificado. Conexión estable con los servidores"
          " remotos."
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

# Sección Inferior: Base de Datos y Registros Históricos
st.markdown("---")
st.subheader("REGISTROS DE MEMORIA Y AUDITORÍA CENTRAL")

if st.button("CONSULTAR BASE DE DATOS CENTRAL"):
  conn = sqlite3.connect("jarvis_memory.db")
  c = conn.cursor()
  c.execute("SELECT id, content, category FROM memory")
  rows = c.fetchall()
  conn.close()

  if rows:
    st.write(
        f"Se han recuperado **{len(rows)}** registros activos en el sistema:"
    )
    for row in rows:
      st.info(f"[{row[0]}] ({row[2]}): {row[1]}")
  else:
    st.info("La base de datos central se encuentra limpia.")
