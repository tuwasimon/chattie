from flask import Flask, render_template, request, jsonify
import openai
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# ✅ Set Groq API key
openai.api_key = "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"
openai.api_base = "https://api.groq.com/openai/v1"

# ✅ Define bot behavior
system_prompt = {
    "role": "system",
    "content": "You are Punch.cool’s AI assistant. Answer only questions about Punch.cool. "
               "If a question is unrelated, respond with 'I can only answer questions about Punch.cool.'"
}

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chatbot_response():
    data = request.get_json()
    user_input = data.get("message", "")

    try:
        response = openai.ChatCompletion.create(
            model="llama3-8b-8192",
            messages=[system_prompt, {"role": "user", "content": user_input}],
            max_tokens=100
        )

        bot_reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": bot_reply})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

# ✅ Email Support
@app.route("/send_email", methods=["POST"])
def send_email():
    data = request.get_json()
    user_email = data.get("email")
    message = data.get("message")

    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your_email@gmail.com"  # Replace with your email
        sender_password = "your_password"  # Replace with your password

        msg = MIMEText(message)
        msg["Subject"] = "Customer Inquiry - Punch.cool"
        msg["From"] = sender_email
        msg["To"] = "support@punch.cool"

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, "support@punch.cool", msg.as_string())
        server.quit()

        return jsonify({"response": "Your inquiry has been sent successfully."})

    except Exception as e:
        return jsonify({"response": f"Failed to send email: {str(e)}"}), 500

if __name__ == "__main__":
    app.run()
