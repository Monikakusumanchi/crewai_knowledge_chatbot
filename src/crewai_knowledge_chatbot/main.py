#!/usr/bin/env python
import sys
import warnings
import pyttsx3  # Offline TTS
from gtts import gTTS  # Online TTS
import os
from crewai_knowledge_chatbot.crew import CrewaiKnowledgeChatbot
from mem0 import MemoryClient

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

client = MemoryClient()
engine = pyttsx3.init()  # Initialize offline TTS engine


def run():
    history = []

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! It was nice talking to you.")
            text_to_speech("Goodbye! It was nice talking to you.")
            break

        chat_history = "\n".join(history)

        inputs = {
            "user_message": f"{user_input}",
            "history": f"{chat_history}",
        }

        response = CrewaiKnowledgeChatbot().crew().kickoff(inputs=inputs)

        history.append(f"User: {user_input}")
        history.append(f"Assistant: {response}")
        client.add(user_input, user_id="User")

        print(f"Assistant: {response}")
        text = str(response) 
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")

