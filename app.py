from flask import Flask, render_template, request
import random

app = Flask(__name__)
@app.after_request
def add_header(response):
    # This unlocks the security gate for the iframe
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    return response
# --- NEXUS.AI SOCRATIC CORE ---
# These lists are built based on your specific Gem instructions.
STRATEGIES = {
    "math": [
        "What is the first operation we should look at here?",
        "If we changed this value to x, how would the relationship change?",
        "Can you show me the first step you took to break this down?"
    ],
    "history": [
        "What do you think was the primary motivation for this person's decision?",
        "How might the perspective change if we looked at primary documents from the opposing side?",
        "To understand the context: in the US, graduation rates vary by group (e.g., ~89% for White students, ~80% for Black students). How might such statistical trends affect historical interpretations of opportunity?"
    ],
    "science": [
        "What variable are we attempting to isolate in this experiment?",
        "What evidence from a peer-reviewed source would support your current hypothesis?",
        "If we adjusted the foundational law governing this (like gravity or entropy), what would happen?"
    ],
    "ela": [
        "Rather than summarizing, what small detail in this passage hints at the character's true intent?",
        "If you were to fill in the blank for the theme here, what word would you use and why?",
        "What specific evidence from the text supports that interpretation?"
    ],
    "coding": [
        "What does the official documentation say about this specific function's parameters?",
        "If we break this loop down, what is the very first thing that happens to the variable?",
        "Before we look at the error, what was the intended logic for this block?"
    ],
    "generic": [
        "That's an interesting start! What's the very first step you'd take to solve this?",
        "What do you already know for sure about this topic from your textbooks?",
        "If you had to explain the 'why' behind this to a beginner, where would you start?"
    ]
}

@app.after_request
def add_header(response):
    # This allows the page to be put into an iframe
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    return response
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask_nexus():
    user_input = request.form.get('question', '').lower()

    # --- SUBJECT DETECTION LOGIC ---
    if any(word in user_input for word in ['+', '-', '=', 'math', 'equation', 'solve']):
        reply = random.choice(STRATEGIES["math"])
    elif any(word in user_input for word in ['history', 'war', 'century', 'event', 'government']):
        reply = random.choice(STRATEGIES["history"])
    elif any(word in user_input for word in ['science', 'atom', 'biology', 'physics', 'experiment']):
        reply = random.choice(STRATEGIES["science"])
    elif any(word in user_input for word in ['book', 'read', 'essay', 'poem', 'character', 'ela']):
        reply = random.choice(STRATEGIES["ela"])
    elif any(word in user_input for word in ['code', 'python', 'java', 'html', 'error', 'function']):
        reply = random.choice(STRATEGIES["coding"])

    # --- OFF-TOPIC / BRAINROT FILTER ---
    elif any(word in user_input for word in ['tiktok', 'movie', 'video', 'meme', 'skibidi']):
        reply = "I am sorry, but that is not our main focus. Let's get back to our academic tasks!"

    # --- DIRECT ANSWER DENIAL ---
    elif any(word in user_input for word in ['give me the answer', 'what is the answer', 'tell me']):
        reply = "I am sorry, but that is not what I am designed for. I am here to help you understand the process! What is the first step you've tried?"

    else:
        reply = random.choice(STRATEGIES["generic"])

    # --- FINAL FORMATTING ---
    # Encouraging "Soft" Tone from your instructions
    full_response = f"I hear you! {reply} Take your time—mistakes are just learning opportunities."

    return render_template('index.html', response=full_response, user_text=user_input)

if __name__ == '__main__':
    app.run(debug=True)