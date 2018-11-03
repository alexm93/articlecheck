
_objects = ["text", "category"]
_properties = ["content", "length", "title"]
_expressions = [
    "contains",
    "not_contains",
    "more",
    "less",
    "equal",
    "in",
    "not_in"
]

CONDITIONS_SCHEMA = {
    "id": "conditions",
    "type": "object",
    "properties": {
        "article": {"type": "string"},
        "conditions": {
            "type": "object",
            "properties": {
                "operator": {"type": "string", "enum": ["or", "and"]},
                "rules": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "object": {"type": "string", "enum": _objects},
                            "property": {"type": "string", "enum": _properties},
                            "expression": {"type": "string", "enum": _expressions},
                            "value": {}
                        },
                        "required": ["object", "property", "expression", "value"]
                    }
                },
                "groups": {
                    "type": "array",
                    "items": {"$ref": "#/properties/conditions"}
                }
            },
            "required": ["operator"]
        }
    },
    "required": ["article", "conditions"]
}
