import tkinter as tk

from utils import generate_text, get_file_path


root = tk.Tk()
root.geometry('860x240')
root.title('Speech to text converter')

label_font = ('Arial', 18, 'bold')
button_font = ('Arial', 16, 'bold')
bg_color = '#778fa2'

file_path_label = tk.Label(
    text="No file path",
    font=label_font, height=2,
    bg=bg_color,
    width=860
)
file_path_label.pack(pady=10)

get_file_path_button = tk.Button(
    text='Get the File',
    command=lambda: get_file_path(file_path_label),
    font=button_font,
)
get_file_path_button.pack(pady=10)

convert_button = tk.Button(
    text="Convert",
    command=lambda: generate_text(file_path_label),
    font=button_font
)
convert_button.pack(pady=20)

root.mainloop()
