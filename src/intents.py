import spacy

nlp = spacy.load("en_core_web_sm")


def get_intent(user_text):
    doc = nlp(user_text)
    user_text = user_text.lower()

    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    time_queries = ["time", "clock", "what time", "current time", "tell me the time"]
    application_queries = ["browser", "file explorer"]
    endings = ["bye", "end", "quit", "exit", "goodbye", "later"]

    for token in doc:
        if any(greet in user_text for greet in greetings):
            return "greeting"
        elif any(time_query in user_text for time_query in time_queries):
            return "time_query"
        elif any(query in user_text for query in application_queries):
            return "browser" if "browser" in user_text else "file_explorer"
        elif any(ending in user_text for ending in endings):
            return "end"

    return "unknown"
