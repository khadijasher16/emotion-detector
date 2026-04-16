from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

positive_words = ["good", "happy", "great", "love", "excellent", "amazing"]
negative_words = ["bad", "sad", "hate", "angry", "worst", "terrible"]

def analyze_sentiment(text):
    text = text.lower().split()

    score = 0
    for word in text:
        if word in positive_words:
            score += 1
        elif word in negative_words:
            score -= 1

    total = len(text) if len(text) > 0 else 1
    percent = int((abs(score) / total) * 100)

    if score > 0:
        return "Positive", min(percent + 50, 100)
    elif score < 0:
        return "Negative", min(percent + 50, 100)
    else:
        return "Neutral", 50


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data["text"]

    sentiment, percent = analyze_sentiment(text)

    return jsonify({
        "sentiment": sentiment,
        "percent": percent
    })


if __name__ == "__main__":
    app.run(debug=True)