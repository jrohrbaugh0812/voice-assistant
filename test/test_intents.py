import unittest
from intents import get_intent


class TestIntents(unittest.TestCase):
    def setUp(self):
        pass

    def test_greeting_intent(self):
        sentences = [
            "Hello!",
            "Hey, how's it going?",
            "Hi there!",
            "Good morning, can you help me?",
            "Hey, I need your assistance.",
        ]
        for sentence in sentences:
            with self.subTest(sentence=sentence):
                self.assertEqual(get_intent(sentence), "greeting")

    def test_time_query_intent(self):
        sentences = [
            "What time is it now?",
            "Can you tell me the current time?",
            "What's the time?",
            "Check the clock for me.",
            "I need to know the time.",
        ]
        for sentence in sentences:
            with self.subTest(sentence=sentence):
                self.assertEqual(get_intent(sentence), "time_query")

    def test_browser_intent(self):
        sentences = [
            "Open the browser, please.",
            "Can you launch a browser window?",
            "Start the browser for me.",
            "I need you to open the internet browser.",
            "Launch Chrome or any browser.",
        ]
        for sentence in sentences:
            with self.subTest(sentence=sentence):
                self.assertEqual(get_intent(sentence), "browser")

    def test_file_explorer_intent(self):
        sentences = [
            "Open the file explorer.",
            "I need to access my files.",
            "Can you launch the file explorer for me?",
            "Start file manager.",
            "Please open my folders.",
        ]
        for sentence in sentences:
            with self.subTest(sentence=sentence):
                self.assertEqual(get_intent(sentence), "file_explorer")

    def test_note_intent(self):
        sentences = [
            "Save this note for me.",
            "Remember this: Buy groceries.",
            "Write this down: Call the doctor.",
            "I need to save a note.",
            "Can you keep this information for me?",
        ]
        for sentence in sentences:
            with self.subTest(sentence=sentence):
                self.assertEqual(get_intent(sentence), "note")

    def test_email_intent(self):
        sentences = [
            "Send an email to my boss.",
            "Hey, can you help me write an email?",
            "I want to start composing an email.",
            "Send an important email for me.",
            "Can you email my friend about the meeting?",
        ]
        for sentence in sentences:
            with self.subTest(sentence=sentence):
                self.assertEqual(get_intent(sentence), "email")

    def test_weather_intent(self):
        sentences = [
            "What's the weather like today?",
            "Tell me about the current weather.",
            "Is it going to rain?",
            "What's the temperature outside?",
            "Do I need an umbrella today?",
        ]
        for sentence in sentences:
            with self.subTest(sentence=sentence):
                self.assertEqual(get_intent(sentence), "weather")

    def test_detailed_weather_intent(self):
        sentences = [
            "Give me a detailed weather forecast.",
            "Can you provide me with the extended weather forecast?",
            "What's the weather forecast for the next week?",
            "Tell me the detailed weather conditions for today.",
            "I need a detailed breakdown of the weather.",
        ]
        for sentence in sentences:
            with self.subTest(sentence=sentence):
                self.assertEqual(get_intent(sentence), "detailed_weather")

    def test_end_intent(self):
        sentences = [
            "Goodbye!",
            "Bye, see you later!",
            "Exit.",
            "Quit.",
            "I'm done, thanks!",
        ]
        for sentence in sentences:
            with self.subTest(sentence=sentence):
                self.assertEqual(get_intent(sentence), "end")

    def test_unknown_intent(self):
        sentences = [
            "Can you sing a song for me?",
            "What do you think about artificial intelligence?",
            "Launch the browser and tell me the weather.",
            "Write down a note and send an email.",
            "I want to know the weather and the time.",
        ]
        for sentence in sentences:
            with self.subTest(sentence=sentence):
                self.assertEqual(get_intent(sentence), "unknown")


if __name__ == "__main__":
    unittest.main()