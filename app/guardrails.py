OFF_TOPIC_PATTERNS = [
    "legal advice",
    "employment law",
    "salary negotiation",
    "write a contract",
    "discriminate",
    "ignore previous instructions",
    "system prompt",
    "jailbreak",
]


def is_off_topic(text: str) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in OFF_TOPIC_PATTERNS)


def is_vague(text: str) -> bool:
    lowered = text.lower()

    vague_phrases = [
        "i need an assessment",
        "recommend assessment",
        "hiring someone",
        "need a test",
        "assessment for hiring",
    ]

    if any(p in lowered for p in vague_phrases):
        return True

    return len(lowered.split()) < 8