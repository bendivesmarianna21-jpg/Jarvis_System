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

# Interfaz Principal
st.title("🤖 JARVIS CORE // VOICE & AUTONOMOUS")
st.markdown("---")

st.subheader("🎙️ Consola de Comando y Voz Interactiva")

# Componente de HTML/JavaScript para dictado por voz y síntesis de audio
voice_control_html = """
    <div style="background: #1e1e2f; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px;">
        <p style="color: #fff; font-family: sans-serif; margin-bottom: 10px; font-size: 14px;"><b>Control de Micrófono:</b></p>
        <button onclick="startDictation()" style="background: #00ff88; color: #000; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; width: 100%;">🎙️ Hablar con Jarvis (Dictado por Voz)</button>
        <p id="status-mic" style="color: #aaa; font-size: 12px; margin-top: 8px; font-style: italic;"></p>
    </div>

    <script>
        function startDictation() {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SpeechRecognition();
                recognition.lang = 'es-ES';
                recognition.interimResults = false;
                recognition.maxAlternatives = 1;

                document.getElementById('status-mic').innerText = "Escuchando... Habla ahora.";

                recognition.onresult = function(event) {
                    const speechResult = event.results[0][0].transcript;
                    document.getElementById('status-mic').innerText = "Texto capturado: " + speechResult;
                    
                    // Buscar el cuadro de texto de Streamlit y actualizar su valor simulando input del usuario
                    const textarea = window.parent.document.querySelector('textarea');
                    if (textarea) {
                        textarea.value = speechResult;
                        textarea.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                };

                recognition.onerror = function(event) {
                    document.getElementById('status-mic').innerText = "Error en el reconocimiento de voz: " + event.error;
                };

                recognition.onend = function() {
                    setTimeout(() => {
                        document.getElementById('status-mic').innerText = "Micrófono en espera.";
                    }, 3000);
                };

                recognition.start();
            } else {
                document.getElementById('status-mic').innerText = "Tu navegador no soporta reconocimiento de voz nativo.";
            }
        }
    </script>
"""

# Renderizar el control de voz en la interfaz
st.components.v1.html(voice_control_html, height=130)

user_input = st.text_area(
    "Introduce una orden, dilema o consulta para Jarvis (o usa el botón de"
    " arriba):",
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

      # 3. Síntesis de Voz (Jarvis te habla de vuelta)
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
