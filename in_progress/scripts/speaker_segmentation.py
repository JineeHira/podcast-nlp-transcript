from pyannote.audio import Model
from pyannote.audio.pipelines import VoiceActivityDetection
from pyannote.audio.pipelines import OverlappedSpeechDetection
from pyannote.audio import Inference
import matplotlib.pyplot as plt
from config import token


# instantiate pretrained model
model = Model.from_pretrained("pyannote/segmentation",
                              use_auth_token=token)

# voice activity detection
pipeline = VoiceActivityDetection(segmentation=model)
HYPER_PARAMETERS = {
  "onset": 0.5, "offset": 0.5,
  "min_duration_on": 0.1,
  "min_duration_off": 0.1
}

pipeline.instantiate(HYPER_PARAMETERS)

vad = pipeline("foods.wav")

# Overlapped Speech Detection
pipeline = OverlappedSpeechDetection(segmentation=model)
pipeline.instantiate(HYPER_PARAMETERS)
osd = pipeline("foods.wav")


def plot_result(vad, osd):
    vad_intervals = [(segment.start, segment.end) for segment in vad.get_timeline()]
    osd_intervals = [(segment.start, segment.end) for segment in osd.get_timeline()]

    print("overlap:", osd_intervals)

    # Plot VAD
    for start, end in vad_intervals:
        plt.fill_between([start, end], 0, 1, color='blue', alpha=0.3)

    # Plot OSD
    for start, end in osd_intervals:
        plt.fill_between([start, end], 1, 2, color='red', alpha=0.3)

    plt.yticks([0.5, 1.5], ["VAD", "OSD"])
    plt.xlabel('Time (s)')
    plt.ylabel('Activity')
    plt.savefig('vad_osd_plot.png')
    plt.show()

plot_result(vad, osd)














