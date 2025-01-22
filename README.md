# Voice Assistant
This project is a Python-powered voice assistant for PCs, designed to recognize spoken commands, provide spoken responses, and execute relevant actions. The project is being actively developed to add new functionality and features and improve accuracy.

> 🚧 **Work in Progress**  
> This project is actively being developed and is not yet complete.

## Current Features
- Voice Recognition: Accurately recognizes spoken commands using a speech recognition library.
- Command Execution: Responds to specific intents such as:
  - Greeting the user.
  - Telling the current time.
  - Opening the default web browser.
  - Launching the file explorer and opening selected files.
  - Saving notes to be remembered later.
  - Fetches weather data from user-defined locations.
  - Exiting the program with a farewell.
  - And much more!
- Text-to-Speech Responses: Delivers audible feedback using a text-to-speech engine.
- Flexible Input Recognition: Adapts to variations in user input, such as different phrasings for the same command.
  
## How It Works
1. Listening for Commands: The program starts listening when a designated hotkey is pressed, which is currently set to **CTRL+SHIFT+SPACE**.
2. Processing Input:
   - Captures speech input and converts it into text.
   - Determines the user's intent using natural language processing (NLP) with a Spacy-based system.
3. Executing Actions: Matches the detected intent to pre-defined commands and performs the associated action.
4. Providing Feedback: Uses the pyttsx3 library to provide audible responses.

## Technologies Used
- Python: Core language for development.
- SpeechRecognition: Converts speech to text.
- Pyttsx3: Provides text-to-speech capabilities.
- Spacy: Natural Language Processing for intent detection.
- Keyboard: Handles hotkey activation.
- Tkinter: File explorer integration.
- Browser: Opens the default web browser.

## Planned Features
- Support for additional commands and applications.
- Improved flexibility and accuracy in command recognition.
- Enhanced configuration options for hotkeys and responses.
- Multi-platform support and compatibility testing.