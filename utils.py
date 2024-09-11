import os
from dotenv import load_dotenv
import assemblyai as aai


load_dotenv()

API_KEY = os.getenv('ASSEMBLY_API_KEY')

aai.settings.api_key = API_KEY

OUTPUT_DIR = os.path.join(os.path.expanduser('~'), 'Documents/Interviews')

try:
    os.listdir(OUTPUT_DIR)
except FileNotFoundError:
    os.mkdir(OUTPUT_DIR)

def generate_text(label) -> None:
    file_path = label.cget('text')
    file_name = file_path.split('/')[-1].split('.')[0] + '.txt'

    config = aai.TranscriptionConfig(language_code='pl')

    transcriber = aai.Transcriber(config=config)

    transcript = transcriber.transcribe(file_path)

    if transcript.status == aai.TranscriptStatus.error:
        print(transcript.error)
    else:
        with open(os.path.join(OUTPUT_DIR, file_name), 'w') as file:
            file.write(transcript.text)
