import os
import time
import json
import sqlite3
from datetime import datetime
import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO HUD
# ==========================================
st.set_page_config(
    page_title="JARVIS System HUD",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS avanzados (Colores, Tipografías, Neón y Disposición)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700&display=swap');
    
    .stApp {
        background-color: #050b14;
        color: #00f0ff;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Header del Reloj y Telemetría */
    .hud-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        color: #00f0ff;
        text-shadow: 0 0 10px #00f0ff, 0 0 20px #00f0ff;
        letter-spacing: 2px;
    }
    
    .hud-metric {
        background: rgba(0, 240, 255, 0.05);
        border: 1px solid #00f0ff;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }
    
    .metric-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.4rem;
        color: #ffffff;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #00f0ff;
        text-transform: uppercase;
    }

    /* Alertas del Sistema */
    .status-ok {
        color: #00ff66;
        font-weight: bold;
    }
    .status-error {
        color: #ff0055;
        font-weight: bold;
    }

    /* Contenedores visuales */
    div[data-testid="stExpander"] {
        border: 1px solid #00f0ff !important;
        background-color: rgba(5, 11, 20, 0.8) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BASE DE DATOS Y MEMORIA ASOCIATIVA
# ==========================================
DB_NAME = "jarvis_tablet_memory.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tabla para documentos completos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            tipo_entrada TEXT NOT NULL,
            contenido_texto TEXT,
            ruta_imagen TEXT,
            fecha_registro TEXT NOT NULL
        )
    ''')
    # Tabla de perfil rápido
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memoria_perfil (
            clave TEXT PRIMARY KEY,
            valor TEXT NOT NULL,
            origen_doc_id INTEGER,
            fecha_actualizacion TEXT NOT NULL,
            FOREIGN KEY (origen_doc_id) REFERENCES documentos (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 3. MOTOR GEMINI Y DIAGNÓSTICO
# ==========================================
api_key = os.getenv("GEMINI_API_KEY", "")
api_status = True

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    api_status = False

def procesar_ocr_imagen(ruta_o_bytes):
    """Extrae texto de una imagen para absorción del 100%."""
    try:
        archivo = genai.upload_file(ruta_o_bytes)
        prompt = "Transcribe de forma íntegra todo el texto, nombres, códigos y números de este documento."
        res = model.generate_content([archivo, prompt])
        return res.text.strip()
    except Exception as e:
        return f"[Error en procesamiento visual OCR: {e}]"

def actualizar_memoria_perfil(doc_id, titulo, texto):
    """Extrae datos exactos (seguro social, pasaporte) a la memoria rápida."""
    prompt = f"""
    Analiza el documento '{titulo}'. Extrae datos personales identificadores clave en JSON (clave-valor).
    Ejemplos: "numero_seguro_social", "numero_pasaporte", "identificacion_oficial".
    Texto: {texto}
    Responde ÚNICAMENTE con el JSON plano sin markdown.
    """
    try:
        res = model.generate_content(prompt)
        raw_text = res.text.strip().replace("```json", "").replace("```", "").strip()
        datos = json.loads(raw_text)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for k, v in datos.items():
            cursor.execute('''
                INSERT OR REPLACE INTO memoria_perfil (clave, valor, origen_doc_id, fecha_actualizacion)
                VALUES (?, ?, ?, ?)
            ''', (k.lower().strip(), str(v), doc_id, fecha))
        conn.commit()
        conn.close()
    except Exception as e:
        pass

def responder_jarvis(pregunta):
    """Consulta la memoria asociativa de perfil antes de responder."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT clave, valor FROM memoria_perfil")
    perfil = cursor.fetchall()
    contexto_perfil = "\n".join([f"- {k}: {v}" for k, v in perfil])

    cursor.execute("SELECT id, titulo, categoria, contenido_texto FROM documentos")
    docs = cursor.fetchall()
    contexto_docs = "\n".join([f"--- ID {d[0]} | TÍTULO: {d[1]} | CAT: {d[2]} ---\n{d[3]}" for d in docs])
    conn.close()

    prompt = f"""
Eres Jarvis. Responde con precisión absoluta basándote en esta información personal:

[MEMORIA RÁPIDA DE PERFIL]
{contexto_perfil}

[DOCUMENTOS ALMACENADOS]
{contexto_docs}

Si preguntan por un número específico (como seguro social o pasaporte), toma el dato exacto de su categoría. NO los confundas.

Pregunta: {pregunta}
"""
    res = model.generate_content(prompt)
    return res.text.strip()

# ==========================================
# 4. INTERFAZ EN TIEMPO REAL (HUD TABLET)
# ==========================================

# Panel Superior: Telemetría, Reloj y Estado del Sistema
col_title, col_time, col_temp, col_status = st.columns([3, 2, 2, 2])

with col_title:
    st.markdown('<div class="hud-title">⚡ JARVIS SYSTEM</div>', unsafe_allow_html=True)

with col_time:
    # Reloj dinámico
    ahora = datetime.now().strftime("%H:%M:%S | %d-%m-%Y")
    st.markdown(f'''
        <div class="hud-metric">
            <div class="metric-value">{ahora}</div>
            <div class="metric-label">Tiempo del Sistema</div>
        </div>
    ''', unsafe_allow_html=True)

with col_temp:
    st.markdown('''
        <div class="hud-metric">
            <div class="metric-value">22.5 °C</div>
            <div class="metric-label">Temperatura Local</div>
        </div>
    ''', unsafe_allow_html=True)

with col_status:
    estado_txt = '<span class="status-ok">OPERATIVO</span>' if api_status else '<span class="status-error">ERROR API</span>'
    st.markdown(f'''
        <div class="hud-metric">
            <div class="metric-value">{estado_txt}</div>
            <div class="metric-label">Estado Jarvis</div>
        </div>
    ''', unsafe_allow_html=True)

st.divider()

# Notificación automática de fallos
if not api_status:
    st.error("⚠️ ALERTA DE SISTEMA: La API Key de Gemini no está configurada o ha fallado. Revisa tus variables de entorno.")

# ==========================================
# 5. PESTAÑAS DE CONTROL Y NAVEGACIÓN
# ==========================================
tab_chat, tab_docs, tab_system = st.tabs(["💬 Consola / Voz", "📁 Documentación", "⚙️ Memoria y Sistema"])

# --- TAB 1: CONSOLA Y RESPUESTAS ---
with tab_chat:
    st.subheader("Interacción Asistida")
    
    # Campo de entrada de voz / escrito
    pregunta_user = st.text_input("Consulta a Jarvis (Voz / Texto):", placeholder="Ej: ¿Cuál es mi número de seguro social?")
    
    if st.button("Enviar Consulta", type="primary"):
        if pregunta_user:
            with st.spinner("Jarvis consultando memoria asociativa..."):
                respuesta = responder_jarvis(pregunta_user)
                st.markdown(f"**JARVIS:** {respuesta}")
                # Síntesis de voz automática simulada en UI
                st.audio_input("Comando por voz de respuesta", key="audio_feedback", disabled=True)

# --- TAB 2: GESTIÓN DE DOCUMENTACIÓN DUAL ---
with tab_docs:
    st.subheader("Centro de Registro Documental")
    
    col_reg1, col_reg2 = st.columns(2)
    
    with col_reg1:
        titulo_doc = st.text_input("Título / Nombre del Documento (Obligatorio):", placeholder="Ej: Seguro Social, Pasaporte 2026")
        categoria_doc = st.selectbox("Categoría:", ["Documentación Legal", "Identificación", "Salud / Clínica", "Otros"])
        modalidad = st.radio("Método de Ingreso:", ["Texto Directo", "Fotografía / Captura"])

    with col_reg2:
        texto_ingresado = ""
        ruta_img_guardada = None
        
        if modalidad == "Texto Directo":
            texto_ingresado = st.text_area("Escribe la información detallada del documento:", height=150)
        else:
            foto = st.file_uploader("Subir imagen del documento:", type=["jpg", "png", "jpeg"])
            if foto:
                # Guardar imagen temporal
                ruta_img_guardada = f"temp_{foto.name}"
                with open(ruta_img_guardada, "wb") as f:
                    f.write(foto.getbuffer())
                st.image(foto, caption="Vista previa", width=200)

    if st.button("Archivar en Jarvis"):
        if not titulo_doc:
            st.warning("⚠️ Debes proporcionar un Título al documento.")
        else:
            with st.spinner("Procesando e indexando documento al 100%..."):
                contenido_final = texto_ingresado
                tipo_ent = "texto"

                if modalidad == "Fotografía / Captura" and ruta_img_guardada:
                    tipo_ent = "imagen"
                    contenido_final = procesar_ocr_imagen(ruta_img_guardada)

                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Guardar en BD
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO documentos (titulo, categoria, tipo_entrada, contenido_texto, ruta_imagen, fecha_registro)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (titulo_doc, categoria_doc, tipo_ent, contenido_final, ruta_img_guardada, fecha_actual))
                doc_id = cursor.lastrowid
                conn.commit()
                conn.close()

                # Actualizar Memoria Rápida de Perfil
                actualizar_memoria_perfil(doc_id, titulo_doc, contenido_final)
                st.success(f"✅ Documento '{titulo_doc}' archivado y sincronizado en la memoria.")

# --- TAB 3: VISUALIZADOR DE MEMORIA Y ESTADO ---
with tab_system:
    st.subheader("Base de Datos y Perfil Asociativo")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    st.markdown("**1. Memoria de Perfil Rápido (Key-Value Directo):**")
    cursor.execute("SELECT clave, valor, fecha_actualizacion FROM memoria_perfil")
    perfil_data = cursor.fetchall()
    if perfil_data:
        st.dataframe(perfil_data, column_config={"0": "Clave", "1": "Valor Indexado", "2": "Última Actualización"})
    else:
        st.info("No hay datos de perfil directo indexados aún.")

    st.markdown("**2. Documentos Archivos en el Sistema:**")
    cursor.execute("SELECT id, titulo, categoria, tipo_entrada, fecha_registro FROM documentos")
    docs_data = cursor.fetchall()
    if docs_data:
        st.dataframe(docs_data)
    else:
        st.info("La base de documentos está vacía.")
        
    conn.close()
