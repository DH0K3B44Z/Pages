from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Auto Comment Tool</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f2f2f2; padding: 40px; }
        .container { max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #333; }
        input[type=text], input[type=number], textarea {
            width: 100%; padding: 10px; margin: 10px 0 20px; border: 1px solid #ccc; border-radius: 6px;
        }
        input[type=submit] {
            background-color: #1877f2; color: white; padding: 10px 20px;
            border: none; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px;
        }
        input[type=submit]:hover {
            background-color: #145ec2;
        }
        .footer { text-align: center; font-size: 12px; color: #888; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔥 Facebook Auto Comment Tool</h2>
        <form action="/start" method="post" enctype="multipart/form-data">
            <label>🔑 Access Token:</label>
            <input type="text" name="token" required>

            <label>📝 comment.txt File:</label>
            <input type="file" name="comment_file" required>

            <label>😡 Hater's Name (optional):</label>
            <input type="text" name="hater_name">

            <label>🧾 Post ID:</label>
            <input type="text" name="post_id" required>

            <label>⏱ Time Interval (in seconds):</label>
            <input type="number" name="interval" value="60" min="1" required>

            <input type="submit" value="🚀 Start Commenting">
        </form>
        <div class="footer">&copy; 2025 Saiim Lejend Tools</div>
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/start", methods=["POST"])
def start():
    token = request.form.get("token")
    hater_name = request.form.get("hater_name", "")
    post_id = request.form.get("post_id")
    interval = int(request.form.get("interval", 60))

    comment_file = request.files['comment_file']
    comments = comment_file.read().decode("utf-8").splitlines()

    def comment_on_post(token, post_id, message):
        url = f"https://graph.facebook.com/{post_id}/comments"
        payload = {'message': message, 'access_token': token}
        r = requests.post(url, data=payload)
        return r.status_code, r.text

    for comment in comments:
        final_comment = f"{hater_name} {comment}" if hater_name else comment
        status_code, response = comment_on_post(token, post_id, final_comment)
        print(f"[+] Sent comment: {final_comment} → Status: {status_code}, Response: {response}")
        time.sleep(interval)

    return "✅ Commenting started in background. Check logs."

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
