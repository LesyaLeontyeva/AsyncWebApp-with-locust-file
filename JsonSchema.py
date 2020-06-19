SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "array",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": [],
    "examples": [
        [
            {
                "id": "lnn",
                "status": "доставлено"
            },
            {
                "id": "p4drt",
                "status": "выполняется"
            }
        ]
    ],
    "additionalItems": True,
    "items": {
        "anyOf": [
            {
                "$id": "#/items/anyOf/0",
                "type": "object",
                "title": "The first anyOf schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "examples": [
                    {
                        "id": "lnn",
                        "status": "доставлено"
                    }
                ],
                "required": [
                    "id",
                    "status"
                ],
                "additionalProperties": True,
                "properties": {
                    "id": {
                        "$id": "#/items/anyOf/0/properties/id",
                        "type": "string",
                        "title": "The id schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "lnn"
                        ]
                    },
                    "status": {
                        "$id": "#/items/anyOf/0/properties/status",
                        "type": "string",
                        "title": "The status schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "доставлено"
                        ]
                    }
                }
            }
        ],
        "$id": "#/items"
    }
}