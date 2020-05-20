from flask import Flask, jsonify, request

app = Flask(__name__)

from Competition import Competition
from Registration import Registration
from schema.payloads import register_competition_payload, update_competition_payload
from config import modalities
import json
from jsonschema import validate

@app.route("/health_check", methods=["GET"])
def health_check():
    return jsonify({"Message": "Success"}), 200


@app.route("/competition", methods=["POST"])
def register_competition():
    payload = request.get_json()

    #Validate payload
    try:
        validate(instance=payload, schema=register_competition_payload)
    except:
        return jsonify({'Error': "Invalid payload"}), 400

    competition = Competition()

    competition_data = competition.register_competition(
        name=payload["name"],
        modality=payload["modality"],
        event_date=payload["event_date"]
    )
    return jsonify({'competition_id': competition_data}), 201


@app.route("/competition/<public_id>", methods=["PUT"])
def update_competition(public_id):
    payload = request.get_json()

    #Validate payload
    try:
        validate(instance=payload, schema=update_competition_payload)
    except:
        return jsonify({'Error': "Invalid payload"}), 400

    competition = Competition()
    competition.get_competition_by_public_id(
        public_id=public_id
    )

    competition.update_competition_by_public_id(
        public_id=public_id,
        name=payload["name"],
        modality=payload["modality"],
        event_date=payload["event_date"],
        status=payload["status"]
    )
    return jsonify({'Message': "Success"}), 200


@app.route("/competition/<competition_id>", methods=["GET"])
def show_competition(competition_id):
    competition = Competition()

    competition_data = competition.get_competition_by_public_id(
        public_id=competition_id
    )
    return jsonify({'entry': competition_data}), 200


@app.route("/competitions", methods=["GET"])
def list_competitions():
    competition = Competition()
    competition_data = competition.get_competitions()
    return jsonify({'entries': competition_data}), 200


@app.route("/competition/<competition_id>/register", methods=["POST"])
def register_for_competition(competition_id):

    payload = request.get_json()
    competition = Competition()

    competition_data = competition.get_competition_by_public_id(
        public_id=competition_id
    )

    if len(competition_data) == 1:
        if competition_data[0]['status'] != "Open":
            return jsonify({'Error': "This competition is closed for registrations"}), 400

        if competition_data[0]['modality'] == modalities["1"]:
            unit = "s"
        else:
            tries_limit = 3
            unit = "m"
    else:
        return jsonify({"Message": "Competition not found. Please check the competition ID"}), 404

    registration = Registration()

    # Check participant tries for this subscription
    tries = registration.count_tries_in_competition(competition_id, payload['atleta'])

    if competition_data[0]['modality'] == modalities["2"] and tries > tries_limit - 1:
        # if tries limit exceeded do not register a new try on this competition
        return jsonify({"Message": f"For {modalities['2']} each person can try only {tries_limit} times"}), 400

    registration_data = registration.register_for_competition(
        competition_id=competition_id,
        athlete=payload["atleta"],
        value=payload["value"],
        unit=unit,
    )
    return jsonify({'registration_id': registration_data}), 201


@app.route("/competition/<competition_id>/registrations", methods=["GET"])
def show_competition_registrations(competition_id):
    registration = Registration()

    competition_data = registration.list_registers_by_competition_id(competition_id)
    return jsonify({'entries': competition_data}), 200


@app.route("/competition/<competition_id>/<registration_id>", methods=["GET"])
def get_registrations(competition_id, registration_id):
    registration = Registration()

    competition_data = registration.get_registrations(competition_id, registration_id)
    return jsonify({'entry': competition_data}), 200


@app.route("/competition/<competition_id>/ranking", methods=["GET"])
def show_competition_results(competition_id):
    registration = Registration()

    competition_data = registration.get_competition_results(competition_id)
    return jsonify({'ranking': competition_data}), 200


if __name__ == "__main__":
    app.run()