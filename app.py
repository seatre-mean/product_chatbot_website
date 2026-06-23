from flask import Flask, render_template, request, jsonify
from difflib import SequenceMatcher
from pathlib import Path
import json
import re

app = Flask(__name__)

DATA_PATH = Path(__file__).parent / "data" / "product_info.json"


def load_product_data():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9₹$.\s]", " ", text)
    return " ".join(text.split())


def similarity(a, b):
    return SequenceMatcher(None, clean_text(a), clean_text(b)).ratio()


def keyword_score(message, keywords):
    message = clean_text(message)
    score = 0

    for keyword in keywords:
        keyword = clean_text(keyword)
        if keyword and keyword in message:
            score += 0.35

    return score


def get_suggestions(product_data):
    return [faq["question"] for faq in product_data["faqs"][:4]]


def get_bot_reply(user_message):
    product_data = load_product_data()
    message = clean_text(user_message)

    if not message:
        return {
            "reply": "Please type a question.",
            "suggestions": get_suggestions(product_data)
        }

    greetings = ["hi", "hello", "hey", "hii", "good morning", "good evening"]
    if message in greetings:
        return {
            "reply": f"Hi! I am the {product_data['product_name']} assistant. You can ask me about price, features, download, refund, or support.",
            "suggestions": get_suggestions(product_data)
        }

    best_faq = None
    best_score = 0

    for faq in product_data["faqs"]:
        question_match = similarity(message, faq["question"])
        keyword_match = keyword_score(message, faq.get("keywords", []))
        total_score = question_match + keyword_match

        if total_score > best_score:
            best_score = total_score
            best_faq = faq

    if best_faq and best_score >= 0.35:
        return {
            "reply": best_faq["answer"],
            "matched_question": best_faq["question"],
            "confidence": round(best_score, 2),
            "suggestions": get_suggestions(product_data)
        }

    fallback = (
        "Sorry, I could not find the exact answer. "
        f"You can ask about price, features, download, refund, or contact support at {product_data['contact_email']}."
    )

    return {
        "reply": fallback,
        "suggestions": get_suggestions(product_data)
    }


@app.route("/")
def home():
    product_data = load_product_data()
    return render_template("index.html", product=product_data)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "")
    return jsonify(get_bot_reply(user_message))


@app.route("/api/product")
def api_product():
    return jsonify(load_product_data())


if __name__ == "__main__":
    app.run(debug=True)
