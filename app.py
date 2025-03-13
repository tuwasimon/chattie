from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# ✅ Set Groq API key and API base URL
openai.api_key = "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"
openai.api_base = "https://api.groq.com/openai/v1"  # ✅ Fix API base for Groq

@app.route("/")
def index():
    return render_template("chat.html")  # Ensure 'templates/chat.html' exists

@app.route("/chat", methods=["POST"])
def chatbot_response():
    data = request.get_json()
    user_input = data.get("message", "")

    # ✅ Restrict bot to only school-related questions
    system_prompt = {
        "role": "system",
        "content": "You are a school chatbot. Answer only school-related questions. "
                   "If a question is unrelated to school, respond with 'I can only answer school-related questions.'"
    }

    try:
        response = openai.ChatCompletion.create(
            model="llama3-8b-8192",
            messages=[system_prompt, {"role": "user", "content": user_input}],
            max_tokens=50  # ✅ Keep responses short and precise
        )

        bot_reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": bot_reply})

    except Exception as e:  # ✅ Handles errors correctly
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
