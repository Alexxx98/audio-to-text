import tkinter as tk
import multiprocessing
from functools import partial

from utils import generate_text, get_file_path, start_process


root = tk.Tk()
root.geometry('860x320')
root.title('Speech to text converter')

label_font = ('Arial', 14, 'bold')
button_font = ('Arial', 16, 'bold')
bg_color = '#778fa2'

file_path_label = tk.Label(text="No file path", font=label_font, height=2, width=860, bg=bg_color)
file_path_label.pack(pady=10)

get_file_path_button = tk.Button(text='Get the File', command=lambda: get_file_path(file_path_label), font=button_font, bg=bg_color)
get_file_path_button.pack(pady=10)

convert_button = tk.Button(
    text="Convert",
    command=lambda: start_process(generate_text, file_path_label),
    font=button_font,
    bg=bg_color
)
convert_button.pack(pady=20)

progress_label = tk.Label(root, text="")
progress_label.pack(pady=20)

if multiprocessing.active_children():
    progress_label.config(text="Converting...")
else:
    progress_label.config(text="")

root.mainloop()
