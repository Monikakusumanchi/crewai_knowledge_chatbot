#!/usr/bin/env python
import sys
import warnings

from crewai_knowledge_chatbot.crew import CrewaiKnowledgeChatbot
from mem0 import MemoryClient

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

client = MemoryClient()

def run():
    history = []

    while True:
        user_input = input("Your Responseser: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! It was nice talking to you.")
            break

        chat_history = "\n".join(history)

        inputs = {
            "user_message": f"{user_input}",
            "history": f"{chat_history}",
        }

        response = CrewaiKnowledgeChatbot().crew().kickoff(inputs=inputs)

        history.append(f"Your Response: {user_input}")
        history.append(f"Interviewer: {response}")
        client.add(user_input, user_id="Your Response")

        print(f"Interviewer: {response}")
