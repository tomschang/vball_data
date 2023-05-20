import jsonschema
import json
import os

scheme = {
    "title": "Plays",
    "description": "A list of possible plays in some game.",
    "type": "array",
    "items": {
        "description": "One possible play.",
        "type": "object",
        "properties": {
            "play_name": {
                "type": "string",
            },
            "key_bind": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1,
            },
            "quality_options": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "quality_name": {
                            "type": "string",
                        },
                        "key_bind": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 1,
                        },
                        "value": {
                            "type": "integer",
                        },
                        "point_value": {
                            "type": "integer",
                        },
                    },
                    "required": ["quality_name", "key_bind", "point_value"],
                },
                "uniqueItems": True,
            },
        },
        "required": [
            "play_name",
            "key_bind",
            "quality_options",
        ],
    },
    "minItems": 1,
    "uniqueItems": True,
}


dirname = os.path.dirname(__file__)


def validate_json(fname):
    json_file = open(os.path.join(dirname, fname))
    plays = json.load(json_file)
    jsonschema.validate(plays, scheme)
