import whisper
import csv
import os

# ASR model
model = whisper.load_model("base.en")

audio_folder = 'mp3_files'
transcripts_csv = 'transcripts.csv'

# produces transcripts of audio files
def transcribe_and_save():
    transcripts = []

    for audio_file in os.listdir(audio_folder):
        if audio_file.endswith('.wav'):
            audio_file_path = os.path.join(audio_folder, audio_file)
            result = model.transcribe(audio_file_path, verbose=True)
            transcribed_text = result['text']
            transcripts.append({'filename': audio_file, 'transcript': transcribed_text})

    with open(transcripts_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['filename', 'transcript']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transcripts)

if __name__ == "__main__":
    transcribe_and_save()



