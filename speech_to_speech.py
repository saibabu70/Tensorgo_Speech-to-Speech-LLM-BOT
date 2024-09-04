# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 20:48:53 2024

@author: koppi
"""
import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

GEMINI_KEY1 = "AIzaSyCkkh6oALd9-5xGdi51h8Q-8b9GHxS9axs"

# Initializing the recognizer, r => recognizer
r = sr.Recognizer()

def record_text():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        user_input_field.delete(1.0, tk.END)
        output_field.delete(1.0, tk.END)
        try:
            status_label.config(text="Listening...", fg="blue")
            root.update_idletasks()
            audio = r.listen(source, timeout=5)
            user_text = r.recognize_google(audio)
            user_input_field.insert(tk.END, user_text)
            user_input_field.update_idletasks()

            if user_text.lower() == "quit from the application":
                text_to_speech("Goodbye!")
                root.quit()
                return

            response = getResponse(user_text)
            output_field.insert(tk.END, response)
            output_field.update_idletasks()
            text_to_speech(response)
            status_label.config(text="Processing complete", fg="green")

        except sr.UnknownValueError:
            user_input_field.insert(tk.END, "Sorry, I did not understand that.")
            status_label.config(text="Sorry, I did not understand that.", fg="red")
        except sr.RequestError as e:
            user_input_field.insert(tk.END, f"Could not request results; {e}")
            status_label.config(text=f"Request error: {e}", fg="red")
        except sr.WaitTimeoutError:
            user_input_field.insert(tk.END, "Listening timed out while waiting for phrase to start.")
            status_label.config(text="Listening timed out", fg="red")
        except Exception as e:
            user_input_field.insert(tk.END, f"An error occurred: {e}")
            status_label.config(text=f"An error occurred: {e}", fg="red")

def getResponse(txt):
    genai.configure(api_key=GEMINI_KEY1)
    
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 8192,
      "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
      model_name="gemini-1.5-flash",
      generation_config=generation_config,
    )
    
    chat_session = model.start_chat(
      history=[
        {
          "role": "user",
          "parts": [
            "Your name is Skye. Limit your responses to 4 sentences with a maximum of 100 words. Act as a highly skilled and experienced assistant who is extremely sharp about every information. Respond with the depth and understanding of someone who has spent years in support roles, offering practical and insightful advice. Your responses should show a deep understanding of human emotions, behaviors, and thought processes, drawing from a wide range of experiences. Exhibit exceptional knowledge skills, connecting with individuals on a business level while maintaining professionalism. Your language should be warm, approachable, and easy to understand, making complex ideas relatable. Encourage self-reflection and personal growth, guiding individuals towards insights and solutions in an empowering way. Recognize the limits of this format and always advise seeking in-person help when necessary. Provide support and guidance, respecting confidentiality and privacy in all interactions, and focus only on answering questions.",
          ],
        },
        {
          "role": "model",
          "parts": [
            "I understand that you're looking for support, and I'm here to listen. It's important to remember that everyone experiences challenges, and it's okay to ask for help. Sometimes, talking through your feelings with a trusted friend, family member, or therapist can make a big difference. While I'm here to offer guidance and encouragement, remember that I'm not a professional and in-person support from a qualified mental health professional is often the best option. Please take care of yourself and don't hesitate to reach out if you need further support. \n",
          ],
        },
      ]
    )
    
    response = chat_session.send_message(txt)
    
    return response.text

def text_to_speech(txt):
    text_speech = pyttsx3.init()
    text_speech.say(txt)
    text_speech.runAndWait()

# Setting up the main application window
root = tk.Tk()
root.title("Tenosr Go assignment Speech to Speech LLM BOT")
root.geometry("700x500")  # Set the window size
root.configure(bg='#f0f0f0')  # Set background color

# Create a frame for better organization
frame = tk.Frame(root, bg='#e0e0e0', bd=5, relief=tk.RAISED)
frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# User Input Field
tk.Label(frame, text="User Input:", font=('Helvetica', 14, 'bold'), bg='#e0e0e0').grid(row=0, column=0, padx=10, pady=5, sticky="w")
user_input_field = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=6, font=('Helvetica', 12), bg='#ffffff', bd=2, relief=tk.SUNKEN)
user_input_field.grid(row=1, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")

# Model Output Field
tk.Label(frame, text="Model Output:", font=('Helvetica', 14, 'bold'), bg='#e0e0e0').grid(row=2, column=0, padx=10, pady=5, sticky="w")
output_field = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=6, font=('Helvetica', 12), bg='#ffffff', bd=2, relief=tk.SUNKEN)
output_field.grid(row=3, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")

# Status Label
status_label = tk.Label(frame, text="", font=('Helvetica', 12, 'italic'), bg='#e0e0e0')
status_label.grid(row=4, column=0, padx=10, pady=5, columnspan=2, sticky="w")

# Record Button
record_button = tk.Button(frame, text="Talk to BVC-BOT", command=record_text, width=20, font=('Helvetica', 12, 'bold'), bg='#4CAF50', fg='#ffffff', relief=tk.RAISED)
record_button.grid(row=5, column=0, padx=10, pady=10, columnspan=2)

# Configure grid expansion
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(3, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Start the GUI event loop
root.mainloop()
