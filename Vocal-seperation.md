

---

### ✅ **Options to Implement Vocal Separation**

#### 1. **Using Pre-trained Models (Recommended for Best Results)**

Libraries and tools that offer high-quality separation:

* **Spleeter by Deezer**

  * Fast and high-quality.
  * Separates into 2, 4, or 5 stems.
  * Easy to use via Python or command line.
* **Demucs by Facebook AI**

  * Even better separation quality in some cases.
  * Slower but more advanced deep learning model.
* **UVR (Ultimate Vocal Remover GUI)**

  * Combines several models.
  * Open-source and desktop-ready (if you want a GUI).

#### 2. **Using Traditional DSP (Not recommended for high quality)**

* Phase inversion, band-pass filters, or center channel extraction.
* Poor quality compared to machine learning-based approaches.

---

### ✅ **Option 1: Spleeter Example (Python)**

#### Installation:

```bash
pip install spleeter
```

#### Code to Separate Vocals (2-stem: vocals + accompaniment)

```python
from spleeter.separator import Separator

# Load the model (2stems = vocals + accompaniment)
separator = Separator('spleeter:2stems')

# Separate the audio file
separator.separate_to_file('your_song.mp3', 'output_folder/')
```

This will create:

* `vocals.wav`
* `accompaniment.wav`

Inside the `output_folder/your_song/`.

---

### ✅ **Option 2: Use Demucs (More Advanced)**

Install via:

```bash
pip install demucs
```

Then run:

```bash
demucs your_song.mp3
```

This will create stems like:

* `vocals.wav`
* `drums.wav`
* `bass.wav`
* `other.wav`

---

### ✅ Article by Martin Kitonga

