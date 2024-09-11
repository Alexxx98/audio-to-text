import tkinter as tk
from tkinter import filedialog

from utils import generate_text


root = tk.Tk()
root.geometry('860x240')
root.title('Speech to text converter')

label_font = ('Arial', 18, 'bold')
button_font = ('Arial', 16, 'bold')

file_path_label = tk.Label(text="No file path", font=label_font, height=2)
file_path_label.pack(pady=10)

# Get the audio file
def get_file_path():
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[
        ('Audio Files', '*.mp3 *.wav *.m4a')
    ])

    file_path_label.config(text=file_path)


get_file_path_button = tk.Button(text='Get the File', command=get_file_path, font=button_font)
get_file_path_button.pack(pady=10)

convert_button = tk.Button(text="Convert", command=lambda: generate_text(file_path_label), font=button_font)
convert_button.pack(pady=20)

root.mainloop()
