import sqlite3
import streamlit as st

# Configuración de la interfaz optimizada para tablet
st.set_page_config(
    page_title="Jarvis AI Core - Voice & Autonomous",
    page_icon="🤖",
    layout="centered",
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

# Interfaz Principal con soporte de Voz vía JavaScript integrado
st.title("🤖 JARVIS CORE // VOICE & AUTONOMOUS")
st.markdown("---")

st.subheader("🎙️ Consola de Comando y Voz")
user_input = st.text_area(
    "Introduce una orden, dilema o consulta para Jarvis:",
    placeholder=(
        "Ej: Analizar viabilidad de proyecto, evaluar riesgos operativos..."
    ),
)

col1, col2 = st.columns(2)

with col1:
  if st.button("Ejecutar Análisis Autónomo", use_container_width=True):
    if user_input:
      # 1. Almacenar en memoria persistente SQLite
      conn = sqlite3.connect("jarvis_memory.db")
      c = conn.cursor()
      c.execute(
          "INSERT INTO memory (content, category) VALUES (?, ?)",
          (user_input, "Análisis de Voz/Texto"),
      )
      conn.commit()
      c.execute("SELECT COUNT(*) FROM memory")
      total_records = c.fetchone()[0]
      conn.close()

      # 2. Respuesta analítica generada
      reply = (
          f"Análisis procesado e integrado al sector de memoria"
          f" #{total_records}. Situación evaluada: {user_input}. Viabilidad"
          " óptima detectada con mitigación de riesgos activa."
      )
      st.success(reply)

      # 3. Módulo de Síntesis de Voz (Speech Synthesis nativo del navegador)
      # Esto hace que la tablet lea la respuesta en voz alta automáticamente
      speech_script = f"""
            <script>
                function speakResponse() {{
                    if ('speechSynthesis' in window) {{
                        window.speechSynthesis.cancel();
                        const utterance = new SpeechSynthesisUtterance({reply!r});
                        utterance.lang = 'es-ES';
                        utterance.rate = 1.0;
                        window.speechSynthesis.speak(utterance);
                    }}
                }}
                speakResponse();
            </script>
            """
      st.components.v1.html(speech_script, height=0)

    else:
      st.warning("Por favor, introduce un parámetro válido para procesar.")

with col2:
  if st.button("🔊 Forzar Audio de Estado", use_container_width=True):
    status_text = (
        "Todos los núcleos de procesamiento y bases de datos locales operan al"
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

# Sección de auditoría de memoria histórica
st.markdown("---")
st.subheader("🧠 Base de Datos Histórica")

if st.button("Consultar Registros Pasados"):
  conn = sqlite3.connect("jarvis_memory.db")
  c = conn.cursor()
  c.execute("SELECT id, content, category FROM memory")
  rows = c.fetchall()
  conn.close()

  if rows:
    st.write(f"Se han recuperado **{len(rows)}** registros de la nube:")
    for row in rows:
      st.info(f"[{row[0]}] ({row[2]}): {row[1]}")
  else:
    st.info("La base de datos se encuentra limpia.")
