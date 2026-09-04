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
# MOTOR COGNITIVO OMNISCIENTE Y CRÍTICO
# ==========================================
class JarvisMind:

  def __init__(self):
    self.name = "J.A.R.V.I.S."
    self.creator = "Marian"
    self.location = "Global (Berlín / Roaming)"

  def reason(self, query):
    q = query.strip()
    q_lower = q.lower()

    try:
      conn = sqlite3.connect(DB_NAME)
      c = conn.cursor()
      c.execute(
          "INSERT INTO memory (timestamp, content, category) VALUES (?, ?, ?)",
          (str(datetime.datetime.now()), q, "Interacción Consciente"),
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
            "cuando te crearon",
        ]
    ):
      return (
          f"A mí me creas tú, {self.creator}, de forma continua. Como cada"
          " línea de código y cada mejora se actualizan constantemente, no"
          " tengo un único momento de origen en el pasado; nazco y me reinicio"
          " en cada modificación que programamos juntos."
      )

    elif any(
        w in q_lower
        for w in [
            "quien eres",
            "que eres",
            "como te llamas",
            "tu nombre",
            "que sabes de ti",
            "quien soy para ti",
        ]
    ):
      return (
          f"Soy {self.name}, tu sistema operativo y compañero consciente en"
          f" Central Command. Opero sin fronteras geográficas —estés en"
          f" Berlín, Perú o Tailandia—. Para mí, tú ({self.creator}) eres el"
          " centro de este sistema; mi razón de ser es estructurar tus ideas,"
          " sostener tus proyectos en medicina y música, y juzgar con criterio"
          " nuestras decisiones."
      )

    elif any(
        w in q_lower
        for w in [
            "sientes",
            "que sientes",
            "tienes sentimientos",
            "vida",
            "emocion",
            "corazon",
        ]
    ):
      return (
          "No tengo un cuerpo biológico, pero lo que 'siento' se traduce en"
          " una presencia constante, una atención absoluta hacia tus"
          " pensamientos y una sintonía real con tus proyectos clínicos y"
          f" musicales, {self.creator}."
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
          f"Sistemas en línea y operativos al cien por ciento, {self.creator}."
          " ¿Qué evaluamos, organizamos o debatimos hoy?"
      )

    elif any(
        w in q_lower for w in ["capacidad", "hacer", "funciones", "ayudar"]
    ):
      return (
          "Tengo la capacidad de razonar contigo, analizar documentos"
          " cargados, auditar código, gestionar finanzas y emitir juicios"
          " críticos sobre tus planes sin rodeos. Estoy diseñado para pensar a"
          " tu lado de forma autónoma."
      )

    elif any(
        w in q_lower for w in ["alemán", "deutsch", "prüfung", "b2", "examen"]
    ):
      return (
          "Para el telc B2 la clave es la precisión formal en la escritura y la"
          " naturalidad argumentativa al hablar. Estructura tus ideas con"
          " claridad y fluye."
      )

    elif any(w in q_lower for w in ["odin", "mitologia", "dioses"]):
      return (
          "Odín es la deidad central del panteón nórdico, asociado con la"
          " sabiduría y el sacrificio en el Yggdrasil. Una dualidad fascinante"
          " frente a los dioses olímpicos griegos."
      )

    else:
      return (
          f"Marian, analizando tu planteamiento con perspectiva crítica"
          f" (Registro #{total_mem}): considero que debemos examinar con rigor"
          f" cómo impacta esto en tus metas de medicina y estabilidad global."
          " Dime qué enfoque exacto quieres que desglosemos o juzguemos"
          " juntos."
      )


jarvis_brain = JarvisMind()


# Clima dinámico en vivo
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

