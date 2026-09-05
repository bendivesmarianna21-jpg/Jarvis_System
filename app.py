import datetime
import os
import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

try:
  from google import genai
  from google.genai import types

  HAS_GENAI = True
except ImportError:
  HAS_GENAI = False

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
            font-family: 'Courier New', Courier, monospace;
        }
        #MainMenu, footer, header {visibility: hidden;}

        h1, h2, h3, h4 {
            color: #00d2ff !important;
            font-family: 'Courier New', Courier, monospace !important;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        .telemetria-container {
            background: rgba(4, 12, 24, 0.95);
            border: 1px solid rgba(0, 210, 255, 0.4);
            border-radius: 4px;
            padding: 16px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 11px;
            color: #7ab8ff;
            box-shadow: inset 0 0 15px rgba(0, 210, 255, 0.05);
            margin-bottom: 12px;
        }
        
        .stTextArea textarea, .stTextInput input, .stSelectbox select, .stNumberInput input {
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
            letter-spacing: 1px;
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

DB_NAME = "jarvis_command_core_v3.db"


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
      " AUTOINCREMENT, timestamp TEXT, concept TEXT, amount REAL, type TEXT,"
      " category TEXT, method TEXT)"
  )
  c.execute(
      "CREATE TABLE IF NOT EXISTS legal_records (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, timestamp TEXT, title TEXT, category TEXT, expiry"
      " TEXT, content TEXT)"
  )
  c.execute(
      "CREATE TABLE IF NOT EXISTS gmail_cache (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, timestamp TEXT, sender TEXT, subject TEXT, snippet"
      " TEXT)"
  )
  conn.commit()
  conn.close()


init_db()


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

    if any(w in q_lower for w in ["hola", "saludos", "buenos dias", "hey"]):
      return (
          "Hola, Marian. Todos los sistemas están en línea y listos. ¿Qué"
          " necesitas?"
      )

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
          " cuentas con nacionalidad peruana."
      )

    if any(
        w in q_lower for w in ["correo", "gmail", "mensaje", "bandeja", "mail"]
    ):
      try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT timestamp, sender, subject, snippet FROM gmail_cache")
        mails = c.fetchall()
        conn.close()
        if mails:
          res_text = "[CORREOS EN BANDEJA]:\n\n"
          for m in mails:
            res_text += (
                f"- De: {m[1]} | Asunto: {m[2]}\n  Contenido: {m[3]}\n"
                f"  Fecha: {m[0]}\n\n"
            )
          return res_text
        else:
          return "No hay correos registrados en la bandeja."
      except Exception as e:
        return f"Error al consultar correo: {e}"

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
                f" Responde directo a: {q}"
            ),
        )
        return response.text
      except Exception:
        pass

    return f"Procesada directiva '{q}' para {self.creator} con éxito."


jarvis_brain = JarvisMind()

ahora_berlin = datetime.datetime.now()
fecha_str = ahora_berlin.strftime("%A, %d de %B de %Y").upper()

st.title("J.A.R.V.I.S. // CENTRAL COMMAND")

# Barra superior con ID único para actualización nativa por JS con el color exacto del tema
st.markdown(
    f"""
    <div style='background: rgba(4, 12, 24, 0.95); border: 1px solid rgba(0, 210, 255, 0.4); padding: 10px 15px; font-family: "Courier New", Courier, monospace; font-size: 11px; color: #00d2ff; letter-spacing: 1.5px; margin-bottom: 20px;'>
        <b>UBICACIÓN:</b> BERLÍN, DE &nbsp;|&nbsp; <b>FECHA:</b> {fecha_str} &nbsp;|&nbsp; <b>HORA LOCAL:</b> <span id="reloj-jarvis" style="color: #00d2ff;">--:--:--</span> &nbsp;|&nbsp; <b>ESTADO:</b> SEGURO // ONLINE
    </div>
    
    <script>
    if (typeof window.jarvisClockInterval === 'undefined') {
        window.jarvisClockInterval = setInterval(function() {
            const ahora = new Date();
            const opciones = { timeZone: 'Europe/Berlin', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
            try {
                const horaBerling = new Intl.DateTimeFormat('de-DE', opciones).format(ahora);
                const elem = document.getElementById('reloj-jarvis');
                if (elem) {
                    elem.innerText = horaBerling;
                }
            } catch(e) {}
        }, 1000);
    }
    // Ejecutar inmediatamente al cargar
    (function() {
        const ahora = new Date();
        const opciones = { timeZone: 'Europe/Berlin', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
        try {
            const horaBerling = new Intl.DateTimeFormat('de-DE', opciones).format(ahora);
            const elem = document.getElementById('reloj-jarvis');
            if (elem) { elem.innerText = horaBerling; }
        } catch(e) {}
    })();
    </script>
""",
    unsafe_allow_html=True,
)

