#!/usr/bin/env python
import warnings
import pyttsx3  # Offline TTS
from gtts import gTTS  # Online TTS
import os
import gradio as gr
from crewai_knowledge_chatbot.crew import CrewaiKnowledgeChatbot
from mem0 import MemoryClient

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

client = MemoryClient()
engine = pyttsx3.init()  # Initialize offline TTS engine
history = []  # Store chat history


def chatbot_response(user_input):
    """Handles user messages and generates chatbot responses."""
    global history

    if user_input.lower() in ["exit", "quit", "bye"]:
        return "Chatbot: Goodbye! It was nice talking to you."

    chat_history = "\n".join(history)
    inputs = {"user_message": user_input, "history": chat_history}
    response = CrewaiKnowledgeChatbot().crew().kickoff(inputs=inputs)

    history.append(f"User: {user_input}")
    history.append(f"Assistant: {response}")
    client.add(user_input, user_id="User")

    return response


def text_to_speech(text):
    """Converts chatbot response to speech using gTTS."""
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    return "output.mp3"


def chat_interface(user_input):
    """Generates text and speech output for the chatbot response."""
    response = chatbot_response(user_input)
    audio_file = text_to_speech(str(response))
    return response, audio_file


# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Interviewer")
    
    with gr.Row():
        user_input = gr.Textbox(label="Your Message", placeholder="Type your message here...")
        send_btn = gr.Button("Send")
    
    chatbot_output = gr.Textbox(label="Chatbot Response", interactive=False)
    audio_output = gr.Audio(label="Speech Output", autoplay=True)

    send_btn.click(chat_interface, inputs=[user_input], outputs=[chatbot_output, audio_output])

demo.launch()
