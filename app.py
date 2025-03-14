from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# ✅ Set Groq API key
openai.api_key = "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"
openai.api_base = "https://api.groq.com/openai/v1"  # ✅ Correct API base

@app.route("/")
def index():
    return render_template("chat.html")  # ✅ Ensure chat.html exists in 'templates' folder

@app.route("/chat", methods=["POST"])
def chatbot_response():
    data = request.get_json()
    user_input = data.get("message", "")

    # ✅ Bot's role as Cherry Field College customer support
    system_prompt = {
        "role": "system",
        "content": "You are Tuwa, a friendly customer support chatbot for Cherry Field College Abuja. "
                   "Assist with admissions, school fees, curriculum, and general inquiries. "
                   "If a question is unrelated to the school, respond with 'I only assist with Cherry Field College inquiries.'"
    }

    try:
        response = openai.ChatCompletion.create(
            model="llama3-8b-8192",
            messages=[system_prompt, {"role": "user", "content": user_input}],
            max_tokens=50  # ✅ Keep responses clear and concise
        )

        bot_reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": bot_reply})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run()