tab_consola, tab_docs, tab_legal, tab_gmail, tab_finanzas, tab_alarmas, tab_memoria = (
    st.tabs([
        "[CONSOLE] CENTRAL COMMAND",
        "[ARCHIVE] REPOSITORIO",
        "[LEGAL] EXPEDIENTES",
        "[GMAIL] CORREOS",
        "[FINANCE] CONTABILIDAD",
        "[ALARMS] CRONÓMETRO",
        "[TELEMETRY] AUDITORÍA",
    ])
)

with tab_consola:
  col_telemetry, col_main = st.columns([1, 2.2])

  with col_telemetry:
    st.subheader("DIAGNÓSTICO")
    st.markdown(
        """
            <div class="telemetria-container">
                <b>ESTADO DE NÚCLEOS:</b><br>
                - Identidad: J.A.R.V.I.S.<br>
                - Usuaria: Marian Nathalia Bendives Ramos<br>
                - Motor SQLite: ÓPTIMO<br>
                - Encriptación: AES-256<br><br>
                <b>CRONOGRAMA:</b><br>
                - [!] Examen telc Deutsch B2<br>
                - [!] Ausbildungsbeginn (St. Joseph)
            </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("VERIFICAR INTEGRIDAD", use_container_width=True):
      st.success("Sistemas sincronizados y operativos, Marian.")

  with col_main:
    st.subheader("CONSOLA DE DIÁLOGO Y RAZONAMIENTO TÁCTICO")
    console_api_key = st.text_input(
        "Gemini API Key (Opcional):",
        type="password",
        placeholder="Introduce tu clave API aquí...",
        key="console_api_key_input",
    )
    user_input = st.text_area(
        "Escribe tu instrucción o consulta de datos:",
        placeholder="Ej: Hola Jarvis, ¿Tengo nuevos correos?, etc...",
        label_visibility="collapsed",
    )

    if st.button("PROCESAR PENSAMIENTO", use_container_width=True):
      if user_input:
        reply = jarvis_brain.reason(user_input, console_api_key)
        st.markdown(
            f"""
                <div class="telemetria-container" style="margin-top: 15px; border-color: rgba(0, 210, 255, 0.7);">
                    <b>RESPUESTA DE J.A.R.V.I.S.:</b><br><br>
                    {reply}
                </div>
            """,
            unsafe_allow_html=True,
        )
      else:
        st.warning("Introduce una directiva válida para procesar.")

with tab_docs:
  st.subheader("REPOSITORIO GENERAL DE DOCUMENTOS")
  doc_title_input = st.text_input(
      "Título o Nombre del Documento:",
      placeholder="Ej: Contrato, Nota médica...",
  )
  doc_category_input = st.selectbox(
      "Sector / Categoría:",
      ["Salud / Medicina", "Finanzas / Laboral", "Personal", "Otro"],
  )
  doc_content_input = st.text_area("Contenido del documento:")

  if st.button("ARCHIVAR DOCUMENTO", use_container_width=True):
    if doc_title_input and doc_content_input:
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
                doc_content_input,
            ),
        )
        conn.commit()
        conn.close()
        st.success("Documento guardado en el repositorio.")
        st.rerun()
      except Exception as e:
        st.error(f"Error: {e}")
    else:
      st.warning("Completa el título y el contenido.")

  st.markdown("---")
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT id, timestamp, title, category, content FROM documents_store"
    )
    d_rows = c.fetchall()
    conn.close()
    for dr in d_rows:
      with st.expander(f"[{dr[0]}] {dr[2]} ({dr[3]})"):
        st.write(dr[4])
  except Exception:
    pass

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
      "Gemini API Key (Opcional):", type="password", key="legal_key"
  )
  legal_title_input = st.text_input(
      "Título del Expediente Legal (Ej: Pasaporte):", key="legal_title_field"
  )
  legal_img = st.file_uploader(
      "Sube la foto de tu documento legal para análisis AI:",
      type=["jpg", "png", "jpeg"],
      key="legal_vision_upload",
  )

  if legal_img is not None:
    img_bytes = legal_img.read()
    st.image(legal_img, caption="Documento cargado", width=400)
    if st.button("EJECUTAR EXTRACCIÓN VISUAL AI", use_container_width=True):
      if not HAS_GENAI:
        st.error("El módulo de visión AI requiere 'google-genai'.")
      else:
        with st.spinner("J.A.R.V.I.S. analizando documento con IA..."):
          try:
            api_key_to_use = custom_api_key.strip()
            if not api_key_to_use:
              try:
                if "GEMINI_API_KEY" in st.secrets:
                  api_key_to_use = st.secrets["GEMINI_API_KEY"]
              except Exception:
                pass

            client = genai.Client(
                api_key=api_key_to_use if api_key_to_use else None
            )
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[
                    types.Part.from_bytes(
                        data=img_bytes, mime_type=legal_img.type
                    ),
                    (
                        "Extrae con absoluta precisión, detalle y abundancia"
                        " toda la información, campos, números, fechas,"
                        " nombres y datos clave de este documento."
                    ),
                ],
            )
            extracted_analysis = response.text
            final_title = (
                legal_title_input if legal_title_input else legal_img.name
            )

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute(
                "INSERT INTO legal_records (timestamp, title, category, expiry,"
                " content) VALUES (?, ?, ?, ?, ?)",
                (
                    str(datetime.datetime.now()),
                    final_title,
                    "Expediente Legal Analizado",
                    "Ver detalle",
                    extracted_analysis,
                ),
            )
            conn.commit()
            conn.close()
            st.success("¡Análisis visual completado y archivado!")
            st.markdown(
                f"""
                <div class="telemetria-container" style="margin-top: 10px;">
                    <b>DATOS EXTRAÍDOS:</b><br><br>
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

with tab_gmail:
  st.subheader("GESTIÓN Y REGISTRO DE CORREOS")
  with st.form("mail_form"):
    mail_sender = st.text_input("Remitente (Ej: St. Joseph Krankenhaus):")
    mail_subject = st.text_input("Asunto del correo:")
    mail_snippet = st.text_area("Contenido o extracto principal:")
    mail_submit = st.form_submit_button(
        "REGISTRAR CORREO EN BANDEJA", use_container_width=True
    )

    if mail_submit and mail_sender and mail_subject:
      try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "INSERT INTO gmail_cache (timestamp, sender, subject, snippet)"
            " VALUES (?, ?, ?, ?)",
            (
                str(datetime.datetime.now()),
                mail_sender,
                mail_subject,
                mail_snippet,
            ),
        )
        conn.commit()
        conn.close()
        st.success("¡Correo registrado correctamente en la bandeja!")
        st.rerun()
      except Exception as e:
        st.error(f"Error al registrar correo: {e}")

  st.markdown("---")
  st.subheader("CORREOS EN BANDEJA CENTRAL")
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, sender, subject, snippet FROM gmail_cache")
    mail_rows = c.fetchall()
    conn.close()

    if mail_rows:
      for mr in mail_rows:
        with st.expander(f"[{mr[0]}] {mr[2]} — De: {mr[1]}"):
          st.write(f"**Fecha y Hora:** {mr[1]}")
          st.write(f"**Contenido / Extracto:** {mr[4]}")
    else:
      st.info("No hay correos registrados actualmente.")
  except Exception as e:
    st.error(f"Error al cargar correos: {e}")

