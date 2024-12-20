import spacy

nlp = spacy.load("en_core_web_sm")


def get_intent(user_text):
    doc = nlp(user_text)
    user_text = user_text.lower()

    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    time_queries = ["time", "clock", "what time", "current time", "tell me the time"]
    browser_queries = ["browser"]

    for token in doc:
        if any(greet in user_text for greet in greetings):
            return "greeting"
        elif any(time_query in user_text for time_query in time_queries):
            return "time_query"
        elif any(browser_query in user_text for browser_query in browser_queries):
            return "browser"

    return "unknown"
