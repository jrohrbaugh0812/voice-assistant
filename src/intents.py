def get_intent(user_text):
    if "hello" in user_text or "hi" in user_text:
        return "greeting"
    elif "time" in user_text:
        return "time_query"
    return "unknown"