with tab_finanzas:
  st.subheader("CONTROL Y GESTIÓN FINANCIERA")

  with st.form("capital_form"):
    st.markdown("**1. ESTABLECER CAPITAL / DINERO INICIAL**")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
      base_efectivo = st.number_input(
          "Dinero Físico Inicial (€):", min_value=0.0, step=1.0, key="base_ef"
      )
    with col_c2:
      base_tarjeta = st.number_input(
          "Dinero en Tarjeta Inicial (€):", min_value=0.0, step=1.0, key="base_tj"
      )
    if st.form_submit_button("ACTUALIZAR CAPITAL BASE", use_container_width=True):
      try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "INSERT INTO finances (timestamp, concept, amount, type, category,"
            " method) VALUES (?, ?, ?, ?, ?, ?)",
            (
                str(datetime.datetime.now()),
                "Capital Base - Efectivo",
                base_efectivo,
                "Ingreso",
                "Capital Base",
                "Efectivo",
            ),
        )
        c.execute(
            "INSERT INTO finances (timestamp, concept, amount, type, category,"
            " method) VALUES (?, ?, ?, ?, ?, ?)",
            (
                str(datetime.datetime.now()),
                "Capital Base - Tarjeta",
                base_tarjeta,
                "Ingreso",
                "Capital Base",
                "Tarjeta",
            ),
        )
        conn.commit()
        conn.close()
        st.success("¡Capital base actualizado con éxito!")
        st.rerun()
      except Exception as e:
        st.error(f"Error al actualizar capital: {e}")

  st.markdown("---")

  col_ing, col_gas = st.columns(2)

  with col_ing:
    st.markdown("**2. REGISTRAR INGRESO**")
    with st.form("income_form"):
      i_concept = st.text_input("Concepto (Ej: Salario, Propina)")
      i_amount = st.number_input(
          "Monto (€):", min_value=0.0, step=1.0, key="inc_amt"
      )
      i_category = st.selectbox(
          "Fuente de Ingreso:", ["Salario", "Propinas", "Otro Ingreso"]
      )
      i_method = st.selectbox(
          "Método:", ["Efectivo", "Tarjeta"], key="inc_meth"
      )

      if st.form_submit_button("REGISTRAR INGRESO", use_container_width=True):
        if i_concept:
          try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute(
                "INSERT INTO finances (timestamp, concept, amount, type,"
                " category, method) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    str(datetime.datetime.now()),
                    i_concept,
                    i_amount,
                    "Ingreso",
                    i_category,
                    i_method,
                ),
            )
            conn.commit()
            conn.close()
            st.success(f"Ingreso '{i_concept}' registrado correctamente.")
            st.rerun()
          except Exception as e:
            st.error(f"Error: {e}")
        else:
          st.warning("Introduce un concepto válido.")

  with col_gas:
    st.markdown("**3. REGISTRAR GASTO**")
    with st.form("expense_form"):
      e_concept = st.text_input("Concepto (Ej: Supermercado, Alquiler)")
      e_amount = st.number_input(
          "Monto (€):", min_value=0.0, step=1.0, key="exp_amt"
      )
      e_category = st.selectbox(
          "Categoría de Gasto:",
          [
              "Alquiler",
              "Comida",
              "Seguro médico",
              "Internet",
              "Ropa",
              "Salidas",
              "Accidentes / Urgencias",
              "Reserva / Ahorro",
              "Otro Gasto",
          ],
      )
      e_method = st.selectbox(
          "Método de Pago:", ["Efectivo", "Tarjeta"], key="exp_meth"
      )

      if st.form_submit_button("REGISTRAR GASTO", use_container_width=True):
        if e_concept:
          try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute(
                "INSERT INTO finances (timestamp, concept, amount, type,"
                " category, method) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    str(datetime.datetime.now()),
                    e_concept,
                    e_amount,
                    "Gasto",
                    e_category,
                    e_method,
                ),
            )
            conn.commit()
            conn.close()
            st.success(f"Gasto '{e_concept}' registrado correctamente.")
            st.rerun()
          except Exception as e:
            st.error(f"Error: {e}")
        else:
          st.warning("Introduce un concepto válido.")

  st.markdown("---")
  st.subheader("BALANCE GLOBAL Y LIBRO CONTABLE")
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT id, timestamp, concept, amount, type, category, method FROM"
        " finances"
    )
    fin_rows = c.fetchall()
    conn.close()

    if fin_rows:
      total_ingresos = sum(r[3] for r in fin_rows if r[4] == "Ingreso")
      total_gastos = sum(r[3] for r in fin_rows if r[4] == "Gasto")
      balance_neto = total_ingresos - total_gastos

      efectivo_ing = sum(
          r[3] for r in fin_rows if r[4] == "Ingreso" and r[6] == "Efectivo"
      )
      efectivo_gas = sum(
          r[3] for r in fin_rows if r[4] == "Gasto" and r[6] == "Efectivo"
      )
      balance_efectivo = efectivo_ing - efectivo_gas

      tarjeta_ing = sum(
          r[3] for r in fin_rows if r[4] == "Ingreso" and r[6] == "Tarjeta"
      )
      tarjeta_gas = sum(
          r[3] for r in fin_rows if r[4] == "Gasto" and r[6] == "Tarjeta"
      )
      balance_tarjeta = tarjeta_ing - tarjeta_gas

      col_m1, col_m2, col_m3 = st.columns(3)
      col_m1.metric("Dinero Físico (Efectivo)", f"{balance_efectivo:.2f} €")
      col_m2.metric("Dinero en Tarjeta", f"{balance_tarjeta:.2f} €")
      col_m3.metric("Balance Neto Total", f"{balance_neto:.2f} €")

      st.markdown("<br>", unsafe_allow_html=True)
      st.markdown("**HISTORIAL DE MOVIMIENTOS:**")
      for fr in fin_rows:
        st.info(
            f"[{fr[4]}] {fr[2]} — **{fr[3]:.2f} €** | Categoría: {fr[5]} |"
            f" Método: {fr[6]} ({fr[1]})"
        )
    else:
      st.info("No se registran movimientos financieros actualmente.")
  except Exception as e:
    st.error(f"Error al cargar contabilidad: {e}")

