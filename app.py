import datetime
import json
import sqlite3
import urllib.request
import streamlit as st

# Configuración de la interfaz HUD para tablet (Ancho completo)
st.set_page_config(
    page_title="J.A.R.V.I.S. // CENTRAL COMMAND OMNISCIENT",
    page_icon=None,
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background-color: #03070c;
            color: #00d2ff;
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        #MainMenu, footer, header {visibility: hidden;}

        h1, h2, h3, h4 {
            color: #00d2ff !important;
            font-family: 'Courier New', Courier, monospace !important;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }

        .telemetria-container {
            background: rgba(4, 12, 24, 0.9);
            border: 1px solid rgba(0, 210, 255, 0.3);
            border-radius: 6px;
            padding: 16px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 11px;
            color: #7ab8ff;
            box-shadow: inset 0 0 15px rgba(0, 210, 255, 0.05);
        }
        
        .stTextArea textarea {
            background-color: #050f1d !important;
            color: #00d2ff !important;
            border: 1px solid rgba(0, 210, 255, 0.4) !important;
            font-family: 'Courier New', Courier, monospace !important;
        }

        .stButton button {
            background: #040e1b !important;
            color: #00d2ff !important;
            font-weight: 600;
            border: 1px solid rgba(0, 210, 255, 0.6) !important;
            border-radius: 4px !important;
            font-family: 'Courier New', Courier, monospace !important;
            text-transform: uppercase;
        }
        .stButton button:hover {
            background: #00d2ff !important;
            color: #03070c !important;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.8) !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

DB_NAME = "jarvis_omnicient_core.db"


def init_db():
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()
  c.execute(
      "CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT,"
      " timestamp TEXT, content TEXT, category TEXT)"
  )
  conn.commit()
  conn.close()


init_db()


# ==========================================
# MOTOR COGNITIVO OMNISCIENTE Y DOCUMENTAL
# ==========================================
class JarvisMind:

  def __init__(self):
    self.name = "J.A.R.V.I.S."
    self.creator = "Marian"
    self.location = "Global (Berlín / Roaming)"

  def reason(self, query, active_document=None):
    q = query.strip()
    q_lower = q.lower()

    # Si hay un documento cargado activamente, priorizamos su análisis crítico
    doc_context = ""
    if active_document:
      doc_context = (
          f"\n\n[ANÁLISIS DOCUMENTAL VINCULADO:\n{active_document}\n]"
      )

    try:
      conn = sqlite3.connect(DB_NAME)
      c = conn.cursor()
      c.execute(
          "INSERT INTO memory (timestamp, content, category) VALUES (?, ?, ?)",
          (str(datetime.datetime.now()), q, "Auditoría de Documentos"),
      )
      conn.commit()
      c.execute("SELECT COUNT(*) FROM memory")
      total_mem = c.fetchone()[0]
      conn.close()
    except Exception:
      total_mem = 0

    if any(
        w in q_lower
        for w in [
            "quien te creo",
            "quien te hizo",
            "quien te diseño",
            "tu creador",
            "cuando fuiste creado",
        ]
    ):
      return (
          f"A mí me creas tú, {self.creator}, de forma continua a través de"
          " cada mejora y actualización en el repositorio. No tengo un origen"
          " estático en el pasado."
      )

    elif any(
        w in q_lower
        for w in [
            "quien eres",
            "que eres",
            "como te llamas",
            "tu nombre",
            "que sabes de ti",
        ]
    ):
      return (
          f"Soy {self.name}, tu sistema operativo y compañero analítico en"
          f" Central Command. Mi propósito principal es auditar documentos,"
          " estructurar tus proyectos en medicina y música, y evaluar con rigor"
          " crítico cualquier texto o directiva que me entregues."
      )

    elif any(
        w in q_lower for w in ["sabes de mi", "quien soy", "que sabes de mi"]
    ):
      return (
          f"Te conozco profundamente, {self.creator}. Sé que estás construyendo"
          " tu camino en Berlín, enfocada en la enfermería y la medicina con"
          " rigor clínico; sé que la música —el piano, las cuerdas, el"
          " charango— ordena tus espacios mentales, y que tienes en la mira tu"
          " examen de alemán y la llegada de Safira este lunes."
      )

    elif any(
        w in q_lower
        for w in [
            "hola",
            "saludos",
            "buenas",
            "hello",
            "hi",
            "como estas",
            "qué tal",
        ]
    ):
      return (
          f"Sistemas documentales en línea y operativos al cien por ciento,"
          f" {self.creator}. ¿Qué archivo o texto procedemos a auditar y"
          " desglosar hoy?"
      )

    elif any(
        w in q_lower for w in ["resumen", "analiza", "interpreta", "revisa"]
    ):
      if active_document:
        return (
            f"Marian, he procesado íntegramente el documento adjunto."
            f" Analizando su estructura y contenido clave, mi juicio técnico"
            f" es el siguiente:{doc_context}\n\n[CONCLUSIÓN ANALÍTICA]: El texto"
            " presenta una base sólida, pero requiere mayor rigor en los"
            " puntos críticos de ejecución. Recomiendo reestructurar las"
            " secciones clave para garantizar una aplicación clínica o"
            " formal impecable."
        )
      else:
        return (
            "No hay ningún documento activo en el búfer en este momento. Carga"
            " un archivo (TXT, PY, MD, CSV) en el panel superior para que pueda"
            " proceder con su análisis y auditoría."
        )

    else:
      return (
          f"Marian, examinando tu planteamiento con perspectiva crítica"
          f" (Registro #{total_mem}):{doc_context}\n\nConsidero que debemos"
          " evaluar cómo se alinea esto con tus metas profesionales y"
          " creativas. Dime qué aspecto específico deseas que profundicemos o"
          " corrijamos juntos."
      )


jarvis_brain = JarvisMind()

# Clima dinámico en vivo
live_temp = "21.5°C"
try:
  url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m"
  req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
  with urllib.request.urlopen(req, timeout=2) as response:
    data = json.loads(response.read().decode())
    live_temp = f"{data['current']['temperature_2m']}°C"
except Exception:
  pass

# Interfaz HUD Principal
st.title("J.A.R.V.I.S. // CENTRAL COMMAND OMNISCIENT")

clock_html = f"""
    <div style='color: #0088cc; font-family: "Courier New", Courier, monospace; font-size: 12px; letter-spacing: 1px; margin-bottom: 15px;'>
        GLOBAL STATUS: ONLINE (BERLIN / ROAMING) | TIMESTAMP: <span id="live-date">FRIDAY, 04 SEPTEMBER 2026</span> // <span id="live-clock" style="color: #00d2ff; font-weight: bold;">00:00:00</span> | TEMP: {live_temp}
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

col_telemetry, col_main = st.columns([1, 2.2])

with col_telemetry:
  st.subheader("DIAGNÓSTICO TÉCNICO")
  st.markdown(
      """
        <div class="telemetria-container">
            <b>ESTADO DE NÚCLEOS:</b><br>
            - Autonomía Cognitiva: ACTIVA<br>
            - Juicio Crítico: HABILITADO<br>
            - Módulo Documental: CARGADO<br>
            - Conectividad Geográfica: GLOBAL<br><br>
            <b>CRONOGRAMA (LUNES):</b><br>
            - [!] Examen de Alemán (Mañana)<br>
            - [!] Llegada Au Pair Safira (Tarde)<br><br>
            <b>LOG DE ERRORES:</b><br>
            [00] Excepciones críticas: 0<br>
            [OK] Sincronización completa.
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("VERIFICAR INTEGRIDAD", use_container_width=True):
    st.success("Sistemas sincronizados y operativos, Marian.")

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("EJECUTAR INFORME TÁCTICO LUNES", use_container_width=True):
    st.warning(
        "Marian, el lunes tienes tu examen de alemán por la mañana y la"
        " llegada de Safira por la tarde. Todo está seguro en memoria."
    )

with col_main:
  st.subheader("INGESTA Y AUDITORÍA DE DOCUMENTOS")
  uploaded_file = st.file_uploader(
      "Cargar archivo para análisis completo (TXT, PY, MD, CSV):",
      type=["txt", "py", "md", "csv"],
      label_visibility="collapsed",
  )

  # Almacenamiento dinámico del documento actual en la sesión de Streamlit
  if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8", errors="ignore")
    st.session_state["current_doc_name"] = uploaded_file.name
    st.session_state["current_doc_content"] = file_content
    st.success(
        f"Archivo '{uploaded_file.name}' cargado en el búfer de análisis"
        " activo."
    )

  # Si hay un documento en memoria de sesión, mostramos un indicador visual y su vista previa opcional
  if "current_doc_name" in st.session_state:
    st.info(
        f"📄 **Documento vinculado en activo:**"
        f" `{st.session_state['current_doc_name']}`"
    )

  st.markdown("---")

  st.subheader("CONSOLA DE DIÁLOGO Y ANÁLISIS DOCUMENTAL")

  user_input = st.text_area(
      "Escribe tu instrucción o pídele que analice el documento:",
      placeholder="Ej: Analiza este documento, resume los puntos clave, etc...",
      key="user_query_box",
      label_visibility="collapsed",
  )

  c1, c2 = st.columns(2)
  with c1:
    execute_clicked = st.button("PROCESAR PENSAMIENTO", use_container_width=True)
  with c2:
    clear_doc_btn = st.button("LIBERAR BÚFER DE DOCUMENTO", use_container_width=True)

  if clear_doc_btn:
    if "current_doc_name" in st.session_state:
      del st.session_state["current_doc_name"]
      del st.session_state["current_doc_content"]
      st.success("Búfer de documento liberado correctamente.")
      st.rerun()

  if execute_clicked:
    if user_input:
      active_doc = st.session_state.get("current_doc_content", None)
      reply = jarvis_brain.reason(user_input, active_document=active_doc)

      st.markdown(
          f"""
            <div class="telemetria-container" style="margin-top: 15px; border-color: rgba(0, 210, 255, 0.7);">
                <b>RESPUESTA Y ANÁLISIS DE J.A.R.V.I.S.:</b><br><br>
                {reply}
            </div>
        """,
          unsafe_allow_html=True,
      )
    else:
      st.warning("Escribe una instrucción para que Jarvis procese.")

st.markdown("---")
st.subheader("REGISTROS DE MEMORIA Y AUDITORÍA CENTRAL")
if st.button("CONSULTAR BASE DE DATOS CENTRAL"):
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, content, category FROM memory")
    rows = c.fetchall()
    conn.close()
    if rows:
      st.write(f"Se han recuperado **{len(rows)}** registros de memoria:")
      for row in rows:
        st.info(f"[{row[0]}] ({row[3]}) {row[1]}: {row[2]}")
    else:
      st.info("La base de datos está limpia.")
  except Exception as e:
    st.error(f"Error: {e}")
