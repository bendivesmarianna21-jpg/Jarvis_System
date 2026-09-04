from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

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
        <h3>🎙️ Consola del Sistema</h3>
        <textarea id="userInput" placeholder="Escribe un comando..."></textarea>
        <button onclick="sendToJarvis()">Enviar Comando</button>
        
        <h4>Respuesta de Jarvis:</h4>
        <div id="response-box">Sistemas operativos en línea.</div>
    </div>

    <script>
        function speak(text) {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'es-ES';
            utterance.rate = 1.0;
            window.speechSynthesis.speak(utterance);
        }

        async function sendToJarvis() {
            const input = document.getElementById('userInput').value;
            const box = document.getElementById('response-box');
            if(!input) return;
            
            box.innerText = "Procesando...";
            
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
    user_input = request.json.get('prompt', '').lower()
    
    if 'hola' in user_input:
        reply = "Hola. Todos los sistemas funcionando al máximo rendimiento."
    elif 'estado' in user_input:
        reply = "Los núcleos de procesamiento local están estables y operativos."
    else:
        reply = f"Comando recibido y procesado correctamente: {user_input}"
        
    return jsonify({'response': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
