import os
import io
import threading
import tkinter as tk
import assemblyai as aai

from tkinter import filedialog
from pydub import AudioSegment
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv('ASSEMBLY_API_KEY')
FFMPEG = os.path.join(os.getcwd(), 'ffmpeg', 'ffmpeg.exe')

AudioSegment.converter = FFMPEG

aai.settings.api_key = API_KEY

class Converter:
    output_dir = os.path.join(os.path.expanduser('~'), 'Documents/Interviews')

    # If directory does not exist yet, create one
    try:
        os.listdir(output_dir)
    except FileNotFoundError:
        os.mkdir(output_dir)
        

    def __init__(self, root):
        self.input_file = ''

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
        self.input_file = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[('Audio Files', '*.mp3 *.wav *.m4a')]
        )
        self.progress_label.config(text='')
        self.file_path_label.config(text=self.input_file)


    def convert_to_text(self):
        try:
            if self.input_file:
                output_file = self.input_file.split('/')[-1].split('.')[0] + '.odt'
                output_file= os.path.join(self.output_dir, output_file)

                config = aai.TranscriptionConfig(language_code='pl')
                transcriber = aai.Transcriber(config=config)

                # If input file has not mp3 extension, convert it
                if self.input_file.split('\\')[-1].split('.')[1] != 'mp3':
                    self.progress_label.config(text='Converting to mp3...')

                    with open(self.input_file, 'rb') as file:
                        audio_bytes = file.read()

                    format =self.input_file.split('\\')[-1].split('.')[1]
                    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format)
                    audio_buffer = io.BytesIO()
                    audio.export(audio_buffer, format="mp3", bitrate="192k")

                    # Move the cursor of the buffer to the beginning so it can be read
                    audio_buffer.seek(0)
                    
                    # Transcribe from a binary data
                    self.progress_label.config(text='Transcribing...')
                    transcript = transcriber.transcribe(audio_buffer)
                else:
                    # Transcribe from a file
                    self.progress_label.config(text='Transcribing...')
                    transcript = transcriber.transcribe(self.input_file)

                if transcript.status == aai.TranscriptStatus.error:
                    self.progress_label.config(
                        text=f'Error: {transcript.error}',
                        foreground='red'
                    )
                    return

                with open(output_file, 'w') as file:
                    file.write(transcript.text)
                    self.progress_label.config(
                        text='Transcription has been successfully done',
                        foreground='green'
                    )
                
                os.startfile(output_file)
        except Exception as e:
            self.progress_label.config(f'Error: {e}', foreground='red')

    
    def start_process(self):
        threading.Thread(target=self.convert_to_text).start()


if __name__ == '__main__':
    root = tk.Tk()
    Converter(root)
    root.mainloop()
