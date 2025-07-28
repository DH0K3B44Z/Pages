import os
import threading
import time
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Shared state
shared_data = {
    'tokens': [],
    'comment': '',
    'name': '',
    'interval': 10  # default interval in seconds
}

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Token & Comment App</title>
<style>
    body {
        font-family: Arial, sans-serif;
        max-width: 500px;
        margin: auto;
        padding: 20px;
        background: #f9f9f9;
    }
    h2 { text-align: center; color: #2c3e50; }
    label { font-weight: bold; display: block; margin-top: 15px; }
    textarea, input[type=text], input[type=number], input[type=file], button {
        width: 100%; padding: 10px; margin-top: 5px; border-radius: 5px; border: 1px solid #ccc;
    }
    button {
        background: #3498db; color: white; border: none; cursor: pointer;
    }
    button:hover { background: #2980b9; }
    .output {
        background: #ecf0f1;
        padding: 10px;
        margin-top: 20px;
        border-left: 5px solid #3498db;
        white-space: pre-wrap;
        font-family: monospace;
    }
</style>
</head>
<body>
    <h2>Token + Comment Input</h2>
    <form method="POST" enctype="multipart/form-data">
        <label>Your Name:</label>
        <input type="text" name="name" value="{{ name }}">

        <label>Interval (in seconds):</label>
        <input type="number" name="interval" value="{{ interval }}">

        <label>Tokens (one per line):</label>
        <textarea name="tokens_box" rows="5">{{ tokens_text }}</textarea>

        <label>Upload Comment File (.txt):</label>
        <input type="file" name="comment_file" accept=".txt">

        <label>Or Type Comment:</label>
        <textarea name="comment_text" rows="3">{{ comment_text }}</textarea>

        <button type="submit">Submit</button>
    </form>

    {% if name or interval or tokens or comment_result %}
    <div class="output">
        {% if name %}<b>👤 Name:</b> {{ name }}<br>{% endif %}
        {% if interval %}<b>⏱ Interval:</b> {{ interval }} seconds<br>{% endif %}
        {% if tokens %}<b>🔐 Tokens:</b><br>{{ tokens|join('\\n') }}<br>{% endif %}
        {% if comment_result %}<b>📝 Comment:</b><br>{{ comment_result }}{% endif %}
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    tokens_text = ""
    comment_text = ""
    name = shared_data.get('name', '')
    interval = shared_data.get('interval', 10)
    tokens = shared_data.get('tokens', [])
    comment_result = shared_data.get('comment', '')

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        interval = int(request.form.get('interval', 10))

        tokens_text = request.form.get('tokens_box', '')
        tokens = [line.strip() for line in tokens_text.strip().split('\n') if line.strip()]

        uploaded_file = request.files.get('comment_file')
        if uploaded_file and uploaded_file.filename != '':
            comment_result = uploaded_file.read().decode('utf-8')
        else:
            comment_text = request.form.get('comment_text', '')
            comment_result = comment_text.strip()

        # Update shared data
        shared_data.update({
            'name': name,
            'interval': interval,
            'tokens': tokens,
            'comment': comment_result
        })

    return render_template_string(HTML,
                                  name=name,
                                  interval=interval,
                                  tokens=tokens,
                                  tokens_text='\n'.join(tokens),
                                  comment_text=comment_text,
                                  comment_result=comment_result)

# ✅ HEALTH CHECK ROUTE
@app.route('/health')
def health():
    return 'OK', 200

# 🔁 BACKGROUND THREAD
def background_worker():
    while True:
        tokens = shared_data.get('tokens', [])
        comment = shared_data.get('comment', '')
        name = shared_data.get('name', '')
        interval = shared_data.get('interval', 10)

        if tokens and comment:
            print(f"[LOOP] Name: {name}, Interval: {interval}s")
            for token in tokens:
                print(f"➡️ Token: {token} | Comment: {comment}")
                # 🛠️ Add your logic here (e.g., post to API, log, etc.)

        time.sleep(max(5, interval))  # Ensure minimum 5 sec to avoid 502

# 🔁 Start background thread
threading.Thread(target=background_worker, daemon=True).start()

# ❌ NO app.run() if using Gunicorn
