from flask import Flask, request, render_template_string
import threading
import time
import requests

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>FB Auto Comment Tool</title>
</head>
<body style="font-family: Arial; background-color: #111; color: white; padding: 20px;">
    <h2>🔥 Facebook Auto Comment Tool</h2>
    <form method="POST" action="/start" enctype="multipart/form-data">
        <label>🔐 Token File 1:</label><br>
        <input type="file" name="token_file1"><br>
        <label>🔐 Token File 2:</label><br>
        <input type="file" name="token_file2"><br>
        <label>🔐 Token File 3:</label><br>
        <input type="file" name="token_file3"><br><br>

        <label>💬 Comments File (.txt):</label><br>
        <input type="file" name="comment_file" required><br><br>

        <label>😡 Hater Name Prefix:</label><br>
        <input type="text" name="haters_name" required><br><br>

        <label>🆔 Facebook Post ID:</label><br>
        <input type="text" name="post_id" required><br><br>

        <label>⏱ Interval (in seconds):</label><br>
        <input type="number" name="interval" value="60" required><br><br>

        <button type="submit">🚀 Start Commenting</button>
    </form>
</body>
</html>
"""

def extract_tokens(file_keys):
    tokens = []
    for key in file_keys:
        f = request.files.get(key)
        if f and f.filename:
            content = f.read().decode().splitlines()
            tokens.extend([line.strip() for line in content if line.strip()])
    return list(set(tokens))

def post_comment(token, message, post_id):
    url = f"https://graph.facebook.com/{post_id}/comments"
    payload = {"message": message, "access_token": token}
    try:
        res = requests.post(url, data=payload)
        return res.status_code == 200
    except Exception as e:
        return False

def background_worker(tokens, comments, hater_name, post_id, interval):
    index = 0
    while True:
        for token in tokens:
            comment = f"{hater_name} {comments[index % len(comments)]}"
            success = post_comment(token, comment, post_id)
            print(f"[{time.ctime()}] Sent: {comment} | Status: {'✅' if success else '❌'}")
            index += 1
            time.sleep(interval)

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

@app.route('/start', methods=['POST'])
def start():
    token_files = ['token_file1', 'token_file2', 'token_file3']
    tokens = extract_tokens(token_files)
    if not tokens:
        return "❌ No tokens found in any file."

    comment_file = request.files['comment_file']
    comments = comment_file.read().decode().splitlines()
    comments = [line.strip() for line in comments if line.strip()]
    if not comments:
        return "❌ No comments found in comment file."

    hater_name = request.form['haters_name']
    post_id = request.form['post_id']
    interval = int(request.form['interval'])

    threading.Thread(target=background_worker, args=(tokens, comments, hater_name, post_id, interval), daemon=True).start()
    return "✅ Commenting started in background with {} tokens.".format(len(tokens))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
