import sqlite3
import streamlit as st

# Configuración de la página con estilo moderno
st.set_page_config(
    page_title="Jarvis AI Core", page_icon="🤖", layout="centered"
)


# Inicializar la base de datos de memoria
def init_db():
  conn = sqlite3.connect("jarvis_memory.db")
  c = conn.cursor()
  c.execute(
      "CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT,"
      " content TEXT)"
  )
  conn.commit()
  conn.close()


init_db()

# Interfaz visual principal
st.title("🤖 JARVIS CORE ACTIVE")
st.markdown("---")

# Tarjeta de consola y control de comandos
st.subheader("🎙️ Control de Consola y Memoria")
user_input = st.text_area(
    "Escribe un comando o instrucción para Jarvis:",
    placeholder="Ej: Iniciar diagnósticos o recordar datos...",
)

col1, col2 = st.columns(2)

with col1:
  if st.button("Enviar Comando", use_container_width=True):
    if user_input:
      # Guardar interacción en la base de datos de memoria
      conn = sqlite3.connect("jarvis_memory.db")
      c = conn.cursor()
      c.execute("INSERT INTO memory (content) VALUES (?)", (user_input,))
      conn.commit()

      # Contar bloques de memoria registrados
      c.execute("SELECT COUNT(*) FROM memory")
      total_memories = c.fetchone()[0]
      conn.close()

      # Lógica de respuesta simulada de Jarvis
      if "hola" in user_input.lower():
        reply = "Hola. Todos los sistemas funcionando al máximo rendimiento."
      elif "estado" in user_input.lower():
        reply = "Los núcleos de procesamiento local están estables y operativos."
      else:
        reply = (
            f"Comando recibido: '{user_input}'. Tengo registrados"
            f" {total_memories} bloques de datos en memoria local."
        )

      st.success(reply)
    else:
      st.warning("Por favor, escribe un comando antes de enviar.")

with col2:
  if st.button("🎙️ Simular Voz", use_container_width=True):
    st.info("Módulo de voz activo en la nube.")

# Sección de registros y memoria almacenada
st.markdown("---")
st.subheader("🧠 Historial de Memoria del Sistema")

if st.button("Cargar Registros Guardados"):
  conn = sqlite3.connect("jarvis_memory.db")
  c = conn.cursor()
  c.execute("SELECT id, content FROM memory")
  records = c.fetchall()
  conn.close()

  if records:
    for row in records:
      st.write(f"**[{row[0]}]** {row[1]}")
  else:
    st.info("La memoria está limpia por ahora.")
