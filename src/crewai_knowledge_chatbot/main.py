import os
import requests
import json
import warnings
import pyttsx3  # Offline TTS
from gtts import gTTS  # Online TTS
import gradio as gr
from crewai_knowledge_chatbot.crew import CrewaiKnowledgeChatbot
from mem0 import MemoryClient
import time

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

client = MemoryClient()
engine = pyttsx3.init()
history = []

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    return "output.mp3"

def lipsync_video(audio_file):
    files = [
        ("input_face", open("/workspace/crewai_knowledge_chatbot/sample.mp4", "rb")),
        ("input_audio", open(audio_file, "rb")),
    ]
    payload = {
        "selected_model": "Wav2Lip",
        "face_padding_top": 18,
        "face_padding_bottom": 18,
        "face_padding_left": 18,
        "face_padding_right": 18,
    }
    
    response = requests.post(
        "https://api.gooey.ai/v3/Lipsync/async/form/",
        headers={"Authorization": "bearer " + os.environ["GOOEY_API_KEY"]},
        files=files,
        data={"json": json.dumps(payload)},
    )
    
    assert response.ok, response.content
    status_url = response.headers["Location"]
    
    while True:
        response = requests.get(status_url, headers={"Authorization": "bearer " + os.environ["GOOEY_API_KEY"]})
        assert response.ok, response.content
        result = response.json()
        print("API Response:", result)
       
        if result["status"] == "completed":
            if "output" in result and "output_video" in result["output"]:
                return result["output"]["output_video"]
            else:
                print("Error: 'output_video' not found in API response")
                return None  
        elif result["status"] == "failed":
            return None
        time.sleep(3)

def chatbot_response(user_input, name, college, branch, skills):
    global history
    
    chat_history = "\n".join(history)
    inputs = {
        "user_message": user_input,
        "history": chat_history,
        "name": name,
        "college": college,
        "branch": branch,
        "skills": skills
    }
    
    response = CrewaiKnowledgeChatbot().crew().kickoff(inputs=inputs)
    history.append(f"User: {user_input}")
    history.append(f"Assistant: {response}")
    client.add(user_input, user_id="User")
    
    return response

def chat_interface(user_input, name, college, branch, skills):
    response = chatbot_response(user_input, name, college, branch, skills)
    audio_file = text_to_speech(str(response))
    lipsync_url = lipsync_video(audio_file)
    return response, lipsync_url, gr.update(visible=True)

def start_interview(name, college, branch, skills):
    greeting = f"Hello {name}, welcome to your mock interview. Please introduce yourself."
    history.append(f"Assistant: {greeting}")
    audio_file = text_to_speech(greeting)
    lipsync_url = lipsync_video(audio_file)
    return gr.update(visible=True), gr.update(visible=False), greeting, lipsync_url

demo = gr.Blocks(theme='NoCrypt/miku')
with demo:
    gr.Markdown("# 🤖 Mock Interview Platform")
    
    with gr.Row():
        personal_info_section = gr.Column(visible=True)
        with personal_info_section:
            gr.Markdown("## Personal Information")
            name = gr.Textbox(label="First Name", placeholder="Enter your first name")
            college = gr.Textbox(label="College Name", placeholder="Enter your college name")
            branch = gr.Textbox(label="Branch", placeholder="Enter your branch")
            skills = gr.Textbox(label="Skills", placeholder="Enter your skills (comma-separated)")
            start_btn = gr.Button("Start Interview")
    
    chat_interface_section = gr.Column(visible=False)
    with chat_interface_section:
        chatbot_output = gr.Textbox(label="Interviewer", interactive=False)
        lipsync_output = gr.Video(label="Lip-Synced Interviewer", visible=True)
        user_input = gr.Textbox(label="Your Response", placeholder="Type your message here...")
        send_btn = gr.Button("Send")
    
    start_btn.click(start_interview, 
                    inputs=[name, college, branch, skills], 
                    outputs=[chat_interface_section, personal_info_section, chatbot_output, lipsync_output])
    
    send_btn.click(chat_interface, 
                   inputs=[user_input, name, college, branch, skills], 
                   outputs=[chatbot_output, lipsync_output])

demo.launch()
