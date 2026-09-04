from flask import Flask, render_template_string, request, jsonify
import sqlite3, os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('jarvis_memory.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)')
    conn.commit()
    conn.close()

init_db()

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Jarvis AI Core</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #0a0a12; color: #fff; padding: 20px; }
        h1 { color: #00d2ff; text-align: center; }
        .card { background: #161625; padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #00d2ff55; }
        textarea { width: 100%; height: 70px; background: #0d0d18; color: #fff; border: 1px solid #333; border-radius: 8px; padding: 10px; box-sizing: border-box; }
        button { background: #00d2ff; color: #000; border: none; padding: 12px; font-weight: bold; border-radius: 8px; width: 100%; margin-top: 10px; cursor: pointer; }
        #response-box { background: #000; border-left: 4px solid #00d2ff; padding: 15px; margin-top: 15px; min-height: 40px; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>🤖 JARVIS CORE ACTIVE</h1>
    
    <div class="card">
        <h3>🎙️ Control de Voz y Consola</h3>
        <textarea id="userInput" placeholder="Escribe un comando o presiona Hablar..."></textarea>
        <button onclick="sendToJarvis()">Enviar Comando</button>
        <button onclick="startListening()" style="background:#00ff88;">🎙️ Hablar a Jarvis</button>
        
        <h4>Respuesta de Jarvis:</h4>
        <div id="response-box">Esperando órdenes...</div>
    </div>

    <script>
        function speak(text) {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'es-ES';
            utterance.rate = 1.0;
            window.speechSynthesis.speak(utterance);
        }

        function startListening() {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'es-ES';
            recognition.onresult = function(event) {
                document.getElementById('userInput').value = event.results[0][0].transcript;
                sendToJarvis();
            };
            recognition.start();
        }

        async function sendToJarvis() {
            const input = document.getElementById('userInput').value;
            const box = document.getElementById('response-box');
            if(!input) return;
            
            box.innerText = "Pensando...";
            
            const res = await fetch('/process', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: input})
            });
            const data = await res.json();
            
            box.innerText = data.response;
            speak(data.response);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/process', methods=['POST'])
def process():
    user_input = request.json.get('prompt', '')
    
    # 1. Recuperar contexto/memoria local
    conn = sqlite3.connect('jarvis_memory.db')
    c = conn.cursor()
    c.execute('SELECT content FROM memory')
    memories = [row[0] for row in c.fetchall()]
    conn.close()
    
    # 2. Lógica de Respuesta / Ejecución de comandos
    reply = f"Comando recibido: '{user_input}'. Tengo registrados {len(memories)} bloques de datos en memoria local."
    
    return jsonify({'response': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501)
o
x
