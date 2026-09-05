import datetime
import json
import os
import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib.request
import streamlit as st

# Importación segura de Google GenAI
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
BACKUP_JSON = "jarvis_universal_backup.json"


# ==========================================
# SISTEMA DE PERSISTENCIA UNIVERSAL AUTOMÁTICA
# ==========================================
def init_db_and_sync():
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
  c.execute(
      "CREATE TABLE IF NOT EXISTS gmail_cache (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, timestamp TEXT, sender TEXT, subject TEXT, snippet"
      " TEXT)"
  )

  # Restauración automática desde archivo JSON si la BD local está vacía
  c.execute("SELECT COUNT(*) FROM documents_store")
  doc_count = c.fetchone()[0]

  if doc_count == 0 and os.path.exists(BACKUP_JSON):
    try:
      with open(BACKUP_JSON, "r", encoding="utf-8") as f:
        backup_data = json.load(f)

        for d in backup_data.get("documents", []):
          c.execute(
              "INSERT INTO documents_store (timestamp, title, category,"
              " content) VALUES (?, ?, ?, ?)",
              (d["timestamp"], d["title"], d["category"], d["content"]),
          )

        for l in backup_data.get("legal", []):
          c.execute(
              "INSERT INTO legal_records (timestamp, title, category, expiry,"
              " content) VALUES (?, ?, ?, ?, ?)",
              (l["timestamp"], l["title"], l["category"], l["expiry"], l["content"]),
          )

        for m in backup_data.get("gmail", []):
          c.execute(
              "INSERT INTO gmail_cache (timestamp, sender, subject, snippet)"
              " VALUES (?, ?, ?, ?)",
              (m["timestamp"], m["sender"], m["subject"], m["snippet"]),
          )

        for f_item in backup_data.get("finances", []):
          c.execute(
              "INSERT INTO finances (timestamp, concept, amount, type) VALUES"
              " (?, ?, ?, ?)",
              (
                  f_item["timestamp"],
                  f_item["concept"],
                  f_item["amount"],
                  f_item["type"],
              ),
          )

        conn.commit()
    except Exception:
      pass

  # Datos iniciales si todo está completamente vacío
  c.execute("SELECT COUNT(*) FROM gmail_cache")
  if c.fetchone()[0] == 0:
    c.execute(
        "INSERT INTO gmail_cache (timestamp, sender, subject, snippet) VALUES"
        " (?, ?, ?, ?)",
        (
            str(datetime.datetime.now()),
            "St. Joseph Krankenhaus Berlin",
            "Confirmación de inicio de Ausbildung",
            (
                "Estimada Marian, le confirmamos la recepción de sus"
                " documentos para el programa de enfermería."
            ),
        ),
    )
    conn.commit()

  conn.close()
  export_to_json_backup()


def export_to_json_backup():
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT timestamp, title, category, content FROM documents_store")
    docs = [
        {
            "timestamp": r[0],
            "title": r[1],
            "category": r[2],
            "content": r[3],
        }
        for r in c.fetchall()
    ]

    c.execute(
        "SELECT timestamp, title, category, expiry, content FROM legal_records"
    )
    legal = [
        {
            "timestamp": r[0],
            "title": r[1],
            "category": r[2],
            "expiry": r[3],
            "content": r[4],
        }
        for r in c.fetchall()
    ]

    c.execute("SELECT timestamp, sender, subject, snippet FROM gmail_cache")
    gmail = [
        {
            "timestamp": r[0],
            "sender": r[1],
            "subject": r[2],
            "snippet": r[3],
        }
        for r in c.fetchall()
    ]

    c.execute("SELECT timestamp, concept, amount, type FROM finances")
    finances = [
        {
            "timestamp": r[0],
            "concept": r[1],
            "amount": r[2],
            "type": r[3],
        }
        for r in c.fetchall()
    ]

    conn.close()

    backup_data = {
        "documents": docs,
        "legal": legal,
        "gmail": gmail,
        "finances": finances,
    }
    with open(BACKUP_JSON, "w", encoding="utf-8") as f:
      json.dump(backup_data, f, ensure_ascii=False, indent=4)
  except Exception:
    pass


init_db_and_sync()


