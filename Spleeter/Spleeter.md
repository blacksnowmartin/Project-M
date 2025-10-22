

Here’s **working Python code** to separate vocals from a song using **Spleeter**. This is a minimal example that:

* Downloads the pretrained model
* Separates vocals and instrumental
* Saves them as WAV files

---

### 🔧 **1. Install Spleeter**

```bash
pip install spleeter
```

---

### 📄 **2. Python Code (Basic Vocal Separation)**

```python
from spleeter.separator import Separator
import os

# Input audio file path (can be .mp3 or .wav)
input_file = 'path/to/your/song.mp3'

# Output directory
output_dir = 'separated_audio'

# Create separator (2 stems = vocals + accompaniment)
separator = Separator('spleeter:2stems')

# Separate the audio
separator.separate_to_file(audio_descriptor=input_file, destination=output_dir)

print(f"Separation complete. Files saved in: {os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0])}")
```

---

### 🗂 Output Structure

After execution, you'll get:

```
separated_audio/
└── song/
    ├── vocals.wav
    └── accompaniment.wav
```

---

### 💡 Notes

* Input formats supported: `.mp3`, `.wav`, `.ogg`, etc.
* Output is always `.wav`.
* It uses TensorFlow under the hood (will download model weights on first run).

---

### ✅ One-liner CLI (if preferred):

```bash
spleeter separate -i your_song.mp3 -p spleeter:2stems -o output_dir
```

---

If you want to integrate this into a larger pipeline (Flask app, CLI tool, etc.), I can help modularize or package it.

Let me know if you want a version using **Demucs** or if GPU support matters to you.


Figure out on how the GUI will look like.