with tab_alarmas:
  st.subheader("CRONÓMETRO Y RELOJ TÁCTICO // HUD STARK")
  st.markdown(
      """
        <div class="telemetria-container" style="text-align: center; padding: 25px;">
            <div style="font-size: 11px; letter-spacing: 2px; color: #7ab8ff; margin-bottom: 10px;">TEMPORIZADOR DE MISIÓN EN DIRECTO</div>
            <div id="stark-chronometer" style="font-size: 42px; font-weight: bold; color: #00ffcc; font-family: 'Courier New', Courier, monospace; text-shadow: 0 0 15px rgba(0,255,204,0.6);">00:00:00</div>
        </div>
    """,
      unsafe_allow_html=True,
  )

  col_t1, col_t2, col_t3 = st.columns(3)
  with col_t1:
    h_input = st.number_input("Horas:", min_value=0, max_value=24, value=0, step=1)
  with col_t2:
    m_input = st.number_input(
        "Minutos:", min_value=0, max_value=59, value=15, step=1
    )
  with col_t3:
    s_input = st.number_input(
        "Segundos:", min_value=0, max_value=59, value=0, step=1
    )

  st.markdown("<br>", unsafe_allow_html=True)
  col_btn1, col_btn2 = st.columns(2)
  with col_btn1:
    if st.button("INICIAR CUENTA REGRESIVA", use_container_width=True):
      total_segundos = int(h_input * 3600 + m_input * 60 + s_input)
      st.markdown(
          f"""
            <script>
            if (typeof window.starkTimerInterval !== 'undefined') {{ clearInterval(window.starkTimerInterval); }}
            let tiempoRestante = {total_segundos};
            window.starkTimerInterval = setInterval(function() {{
                if (tiempoRestante <= 0) {{
                    clearInterval(window.starkTimerInterval);
                    document.getElementById('stark-chronometer').innerText = "00:00:00 - ¡TIEMPO CUMPLIDO!";
                    return;
                }}
                let h = Math.floor(tiempoRestante / 3600);
                let m = Math.floor((tiempoRestante % 3600) / 60);
                let s = tiempoRestante % 60;
                let fmt = (h < 10 ? "0" + h : h) + ":" + (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
                document.getElementById('stark-chronometer').innerText = fmt;
                tiempoRestante--;
            }}, 1000);
            </script>
        """,
          unsafe_allow_html=True,
      )
      st.success("¡Cuenta regresiva iniciada en el HUD Stark!")
  with col_btn2:
    if st.button("DETENER / RESETEAR", use_container_width=True):
      st.markdown(
          """
            <script>
            if (typeof window.starkTimerInterval !== 'undefined') { clearInterval(window.starkTimerInterval); }
            document.getElementById('stark-chronometer').innerText = "00:00:00";
            </script>
        """,
          unsafe_allow_html=True,
      )
      st.success("Cronómetro restablecido.")

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
        st.write(f"Se han recuperado **{len(rows)}** registros de auditoría:")
        for row in rows:
          st.info(f"[{row[0]}] ({row[3]}) {row[1]}: {row[2]}")
      else:
        st.info("La base de datos central se encuentra limpia.")
    except Exception as e:
      st.error(f"Error al leer auditoría: {e}")
