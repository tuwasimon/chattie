from flask import Flask, render_template, request, jsonify
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# ✅ Groq API configuration
openai.api_key = "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"
openai.api_base = "https://api.groq.com/openai/v1"

# ✅ Email Configuration
EMAIL_HOST = "smtp.gmail.com"  # Change if using another provider
EMAIL_PORT = 587
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_PASSWORD = "your-email-password"  # Use app password if needed

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chatbot_response():
    data = request.get_json()
    user_input = data.get("message", "")

    # ✅ Chatbot role
    system_prompt = {
        "role": "system",
        "content": "You are Tuwa, a customer support assistant for Cherry Field College, Abuja. "
                   "Answer inquiries about the college, admissions, fees, courses, and general school policies."
    }

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

@app.route("/send_email", methods=["POST"])
def send_email():
    data = request.get_json()
    subject = data.get("subject", "No Subject")
    message = data.get("message", "No Message")
    sender_email = data.get("email", "unknown@example.com")

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = f"Customer Inquiry: {subject}"
        msg.attach(MIMEText(f"From: {sender_email}\n\n{message}", "plain"))

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        server.quit()

        return jsonify({"response": "Email sent successfully!"})

    except Exception as e:
        return jsonify({"response": f"Email Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
