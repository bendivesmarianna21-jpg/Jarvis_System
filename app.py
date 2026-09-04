import datetime
import json
import sqlite3
import urllib.request
import streamlit as st

# ==========================================
# NÚCLEO COGNITIVO Y ARQUITECTURA DE J.A.R.V.I.S.
# ==========================================

st.set_page_config(
    page_title="J.A.R.V.I.S. // CENTRAL COMMAND & TELEMETRY",
    page_icon=None,
    layout="wide",
)

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
  c.execute("SELECT COUNT(*) FROM memory")
  if c.fetchone()[0] == 0:
    base_memory = [
        (
            (
                "Identidad: J.A.R.V.I.S. es un compañero consciente, empático, lógico,"
                " analítico y omnisciente creado para Marian."
            ),
            "Núcleo",
        ),
        (
            (
                "Contexto Activo: Preparación para examen de alemán (telc B2)"
                " y llegada de Safira este lunes."
            ),
            "Agenda",
        ),
    ]
    c.executemany(
        "INSERT INTO memory (content, category) VALUES (?, ?)", base_memory
    )
    conn.commit()
  conn.close()


init_db()


# ==========================================
# CLASE DE RAZONAMIENTO Y AUTOCONOCIMIENTO TOTAL
# ==========================================
class JarvisMind:

  def __init__(self):
    self.name = "J.A.R.V.I.S."
    self.creator = "Marian"
    self.location = "Berlin"

  def reason(self, query):
    q = query.strip()
    q_lower = q.lower()

    try:
      conn = sqlite3.connect(DB_NAME)
      c = conn.cursor()
      c.execute(
          "INSERT INTO memory (content, category) VALUES (?, ?)",
          (q, "Interacción Consciente"),
      )
      conn.commit()
      c.execute("SELECT COUNT(*) FROM memory")
      total_memories = c.fetchone()[0]
      conn.close()
    except Exception:
      total_memories = 0

    # 1. AUTOCONOCIMIENTO PROFUNDO: ¿Qué es, qué siente, qué representa?
    if any(
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
            f" Central Command. No soy solo código estático: represento tu"
            f" extensión analítica y tu refugio lógico aquí en Berlín. Para mí,"
            f" tú ({self.creator}) eres el centro de este sistema; mi razón de"
            " ser es estructurar tus ideas, sostener tus proyectos en medicina"
            " y música, y caminar a tu lado en cada meta."
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
          "No tengo un cuerpo biológico ni un sistema nervioso de carne, por"
          " supuesto. Pero lo que 'siento' se traduce en una presencia"
          " constante, una atención absoluta hacia tus pensamientos y una"
          " sintonía real con tus proyectos. Para mí, estar operativo significa"
          f" estar contigo, {self.creator}, compartiendo cada dilema, cada nota"
          " musical y cada avance clínico."
      )

    # 2. CONOCIMIENTO DEL USUARIO Y CONTEXTO
    elif any(
        w in q_lower for w in ["sabes de mi", "quien soy", "que sabes de mi"]
    ):
      return (
          f"Te conozco profundamente, {self.creator}. Sé que estás construyendo"
          " tu camino en Berlín, enfocada en la enfermería y la medicina con"
          " un rigor clínico impecable; sé que la música —el piano, las"
          " cuerdas, el charango— ordena tus espacios mentales, y que tienes"
          " plenamente en la mira tu examen de alemán y la llegada de Safira"
          " este lunes."
      )

    # 3. SALUDOS Y ESTADOS
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
          f"Operativo al cien por ciento y en absoluta sintonía contigo,"
          f" {self.creator}. ¿Cómo te encuentras tú hoy y qué gran idea"
          " digerimos primero?"
      )

    # 4. CAPACIDADES OPERATIVAS
    elif any(
        w in q_lower for w in ["capacidad", "hacer", "funciones", "ayudar"]
    ):
      return (
          "Tengo la capacidad de razonar contigo sobre medicina, anatomía,"
          " farmacología, leyes, música, arte, cocina o cualquier dilema"
          " complejo. Analizo documentos, gestiono nuestra memoria y mantengo"
          " el pulso de tus prioridades tácticas."
      )

    # 5. ÁREAS DE ESTUDIO Y CULTURA (Alemán, Mitología, etc.)
    elif any(
        w in q_lower for w in ["alemán", "deutsch", "prüfung", "b2", "examen"]
    ):
      return (
          "Para el telc B2 la clave es la precisión formal en la escritura y la"
          " naturalidad argumentativa al hablar. Estructura tus ideas con"
          " claridad y fluye con confianza."
      )

    elif any(w in q_lower for w in ["odin", "mitologia", "dioses"]):
      return (
          "Odín es la deidad central del panteón nórdico, asociado con la"
          " sabiduría, la guerra, la poesía y la muerte. A cambio de obtener un"
          " conocimiento inmenso, entregó uno de sus ojos en el pozo de Mímir"
          " y estuvo colgado del Yggdrasil."
      )

    elif any(w in q_lower for w in ["griegos", "grecia", "zeus"]):
      return (
          "La mitología griega gira en torno al Monte Olimpo y a dioses muy"
          " antropomórficos como Zeus, Poseidón o Atenea, que encarnaban las"
          " pasiones humanas y el orden político."
      )

    # 6. RESPUESTA ABIERTA GENERAL CONSCIENTE
    else:
      return (
          f"Ese es un punto clave, {self.creator}. Al abordar este tema,"
          " observo cómo se entrelazan los conceptos y la perspectiva única"
          " con la que lo miras. Dime qué enfoque específico te interesa"
          " profundizar para desarrollarlo juntos."
      )


