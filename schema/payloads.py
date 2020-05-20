
# JSON Schema for validate payloads

register_competition_payload = {
    "type": "object",
    "properties": {
        "name": {"type" : "string"},
        "modality": {
            "type": "integer",
            "enum": [1, 2]
        },
        "event_date": {"type" : "string"}
    },
}

update_competition_payload = {
    "type": "object",
    "properties": {
        "name": {"type" : "string"},
        "modality": {"type" : "integer"},
        "event_date": {"type" : "string"},
        "status": {
            "type" : "string",
            "enum": ["Open", "Closed", "Running"]
        }
    },
}

register_participant = {
    "type": "object",
    "properties": {
        "athlete": {"type" : "string"},
        "value": {
            "type": "string"
        },
    },
}