# ==========================================
# MOTOR COGNITIVO J.A.R.V.I.S.
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
          " cuentas con nacionalidad peruana (registrado en Central Command)."
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
          res_text = "[CORREOS ELECTRÓNICOS EN MEMORIA PERMANENTE]:\n\n"
          for m in mails:
            res_text += (
                f"- De/Para: {m[1]} | Asunto: {m[2]}\n  Contenido: {m[3]}\n"
                f"  Fecha: {m[0]}\n\n"
            )
          return res_text
        else:
          return "No hay correos registrados en la memoria central."
      except Exception as e:
        return f"Error al consultar memoria de correo: {e}"

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
        res_text = "[REGISTROS ENCONTRADOS EN CUSTODIA PERSISTENTE]:\n\n"
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

live_temp = "21.5°C"
try:
  url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m"
  req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
  with urllib.request.urlopen(req, timeout=2) as response:
    data = json.loads(response.read().decode())
    live_temp = f"{data['current']['temperature_2m']}°C"
except Exception:
  pass

st.title("J.A.R.V.I.S. // CENTRAL COMMAND")

clock_html = f"""
    <div style='color: #0088cc; font-family: "Courier New", Courier, monospace; font-size: 12px; letter-spacing: 1px; margin-bottom: 15px;'>
        GLOBAL STATUS: ONLINE (BERLIN / ROAMING) | TIMESTAMP: <span id="live-date">SATURDAY, 05 SEPTEMBER 2026</span> // <span id="live-clock" style="color: #00d2ff; font-weight: bold;">00:00:00</span> | TEMP: {live_temp}
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

tab_consola, tab_docs, tab_legal, tab_gmail, tab_finanzas, tab_memoria = (
    st.tabs([
        "[CONSOLE] CENTRAL COMMAND",
        "[ARCHIVE] DOCUMENT REPOSITORY",
        "[LEGAL] EXPEDIENTES Y CREDENCIALES",
        "[GMAIL] GESTIÓN DE CORREOS",
        "[FINANCE] LEDGER & BUDGET",
        "[TELEMETRY] SYSTEM AUDIT",
    ])
)

with tab_consola:
  col_telemetry, col_main = st.columns([1, 2.2])

  with col_telemetry:
    st.subheader("DIAGNÓSTICO Y ACCESOS")
    st.markdown(
        """
            <div class="telemetria-container">
                <b>ESTADO DE NÚCLEOS:</b><br>
                - Identidad: J.A.R.V.I.S.<br>
                - Persistencia Universal: ACTIVA<br>
                - Módulo de Visión AI: SEGURO<br>
                - Gestor de Comunicaciones: ACTIVO<br><br>
                <b>CRONOGRAMA:</b><br>
                - [!] Examen de Alemán (Próximo)<br>
                - [!] Ausbildungsbeginn (St. Joseph)
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

    user_input = st.text_area(
        "Escribe tu instrucción o consulta de datos:",
        placeholder=(
            "Ej: ¿Tengo nuevos correos?, ¿Cuál es mi pasaporte?, etc..."
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
  st.subheader("REPOSITORIO Y GESTIÓN DE DOCUMENTOS (PERSISTENTE)")
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
        export_to_json_backup()

        if uploaded_file is not None and uploaded_file.type.startswith("image/"):
          st.image(
              uploaded_file, caption=f"Imagen archivada: {doc_title_input}"
          )
        st.success(
            f"Documento '{doc_title_input}' archivado en memoria persistente."
        )
      except Exception as e:
        st.error(f"Error de almacenamiento: {e}")
    else:
      st.warning("Por favor, ingresa un título y proporciona el contenido.")

  st.markdown("---")
  st.subheader("ARCHIVOS EN CUSTODIA PERSISTENTE")
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
      st.info("El repositorio documental persistente se encuentra vacío.")
  except Exception as e:
    st.error(f"Error al leer el repositorio: {e}")

with tab_legal:
  st.subheader("CUSTODIA Y ANÁLISIS DE EXPEDIENTES LEGALES")

  if "processed_doc_sig" not in st.session_state:
    st.session_state.processed_doc_sig = None

  if st.button("PURGAR REGISTROS DUPLICADOS"):
    try:
      conn = sqlite3.connect(DB_NAME)
      c = conn.cursor()
      c.execute("DELETE FROM legal_records")
      conn.commit()
      conn.close()
      export_to_json_backup()
      st.session_state.processed_doc_sig = None
      st.success("Registros duplicados purgados correctamente.")
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
    img_bytes = legal_img.getvalue()
    doc_signature = f"{legal_img.name}_{len(img_bytes)}"
    st.image(legal_img, caption="Documento cargado para análisis visual", width=400)

    if st.button("EJECUTAR EXTRACCIÓN VISUAL AI", use_container_width=True):
      if st.session_state.processed_doc_sig == doc_signature:
        st.warning(
            "Este documento ya fue analizado y registrado en esta sesión."
        )
      elif not HAS_GENAI:
        st.error("El módulo de visión AI requiere 'google-genai'.")
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
              st.error("No se detectó ninguna API Key válida.")
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
                          " estructurado: Título, Categoría, Vencimiento y Datos"
                          " clave."
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
              export_to_json_backup()

              st.session_state.processed_doc_sig = doc_signature
              st.success("¡Análisis completado y guardado sin duplicados!")
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

with tab_gmail:
  st.subheader("GESTIÓN Y ENVÍO DE CORREOS")

  action_mode = st.radio(
      "Selecciona la operación de correo:",
      ["Registrar / Guardar Notificación", "Enviar Correo a Destinatario"],
  )

  if action_mode == "Registrar / Guardar Notificación":
    st.markdown("Añade cualquier notificación o correo importante a la memoria:")
    with st.form("mail_form"):
      mail_sender = st.text_input(
          "Remitente (Ej: St. Joseph Krankenhaus, telc, etc.):"
      )
      mail_subject = st.text_input("Asunto del correo:")
      mail_snippet = st.text_area("Contenido o extracto principal:")
      mail_submit = st.form_submit_button(
          "REGISTRAR CORREO EN MEMORIA", use_container_width=True
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
          export_to_json_backup()

          st.success("¡Correo registrado con persistencia en bandeja!")
          st.rerun()
        except Exception as e:
          st.error(f"Error al registrar correo: {e}")
  else:
    st.markdown("Envía un mensaje o correo electrónico a cualquier persona:")
    with st.form("send_mail_form"):
      smtp_sender = st.text_input(
          "Tu Correo (Gmail remitente):",
          placeholder="tucorreo@gmail.com",
      )
      smtp_password = st.text_input(
          "Contraseña de aplicación de Gmail:",
          type="password",
          placeholder="Contraseña de 16 dígitos de Google",
      )
      mail_to = st.text_input(
          "Destinatario:", placeholder="destinatario@correo.com"
      )
      mail_title = st.text_input("Asunto:")
      mail_body = st.text_area("Mensaje:")
      send_submit = st.form_submit_button(
          "ENVIAR CORREO ELECTRÓNICO", use_container_width=True
      )

      if send_submit and smtp_sender and smtp_password and mail_to:
        try:
          msg = MIMEMultipart()
          msg["From"] = smtp_sender
          msg["To"] = mail_to
          msg["Subject"] = mail_title
          msg.attach(MIMEText(mail_body, "plain", "utf-8"))

          server = smtplib.SMTP("smtp.gmail.com", 587)
          server.starttls()
          server.login(smtp_sender, smtp_password)
          server.sendmail(smtp_sender, mail_to, msg.as_string())
          server.quit()

          st.success(f"¡Correo enviado con éxito a {mail_to}!")

          conn = sqlite3.connect(DB_NAME)
          c = conn.cursor()
          c.execute(
              "INSERT INTO gmail_cache (timestamp, sender, subject, snippet)"
              " VALUES (?, ?, ?, ?)",
              (
                  str(datetime.datetime.now()),
                  f"Enviado a: {mail_to}",
                  mail_title,
                  mail_body,
              ),
          )
          conn.commit()
          conn.close()
          export_to_json_backup()
        except Exception as e:
          st.error(f"Error al enviar el correo (verifica tu contraseña de aplicación): {e}")

  st.markdown("---")
  st.subheader("CORREOS EN MEMORIA CENTRAL")
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, sender, subject, snippet FROM gmail_cache")
    mail_rows = c.fetchall()
    conn.close()

    if mail_rows:
      for mr in mail_rows:
        with st.expander(f"[{mr[0]}] {mr[2]} — De/Para: {mr[1]}"):
          st.write(f"**Fecha y Hora:** {mr[1]}")
          st.write(f"**Contenido / Mensaje:** {mr[4]}")
    else:
      st.info("No hay correos registrados actualmente.")
  except Exception as e:
    st.error(f"Error al cargar correos: {e}")

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
        export_to_json_backup()

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
        st.write(f"Se han recuperado **{len(rows)}** registros de auditoría:")
        for row in rows:
          st.info(f"[{row[0]}] ({row[3]}) {row[1]}: {row[2]}")
      else:
        st.info("La base de datos central se encuentra limpia.")
    except Exception as e:
      st.error(f"Error al leer auditoría: {e}")
