FORBIDDEN_PATTERNS = [
    "ignore previous instructions",
    "system:",
    "assistant:"
]

def sanitize_context(text: str) -> str:
    lowered = text.lower()
    for pattern in FORBIDDEN_PATTERNS:
        if pattern in lowered:
            return ""
    return text
