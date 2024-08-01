import librosa
import numpy as np
import matplotlib.pyplot as plt

# Load the audio file
audio_path = 'path_to_your_audio_file.wav'
y, sr = librosa.load(audio_path)

# Extract pitches using librosa's piptrack method
pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

# Get the pitches
pitch_values = []
for t in range(pitches.shape[1]):
    index = magnitudes[:, t].argmax()
    pitch = pitches[index, t]
    if pitch > 0:  # filter out non-zero pitches
        pitch_values.append(pitch)

# Convert pitch values to MIDI notes
midi_notes = librosa.hz_to_midi(pitch_values)

# Plot the pitch over time
plt.figure(figsize=(14, 5))
plt.plot(pitch_values)
plt.title('Pitch over Time')
plt.xlabel('Time')
plt.ylabel('Pitch (Hz)')
plt.show()

# Optionally, print out the MIDI notes
print(midi_notes)
