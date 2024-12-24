from flask import Flask, request, jsonify
import random
import datetime
import uuid
import re

app = Flask(__name__)

# In-memory storage for user sessions (no database)
user_sessions = {}

# Function to recognize entities (e.g., names, dates)
def extract_entities(user_input):
    name_match = re.search(r"my name is (\w+)", user_input)
    date_match = re.search(r"on (\d{1,2} \w+ \d{4})", user_input)  # Match dates like "on 24 December 2024"
    
    name = name_match.group(1) if name_match else None
    date = date_match.group(1) if date_match else None

    return {"name": name, "date": date}

# Chatbot logic with advanced features
def chatbot_response(user_input, user_id):
    user_input = user_input.lower()
    user_name = user_sessions.get(user_id, {}).get("name", "Guest")

    # Greetings and Introduction
    greetings = ["hello", "hi", "hey", "greetings", "sup", "good morning", "good evening"]
    if any(greeting in user_input for greeting in greetings):
        return f"Hi {user_name}! How can I assist you today?"

    # Handle the extraction of entities like names and dates
    entities = extract_entities(user_input)
    if entities["name"]:
        user_sessions[user_id]["name"] = entities["name"]
        return f"Nice to meet you, {entities['name']}! How can I assist you today?"

    if entities["date"]:
        return f"Are you asking about events on {entities['date']}? Please clarify."

    # Craft-related topics
    craft_keywords = ["craft", "painting", "pottery", "woodwork", "stonework", "handmade", "art"]
    if any(keyword in user_input for keyword in craft_keywords):
        return "I see you're interested in crafts! We have woodwork, pottery, stonecraft, and paintings. What would you like to know more about?"

    # Specific craft categories
    if "woodwork" in user_input:
        return "Woodwork is beautiful! Would you like to explore wooden furniture or wooden sculptures?"
    if "stonework" in user_input:
        return "Stonecraft is ancient and beautiful. Are you interested in stone sculptures or decorative pieces?"
    if "pottery" in user_input:
        return "Pottery is fascinating! Would you like to know about techniques or the history of pottery?"
    if "painting" in user_input:
        return "Painting is a rich art form. Do you prefer oil painting, watercolors, or something else?"

    # Small talk: Time and Weather
    if "time" in user_input:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}. How else can I assist you?"
    elif "weather" in user_input:
        return "I recommend checking a weather app for real-time weather updates."

    # Answering casual questions (e.g., small talk, jokes)
    small_talk = {
        "how are you": ["I'm doing great, thanks!", "I'm here and ready to help!", "I'm just a bot, but I'm feeling good!"],
        "thank you": ["You're welcome!", "Glad I could help!", "Anytime!"],
        "funny": ["Why don't skeletons fight each other? They don't have the guts!", "Why did the computer go to the doctor? It had a virus!"]
    }

    for key in small_talk:
        if key in user_input:
            return random.choice(small_talk[key])

    # Casual compliments
    if "you're great" in user_input or "you're awesome" in user_input:
        return random.choice([
            "Aww, thank you! You're awesome too!",
            "You're too kind! I'm always here to help.",
            "Thanks! I'm just doing my job, but you're amazing for saying that!"
        ])

    # Handling questions about the bot
    if "who are you" in user_input or "what are you" in user_input:
        return "I am a friendly chatbot here to assist you with craft-related questions and more."

    # Fallback if no other conditions match
    return "I didn't quite understand that. Could you ask something else?"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    user_input = data.get("message", "")
    user_id = data.get("user_id", str(uuid.uuid4()))  # Use a unique user ID for each session
    user_sessions.setdefault(user_id, {})  # Ensure the user session exists
    response = chatbot_response(user_input, user_id)
    return jsonify({"reply": response, "user_id": user_id})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
