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
        .stApp { background-color: #03070c; color: #00d2ff; font-family: monospace; }
        #MainMenu, footer, header {visibility: hidden;}
        h1, h2, h3 { color: #00d2ff !important; font-family: monospace !important; }
        .telemetria-container { background: rgba(4, 12, 24, 0.9); border: 1px solid rgba(0, 210, 255, 0.3); padding: 15px; border-radius: 5px; color: #7ab8ff; }
        .stTextInput input, .stSelectbox select, .stNumberInput input, .stTextArea textarea { background-color: #050f1d !important; color: #00d2ff !important; border: 1px solid rgba(0, 210, 255, 0.4) !important; }
        .stButton button { background: #040e1b !important; color: #00d2ff !important; border: 1px solid rgba(0, 210, 255, 0.6) !important; font-weight: bold; }
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
                f"Eres J.A.R.V.I.S., asistente personal de {self.creator}."
                f" Responde directo a: {q}"
            ),
        )
        return response.text
      except Exception:
        pass

    return f"Procesada directiva '{q}' para {self.creator} con éxito."


jarvis_brain = JarvisMind()

st.title("J.A.R.V.I.S. // CENTRAL COMMAND")
st.markdown(
    "<div style='color: #0088cc; font-size: 11px;'>SISTEMA ESTABLE // BERLIN"
    " // NÚCLEOS COMPLETOS</div>",
    unsafe_allow_html=True,
)
st.markdown("---")

tab_consola, tab_legal, tab_gmail, tab_finanzas = st.tabs([
    "[CONSOLE] GENERAL",
    "[LEGAL] EXPEDIENTES",
    "[GMAIL] CORREOS",
    "[FINANCE] CONTABILIDAD",
])

with tab_consola:
  col_t, col_m = st.columns([1, 2])
  with col_t:
    st.subheader("DIAGNÓSTICO")
    st.markdown(
        """
            <div class="telemetria-container">
                - Asistente: J.A.R.V.I.S.<br>
                - Usuaria: Marian Nathalia Bendives Ramos<br>
                - Estado: Operativo
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col_m:
    st.subheader("CONSOLA DE DIÁLOGO")
    c_key = st.text_input("Gemini API Key (Opcional):", type="password")
    u_input = st.text_area("Instrucción:")
    if st.button("PROCESAR PENSAMIENTO"):
      if u_input:
        reply = jarvis_brain.reason(u_input, c_key)
        st.markdown(
            f"<div class='telemetria-container'>{reply}</div>",
            unsafe_allow_html=True,
        )

with tab_legal:
  st.subheader("CUSTODIA DE EXPEDIENTES LEGALES")
  if st.button("LIMPIAR REGISTROS LEGALES"):
    try:
      conn = sqlite3.connect(DB_NAME)
      c = conn.cursor()
      c.execute("DELETE FROM legal_records")
      conn.commit()
      conn.close()
      st.success("Registros limpiados.")
      st.rerun()
    except Exception as e:
      st.error(f"Error: {e}")

  legal_title = st.text_input("Título del Documento (Ej: Pasaporte):")
  legal_img = st.file_uploader(
      "Sube tu documento:", type=["jpg", "png", "jpeg"]
  )

  if legal_img is not None and st.button("EJECUTAR ANÁLISIS VISUAL"):
    if not HAS_GENAI:
      st.error("Falta el módulo google-genai.")
    else:
      try:
        img_bytes = legal_img.read()
        st.image(legal_img, width=300)
        client = genai.Client(
            api_key=c_key.strip()
            if c_key
            else st.secrets.get("GEMINI_API_KEY", None)
        )
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                types.Part.from_bytes(data=img_bytes, mime_type=legal_img.type),
                (
                    "Extrae con absoluto detalle: Título, Categoría, Vencimiento"
                    " y todos los datos clave."
                ),
            ],
        )
        res_text = response.text
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "INSERT INTO legal_records (timestamp, title, category, expiry,"
            " content) VALUES (?, ?, ?, ?, ?)",
            (
                str(datetime.datetime.now()),
                legal_title if legal_title else legal_img.name,
                "Expediente Legal",
                "Ver detalle",
                res_text,
            ),
        )
        conn.commit()
        conn.close()
        st.success("¡Guardado con éxito!")
        st.markdown(
            f"<div class='telemetria-container'>{res_text}</div>",
            unsafe_allow_html=True,
        )
      except Exception as e:
        st.error(f"Error en visión AI: {e}")

  st.markdown("---")
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT id, timestamp, title, content FROM legal_records ORDER BY id DESC"
    )
    rows = c.fetchall()
    conn.close()
    for r in rows:
      with st.expander(f"[{r[0]}] {r[2]} ({r[1]})"):
        st.write(r[3])
  except Exception:
    pass

with tab_gmail:
  st.subheader("GESTIÓN Y REGISTRO DE CORREOS")
  with st.form("mail_form"):
    m_sender = st.text_input("Remitente (Ej: St. Joseph Krankenhaus):")
    m_subject = st.text_input("Asunto:")
    m_snippet = st.text_area("Contenido / Mensaje:")
    if st.form_submit_button("REGISTRAR CORREO"):
      if m_sender and m_subject:
        try:
          conn = sqlite3.connect(DB_NAME)
          c = conn.cursor()
          c.execute(
              "INSERT INTO gmail_cache (timestamp, sender, subject, snippet)"
              " VALUES (?, ?, ?, ?)",
              (
                  str(datetime.datetime.now()),
                  m_sender,
                  m_subject,
                  m_snippet,
              ),
          )
          conn.commit()
          conn.close()
          st.success("¡Correo registrado!")
          st.rerun()
        except Exception as e:
          st.error(f"Error: {e}")

  st.markdown("---")
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT id, timestamp, sender, subject, snippet FROM gmail_cache"
    )
    m_rows = c.fetchall()
    conn.close()
    for mr in m_rows:
      with st.expander(f"[{mr[0]}] {mr[2]} — De: {mr[1]}"):
        st.write(f"Fecha: {mr[1]}")
        st.write(f"Mensaje: {mr[4]}")
  except Exception:
    pass

with tab_finanzas:
  st.subheader("CONTROL FINANCIERO Y GASTOS")
  with st.form("cap_form"):
    st.markdown("**1. CAPITAL INICIAL**")
    c1, c2 = st.columns(2)
    ef_ini = c1.number_input("Dinero Físico (€):", min_value=0.0, step=1.0)
    tj_ini = c2.number_input("Dinero en Tarjeta (€):", min_value=0.0, step=1.0)
    if st.form_submit_button("ESTABLECER CAPITAL INICIAL"):
      conn = sqlite3.connect(DB_NAME)
      c = conn.cursor()
      c.execute(
          "INSERT INTO finances (timestamp, concept, amount, type, category,"
          " method) VALUES (?, ?, ?, ?, ?, ?)",
          (
              str(datetime.datetime.now()),
              "Capital Inicial Físico",
              ef_ini,
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
              "Capital Inicial Tarjeta",
              tj_ini,
              "Ingreso",
              "Capital Base",
              "Tarjeta",
          ),
      )
      conn.commit()
      conn.close()
      st.success("Capital actualizado.")
      st.rerun()

  st.markdown("---")
  col_i, col_g = st.columns(2)

  with col_i:
    st.markdown("**2. REGISTRAR INGRESO**")
    with st.form("inc_form"):
      inc_con = st.text_input("Concepto (Ej: Salario, Propina):")
      inc_amt = st.number_input("Monto (€):", min_value=0.0, step=1.0)
      inc_cat = st.selectbox("Fuente:", ["Salario", "Propinas", "Otro Ingreso"])
      inc_met = st.selectbox("Método:", ["Efectivo", "Tarjeta"])
      if st.form_submit_button("GUARDAR INGRESO"):
        if inc_con:
          conn = sqlite3.connect(DB_NAME)
          c = conn.cursor()
          c.execute(
              "INSERT INTO finances (timestamp, concept, amount, type,"
              " category, method) VALUES (?, ?, ?, ?, ?, ?)",
              (
                  str(datetime.datetime.now()),
                  inc_con,
                  inc_amt,
                  "Ingreso",
                  inc_cat,
                  inc_met,
              ),
          )
          conn.commit()
          conn.close()
          st.success("Ingreso guardado.")
          st.rerun()

  with col_g:
    st.markdown("**3. REGISTRAR GASTO**")
    with st.form("exp_form"):
      exp_con = st.text_input("Concepto (Ej: Comida, Alquiler):")
      exp_amt = st.number_input("Monto (€):", min_value=0.0, step=1.0, key="e_amt")
      exp_cat = st.selectbox(
          "Categoría:",
          [
              "Alquiler",
              "Comida",
              "Seguro médico",
              "Internet",
              "Ropa",
              "Salidas",
              "Accidentes",
              "Reserva",
              "Otro Gasto",
          ],
      )
      exp_met = st.selectbox(
          "Método de Pago:", ["Efectivo", "Tarjeta"], key="e_met"
      )
      if st.form_submit_button("GUARDAR GASTO"):
        if exp_con:
          conn = sqlite3.connect(DB_NAME)
          c = conn.cursor()
          c.execute(
              "INSERT INTO finances (timestamp, concept, amount, type,"
              " category, method) VALUES (?, ?, ?, ?, ?, ?)",
              (
                  str(datetime.datetime.now()),
                  exp_con,
                  exp_amt,
                  "Gasto",
                  exp_cat,
                  exp_met,
              ),
          )
          conn.commit()
          conn.close()
          st.success("Gasto guardado.")
          st.rerun()

  st.markdown("---")
  st.subheader("RESUMEN Y BALANCE")
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT id, timestamp, concept, amount, type, category, method FROM"
        " finances"
    )
    rows = c.fetchall()
    conn.close()

    if rows:
      t_ing = sum(r[3] for r in rows if r[4] == "Ingreso")
      t_gas = sum(r[3] for r in rows if r[4] == "Gasto")
      neto = t_ing - t_gas

      ef_ing = sum(r[3] for r in rows if r[4] == "Ingreso" and r[6] == "Efectivo")
      ef_gas = sum(r[3] for r in rows if r[4] == "Gasto" and r[6] == "Efectivo")
      ef_tot = ef_ing - ef_gas

      tj_ing = sum(r[3] for r in rows if r[4] == "Ingreso" and r[6] == "Tarjeta")
      tj_gas = sum(r[3] for r in rows if r[4] == "Gasto" and r[6] == "Tarjeta")
      tj_tot = tj_ing - tj_gas

      m1, m2, m3 = st.columns(3)
      m1.metric("Efectivo Físico", f"{ef_tot:.2f} €")
      m2.metric("En Tarjeta", f"{tj_tot:.2f} €")
      m3.metric("Balance Total", f"{neto:.2f} €")

      st.markdown("<br>**MOVIMIENTOS:**", unsafe_allow_html=True)
      for r in rows:
        st.info(
            f"[{r[4]}] {r[2]} — **{r[3]:.2f} €** | Cat: {r[5]} | Método: {r[6]}"
        )
    else:
      st.info("No hay registros financieros.")
  except Exception as e:
    st.error(f"Error al cargar finanzas: {e}")
