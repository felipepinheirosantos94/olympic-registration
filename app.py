from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/health_check", methods=["GET"])
def health_check():
    return jsonify({"Message": "Success"}), 200


@app.route("/competition", methods=["POST"])
def register_competition():
    return jsonify({"Message": "Success"}), 201


@app.route("/competition", methods=["PUT"])
def update_competition():
    return jsonify({"Message": "Success"}), 200


@app.route("/competition/<competition_id>", methods=["GET"])
def show_competition(competition_id):
    return jsonify({"Message": "Success"}), 200


@app.route("/competitions", methods=["GET"])
def list_competition():
    return jsonify({"Message": "Success"}), 200