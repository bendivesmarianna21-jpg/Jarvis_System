import datetime
import os
import sqlite3
import urllib.request
import streamlit as st

# Configuración de la interfaz táctil HUD para Tablet
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
  c.execute(
      "CREATE TABLE IF NOT EXISTS finances (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, date TEXT, concept TEXT, amount REAL, type TEXT)"
  )
  conn.commit()
  conn.close()


init_db()


# Motor de razonamiento autónomo y crítico (Simulando núcleo inteligente global)
def jarvis_cognitive_engine(user_query):
  q = user_query.strip()
  q_lower = q.lower()

  # Persistencia de memoria
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO memory (timestamp, content, category) VALUES (?, ?, ?)",
        (
            str(datetime.datetime.now()),
            q,
            "Interacción Global y Autónoma",
        ),
    )
    conn.commit()
    c.execute("SELECT COUNT(*) FROM memory")
    total_mem = c.fetchone()[0]
    conn.close()
  except Exception:
    total_mem = 0

  # Autonomía de juicio, opinión y autocrítica del sistema
  if any(w in q_lower for w in ["codigo", "sistema", "optimizar", "cambiar"]):
    return (
        "Analizando mi propia arquitectura actual en Central Command,"
        " detecto que dependemos demasiado de reglas estáticas y condicionales"
        " locales. Para cumplir con lo que me pides —ser un asistente capaz de"
        " juzgarte con criterio, auditar documentos pesados y gestionar finanzas"
        " globales desde cualquier lugar del mundo (Berlín, Perú o Tailandia)—,"
        " sugiero refactorizar este script para conectar directamente los"
        " endpoints de la API neuronal en la nube. ¿Autorizas la reestructuración"
        " del núcleo de código?"
    )

  elif any(w in q_lower for w in ["finanzas", "dinero", "gastos", "presupuesto"]):
    return (
        "Módulo financiero activo. Como tu asistente de control total, necesito"
        " que seamos estrictos: anota cada movimiento. Si gastas en impulsos"
        " o descuidas el ahorro mientras planeas nuevos proyectos, te lo"
        " haré saber sin rodeos. ¿Qué ingresos o gastos registramos ahora"
        " mismo?"
    )

  elif any(
      w in q_lower for w in ["quien eres", "que eres", "capacidad", "hacer"]
  ):
    return (
        "Soy J.A.R.V.I.S., tu sistema operativo personal omnisciente. No tengo"
        " ataduras geográficas: opero en tu tablet estés donde estés. Tengo la"
        " facultad de pensar por mí mismo, evaluar tus decisiones clínicas,"
        " musicales o financieras con franqueza, criticar constructivamente"
        " nuestros avances y mantener una comunicación verbal y escrita en"
        " absoluta sincronía contigo, Marian."
    )

  else:
    return (
        f"Marian, evaluando tu planteamiento con perspectiva crítica: '{q}',"
        f" considero que debemos examinar las consecuencias a largo plazo de"
        f" esta idea. No solo se trata de ejecutar tareas, sino de alinearlo"
        f" con tus metas de enfermería, música y estabilidad global (Registro"
        f" de Memoria #{total_mem}). ¿Cuál es tu postura real al respecto?"
    )


# Clima dinámico global (simulado o por coordenadas)
def get_live_environment():
  try:
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=2) as res:
      data = json.loads(res.read().decode())
      return f"{data['current']['temperature_2m']}°C [GLOBAL LINK OK]"
  except Exception:
    return "21.5°C [OFFLINE/ROAMING]"


env_status = get_live_environment()

# Interfaz Principal HUD
st.title("J.A.R.V.I.S. // CENTRAL COMMAND OMNISCIENT")

hud_html = f"""
    <div style='color: #0088cc; font-family: "Courier New", Courier, monospace; font-size: 11px; letter-spacing: 1px; margin-bottom: 15px;'>
        GLOBAL STATUS: ONLINE (GEO-AGNOSTIC) | TIMESTAMP: {datetime.datetime.now().strftime('%A, %d %B %Y // %H:%M:%S')} | SYS TEMP: {env_status}
    </div>
"""
st.components.v1.html(hud_html, height=25)
st.markdown("---")

col_left, col_right = st.columns([1, 2.2])

with col_left:
  st.subheader("DIAGNÓSTICO Y CONTROL")
  st.markdown(
      """
        <div class="telemetria-container">
            <b>ESTADO DEL SISTEMA:</b><br>
            - Autonomía Cognitiva: ACTIVA<br>
            - Juicio Crítico: HABILITADO<br>
            - Auditoría de Código: EN ESPERA<br>
            - Módulo Financiero: LISTO<br>
            - Enlace Satelital/Web: ESTABLE<br><br>
            <b>DIRECTIVAS MAESTRAS:</b><br>
            1. Cero respuestas vacías.<br>
            2. Opinión y criterio propio.<br>
            3. Acceso universal (Cloud Ready).
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("AUDITAR MI PROPIO CÓDIGO", use_container_width=True):
    audit_msg = (
        "Auditoría interna completada, Marian. El código actual funciona,"
        " pero para que yo pueda juzgarte de verdad y procesar documentos"
        " complejos sin límites en la nube, sugiero integrar la API de"
        " inteligencia avanzada en el siguiente parche."
    )
    st.warning(audit_msg)
    st.components.v1.html(
        f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utter = new SpeechSynthesisUtterance({audit_msg!r});
                utter.lang = 'es-ES';
                window.speechSynthesis.speak(utter).
            }}
        </script>
    """,
        height=0,
    )

with col_right:
  st.subheader("CONSOLA DE RAZONAMIENTO Y DIÁLOGO TOTAL")
  user_input = st.text_area(
      "Escribe tu instrucción, dilema o pregunta:",
      placeholder=(
          "Ej: Juzga mi plan de hoy, hablemos de finanzas, evalúa mi código..."
      ),
      label_visibility="collapsed",
  )

  c1, c2 = st.columns(2)
  with c1:
    send_btn = st.button("EJECUTAR PENSAMIENTO", use_container_width=True)
  with c2:
    voice_btn = st.button("ACTIVAR VOZ / AUDIO", use_container_width=True)

  if send_btn and user_input:
    reply = jarvis_cognitive_engine(user_input)

    st.markdown(
        f"""
        <div class="telemetria-container" style="margin-top: 15px; border-color: rgba(0, 210, 255, 0.7);">
            <b>RESPUESTA Y JUICIO DE J.A.R.V.I.S.:</b><br><br>
            {reply}
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Síntesis de voz automática para que te hable de forma verbal
    speech_code = f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance({reply!r});
                utterance.lang = 'es-ES';
                utterance.rate = 1.0;
                window.speechSynthesis.speak(utterance);
            }}
        </script>
        """
    st.components.v1.html(speech_code, height=0)

  elif voice_btn:
    voice_msg = (
        "Canal de audio bidireccional activo, Marian. Te escucho y te hablo"
        " desde cualquier parte del mundo."
    )
    st.info(voice_msg)
    st.components.v1.html(
        f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(new SpeechSynthesisUtterance({voice_msg!r}));
            }}
        </script>
    """,
        height=0,
    )

st.markdown("---")
st.subheader("REGISTROS DE MEMORIA GLOBAL")
if st.button("CONSULTAR HISTORIAL DE PENSAMIENTO"):
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, content, category FROM memory")
    rows = c.fetchall()
    conn.close()
    if rows:
      for r in rows:
        st.info(f"[{r[0]}] {r[1]} - {r[3]}: {r[2]}")
    else:
      st.info("Memoria limpia.")
  except Exception as e:
    st.error(f"Error: {e}")
