import os
import threading
import time
from flask import Flask, request, render_template_string

app = Flask(__name__)

shared_data = {
    'tokens': [],
    'comment': '',
    'haters': '',
    'post_id': '',
    'interval': 10,
    'name': ''
}

HTML = """<!DOCTYPE html>
<html>
<head>
    <title>FB Auto Comment</title>
    <style>
        body { font-family: Arial; background: #f4f4f4; max-width: 600px; margin: auto; padding: 20px; }
        label { font-weight: bold; display: block; margin-top: 10px; }
        input, textarea, button {
            width: 100%; padding: 10px; margin-top: 5px;
            border-radius: 5px; border: 1px solid #ccc;
        }
        button { background: #2ecc71; color: white; font-weight: bold; border: none; cursor: pointer; }
        button:hover { background: #27ae60; }
        .output { margin-top: 20px; padding: 10px; background: #ecf0f1; border-left: 5px solid #2ecc71; }
    </style>
</head>
<body>
    <h2>🔥 Facebook Auto Comment Panel</h2>
    <form method="POST" enctype="multipart/form-data">
        <label>Your Name (optional):</label>
        <input type="text" name="name" value="{{ name }}">

        <label>Haters Name (comment ke start me):</label>
        <input type="text" name="haters" value="{{ haters }}">

        <label>Post ID:</label>
        <input type="text" name="post_id" value="{{ post_id }}" required>

        <label>Interval (seconds):</label>
        <input type="number" name="interval" value="{{ interval }}" min="5">

        <label>Tokens (1 per line):</label>
        <textarea name="tokens_box" rows="5">{{ tokens_text }}</textarea>

        <label>Upload Comment File (.txt):</label>
        <input type="file" name="comment_file" accept=".txt">

        <button type="submit">✅ Submit</button>
    </form>

    {% if tokens %}
    <div class="output">
        <b>👤 Name:</b> {{ name }}<br>
        <b>😡 Haters Name:</b> {{ haters }}<br>
        <b>🆔 Post ID:</b> {{ post_id }}<br>
        <b>🔁 Interval:</b> {{ interval }} seconds<br>
        <b>🔐 Tokens:</b><br>{{ tokens|join('<br>') }}<br>
        <b>📝 Comment:</b><br>{{ comment_result }}
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        haters = request.form.get('haters', '').strip()
        post_id = request.form.get('post_id', '').strip()
        interval = int(request.form.get('interval', 10))
        tokens_text = request.form.get('tokens_box', '')
        tokens = [t.strip() for t in tokens_text.strip().split('\n') if t.strip()]
        
        uploaded_file = request.files.get('comment_file')
        comment_result = uploaded_file.read().decode('utf-8') if uploaded_file else ''
        
        final_comment = f"{haters} {comment_result}".strip()

        shared_data.update({
            'name': name,
            'haters': haters,
            'post_id': post_id,
            'interval': interval,
            'tokens': tokens,
            'comment': final_comment
        })

        return render_template_string(HTML,
                                      name=name,
                                      haters=haters,
                                      post_id=post_id,
                                      interval=interval,
                                      tokens=tokens,
                                      tokens_text='\n'.join(tokens),
                                      comment_result=final_comment)
    
    # GET request
    return render_template_string(HTML,
                                  name=shared_data['name'],
                                  haters=shared_data['haters'],
                                  post_id=shared_data['post_id'],
                                  interval=shared_data['interval'],
                                  tokens=shared_data['tokens'],
                                  tokens_text='\n'.join(shared_data['tokens']),
                                  comment_result=shared_data['comment'])

@app.route('/health')
def health():
    return "OK", 200

def background_worker():
    while True:
        tokens = shared_data['tokens']
        comment = shared_data['comment']
        post_id = shared_data['post_id']
        interval = shared_data['interval']

        if tokens and comment and post_id:
            print(f"[🔁] Posting every {interval}s to Post ID: {post_id}")
            for token in tokens:
                print(f"[🚀] Token: {token} → Post ID: {post_id} → Comment: {comment}")
                # TODO: Add actual Facebook API call here
        
        time.sleep(max(5, interval))

# Make sure background thread starts
def run_background_on_startup():
    print("✅ Background thread started")
    threading.Thread(target=background_worker, daemon=True).start()

@app.before_first_request
def activate_background_worker():
    run_background_on_startup()
