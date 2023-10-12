from google.oauth2 import service_account
from google.cloud import speech


def transcribe(gsc_uri):
    client_file = 'sa_key.json'
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)

    speaker_diarization_config = speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=True,
            min_speaker_count=2,
            max_speaker_count=2,
        )

    recognition_config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="en-US",
            sample_rate_hertz=48000,
            diarization_config=speaker_diarization_config,
        )

    audio = speech.RecognitionAudio(
            uri=gcs_uri,
        )

    response = client.long_running_recognize(
            config=recognition_config, audio=audio
        ).result(timeout=300)
    
        '''
        Reminder: The transcript within each result is separate and sequential per result.
        But, the words list within an alternative includes all the words
        from all the results so far. 
        To get all the words with speaker tags, you only have to take the words list from the last result
        '''
    
    result = response.results[-1]
    words_info = result.alternatives[0].words

        # Print the output
    for word_info in words_info:
        print(f"word: '{word_info.word}', speaker_tag: {word_info.speaker_tag}")
    return True


gcs_uri = "gs://mindset_doctor/brain.wav"
transcribe(gcs_uri)