from pyannote.database.util import load_rttm
import matplotlib.pyplot as plt

ref_path = "./diary_ceo/foods.rttm"
reference = load_rttm(ref_path)["foods"]

# Define colors for each speaker
colors = ['blue', 'red']

# Map speaker labels to integers
label_mapping = {label: idx for idx, label in enumerate(reference.labels())}

# Plot the reference
plt.figure(figsize=(10, 3))
for segment, _, label in reference.itertracks(yield_label=True):
    label_idx = label_mapping[label]
    color = colors[label_idx % len(colors)] # Use modulo to handle more speakers than defined colors
    plt.plot([segment.start, segment.end], [label_idx, label_idx], color)
    plt.fill_betweenx([label_idx, label_idx + 0.5], segment.start, segment.end, color=color, alpha=0.3)

plt.yticks(range(len(reference.labels())), reference.labels())
plt.xlabel('Time (s)')
plt.ylabel('Speaker ID')
plt.title('Reference RTTM')
plt.savefig('diarization.png')