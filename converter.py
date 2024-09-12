import os
import threading
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
import assemblyai as aai


load_dotenv()

API_KEY = os.getenv('ASSEMBLY_API_KEY')
aai.settings.api_key = API_KEY

class Converter:
    output_dir = os.path.join(os.path.expanduser('~'), 'Documents/Interviews')

    # If directory does not exist yet, create one
    try:
        os.listdir(output_dir)
    except FileNotFoundError:
        os.mkdir(output_dir)

    def __init__(self, root):
        self.file_path = ''

        # Set few options
        self.label_font = ('Arial', 14, 'bold')
        self.button_font = ('Arial', 16, 'bold')
        self.bg_color = '#778fa2'

        # Tkinter window config
        self.root = root
        self.root.geometry('860x320')
        self.root.title('Speech to Text Converter')

        # File path label
        self.file_path_label = tk.Label(
            self.root,
            text='No file path', 
            font=self.label_font,
            bg=self.bg_color
        )
        self.file_path_label.pack(pady=30)

        # Get file path button
        self.get_file_button = tk.Button(
            self.root,
            text="Get file path",
            font=self.button_font,
            command=self.get_file_path
        )
        self.get_file_button.pack(pady=10)

        # Convert button
        self.convert_button = tk.Button(
            self.root,
            text='Convert',
            font=self.button_font,
            command=self.start_process
            )
        self.convert_button.pack(pady=20)

        self.progress_label = tk.Label(text='')
        self.progress_label.pack(pady=20)

    def get_file_path(self):
        self.file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[('Audio Files', '*.mp3 *.wav *.m4a')]
        )
        self.file_path_label.config(text=self.file_path)


    def convert_to_text(self):
        if self.file_path:
            file_name = self.file_path.split('/')[-1].split('.')[0] + '.txt'

            self.progress_label.config(text='Converting in progres...')

            config = aai.TranscriptionConfig(language_code='pl')
            transcriber = aai.Transcriber(config=config)
            transcript = transcriber.transcribe(self.file_path)

            if transcript.status == aai.TranscriptStatus.error:
                print(transcript.error)
            else:
                with open(os.path.join(self.output_dir, file_name), 'w') as file:
                    file.write(transcript.text)

            self.progress_label.config(text='')

    
    def start_process(self):
        threading.Thread(target=self.convert_to_text).start()


if __name__ == '__main__':
    root = tk.Tk()
    Converter(root)
    root.mainloop()
