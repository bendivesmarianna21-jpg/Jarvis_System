import datetime
import sqlite3
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
      "CREATE TABLE IF NOT EXISTS finances (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, timestamp TEXT, concept TEXT, amount REAL, type TEXT,"
      " category TEXT, method TEXT)"
  )
  c.execute(
      "CREATE TABLE IF NOT EXISTS legal_records (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, timestamp TEXT, title TEXT, category TEXT, expiry"
      " TEXT, content TEXT)"
  )
  conn.commit()
  conn.close()


init_db()

st.title("J.A.R.V.I.S. // CENTRAL COMMAND")
st.markdown(
    "<div style='color: #0088cc; font-size: 11px;'>SISTEMA ESTABLE // BERLIN"
    " // MODO RÁPIDO</div>",
    unsafe_allow_html=True,
)
st.markdown("---")

tab_consola, tab_legal, tab_finanzas = st.tabs(
    ["[CONSOLE] GENERAL", "[LEGAL] EXPEDIENTES", "[FINANCE] CONTABILIDAD"]
)

with tab_consola:
  st.subheader("ESTADO DE NÚCLEOS")
  st.markdown(
      """
        <div class="telemetria-container">
            - Asistente: J.A.R.V.I.S.<br>
            - Usuaria: Marian Nathalia Bendives Ramos<br>
            - Estado: En línea y operativo sin bloqueos.
        </div>
    """,
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

  custom_api_key = st.text_input(
      "Gemini API Key (Opcional):", type="password", key="l_key"
  )
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
            api_key=custom_api_key.strip()
            if custom_api_key
            else st.secrets.get("GEMINI_API_KEY", None)
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
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
      inc_con = st.text_input("Concepto (Ej: Propina, Salario):")
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
      exp_con = st.text_input("Concepto (Ej: Supermercado):")
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