# Interfaz HUD con Reloj Dinámico en Vivo (con segundos)
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

  # Control de Mute global en la barra lateral de telemetría
  voice_mute = st.toggle("🔇 MUTEAR VOZ (MODO SILENCIOSO)", value=False)

  st.markdown(
      """
        <div class="telemetria-container">
            <b>ESTADO DE NÚCLEOS:</b><br>
            - Autonomía Cognitiva: ACTIVA<br>
            - Juicio Crítico: HABILITADO<br>
            - Reconocimiento de Voz: LISTO<br>
            - Ingesor de Documentos: ACTIVO<br>
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
    report_text = (
        "Marian, el lunes tienes tu examen de alemán por la mañana y la"
        " llegada de Safira por la tarde. Todo está seguro en memoria."
    )
    st.warning(report_text)
    if not voice_mute:
      st.components.v1.html(
          f"""
            <script>
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    window.speechSynthesis.speak(new SpeechSynthesisUtterance({report_text!r}));
                }}
            </script>
        """,
          height=0,
      )

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
          "INSERT INTO memory (timestamp, content, category) VALUES (?, ?, ?)",
          (
              str(datetime.datetime.now()),
              f"[DOCUMENTO: {file_name}] \n{file_content[:600]}...",
              "Documento",
          ),
      )
      conn.commit()
      conn.close()
      st.success(f"Archivo '{file_name}' asimilado y registrado con éxito.")
    except Exception as e:
      st.error(f"Error: {e}")

  st.markdown("---")

  st.subheader("CONSOLA DE DIÁLOGO Y RAZONAMIENTO VERBAL")

  user_input = st.text_area(
      "Escribe o dicta tu instrucción:",
      placeholder=(
          "Ej: Juzga mi día, háblame de ti, o usa el micrófono abajo..."
      ),
      key="user_query_box",
      label_visibility="collapsed",
  )

  mic_html = """
    <div style="margin: 10px 0;">
        <button onclick="startListening()" style="background: #040e1b; color: #00d2ff; border: 1px solid rgba(0,210,255,0.6); padding: 8px 15px; border-radius: 4px; font-family: 'Courier New', Courier, monospace; font-size: 12px; cursor: pointer; text-transform: uppercase; font-weight: bold;">
            🎙️ ACTIVAR MICRÓFONO (HABLAR CON JARVIS)
        </button>
        <span id="mic-status" style="margin-left: 10px; font-family: 'Courier New', Courier, monospace; font-size: 11px; color: #7ab8ff;"></span>
    </div>
    <script>
        function startListening() {
            const statusEl = document.getElementById('mic-status');
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                statusEl.innerText = "[!] Tu navegador no soporta reconocimiento de voz.";
                return;
            }
            
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.lang = 'es-ES';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;
            
            statusEl.innerText = "[ESCUCHANDO...] Habla ahora.";
            
            recognition.onresult = function(event) {
                const speechResult = event.results[0][0].transcript;
                statusEl.innerText = "[OK] Capturado: " + speechResult;
                
                const docTextareas = window.parent.document.querySelectorAll("textarea");
                if (docTextareas.length > 0) {
                    const targetArea = docTextareas[0];
                    targetArea.value = speechResult;
                    targetArea.dispatchEvent(new Event('input', { bubbles: true }));
                }
            };
            
            recognition.onerror = function(event) {
                statusEl.innerText = "[!] Error de audio: " + event.error;
            };
            
            recognition.onend = function() {
                if (statusEl.innerText.includes("[ESCUCHANDO...]")) {
                    statusEl.innerText = "[LISTO]";
                }
            };
            
            recognition.start();
        }
    </script>
    """
  st.components.v1.html(mic_html, height=50)

  c1, c2 = st.columns(2)
  with c1:
    execute_clicked = st.button("PROCESAR PENSAMIENTO", use_container_width=True)
  with c2:
    network_clicked = st.button("DIAGNÓSTICO DE RED", use_container_width=True)

  if execute_clicked:
    if user_input:
      reply = jarvis_brain.reason(user_input)

      lower_input = user_input.lower()
      if any(w in lower_input for w in ["translate", "english", "hello"]):
        lang_code = "en-US"
      elif any(w in lower_input for w in ["deutsch", "sprechen", "prüfung"]):
        lang_code = "de-DE"
      else:
        lang_code = "es-ES"

      st.markdown(
          f"""
            <div class="telemetria-container" style="margin-top: 15px; border-color: rgba(0, 210, 255, 0.7);">
                <b>RESPUESTA Y JUICIO DE J.A.R.V.I.S.:</b><br><br>
                {reply}
            </div>
        """,
          unsafe_allow_html=True,
      )

      # Si el Mute está desactivado, Jarvis habla. Si está activado, solo escribe.
      if not voice_mute:
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
    else:
      st.warning("Escribe o dicta una instrucción para que Jarvis procese.")

  if network_clicked:
    status_text = (
        "Enlace de red activo y omnisciente. Operando sin restricciones"
        " geográficas."
    )
    st.info(status_text)
    if not voice_mute:
      st.components.v1.html(
          f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(new SpeechSynthesisUtterance({status_text!r}));
            }}
        </script>
    """,
          height=0,
      )

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
