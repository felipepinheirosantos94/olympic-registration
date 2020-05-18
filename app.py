from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/health_check", methods=["GET", "OPTIONS"])
def health_check():
    return jsonify({"Message": "Success"}), 200
