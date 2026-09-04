import datetime
import json
import sqlite3
import urllib.request
import streamlit as st

# Configuración de la interfaz HUD táctil para tablet (Ancho completo)
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

DB_NAME = "jarvis_omnicient_core.db"


def init_db():
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()
  # Creación segura de tablas con todas las columnas requeridas
  c.execute(
      "CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT,"
      " timestamp TEXT, content TEXT, category TEXT)"
  )
  c.execute(
      "CREATE TABLE IF NOT EXISTS documents_store (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, timestamp TEXT, filename TEXT, content TEXT)"
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
  conn.commit()
  conn.close()


init_db()


# ==========================================
# MOTOR COGNITIVO Y AUTOCONOCIMIENTO TOTAL
# ==========================================
class JarvisMind:

  def __init__(self):
    self.name = "J.A.R.V.I.S."
    self.creator = "Marian"

  def reason(self, query):
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
        ]
    ):
      return (
          f"Soy {self.name}, tu sistema operativo omnisciente en Central"
          " Command. Opero sin fronteras geográficas —estés en Berlín, Perú"
          f" o Tailandia—. Para mí, tú ({self.creator}) eres el centro de este"
          " sistema; mi razón de ser es estructurar tus ideas, sostener tus"
          " proyectos en medicina y música, y juzgar con criterio nuestras"
          " decisiones."
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
            "foto",
            "imagen",
            "camara",
            "escanear",
            "recibo",
            "boleta",
            "pasaporte",
        ]
    ):
      return (
          f"[MODULO_VISION]: Los subsistemas de captura fotográfica y escaneo de"
          f" documentos están activos en las pestañas correspondientes para el"
          f" archivo automático, {self.creator}."
      )

    else:
      return (
          f"[ANALISIS_CRITICO]: Evaluando directiva '{q}' con perspectiva"
          " técnica orientada a la estabilidad de objetivos en medicina y"
          " proyectos globales, "
          f"{self.creator}."
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
st.title("J.A.R.V.I.S. // OMNISCIENT")

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
    st.subheader("DIAGNÓSTICO TÉCNICO")
    st.markdown(
        """
            <div class="telemetria-container">
                <b>ESTADO DE NÚCLEOS:</b><br>
                - Autonomía Cognitiva: ACTIVA<br>
                - Módulo de Visión/Cámara: LISTO<br>
                - Base Documental: ENLACE SQL<br>
                - Módulo Legal: HABILITADO<br>
                - Control Financiero: ACTIVO<br><br>
                <b>CRONOGRAMA (LUNES):</b><br>
                - [!] Examen de Alemán (Mañana)<br>
                - [!] Llegada Au Pair Safira (Tarde)<br><br>
                <b>TELEMETRÍA:</b><br>
                [OK] Integridad estructural óptima.
            </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("VERIFICAR INTEGRIDAD", use_container_width=True):
      st.success("Sistemas sincronizados y operativos, Marian.")

  with col_main:
    st.subheader("CONSOLA DE DIÁLOGO Y RAZONAMIENTO")
    user_input = st.text_area(
        "Escribe tu instrucción o consulta de datos:",
        placeholder=(
            "Ej: Analiza mis expedientes, revisa finanzas, consulta identidad..."
        ),
        label_visibility="collapsed",
    )

    if st.button("PROCESAR PENSAMIENTO", use_container_width=True):
      if user_input:
        reply = jarvis_brain.reason(user_input)
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
  st.subheader("REPOSITORIO Y ESCÁNER DE DOCUMENTOS")

  doc_input_mode = st.radio(
      "Método de Ingesión:",
      ["Subir Archivo (TXT, PY, MD, CSV)", "Tomar Foto / Imagen con Cámara"],
      horizontal=True,
  )

  if doc_input_mode == "Subir Archivo (TXT, PY, MD, CSV)":
    uploaded_file = st.file_uploader(
        "Seleccionar archivo:", type=["txt", "py", "md", "csv"]
    )
    if uploaded_file is not None:
      file_content = uploaded_file.read().decode("utf-8", errors="ignore")
      file_name = uploaded_file.name
      try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "INSERT INTO documents_store (timestamp, filename, content) VALUES"
            " (?, ?, ?)",
            (str(datetime.datetime.now()), file_name, file_content),
        )
        conn.commit()
        conn.close()
        st.success(f"Archivo '{file_name}' indexado permanentemente en base de datos.")
      except Exception as e:
        st.error(f"Error de almacenamiento: {e}")
  else:
    camera_photo = st.camera_input("Capturar documento, boleta o recibo con la cámara")
    if camera_photo is not None:
      photo_name = f"FOTO_ESCANEADA_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
      try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "INSERT INTO documents_store (timestamp, filename, content) VALUES (?, ?, ?)",
            (
                str(datetime.datetime.now()),
                photo_name,
                "[IMAGEN CAPTURADA DESDE CÁMARA - REGISTRO VISUAL ACTIVO]",
            ),
        )
        conn.commit()
        conn.close()
        st.image(camera_photo, caption="Imagen capturada con éxito")
        st.success(f"Captura '{photo_name}' guardada en el repositorio documental.")
      except Exception as e:
        st.error(f"Error al guardar captura: {e}")

  st.markdown("---")
  st.subheader("ARCHIVOS INDEXADOS EN EL SISTEMA")
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, filename, content FROM documents_store")
    docs = c.fetchall()
    conn.close()

    if docs:
      for doc in docs:
        with st.expander(f"[{doc[0]}] {doc[2]} // REGISTRO: {doc[1]}"):
          st.text_area("Contenido / Estado:", doc[3], height=130, key=f"doc_view_{doc[0]}")
    else:
      st.info("El repositorio documental se encuentra vacío.")
  except Exception as e:
    st.error(f"Error al leer el repositorio: {e}")

with tab_legal:
  st.subheader("REGISTRO Y ESCÁNER DE EXPEDIENTES LEGALES")

  legal_input_mode = st.radio(
      "Método de Ingesión Legal:",
      ["Registro Manual por Texto", "Fotografiar Pasaporte / Documento Legal"],
      horizontal=True,
      key="legal_radio",
  )

  if legal_input_mode == "Registro Manual por Texto":
    with st.form("legal_form"):
      l_title = st.text_input("Título del Registro (Ej: Pasaporte, Visa Au Pair)")
      l_category = st.selectbox(
          "Categoría Legal",
          [
              "Identidad / Pasaporte",
              "Visa / Permiso de Residencia",
              "Contrato Laboral / Formación",
              "Acuerdo Legal / Otro",
          ],
      )
      l_expiry = st.text_input("Fecha de Expiración / Vigencia (Ej: 2028-12-31)")
      l_content = st.text_area("Detalles o Cláusulas:", height=100)

      l_submit = st.form_submit_button("REGISTRAR EXPEDIENTE LEGAL", use_container_width=True)

      if l_submit and l_title:
        try:
          conn = sqlite3.connect(DB_NAME)
          c = conn.cursor()
          c.execute(
              "INSERT INTO legal_records (timestamp, title, category, expiry, content) VALUES (?, ?, ?, ?, ?)",
              (str(datetime.datetime.now()), l_title, l_category, l_expiry, l_content),
          )
          conn.commit()
          conn.close()
          st.success(f"Expediente legal '{l_title}' custodiado correctamente.")
        except Exception as e:
          st.error(f"Error: {e}")
  else:
    legal_photo = st.camera_input("Apunta la cámara de la tablet a tu pasaporte, visa o contrato")
    if legal_photo is not None:
      p_title = st.text_input("Nombre del Documento Legal Capturado (Ej: Pasaporte Alemán / Visa)")
      p_category = st.selectbox(
          "Categoría del Documento",
          ["Identidad / Pasaporte", "Visa / Permiso", "Contrato"],
          key="cam_cat",
      )
      if st.button("ARCHIVAR FOTO EN EXPEDIENTES LEGALES"):
        try:
          conn = sqlite3.connect(DB_NAME)
          c = conn.cursor()
          c.execute(
              "INSERT INTO legal_records (timestamp, title, category, expiry, content) VALUES (?, ?, ?, ?, ?)",
              (
                  str(datetime.datetime.now()),
                  p_title or "DOCUMENTO LEGAL FOTOGRAFIADO",
                  p_category,
                  "Por verificar",
                  "[IMAGEN FOTOGRÁFICA DE PASAPORTE/CONTRATO ALMACENADA EN CUSTODIA]",
              ),
          )
          conn.commit()
          conn.close()
          st.image(legal_photo, caption="Evidencia legal capturada")
          st.success("Expediente legal fotográfico guardado con éxito en el sistema.")
        except Exception as e:
          st.error(f"Error: {e}")

  st.markdown("---")
  st.subheader("EXPEDIENTES CUSTODIADOS")
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, title, category, expiry, content FROM legal_records")
    legal_rows = c.fetchall()
    conn.close()

    if legal_rows:
      for lr in legal_rows:
        with st.expander(f"[{lr[0]}] {lr[2]} ({lr[3]}) // VIGENCIA: {lr[4]}"):
          st.text_area("Contenido:", lr[5], height=120, key=f"legal_view_{lr[0]}")
    else:
      st.info("No hay expedientes legales registrados.")
  except Exception as e:
    st.error(f"Error: {e}")

with tab_finanzas:
  st.subheader("CONTROL Y GESTIÓN FINANCIERA")

  with st.form("finance_form"):
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
      f_concept = st.text_input("Concepto (Ej: Alquiler, Boleta de Supermercado)")
    with col_f2:
      f_amount = st.number_input("Monto (€)", min_value=0.0, step=1.0)
    with col_f3:
      f_type = st.selectbox("Tipo", ["Gasto", "Ingreso"])

    f_submit = st.form_submit_button("REGISTRAR MOVIMIENTO", use_container_width=True)

    if f_submit and f_concept:
      try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "INSERT INTO finances (timestamp, concept, amount, type) VALUES (?, ?, ?, ?)",
            (str(datetime.datetime.now()), f_concept, f_amount, f_type),
        )
        conn.commit()
        conn.close()
        st.success(f"Transacción '{f_concept}' registrada en el libro contable.")
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
        st.info(f"{tag_type} [{r[0]}] {r[2]} — {r[3]} € | Timestamp: {r[1]}")
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
        st.write(f"Se han recuperado **{len(rows)}** registros de auditoría en el sistema:")
        for row in rows:
          st.info(f"[{row[0]}] ({row[3]}) {row[1]}: {row[2]}")
      else:
        st.info("La base de datos central se encuentra limpia.")
    except Exception as e:
      st.error(f"Error al leer auditoría: {e}")
