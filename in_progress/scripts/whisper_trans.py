import pandas as pd
import whisper

# load ASR model
model = whisper.load_model("base.en")

audio_file_path = "/Users/jinee.hira/Dropbox/virtual_envs/diary_ceo/foods.wav"
rttm_file_path = "/Users/jinee.hira/Dropbox/virtual_envs/diary_ceo/foods.rttm"

# transcribe audio using ASR model
result = model.transcribe(audio_file_path, verbose=True)
transcribed_text = result['text']

# read speaker information from .rttm file
speaker_info = []
with open(rttm_file_path, 'r') as rttm_file:
    for line in rttm_file:
        if line.startswith("SPEAKER"):
            parts = line.strip().split()
            segment_id = parts[1]
            start_time = float(parts[3])
            duration = float(parts[4])
            speaker_id = parts[7]
            speaker_info.append((segment_id, start_time, duration, speaker_id))

# combine transcribed text with speaker info
combined_data = []
for segment_id, start_time, duration, speaker_id in speaker_info:
    text = transcribed_text[int(start_time * 1000):int((start_time + duration) * 1000)]  # Extracts corresponding text
    combined_data.append((segment_id, start_time, duration, speaker_id, text))

columns = ["Segment_ID", "Start_Time", "Duration", "Speaker_ID", "Transcribed_Text"]
df = pd.DataFrame(combined_data, columns=columns)


output_file_path = './diary_ceo/speaker_transcriptions.csv'
df.to_csv(output_file_path, index=False)

print(f"Speaker transcriptions have been saved to {output_file_path}")