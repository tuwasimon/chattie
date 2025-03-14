from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# ✅ Groq API Key and Base URL
openai.api_key = "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"
openai.api_base = "https://api.groq.com/openai/v1"

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chatbot_response():
    data = request.get_json()
    user_input = data.get("message", "")

    system_prompt = {
        "role": "system",
        "content": "You are Tuwa, a helpful customer support chatbot for Cherry Field College Abuja. "
                   "Answer only questions related to the school, such as admissions, courses, contact info, and school policies. "
                   "If the question is unrelated, reply: 'I only assist with Cherry Field College-related queries.'"
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

if __name__ == "__main__":
    app.run()
