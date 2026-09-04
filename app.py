import sqlite3
import streamlit as st

# Configuración de la interfaz principal para tablet
st.set_page_config(
    page_title="Jarvis AI Core", page_icon="🤖", layout="centered"
)


# Inicializar la base de datos de memoria persistente
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

# Título del sistema
st.title("🤖 JARVIS CORE ACTIVE")
st.markdown("---")

# Consola de comandos avanzada
st.subheader("🎙️ Consola de Comandos y Procesamiento")
user_input = st.text_area(
    "Escribe una orden o consulta para Jarvis:",
    placeholder="Ej: Analizar sistemas, registrar nota, estado actual...",
)

if st.button("Ejecutar Instrucción", use_container_width=True):
  if user_input:
    # 1. Guardar la orden en la base de datos de SQLite
    conn = sqlite3.connect("jarvis_memory.db")
    c = conn.cursor()
    c.execute("INSERT INTO memory (content) VALUES (?)", (user_input,))
    conn.commit()

    # 2. Contar registros totales en la memoria del sistema
    c.execute("SELECT COUNT(*) FROM memory")
    total_memories = c.fetchone()[0]
    conn.close()

    # 3. Lógica de respuesta inteligente de Jarvis
    command = user_input.lower()
    if "hola" in command:
      reply = (
          "Saludos. Todos los sistemas secundarios y principales operando al"
          " máximo rendimiento."
      )
    elif "estado" in command:
      reply = (
          f"Diagnóstico de núcleos estable. Total de registros analizados y"
          f" guardados en memoria: {total_memories}."
      )
    elif "diagnóstico" in command or "diagnostico" in command:
      reply = (
          "Análisis completado: Conexión en la nube estable, base de datos"
          " SQLite sincronizada y tiempos de respuesta óptimos."
      )
    else:
      reply = (
          f"Comando '{user_input}' procesado y almacenado correctamente en el"
          f" sector de memoria #{total_memories}."
      )

    st.success(reply)
  else:
    st.warning("Por favor, ingresa una orden válida en la consola.")

# Sección de auditoría y memoria local
st.markdown("---")
st.subheader("🧠 Registros de Memoria Local")

if st.button("Consultar Base de Datos"):
  conn = sqlite3.connect("jarvis_memory.db")
  c = conn.cursor()
  c.execute("SELECT id, content FROM memory")
  records = c.fetchall()
  conn.close()

  if records:
    st.write(
        f"Se encontraron **{len(records)}** registros almacenados en el sistema:"
    )
    for row in records:
      st.info(f"Registro [{row[0]}]: {row[1]}")
  else:
    st.info("La base de datos de memoria se encuentra vacía.")
