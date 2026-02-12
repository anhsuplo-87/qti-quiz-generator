from jsonschema import Draft7Validator

QUESTION_SCHEMA = {
    "type": "object",
    "required": ["question", "options", "answer"],
    "properties": {
        "question": {
            "type": "string"
        },
        "images": {
            "type": "array",
            "items": {"type": "string"},
            "default": []
        },
        "options": {
            "type": "array",
            "minItems": 2,
            "items": {
                "oneOf": [
                    {"type": "string"},
                    {
                        "type": "object",
                        "required": ["text"],
                        "properties": {
                            "text": {"type": "string"},
                            "images": {
                                "type": "array",
                                "items": {"type": "string"},
                                "default": []
                            }
                        },
                        "additionalProperties": False
                    }
                ]
            }
        },
        "answer": {
            "type": ["string", "integer"]
        }
    },
    "additionalProperties": False
}


def validate_question_json(data: dict):
    validator = Draft7Validator(QUESTION_SCHEMA)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

    if errors:
        error_messages = []
        for error in errors:
            path = " -> ".join(map(str, error.path))
            error_messages.append(f"[{path}] {error.message}")

        raise ValueError(
            "JSON validation failed:\n" + "\n".join(error_messages)
        )