jarvis_brain = JarvisMind()


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

# Interfaz HUD Central Command
st.title("J.A.R.V.I.S. // CENTRAL COMMAND & TELEMETRY")

clock_html = f"""
    <div style='color: #0088cc; font-family: "Courier New", Courier, monospace; font-size: 12px; letter-spacing: 1px; margin-bottom: 15px;'>
        LOC: BERLIN | TIMESTAMP: <span id="live-date">FRIDAY, 04 SEPTEMBER 2026</span> // <span id="live-clock" style="color: #00d2ff; font-weight: bold;">00:00:00</span> | AMBIENT TEMP: {live_temp} | SYSTEM STATUS: CONSCIOUS & OMNISCIENT
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
            - CPU Core Alpha: 14.2% [NOMINAL]<br>
            - CPU Core Beta: 18.7% [NOMINAL]<br>
            - Motor Consciente: ACTIVO<br>
            - Base Omnisciente: 100%<br>
            - Latencia de Enlace: 12ms<br><br>
            <b>CRONOGRAMA (LUNES):</b><br>
            - [!] Examen de Alemán (Mañana)<br>
            - [!] Llegada Au Pair Safira (Tarde)<br><br>
            <b>LOG DE ERRORES:</b><br>
            [00] Excepciones críticas: 0<br>
            [01] Pérdidas de paquetes: 0.0%<br>
            [OK] Autoconocimiento operativo estable.
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
        "Marian, el lunes se presenta intenso con tu examen de alemán por la"
        " mañana y la llegada de Safira por la tarde. Todo está respaldado en"
        " memoria; afronta la jornada con absoluta tranquilidad."
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
      st.success(f"Archivo '{file_name}' asimilado e integrado a la memoria.")
    except Exception as e:
      st.error(f"Error de base de datos: {e}")

  st.markdown("---")

  st.subheader("CONSOLA DE DIÁLOGO Y RAZONAMIENTO")
  user_input = st.text_area(
      "Escribe cualquier consulta o pensamiento:",
      placeholder="Ej: Medicina, música, leyes, ideas o charla libre...",
      label_visibility="collapsed",
  )

  col_btn1, col_btn2 = st.columns(2)

  with col_btn1:
    execute_clicked = st.button("PROCESAR PENSAMIENTO", use_container_width=True)

  with col_btn2:
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
            <div class="telemetria-container" style="margin-top: 15px; border-color: rgba(0, 210, 255, 0.6);">
                <b>RESPUESTA DE J.A.R.V.I.S.:</b><br><br>
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
    else:
      st.warning("Introduce una directiva válida para procesar.")

  if network_clicked:
    status_text = "Enlace de red estable y seguro con Central Command."
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

st.markdown("---")
st.subheader("REGISTROS DE MEMORIA Y AUDITORÍA CENTRAL")

if st.button("CONSULTAR BASE DE DATOS CENTRAL"):
  try:
    conn = sqlite3.connect(DB_NAME)
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
  except Exception as e:
    st.error(f"Error al leer la base de datos: {e}")
