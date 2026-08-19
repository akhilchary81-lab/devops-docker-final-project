from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>DevOps Training Application</h1>
    <p><strong>Application Status:</strong> Running</p>
    <p><strong>Environment:</strong> Development</p>
    <p><strong>Database:</strong> Connected</p>
    """


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "running"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
