import sqlite3
import streamlit as st

# Configuración de la interfaz con diseño HUD avanzado
st.set_page_config(
    page_title="Jarvis AI Core - HUD System", page_icon="⚡", layout="centered"
)

# Estilo visual personalizado (Tema Stark HUD / Neón Azul Oscuro)
st.markdown(
    """
    <style>
        .stApp {
            background-color: #050b14;
            color: #00d2ff;
        }
        h1, h2, h3 {
            color: #00d2ff !important;
            font-family: 'Courier New', Courier, monospace;
            text-shadow: 0px 0px 10px rgba(0, 210, 255, 0.4);
        }
        .stTextArea textarea {
            background-color: #0a1628 !important;
            color: #00d2ff !important;
            border: 1px solid #00d2ff88 !important;
            border-radius: 8px;
        }
        .stButton button {
            background: linear-gradient(90deg, #005c8a, #00d2ff) !important;
            color: #000 !important;
            font-weight: bold;
            border: none;
            border-radius: 6px;
            box-shadow: 0 0 10px rgba(0, 210, 255, 0.3);
        }
        .stAlert {
            background-color: #0a1628 !important;
            border: 1px solid #00d2ff55 !important;
            color: #fff !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# Inicializar base de datos de memoria persistente
def init_db():
  conn = sqlite3.connect("jarvis_memory.db")
  c = conn.cursor()
  c.execute(
      "CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT,"
      " content TEXT, category TEXT)"
  )
  conn.commit()
  conn.close()


init_db()

# Título del Sistema HUD
st.title("⚡ J.A.R.V.I.S. // HUD INTERFACE")
st.markdown("---")

# Panel de Subida de Documentos / Enlaces
st.subheader("📂 Ingesta de Datos & Documentos")
uploaded_file = st.file_uploader(
    "Sube archivos (TXT, PDF, código) para que Jarvis absorba la información:",
    type=["txt", "py", "md", "csv"],
)

if uploaded_file is not None:
  file_content = uploaded_file.read().decode("utf-8", errors="ignore")
  file_name = uploaded_file.name

  # Guardar automáticamente el contenido del archivo en la base de datos de memoria
  conn = sqlite3.connect("jarvis_memory.db")
  c = conn.cursor()
  c.execute(
      "INSERT INTO memory (content, category) VALUES (?, ?)",
      (f"[Documento Ingestado: {file_name}] \n{file_content[:500]}...", "Archivo"),
  )
  conn.commit()
  conn.close()

  st.success(
      f"Documento '{file_name}' asimilado correctamente en los núcleos de"
      " memoria."
  )

# Consola de Comandos Principal
st.markdown("---")
st.subheader("🎙️ Consola Táctica y Análisis Autónomo")
user_input = st.text_area(
    "Introduce una directiva, dilema o consulta para el sistema:",
    placeholder=(
        "Ej: Analizar viabilidad de sistema, evaluar riesgos de despliegue..."
    ),
)

col1, col2 = st.columns(2)

with col1:
  if st.button("Ejecutar Protocolo", use_container_width=True):
    if user_input:
      # 1. Almacenar en memoria persistente SQLite
      conn = sqlite3.connect("jarvis_memory.db")
      c = conn.cursor()
      c.execute(
          "INSERT INTO memory (content, category) VALUES (?, ?)",
          (user_input, "Comando Táctico"),
      )
      conn.commit()
      c.execute("SELECT COUNT(*) FROM memory")
      total_records = c.fetchone()[0]
      conn.close()

      # 2. Respuesta analítica generada
      reply = (
          f"Protocolo ejecutado. Datos integrados al sector de memoria"
          f" #{total_records}. Análisis de viabilidad completado con éxito."
      )
      st.success(reply)

      # 3. Módulo de Síntesis de Voz (Jarvis habla)
      speech_script = f"""
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
      st.components.v1.html(speech_script, height=0)

    else:
      st.warning("Introduce una directiva válida para procesar.")

with col2:
  if st.button("🔊 Estado del Sistema", use_container_width=True):
    status_text = (
        "Núcleos HUD enlazados. Enlaces de red estables y servidores operando al"
        " máximo rendimiento."
    )
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

# Auditoría de Memoria y Archivos Ingestados
st.markdown("---")
st.subheader("🧠 Registros de Memoria y Archivos Enlazados")

if st.button("Consultar Base de Datos Central"):
  conn = sqlite3.connect("jarvis_memory.db")
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
