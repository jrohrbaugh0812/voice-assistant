import spacy

# Load SpaCy's English model
nlp = spacy.load("en_core_web_sm")

# Intent mapping with keywords
INTENT_KEYWORDS = {
    "greeting": ["hello", "hi", "hey", "morning", "afternoon", "evening"],
    "time_query": ["what time", "current time", "tell me the time", "clock"],
    "browser": ["open browser", "launch browser", "start browser"],
    "file_explorer": ["open file explorer", "launch file explorer", "explorer"],
    "note": ["save note", "remember this", "write this down"],
    "email": ["send email", "start email", "write an email"],
    "weather": ["weather", "forecast", "temperature", "rain", "sunny"],
    "detailed_weather": ["detailed weather", "specific forecast"],
    "end": ["bye", "quit", "exit", "goodbye", "later"],
}

# Priority of intents when multiple matches occur
INTENT_PRIORITY = [
    "email",  # Prioritize actionable intents like sending an email
    "detailed_weather",  # More specific weather query comes before general weather
    "weather",
    "time_query",
    "browser",
    "file_explorer",
    "note",
    "end",
    "greeting",  # Generic greetings have lower priority
]


def get_intent(user_text):
    doc = nlp(user_text.lower())

    # Extract lemmatized tokens from the user input
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]

    matched_intents = []

    # Check for matches with INTENT_KEYWORDS
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in " ".join(tokens):
                matched_intents.append(intent)
                break  # Avoid duplicate matches for the same intent

    if not matched_intents:
        return "unknown"

    # Resolve conflicts by using the priority list
    for priority_intent in INTENT_PRIORITY:
        if priority_intent in matched_intents:
            return priority_intent

    return "unknown"