import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Token Input & Comment File Upload</title>
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        max-width: 480px;
        margin: 30px auto;
        padding: 0 15px;
        background: #f0f4f8;
        color: #333;
    }
    h2 {
        color: #2c3e50;
        text-align: center;
    }
    textarea {
        width: 100%;
        height: 140px;
        padding: 10px;
        font-size: 16px;
        border: 2px solid #3498db;
        border-radius: 6px;
        resize: vertical;
        box-sizing: border-box;
    }
    input[type="file"] {
        display: block;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    button {
        background-color: #3498db;
        color: white;
        font-size: 18px;
        padding: 10px 25px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        width: 100%;
        transition: background-color 0.3s ease;
    }
    button:hover {
        background-color: #2980b9;
    }
    .output {
        background-color: #ecf0f1;
        border-left: 5px solid #3498db;
        padding: 15px;
        margin-top: 20px;
        white-space: pre-wrap;
        border-radius: 5px;
        font-family: monospace;
        color: #2c3e50;
    }
    label {
        font-weight: 600;
        margin-top: 15px;
        display: block;
        color: #34495e;
    }
</style>
</head>
<body>
    <h2>Enter Tokens or Upload Comment File</h2>
    <form method="POST" enctype="multipart/form-data">
        <label for="tokens_box">Tokens (One per line):</label>
        <textarea id="tokens_box" name="tokens_box" placeholder="Enter tokens line by line...">{{ tokens_text }}</textarea>

        <label for="comment_file">Or Upload Comment File (.txt):</label>
        <input type="file" id="comment_file" name="comment_file" accept=".txt" />

        <button type="submit">Submit</button>
    </form>

    {% if tokens %}
        <h3>Received Tokens:</h3>
        <div class="output">{{ tokens|join('\\n') }}</div>
    {% endif %}

    {% if comment_file_content %}
        <h3>Comment File Content:</h3>
        <div class="output">{{ comment_file_content }}</div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    tokens = None
    comment_file_content = None
    tokens_text = ""

    if request.method == 'POST':
        tokens_text = request.form.get('tokens_box', '')
        if tokens_text.strip():
            tokens = [line.strip() for line in tokens_text.strip().split('\n') if line.strip()]

        uploaded_file = request.files.get('comment_file')
        if uploaded_file and uploaded_file.filename != '':
            comment_file_content = uploaded_file.read().decode('utf-8')

    return render_template_string(HTML, tokens=tokens, comment_file_content=comment_file_content, tokens_text=tokens_text)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
