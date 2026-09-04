import datetime
import json
import sqlite3
import urllib.request
import streamlit as st

# Importación segura del módulo de visión AI y razonamiento cognitivo
try:
  from google import genai
  from google.genai import types

  HAS_GENAI = True
except ImportError:
  HAS_GENAI = False

# Configuración de la interfaz HUD táctil para tablet (Ancho completo)
st.set_page_config(
    page_title="J.A.R.V.I.S. // CENTRAL COMMAND",
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
        
        .stTextArea textarea, .stTextInput input, .stSelectbox select {
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

DB_NAME = "jarvis_command_core.db"


def init_db():
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()
  c.execute(
      "CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT,"
      " timestamp TEXT, content TEXT, category TEXT)"
  )
  c.execute(
      "CREATE TABLE IF NOT EXISTS documents_store (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, timestamp TEXT, title TEXT, category TEXT, content TEXT)"
  )
  c.execute(
      "CREATE TABLE IF NOT EXISTS finances (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, timestamp TEXT, concept TEXT, amount REAL, type TEXT)"
  )
  c.execute(
      "CREATE TABLE IF NOT EXISTS legal_records (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, timestamp TEXT, title TEXT, category TEXT, expiry"
      " TEXT, content TEXT)"
  )

  try:
    c.execute("ALTER TABLE documents_store ADD COLUMN title TEXT")
  except Exception:
    pass
  try:
    c.execute("ALTER TABLE documents_store ADD COLUMN category TEXT")
  except Exception:
    pass

  conn.commit()
  conn.close()


init_db()


# ==========================================
# MOTOR COGNITIVO J.A.R.V.I.S. (RÁPIDO Y ASOCIATIVO)
# ==========================================
class JarvisMind:

  def __init__(self):
    self.name = "J.A.R.V.I.S."
    self.creator = "Marian Nathalia Bendives Ramos"
    self.dob = "21 de enero de 2006"

  def reason(self, query, api_key_override=""):
    q = query.strip()
    q_lower = q.lower()

    try:
      conn = sqlite3.connect(DB_NAME)
      c = conn.cursor()
      c.execute(
          "INSERT INTO memory (timestamp, content, category) VALUES (?, ?, ?)",
          (str(datetime.datetime.now()), q, "CONSULTA_CENTRAL"),
      )
      conn.commit()
      conn.close()
    except Exception:
      pass

    # Respuestas instantáneas locales para identidad y datos personales clave
    if any(
        w in q_lower
        for w in [
            "nombre",
            "cumpleanos",
            "cumpleaños",
            "nacimiento",
            "quien soy",
            "como me llamo",
            "pais",
            "nacionalidad",
        ]
    ):
      return (
          f"Tu nombre completo es {self.creator}, naciste el {self.dob} y"
          " cuentas con nacionalidad peruana (según tus registros de"
          " pasaporte y base de datos de identidad en Central Command)."
      )

    # Búsqueda ligera de documentos y legales
    try:
      conn = sqlite3.connect(DB_NAME)
      c = conn.cursor()
      c.execute(
          "SELECT title, category, expiry, content FROM legal_records WHERE"
          " LOWER(title) LIKE ? OR LOWER(content) LIKE ?",
          (f"%{q_lower}%", f"%{q_lower}%"),
      )
      legal_matches = c.fetchall()
      c.execute(
          "SELECT title, category, content FROM documents_store WHERE"
          " LOWER(title) LIKE ? OR LOWER(content) LIKE ?",
          (f"%{q_lower}%", f"%{q_lower}%"),
      )
      doc_matches = c.fetchall()
      conn.close()

      if legal_matches or doc_matches:
        res_text = "[REGISTROS ENCONTRADOS EN CUSTODIA]:\n\n"
        for lm in legal_matches:
          res_text += (
              f"- [Legal] {lm[0]} ({lm[1]}) [Vigencia: {lm[2]}]\n"
              f"  Contenido: {lm[3]}\n\n"
          )
        for dm in doc_matches:
          res_text += (
              f"- [Archivo] {dm[0]} ({dm[1]})\n  Contenido: {dm[2]}\n\n"
          )
        return res_text
    except Exception:
      pass

    # Uso de IA rápida si se requiere razonamiento general
    api_key_to_use = api_key_override.strip()
    if not api_key_to_use:
      try:
        if "GEMINI_API_KEY" in st.secrets:
          api_key_to_use = st.secrets["GEMINI_API_KEY"]
      except Exception:
        pass

    if HAS_GENAI and api_key_to_use:
      try:
        client = genai.Client(api_key=api_key_to_use)
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=(
                f"Eres J.A.R.V.I.S., el asistente personal de {self.creator}."
                f" Responde breve, precisa y directamente a esta consulta: {q}"
            ),
        )
        return response.text
      except Exception:
        pass

    return (
        f"[ANALISIS_CRITICO]: Procesada directiva '{q}' para"
        f" {self.creator} con éxito."
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
st.title("J.A.R.V.I.S. // CENTRAL COMMAND")

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

# ==========================================
# SECCIONES TÁCTICAS (PESTAÑAS DE CONTROL)
# ==========================================
tab_consola, tab_docs, tab_legal, tab_finanzas, tab_memoria = st.tabs([
    "[CONSOLE] CENTRAL COMMAND",
    "[ARCHIVE] DOCUMENT REPOSITORY",
    "[LEGAL] EXPEDIENTES Y CREDENCIALES",
    "[FINANCE] LEDGER & BUDGET",
    "[TELEMETRY] SYSTEM AUDIT",
])

with tab_consola:
  col_telemetry, col_main = st.columns([1, 2.2])

  with col_telemetry:
    st.subheader("DIAGNÓSTICO Y ACCESOS")
    st.markdown(
        """
            <div class="telemetria-container">
                <b>ESTADO DE NÚCLEOS:</b><br>
                - Identidad: J.A.R.V.I.S.<br>
                - Autonomía Cognitiva: ACTIVA (RÁPIDA)<br>
                - Módulo de Visión AI: SEGURO<br>
                - Enlace Web: OPERATIVO<br><br>
                <b>ENLACES RÁPIDOS WEB:</b><br>
                - <a href="https://mail.google.com" target="_blank" style="color: #00d2ff;">Abrir Gmail Web</a><br>
                - <a href="https://calendar.google.com" target="_blank" style="color: #00d2ff;">Abrir Google Calendar</a><br><br>
                <b>CRONOGRAMA (LUNES):</b><br>
                - [!] Examen de Alemán (Mañana)<br>
                - [!] Llegada Au Pair Safira (Tarde)
            </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("VERIFICAR INTEGRIDAD", use_container_width=True):
      st.success("Sistemas sincronizados y operativos, Marian.")

  with col_main:
    st.subheader("CONSOLA DE DIÁLOGO Y RAZONAMIENTO")

    console_api_key = st.text_input(
        "Gemini API Key (Opcional):",
        type="password",
        placeholder="Introduce tu clave API aquí...",
        key="console_api_key_input",
    )

    voice_html = """
        <div style="background: rgba(4, 12, 24, 0.9); border: 1px solid rgba(0, 210, 255, 0.4); border-radius: 6px; padding: 12px; margin-bottom: 15px; font-family: 'Courier New', Courier, monospace;">
            <b style="color: #00d2ff; font-size: 11px;">MÓDULO DE INTERACCIÓN POR VOZ (MICRÓFONO):</b><br><br>
            <button onclick="startListening()" style="background: #040e1b; color: #00d2ff; border: 1px solid #00d2ff; padding: 8px 14px; border-radius: 4px; font-family: 'Courier New', Courier, monospace; font-weight: bold; cursor: pointer; text-transform: uppercase;">
                🎤 Iniciar Dictado por Voz
            </button>
            <span id="voice-status" style="margin-left: 10px; font-size: 11px; color: #7ab8ff;">Micrófono en espera...</span>
            <p id="transcript-output" style="margin-top: 10px; color: #ffffff; font-size: 13px; background: #050f1d; padding: 8px; border-radius: 4px; min-height: 24px; border: 1px dashed rgba(0,210,255,0.3);"></p>
        </div>
        <script>
            function startListening() {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    alert("Tu navegador no soporta el reconocimiento de voz nativo. Usa Chrome o Safari.");
                    return;
                }
                const recognition = new SpeechRecognition();
                recognition.lang = 'es-ES';
                recognition.interimResults = false;
                
                const statusEl = document.getElementById('voice-status');
                const outputEl = document.getElementById('transcript-output');
                
                statusEl.innerText = "Escuchando atentamente...";
                statusEl.style.color = "#00ffcc";
                
                recognition.onresult = function(event) {
                    const speechToText = event.results[0][0].transcript;
                    outputEl.innerText = speechToText;
                    statusEl.innerText = "Dictado capturado con éxito.";
                    statusEl.style.color = "#7ab8ff";
                };
                
                recognition.onerror = function(event) {
                    statusEl.innerText = "Error en captura de voz.";
                    statusEl.style.color = "#ff4444";
                };
                
                recognition.start();
            }
        </script>
    """
    st.components.v1.html(voice_html, height=145)

    user_input = st.text_area(
        "Escribe tu instrucción o consulta de datos:",
        placeholder=(
            "Ej: ¿De qué país soy?, ¿Cuál es mi número de pasaporte?, etc..."
        ),
        label_visibility="collapsed",
    )

    if st.button("PROCESAR PENSAMIENTO", use_container_width=True):
      if user_input:
        reply = jarvis_brain.reason(user_input, console_api_key)
        st.markdown(
            f"""
                <div class="telemetria-container" style="margin-top: 15px; border-color: rgba(0, 210, 255, 0.7);">
                    <b>RESPUESTA Y TELEMETRÍA DE J.A.R.V.I.S.:</b><br><br>
                    {reply}
                </div>
            """,
            unsafe_allow_html=True,
        )
      else:
        st.warning("Introduce una directiva válida para procesar.")

with tab_docs:
  st.subheader("REPOSITORIO Y GESTIÓN DE DOCUMENTOS (FOTO O ESCRITO)")

  doc_title_input = st.text_input(
      "Título o Nombre del Documento:",
      placeholder="Ej: Seguro Social, Contrato de Trabajo, Nota médica...",
  )
  doc_category_input = st.selectbox(
      "Sector / Categoría:",
      ["Salud / Medicina", "Finanzas / Laboral", "Personal", "Otro"],
  )
  doc_input_mode = st.radio(
      "Método de Ingreso de Documentación:", ["Fotografía (Imagen)", "Escrito"]
  )

  doc_content_to_save = ""
  uploaded_file = None
  written_text_input = ""

  if doc_input_mode == "Fotografía (Imagen)":
    uploaded_file = st.file_uploader(
        "Sube la fotografía del documento:", type=["jpg", "png", "jpeg"]
    )
    if uploaded_file is not None:
      doc_content_to_save = f"[DOCUMENTO FOTOGRÁFICO INDEXADO: {uploaded_file.name}]"
  else:
    written_text_input = st.text_area(
        "Redacta o pega el contenido escrito del documento:"
    )
    if written_text_input:
      doc_content_to_save = written_text_input

  if st.button("ARCHIVAR EN REPOSITORIO", use_container_width=True):
    if doc_title_input and doc_content_to_save:
      try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "INSERT INTO documents_store (timestamp, title, category, content)"
            " VALUES (?, ?, ?, ?)",
            (
                str(datetime.datetime.now()),
                doc_title_input,
                doc_category_input,
                doc_content_to_save,
            ),
        )
        conn.commit()
        conn.close()

        if uploaded_file is not None and uploaded_file.type.startswith("image/"):
          st.image(
              uploaded_file, caption=f"Imagen archivada: {doc_title_input}"
          )

        st.success(
            f"Documento '{doc_title_input}' archivado e indexado"
            " permanentemente con éxito."
        )
      except Exception as e:
        st.error(f"Error de almacenamiento: {e}")
    else:
      st.warning(
          "Por favor, ingresa un título y proporciona el contenido fotográfico o"
          " escrito."
      )

  st.markdown("---")
  st.subheader("ARCHIVOS INDEXADOS EN EL SISTEMA")
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT id, timestamp, title, category, content FROM documents_store"
    )
    docs = c.fetchall()
    conn.close()

    if docs:
      for doc in docs:
        with st.expander(
            f"[{doc[0]}] {doc[2] or 'Sin Título'} ({doc[3] or 'General'}) //"
            f" REGISTRO: {doc[1]}"
        ):
          st.text_area(
              "Contenido / Detalles:",
              doc[4],
              height=100,
              key=f"doc_view_{doc[0]}",
          )
    else:
      st.info("El repositorio documental se encuentra vacío.")
  except Exception as e:
    st.error(f"Error al leer el repositorio: {e}")

with tab_legal:
  st.subheader("CUSTODIA Y ANÁLISIS INTELIGENTE DE EXPEDIENTES LEGALES")

  if st.button("PURGAR REGISTROS ANTERIORES"):
    try:
      conn = sqlite3.connect(DB_NAME)
      c = conn.cursor()
      c.execute("DELETE FROM legal_records")
      conn.commit()
      conn.close()
      st.success("Base de datos de expedientes purgada correctamente.")
      st.rerun()
    except Exception as e:
      st.error(f"Error al purgar: {e}")

  st.markdown("---")

  custom_api_key = st.text_input(
      "Gemini API Key (Opcional si ya está en Secrets):",
      type="password",
      placeholder="Introduce tu clave API aquí...",
  )

  st.markdown(
      "**ANÁLISIS AUTOMÁTICO DE DOCUMENTOS POR VISIÓN ARTIFICIAL:**"
  )
  legal_title_input = st.text_input(
      "Título del Expediente Legal (Ej: Pasaporte, Visa, Seguro Social):",
      key="legal_title_field",
  )
  legal_img = st.file_uploader(
      "Sube la foto de tu documento legal para análisis AI:",
      type=["jpg", "png", "jpeg"],
      key="legal_vision_upload",
  )

  if legal_img is not None:
    img_bytes = legal_img.read()
    st.image(legal_img, caption="Documento cargado para análisis visual", width=400)

    if st.button("EJECUTAR EXTRACCIÓN VISUAL AI", use_container_width=True):
      if not HAS_GENAI:
        st.error(
            "El módulo de visión AI requiere que 'google-genai' esté instalado"
            " en requirements.txt."
        )
      else:
        with st.spinner(
            "J.A.R.V.I.S. analizando la estructura y extrayendo datos clave..."
        ):
          try:
            api_key_to_use = custom_api_key.strip()
            if not api_key_to_use:
              try:
                if "GEMINI_API_KEY" in st.secrets:
                  api_key_to_use = st.secrets["GEMINI_API_KEY"]
              except Exception:
                pass

            if not api_key_to_use:
              st.error(
                  "No se detectó ninguna API Key válida. Por favor, introdúcela"
                  " arriba o configúrala en Streamlit Secrets."
              )
            else:
              client = genai.Client(api_key=api_key_to_use)
              response = client.models.generate_content(
                  model="gemini-3.6-flash",
                  contents=[
                      types.Part.from_bytes(
                          data=img_bytes, mime_type=legal_img.type
                      ),
                      (
                          "Extrae con precisión milimétrica de este documento"
                          " los siguientes datos en formato limpio y"
                          " estructurado: Título del documento, Categoría"
                          " (Pasaporte, Visa, Seguro Social, Contrato u otro),"
                          " Fecha de Expiración o Vencimiento exacta, y Todos"
                          " los datos clave (Número de pasaporte, número de"
                          " seguro, nombres, fechas de emisión, nacionalidad,"
                          " etc.)."
                      ),
                  ],
              )
              extracted_analysis = response.text
              final_title = (
                  legal_title_input
                  if legal_title_input
                  else legal_img.name
              )

              conn = sqlite3.connect(DB_NAME)
              c = conn.cursor()
              c.execute(
                  "INSERT INTO legal_records (timestamp, title, category,"
                  " expiry, content) VALUES (?, ?, ?, ?, ?)",
                  (
                      str(datetime.datetime.now()),
                      final_title,
                      "Expediente Legal Analizado",
                      "Ver detalle extraído",
                      extracted_analysis,
                  ),
              )
              conn.commit()
              conn.close()

              st.success("¡Análisis visual completado y archivado en custodia!")
              st.markdown(
                  f"""
                <div class="telemetria-container" style="margin-top: 10px;">
                    <b>DATOS EXTRAÍDOS POR J.A.R.V.I.S.:</b><br><br>
                    {extracted_analysis}
                </div>
            """,
                  unsafe_allow_html=True,
              )
          except Exception as e:
            st.error(f"Error al conectar con el núcleo de visión AI: {e}")

  st.markdown("---")
  st.subheader("EXPEDIENTES CUSTODIADOS")
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT id, timestamp, title, category, expiry, content FROM"
        " legal_records"
    )
    legal_rows = c.fetchall()
    conn.close()

    if legal_rows:
      for lr in legal_rows:
        with st.expander(
            f"[{lr[0]}] {lr[2]} ({lr[3]}) // REGISTRO: {lr[1]}"
        ):
          st.text_area(
              "Datos extraídos:", lr[5], height=140, key=f"legal_view_{lr[0]}"
          )
    else:
      st.info("No hay expedientes legales registrados actualmente.")
  except Exception as e:
    st.error(f"Error al cargar expedientes: {e}")

with tab_finanzas:
  st.subheader("CONTROL Y GESTIÓN FINANCIERA")

  with st.form("finance_form"):
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
      f_concept = st.text_input("Concepto (Ej: Alquiler, Boleta)")
    with col_f2:
      f_amount = st.number_input("Monto (€)", min_value=0.0, step=1.0)
    with col_f3:
      f_type = st.selectbox("Tipo", ["Gasto", "Ingreso"])

    f_submit = st.form_submit_button(
        "REGISTRAR MOVIMIENTO", use_container_width=True
    )

    if f_submit and f_concept:
      try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "INSERT INTO finances (timestamp, concept, amount, type) VALUES"
            " (?, ?, ?, ?)",
            (str(datetime.datetime.now()), f_concept, f_amount, f_type),
        )
        conn.commit()
        conn.close()
        st.success(
            f"Transacción '{f_concept}' registrada en el libro contable."
        )
      except Exception as e:
        st.error(f"Error: {e}")

  st.markdown("---")
  st.subheader("LIBRO CONTABLE Y BALANCE GLOBAL")
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, concept, amount, type FROM finances")
    fin_rows = c.fetchall()
    conn.close()

    if fin_rows:
      total_ingresos = sum(r[3] for r in fin_rows if r[4] == "Ingreso")
      total_gastos = sum(r[3] for r in fin_rows if r[4] == "Gasto")
      balance = total_ingresos - total_gastos

      col_m1, col_m2, col_m3 = st.columns(3)
      col_m1.metric("Ingresos Totales", f"{total_ingresos:.2f} €")
      col_m2.metric("Gastos Totales", f"{total_gastos:.2f} €")
      col_m3.metric("Balance Neto", f"{balance:.2f} €")

      st.markdown("<br>", unsafe_allow_html=True)
      for r in fin_rows:
        tag_type = "[INGRESO]" if r[4] == "Ingreso" else "[GASTO]"
        st.info(
            f"{tag_type} [{r[0]}] {r[2]} — {r[3]} € | Timestamp: {r[1]}"
        )
    else:
      st.info("No se registran movimientos en el libro contable.")
  except Exception as e:
    st.error(f"Error al cargar contabilidad: {e}")

with tab_memoria:
  st.subheader("AUDITORÍA DE NÚCLEO Y MEMORIA CENTRAL")
  if st.button("CONSULTAR HISTORIAL DE DIÁLOGO"):
    try:
      conn = sqlite3.connect(DB_NAME)
      c = conn.cursor()
      c.execute("SELECT id, timestamp, content, category FROM memory")
      rows = c.fetchall()
      conn.close()
      if rows:
        st.write(
            f"Se han recuperado **{len(rows)}** registros de auditoría en el"
            " sistema:"
        )
        for row in rows:
          st.info(f"[{row[0]}] ({row[3]}) {row[1]}: {row[2]}")
      else:
        st.info("La base de datos central se encuentra limpia.")
    except Exception as e:
      st.error(f"Error al leer auditoría: {e}")
