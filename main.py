import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def open_text_translate():
    # Function to open the text translation window
    messagebox.showinfo("Text Translation", "Opening Text Translation...")

def open_voice_translate():
    # Function to open the voice translation window
    messagebox.showinfo("Voice Translation", "Opening Voice Translation...")

def open_document_translate():
    # Function to open the document translation window
    messagebox.showinfo("Document Translation", "Opening Document Translation...")

# Create main window
root = tk.Tk()
root.title("Language Translator")
root.geometry("500x400")
root.configure(bg="#e0f7fa")

# Title Label
title_label = tk.Label(root, text="Language Translator", font=("Arial", 20, "bold"), bg="#e0f7fa", fg="#00796b")
title_label.pack(pady=20)

# Frame for buttons
button_frame = tk.Frame(root, bg="#e0f7fa")
button_frame.pack(pady=20)

# Button style
style = ttk.Style()
style.configure("TButton", font=("Arial", 14), padding=10)
style.map("TButton",
          foreground=[("active", "#e0f7fa")],
          background=[("active", "#00796b")])

# Translate Text Button
text_button = ttk.Button(button_frame, text="Translate Text", command=open_text_translate)
text_button.grid(row=0, column=0, padx=10, pady=10)

# Translate Using Voice Button
voice_button = ttk.Button(button_frame, text="Translate Using Voice", command=open_voice_translate)
voice_button.grid(row=0, column=1, padx=10, pady=10)

# Translate Document Button
document_button = ttk.Button(button_frame, text="Translate Document", command=open_document_translate)
document_button.grid(row=0, column=2, padx=10, pady=10)

# Animation effect for button hover
def on_enter(e):
    e.widget.configure(style="Hover.TButton")

def on_leave(e):
    e.widget.configure(style="TButton")

# Apply hover animation to all buttons
for button in [text_button, voice_button, document_button]:
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

# Run main loop
root.mainloop()
