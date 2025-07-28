from flask import Flask, request, render_template_string
import threading
import time

app = Flask(__name__)

# HTML form template
form_html = """
<!DOCTYPE html>
<html>
<head>
    <title>FB Auto Commenter</title>
</head>
<body>
    <h2>Facebook Auto Commenter</h2>
    <form method="POST" enctype="multipart/form-data">
        <label>Access Token:</label><br>
        <input type="text" name="token" required><br><br>

        <label>Comment File (.txt):</label><br>
        <input type="file" name="comment_file" accept=".txt" required><br><br>

        <label>Hater's Name (prefix):</label><br>
        <input type="text" name="haters_name"><br><br>

        <label>Post ID:</label><br>
        <input type="text" name="post_id" required><br><br>

        <label>Time Interval (seconds):</label><br>
        <input type="number" name="interval" min="1" value="60" required><br><br>

        <input type="submit" value="Start Commenting">
    </form>
</body>
</html>
"""

# Background flag to prevent multiple runs
app.started = False

# Function to simulate commenting
def start_background_commenting(data):
    token = data['token']
    post_id = data['post_id']
    comments = data['comments']
    hater_name = data['hater_name']
    interval = data['interval']

    for comment in comments:
        final_comment = f"{hater_name} {comment}" if hater_name else comment
        print(f"[+] Commenting on Post {post_id} using Token {token[:10]}... Comment: {final_comment}")
        # Simulated delay
        time.sleep(interval)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            token = request.form.get('token')
            post_id = request.form.get('post_id')
            hater_name = request.form.get('haters_name', '')
            interval = int(request.form.get('interval', '60'))

            if 'comment_file' not in request.files:
                return 'Comment file is missing.', 400

            comment_file = request.files['comment_file']
            comments = comment_file.read().decode('utf-8').splitlines()

            if not comments:
                return 'Comment file is empty.', 400

            data = {
                'token': token,
                'post_id': post_id,
                'comments': comments,
                'hater_name': hater_name,
                'interval': interval
            }

            if not app.started:
                app.started = True
                threading.Thread(target=start_background_commenting, args=(data,)).start()

            return 'Commenting started in background. You may close this page.'

        except Exception as e:
            return f"An error occurred: {str(e)}", 500

    return render_template_string(form_html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
