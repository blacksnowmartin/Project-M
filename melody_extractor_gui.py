import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MelodyExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Melody Extractor")
        
        self.load_label = tk.Label(root, text="Drop audio file here or click to browse", bg="lightgray", relief="ridge", padx=10, pady=10)
        self.load_label.pack(pady=10)
        self.load_label.bind("<Button-1>", lambda e: self.load_file())
        self.load_label.drop_target_register(DND_FILES)
        self.load_label.dnd_bind('<<Drop>>', self.on_drop)
        
        self.save_pitch_button = tk.Button(root, text="Save Pitch Values", command=self.save_pitch, state=tk.DISABLED)
        self.save_pitch_button.pack(pady=10)
        
        self.save_midi_button = tk.Button(root, text="Save MIDI Notes", command=self.save_midi, state=tk.DISABLED)
        self.save_midi_button.pack(pady=10)
        
        self.figure = plt.Figure(figsize=(10, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
        if file_path:
            self.extract_melody(file_path)

    def on_drop(self, event):
        file_path = event.data.strip('{}')
        self.extract_melody(file_path)

    def extract_melody(self, audio_path):
        y, sr = librosa.load(audio_path)
        pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
        
        self.pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                self.pitch_values.append(pitch)
        
        self.midi_notes = librosa.hz_to_midi(self.pitch_values)
        
        self.ax.clear()
        self.ax.plot(self.pitch_values)
        self.ax.set_title('Pitch over Time')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Pitch (Hz)')
        self.canvas.draw()
        
        self.save_pitch_button.config(state=tk.NORMAL)
        self.save_midi_button.config(state=tk.NORMAL)

    def save_pitch(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            np.savetxt(file_path, self.pitch_values, delimiter=',')

    def save_midi(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            np.savetxt(file_path, self.midi_notes, delimiter=',')

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = MelodyExtractorApp(root)
    root.mainloop()
