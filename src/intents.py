import spacy
import re

nlp = spacy.load("en_core_web_sm")

# Intent mapping with keywords or patterns
INTENT_PATTERNS = {
    "greeting": [r"\bhello\b", r"\bhi\b", r"\bhey\b", r"good (morning|afternoon|evening)"],
    "time_query": [r"\bwhat time\b", r"\bcurrent time\b", r"\btell me the time\b", r"\bclock\b"],
    "browser": [r"open.*browser", r"launch.*browser"],
    "file_explorer": [r"open.*file explorer", r"launch.*file explorer"],
    "note": [r"\bsave note\b", r"\bremember this\b", r"\bsave this\b"],
    "email": [r"\bsend email\b", "\bemail\b"],
    "weather": [r"\bget weather\b", "\bweather\b"],
    "end": [r"\bbye\b", r"\bend\b", r"\bquit\b", r"\bexit\b", r"\bgoodbye\b", r"\blater\b"],
}


def get_intent(user_text):
    user_text = user_text.lower()

    # Check for matches in the INTENT_PATTERNS dictionary
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, user_text):
                return intent

    return "unknown"
