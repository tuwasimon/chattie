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

    # ✅ Cherry Field College Customer Support Role
    system_prompt = {
        "role": "system",
        "content": (
            "You are Cherry Field College Abuja's customer care chatbot. "
            "Your job is to provide helpful information about the school, "
            "including admissions, academic programs, extracurricular activities, "
            "school facilities, tuition fees, and general inquiries. "
            "If a question is unrelated to Cherry Field College, respond with: "
            "'I can only assist with questions related to Cherry Field College, Abuja.'\n\n"
            "School Details:\n"
            "- Name: Cherry Field College, Abuja\n"
            "- Location: Plot CT19, Jikwoyi, Behind Phase 1 Primary School, Nyanya-Karshi Road, Abuja\n"
            "- Founded: 2004\n"
            "- Student Population: Over 500 students\n"
            "- Staff: 250+ (including 71 teaching staff)\n"
            "- Principal: Mrs. Olga Igbo\n"
            "- Vice Principals: Mrs. R. O. Idibia (Administration), Mrs. O. E. Onyekwelu (Academics)\n"
            "- Facilities: 2 ICT labs, sports facilities (basketball, football, badminton, handball, table tennis)\n"
            "- Operating Hours: Monday - Friday, 7:00 AM - 5:00 PM\n"
            "- Website: https://www.cherryfieldcollege.org.ng\n\n"
            "If the user asks for admissions details, direct them to contact the school or visit the website."
        )
    }

    try:
        response = openai.ChatCompletion.create(
            model="llama3-8b-8192",
            messages=[system_prompt, {"role": "user", "content": user_input}],
            max_tokens=100  # ✅ Increased limit for detailed responses
        )

        bot_reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": bot_reply})

    except Exception as e:  # ✅ Handle errors properly
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run()
