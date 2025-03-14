from flask import Flask, render_template, request, jsonify
import openai
from flask_mail import Mail, Message  # ✅ Import Flask-Mail

app = Flask(__name__)

# ✅ Configure Groq API
openai.api_key = "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"
openai.api_base = "https://api.groq.com/openai/v1"

# ✅ Configure Flask-Mail (Use your email credentials)
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # Change for another provider
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "your-email@gmail.com"  # 🔹 Replace with real email
app.config["MAIL_PASSWORD"] = "your-email-password"  # 🔹 Replace with real password
app.config["MAIL_DEFAULT_SENDER"] = "your-email@gmail.com"

mail = Mail(app)  # ✅ Initialize Flask-Mail

@app.route("/")
def index():
    return render_template("chat.html")  # ✅ Ensure 'templates/chat.html' exists

@app.route("/chat", methods=["POST"])
def chatbot_response():
    data = request.get_json()
    user_input = data.get("message", "")

    # ✅ Set bot role
    system_prompt = {
        "role": "system",
        "content": "You are Tuwa, a friendly and helpful customer support assistant for Cherry Field College, Abuja. "
                   "Answer questions about admissions, school fees, location, and general inquiries. "
                   "If the question is unrelated to the school, politely inform the user."
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

# ✅ New Route: Send Email Inquiry
@app.route("/send_email", methods=["POST"])
def send_email():
    data = request.get_json()
    user_name = data.get("name", "User")
    user_email = data.get("email", "")
    user_message = data.get("message", "")

    if not user_email or not user_message:
        return jsonify({"response": "Email and message are required!"}), 400

    try:
        msg = Message(
            subject=f"Inquiry from {user_name}",
            recipients=["support@cherryfieldcollege.com"],  # 🔹 Replace with school's email
            body=f"Name: {user_name}\nEmail: {user_email}\n\nMessage:\n{user_message}",
        )
        mail.send(msg)
        return jsonify({"response": "Your inquiry has been sent successfully!"})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run()
