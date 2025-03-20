import warnings
import pyttsx3  # Offline TTS
from gtts import gTTS  # Online TTS
import os
import gradio as gr
from crewai_knowledge_chatbot.crew import CrewaiKnowledgeChatbot
from mem0 import MemoryClient
import time

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

client = MemoryClient()
engine = pyttsx3.init()  # Initialize offline TTS engine
history = []  # Store chat history

def text_to_speech(text):
    """Converts chatbot response to speech using gTTS."""
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    return "output.mp3"

def chatbot_response(user_input, first_name, last_name, college, branch, skills):
    """Handles user messages and generates chatbot responses."""
    global history
    
    if user_input.lower() in ["exit", "quit", "bye"]:
        return "Chatbot: Goodbye! It was nice talking to you."
    
    chat_history = "\n".join(history)
    inputs = {
        "user_message": user_input,
        "history": chat_history,
        "first_name": first_name,
        "last_name": last_name,
        "college": college,
        "branch": branch,
        "skills": skills
    }
    
    response = CrewaiKnowledgeChatbot().crew().kickoff(inputs=inputs)
    
    history.append(f"User: {user_input}")
    history.append(f"Assistant: {response}")
    client.add(user_input, user_id="User")
    
    return response

def chat_interface(user_input, first_name, last_name, college, branch, skills):
    """Generates text and speech output for the chatbot response."""
    response = chatbot_response(user_input, first_name, last_name, college, branch, skills)
    audio_file = text_to_speech(str(response))
    return response, audio_file, gr.update(visible=True), gr.update(visible=False)

def start_interview(first_name, last_name, college, branch, skills):
    """Enables the chat interface and starts the conversation."""
    greeting = f"Hello {first_name}, welcome to your mock interview. Please introduce yourself."
    history.append(f"Assistant: {greeting}")
    audio_file = text_to_speech(greeting)
    return gr.update(visible=True), gr.update(visible=False), greeting, audio_file

demo = gr.Blocks(theme='NoCrypt/miku')
with demo:
    gr.Markdown("# 🤖 Mock Interview Platform")
    
    with gr.Row():
        personal_info_section = gr.Column(visible=True)
        with personal_info_section:
            gr.Markdown("## Personal Information")
            first_name = gr.Textbox(label="First Name", placeholder="Enter your first name")
            last_name = gr.Textbox(label="Last Name", placeholder="Enter your last name")
            college = gr.Textbox(label="College Name", placeholder="Enter your college name")
            branch = gr.Textbox(label="Branch", placeholder="Enter your branch")
            skills = gr.Textbox(label="Skills", placeholder="Enter your skills (comma-separated)")
            start_btn = gr.Button("Start Interview")
    
    chat_interface_section = gr.Column(visible=False)
    with chat_interface_section:
        chatbot_output = gr.Textbox(label="Interviewer", interactive=False)
        audio_output = gr.Audio(label="Speech Output", autoplay=True, visible=False)
        user_input = gr.Textbox(label="Your Response", placeholder="Type your message here...")
        send_btn = gr.Button("Send")
    
    start_btn.click(start_interview, 
                    inputs=[first_name, last_name, college, branch, skills], 
                    outputs=[chat_interface_section, personal_info_section, chatbot_output, audio_output])
    
    send_btn.click(chat_interface, 
                   inputs=[user_input, first_name, last_name, college, branch, skills], 
                   outputs=[chatbot_output, audio_output])

demo.launch()
