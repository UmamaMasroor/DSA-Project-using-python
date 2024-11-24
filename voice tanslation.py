import tkinter as tk
from tkinter import messagebox, ttk
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import playsound
from queue import Queue

# Task Queue for managing speech and translation tasks
task_queue = Queue()
translation_history = []  # To store translation history

# Function to record and translate speech
def record_and_translate():
    recognizer = sr.Recognizer()
    try:
        # Speech recognition
        with sr.Microphone() as source:
            status_label.config(text="Listening... Please speak.")
            root.update()
            
            # Get the input language
            input_language = input_language_var.get()
            input_lang_code = languages[input_language]
            
            # Listen to the user's speech
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)  # Increased time for speaking
            text = recognizer.recognize_google(audio, language=input_lang_code)
            status_label.config(text="Recording complete!")
            
            # Update recognized text in the GUI
            recognized_label.config(text=f"Recognized Text ({input_language}): {text}")
            
            # Get selected target language
            target_language = target_language_var.get()
            target_lang_code = languages[target_language]
            
            # Translation
            translator = Translator()
            translation = translator.translate(text, src=input_lang_code, dest=target_lang_code)
            translated_text = translation.text
            translation_label.config(text=f"Translated Text ({target_language}): {translated_text}")
            
            # Save translation task to the queue
            task_queue.put((translated_text, target_lang_code))
            
            # Save to history
            translation_history.append((text, input_language, translated_text, target_language))
            
            # Enable Play Audio button
            play_button.config(state=tk.NORMAL)
            
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Could not understand the audio. Please try again.")
    except sr.RequestError:
        messagebox.showerror("Error", "Unable to connect to the speech recognition service.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to play the translated text as audio
def play_audio():
    try:
        if not task_queue.empty():
            translated_text, lang_code = task_queue.get()
            
            # Convert translated text to speech
            tts = gTTS(translated_text, lang=lang_code)
            tts.save("translated_audio.mp3")
            
            # Play the audio
            playsound.playsound("translated_audio.mp3")
        else:
            messagebox.showinfo("Info", "No translation available to play.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to clear the current text fields
def clear_fields():
    recognized_label.config(text="")
    translation_label.config(text="")
    status_label.config(text="Press the button to record and translate.")
    play_button.config(state=tk.DISABLED)

# Function to view translation history
def view_history():
    if not translation_history:
        messagebox.showinfo("Info", "No translation history available.")
        return
    
    # Create a new window for history
    history_window = tk.Toplevel(root)
    history_window.title("Translation History")
    history_window.geometry("600x400")
    
    # History Textbox
    history_text = tk.Text(history_window, wrap=tk.WORD, font=("Arial", 12))
    history_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    # Display history
    for entry in translation_history:
        original, input_lang, translated, target_lang = entry
        history_text.insert(tk.END, f"Original ({input_lang}): {original}\n")
        history_text.insert(tk.END, f"Translated ({target_lang}): {translated}\n")
        history_text.insert(tk.END, "-"*50 + "\n")
    
    # Make the history read-only
    history_text.config(state=tk.DISABLED)

# List of languages and their codes
languages = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Hindi": "hi",
    "Urdu": "ur",
    "Chinese": "zh-cn",
    "Arabic": "ar",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko"
}

# GUI Setup
root = tk.Tk()
root.title("Multilingual Speech Translator with TTS")
root.geometry("700x600")

# GUI Widgets
status_label = tk.Label(root, text="Press the button to record and translate.", font=("Arial", 14))
status_label.pack(pady=10)

# Input Language Selection
input_language_label = tk.Label(root, text="Select Input Language:", font=("Arial", 12))
input_language_label.pack(pady=5)

input_language_var = tk.StringVar(value="English")
input_language_dropdown = ttk.Combobox(root, textvariable=input_language_var, values=list(languages.keys()), font=("Arial", 12), state="readonly")
input_language_dropdown.pack(pady=5)

# Target Language Selection
target_language_label = tk.Label(root, text="Select Target Language:", font=("Arial", 12))
target_language_label.pack(pady=5)

target_language_var = tk.StringVar(value="English")
target_language_dropdown = ttk.Combobox(root, textvariable=target_language_var, values=list(languages.keys()), font=("Arial", 12), state="readonly")
target_language_dropdown.pack(pady=5)

record_button = tk.Button(root, text="Record & Translate", command=record_and_translate, font=("Arial", 12), bg="blue", fg="white")
record_button.pack(pady=10)

recognized_label = tk.Label(root, text="", wraplength=650, font=("Arial", 12))
recognized_label.pack(pady=10)

translation_label = tk.Label(root, text="", wraplength=650, font=("Arial", 12))
translation_label.pack(pady=10)

play_button = tk.Button(root, text="Play Audio", command=play_audio, font=("Arial", 12), bg="green", fg="white", state=tk.DISABLED)
play_button.pack(pady=10)

clear_button = tk.Button(root, text="Clear", command=clear_fields, font=("Arial", 12), bg="orange", fg="white")
clear_button.pack(pady=10)

history_button = tk.Button(root, text="View History", command=view_history, font=("Arial", 12), bg="purple", fg="white")
history_button.pack(pady=10)

# Run the GUI event loop
root.mainloop()
