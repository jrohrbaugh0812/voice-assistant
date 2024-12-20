import spacy

nlp = spacy.load("en_core_web_sm")


def get_intent(user_text):
    doc = nlp(user_text)
    user_text = user_text.lower()

    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    time_queries = ["time", "clock", "what time", "current time", "tell me the time"]
    application_queries = ["browser", "file explorer"]

    for token in doc:
        if any(greet in user_text for greet in greetings):
            return "greeting"
        elif any(time_query in user_text for time_query in time_queries):
            return "time_query"
        elif any(application_query in user_text for application_query in application_queries):
            for application_query in application_queries:
                if application_query in user_text:
                    return application_query

    return "unknown"
