#!/usr/bin/env python3
"""
Music Sequencer - Python GUI Version
A melody sequencer with 8 notes × 16 steps, inspired by the web-based Tone.js sequencer.
Features: Play/Stop, Save/Load patterns, 5 save slots, Export/Import JSON, Tempo control.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import json
import os
import threading
import time
from pathlib import Path
import numpy as np
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: pygame not available. Audio playback disabled. Install with: pip install pygame")


class MusicSequencer:
    """Main sequencer application with GUI."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Melody Sequencer")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f3f4f6")
        
        # Set icon if available
        try:
            self.root.iconphoto(False, tk.PhotoImage(file='/usr/share/icons/hicolor/48x48/apps/media-player.png'))
        except:
            pass
        
        # Initialize pygame mixer for audio
        if PYGAME_AVAILABLE:
            pygame.mixer.init()
        
        # Sequencer state
        self.notes = ["C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4"]  # High to low
        self.note_labels = ["C", "B", "A", "G", "F", "E", "D", "C"]
        self.num_steps = 16
        self.grid = [[False] * self.num_steps for _ in range(len(self.notes))]
        
        # Playback state
        self.current_step = 0
        self.is_playing = False
        self.is_paused = False
        self.playback_thread = None
        self.stop_playback_event = threading.Event()
        
        # UI state
        self.current_slot = 0
        self.max_slots = 5
        self.tempo = 120
        self.cell_widgets = {}  # Store cell references for updates
        self.slot_buttons = {}  # Store slot button references
        
        # Save directory
        self.save_dir = Path.home() / ".melody_sequencer"
        self.save_dir.mkdir(exist_ok=True)
        
        # Audio synthesis
        self.synth = SynthEngine()
        
        # Build UI
        self._build_ui()
        self._update_slot_display()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _build_ui(self):
        """Build the main UI components."""
        # Header
        header_frame = tk.Frame(self.root, bg="#f3f4f6")
        header_frame.pack(pady=20)
        
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title_label = tk.Label(header_frame, text="🎵 Melody Sequencer", font=title_font, bg="#f3f4f6", fg="#312e81")
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Create, play, and save your melody patterns!", bg="#f3f4f6", fg="#666")
        subtitle_label.pack()
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg="white", relief=tk.RAISED, borderwidth=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sequencer grid
        grid_frame = tk.Frame(main_frame, bg="white")
        grid_frame.pack(padx=20, pady=20)
        
        self._build_grid(grid_frame)
        
        # Save slots section
        slots_frame = tk.LabelFrame(main_frame, text="Save Slots", bg="white", font=("Helvetica", 10, "bold"))
        slots_frame.pack(fill=tk.X, padx=20, pady=10)
        
        slots_inner = tk.Frame(slots_frame, bg="white")
        slots_inner.pack(pady=10)
        
        for i in range(self.max_slots):
            btn = tk.Button(
                slots_inner,
                text=str(i + 1),
                width=6,
                height=2,
                bg="#d1d5db",
                fg="white",
                font=("Helvetica", 10, "bold"),
                command=lambda slot=i: self._select_slot(slot),
                relief=tk.RAISED,
                bd=2
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.slot_buttons[i] = btn
        
        # Controls section
        controls_frame = tk.LabelFrame(main_frame, text="Controls", bg="white", font=("Helvetica", 10, "bold"))
        controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        controls_inner = tk.Frame(controls_frame, bg="white")
        controls_inner.pack(pady=10, padx=10)
        
        # Row 1: Playback controls
        playback_row = tk.Frame(controls_inner, bg="white")
        playback_row.pack(pady=5)
        
        self.play_btn = tk.Button(
            playback_row,
            text="▶ Play",
            bg="#22c55e",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=15,
            pady=8,
            command=self._start_playback,
            cursor="hand2"
        )
        self.play_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(
            playback_row,
            text="⏹ Stop",
            bg="#ef4444",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=15,
            pady=8,
            command=self._stop_playback,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            playback_row,
            text="🗑 Clear",
            bg="#9ca3af",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=15,
            pady=8,
            command=self._clear_grid,
            cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Row 2: Save/Load controls
        saveload_row = tk.Frame(controls_inner, bg="white")
        saveload_row.pack(pady=5)
        
        save_btn = tk.Button(
            saveload_row,
            text="💾 Save",
            bg="#6366f1",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=15,
            pady=8,
            command=self._save_pattern,
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        load_btn = tk.Button(
            saveload_row,
            text="📂 Load",
            bg="#a855f7",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=15,
            pady=8,
            command=self._load_pattern,
            cursor="hand2"
        )
        load_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(
            saveload_row,
            text="🗑 Delete Slot",
            bg="#f97316",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=15,
            pady=8,
            command=self._delete_slot,
            cursor="hand2"
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Row 3: Import/Export controls
        import_export_row = tk.Frame(controls_inner, bg="white")
        import_export_row.pack(pady=5)
        
        export_btn = tk.Button(
            import_export_row,
            text="📥 Export",
            bg="#0891b2",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=15,
            pady=8,
            command=self._export_pattern,
            cursor="hand2"
        )
        export_btn.pack(side=tk.LEFT, padx=5)
        
        import_btn = tk.Button(
            import_export_row,
            text="📤 Import",
            bg="#0891b2",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=15,
            pady=8,
            command=self._import_pattern,
            cursor="hand2"
        )
        import_btn.pack(side=tk.LEFT, padx=5)
        
        # Tempo section
        tempo_frame = tk.LabelFrame(main_frame, text="Tempo Control", bg="white", font=("Helvetica", 10, "bold"))
        tempo_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tempo_inner = tk.Frame(tempo_frame, bg="white")
        tempo_inner.pack(pady=10, padx=20)
        
        tk.Label(tempo_inner, text="BPM:", bg="white", fg="#374151", font=("Helvetica", 10)).pack(side=tk.LEFT, padx=5)
        
        self.tempo_scale = tk.Scale(
            tempo_inner,
            from_=60,
            to=240,
            orient=tk.HORIZONTAL,
            bg="#e5e7eb",
            fg="#374151",
            command=self._update_tempo,
            length=300
        )
        self.tempo_scale.set(120)
        self.tempo_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.tempo_display = tk.Label(tempo_inner, text="120 BPM", bg="white", fg="#6366f1", font=("Helvetica", 10, "bold"))
        self.tempo_display.pack(side=tk.LEFT, padx=5)
        
        # Status message
        self.status_label = tk.Label(main_frame, text="", bg="white", fg="#374151", font=("Helvetica", 9))
        self.status_label.pack(pady=10)
    
    def _build_grid(self, parent):
        """Build the sequencer grid."""
        for note_idx, (note, label) in enumerate(zip(self.notes, self.note_labels)):
            row_frame = tk.Frame(parent, bg="white")
            row_frame.pack()
            
            # Note label
            note_label = tk.Label(
                row_frame,
                text=label,
                width=3,
                bg="white",
                fg="#6b7280",
                font=("Courier", 10, "bold")
            )
            note_label.pack(side=tk.LEFT, padx=5)
            
            # Grid cells
            for step_idx in range(self.num_steps):
                cell = tk.Button(
                    row_frame,
                    width=4,
                    height=2,
                    bg="white",
                    fg="white",
                    font=("Helvetica", 8),
                    relief=tk.RAISED,
                    bd=1,
                    cursor="hand2",
                    command=lambda n=note_idx, s=step_idx: self._toggle_cell(n, s)
                )
                cell.pack(side=tk.LEFT, padx=2, pady=2)
                self.cell_widgets[(note_idx, step_idx)] = cell
    
    def _toggle_cell(self, note_idx, step_idx):
        """Toggle a grid cell."""
        self.grid[note_idx][step_idx] = not self.grid[note_idx][step_idx]
        self._update_cell_visual(note_idx, step_idx)
    
    def _update_cell_visual(self, note_idx, step_idx):
        """Update a cell's visual appearance."""
        cell = self.cell_widgets[(note_idx, step_idx)]
        if self.grid[note_idx][step_idx]:
            cell.config(bg="#4f46e5", activebackground="#6366f1")  # Indigo-500
        else:
            cell.config(bg="#ffffff", activebackground="#e5e7eb")  # White
    
    def _update_all_cells_visual(self):
        """Update all cells' visual appearance."""
        for note_idx in range(len(self.notes)):
            for step_idx in range(self.num_steps):
                self._update_cell_visual(note_idx, step_idx)
    
    def _highlight_step(self, step_idx):
        """Highlight the current step."""
        for note_idx in range(len(self.notes)):
            cell = self.cell_widgets[(note_idx, step_idx)]
            current_color = cell.cget("bg")
            if current_color == "#4f46e5":
                cell.config(bg="#fbbf24")  # Yellow highlight for on
            else:
                cell.config(bg="#fbbf24")  # Yellow highlight for off
    
    def _clear_highlight(self):
        """Remove step highlight."""
        self._update_all_cells_visual()
    
    def _start_playback(self):
        """Start playback in a separate thread."""
        if self.is_playing:
            return
        
        self.is_playing = True
        self.stop_playback_event.clear()
        self.current_step = 0
        
        self.play_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        self.playback_thread = threading.Thread(target=self._playback_loop, daemon=True)
        self.playback_thread.start()
    
    def _playback_loop(self):
        """Main playback loop."""
        while self.is_playing and not self.stop_playback_event.is_set():
            step = self.current_step % self.num_steps
            
            # Highlight current step
            self.root.after(0, lambda s=step: self._highlight_step(s))
            
            # Play notes for this step
            for note_idx, note in enumerate(self.notes):
                if self.grid[note_idx][step]:
                    self.synth.play_note(note, duration=0.2)
            
            self.current_step += 1
            
            # Calculate delay based on tempo
            # At 120 BPM, 16 steps = 2 beats, so each step = 0.25 beats
            beat_duration = 60 / self.tempo
            step_duration = beat_duration * 0.5  # 8th note
            
            time.sleep(step_duration)
    
    def _stop_playback(self):
        """Stop playback."""
        self.is_playing = False
        self.stop_playback_event.set()
        
        self.root.after(0, self._clear_highlight)
        
        self.play_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def _clear_grid(self):
        """Clear the entire grid."""
        self._stop_playback()
        self.grid = [[False] * self.num_steps for _ in range(len(self.notes))]
        self._update_all_cells_visual()
        self._show_message("Grid cleared")
    
    def _select_slot(self, slot):
        """Select a save slot."""
        self.current_slot = slot
        self._update_slot_display()
        self._show_message(f"Selected Slot {slot + 1}")
    
    def _update_slot_display(self):
        """Update slot button appearances based on saved data."""
        for i in range(self.max_slots):
            slot_key = f"slot_{i}.json"
            slot_path = self.save_dir / slot_key
            
            btn = self.slot_buttons[i]
            
            # Update ring/selection
            if i == self.current_slot:
                btn.config(relief=tk.SUNKEN, bd=3)
            else:
                btn.config(relief=tk.RAISED, bd=2)
            
            # Update color based on data
            if slot_path.exists():
                btn.config(bg="#4f46e5")  # Indigo if has data
            else:
                btn.config(bg="#d1d5db")  # Gray if empty
    
    def _save_pattern(self):
        """Save current pattern to selected slot."""
        try:
            pattern_data = {
                "notes": self.grid,
                "tempo": self.tempo,
                "timestamp": time.time()
            }
            
            slot_key = f"slot_{self.current_slot}.json"
            slot_path = self.save_dir / slot_key
            
            with open(slot_path, 'w') as f:
                json.dump(pattern_data, f, indent=2)
            
            self._update_slot_display()
            self._show_message(f"Pattern saved to Slot {self.current_slot + 1}!")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save pattern: {e}")
    
    def _load_pattern(self):
        """Load pattern from selected slot."""
        try:
            slot_key = f"slot_{self.current_slot}.json"
            slot_path = self.save_dir / slot_key
            
            if not slot_path.exists():
                self._show_message(f"No saved pattern in Slot {self.current_slot + 1}", error=True)
                return
            
            with open(slot_path, 'r') as f:
                pattern_data = json.load(f)
            
            if (isinstance(pattern_data.get("notes"), list) and
                len(pattern_data["notes"]) == len(self.notes) and
                len(pattern_data["notes"][0]) == self.num_steps):
                
                self.grid = pattern_data["notes"]
                self._update_all_cells_visual()
                
                if "tempo" in pattern_data:
                    self.tempo = pattern_data["tempo"]
                    self.tempo_scale.set(self.tempo)
                
                self._show_message(f"Pattern loaded from Slot {self.current_slot + 1}!")
            else:
                self._show_message("Invalid pattern format", error=True)
        
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load pattern: {e}")
    
    def _delete_slot(self):
        """Delete the current slot."""
        try:
            slot_key = f"slot_{self.current_slot}.json"
            slot_path = self.save_dir / slot_key
            
            if slot_path.exists():
                slot_path.unlink()
            
            self._update_slot_display()
            self._show_message(f"Slot {self.current_slot + 1} cleared!")
        except Exception as e:
            messagebox.showerror("Delete Error", f"Failed to delete slot: {e}")
    
    def _export_pattern(self):
        """Export pattern as JSON file."""
        try:
            slot_key = f"slot_{self.current_slot}.json"
            slot_path = self.save_dir / slot_key
            
            if not slot_path.exists():
                self._show_message(f"No pattern in Slot {self.current_slot + 1} to export", error=True)
                return
            
            with open(slot_path, 'r') as f:
                pattern_data = json.load(f)
            
            export_data = {
                "version": 1,
                "name": f"Melody_Slot_{self.current_slot + 1}",
                "grid": pattern_data["notes"],
                "tempo": pattern_data["tempo"],
                "exportDate": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfile=f"melody_pattern_{self.current_slot + 1}.json"
            )
            
            if file_path:
                with open(file_path, 'w') as f:
                    json.dump(export_data, f, indent=2)
                self._show_message("Pattern exported!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export pattern: {e}")
    
    def _import_pattern(self):
        """Import pattern from JSON file."""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
            
            with open(file_path, 'r') as f:
                imported_data = json.load(f)
            
            if (isinstance(imported_data.get("grid"), list) and
                len(imported_data["grid"]) == len(self.notes) and
                len(imported_data["grid"][0]) == self.num_steps):
                
                pattern_data = {
                    "notes": imported_data["grid"],
                    "tempo": imported_data.get("tempo", 120),
                    "timestamp": time.time()
                }
                
                slot_key = f"slot_{self.current_slot}.json"
                slot_path = self.save_dir / slot_key
                
                with open(slot_path, 'w') as f:
                    json.dump(pattern_data, f, indent=2)
                
                self.grid = pattern_data["notes"]
                self.tempo = pattern_data["tempo"]
                self.tempo_scale.set(self.tempo)
                
                self._update_all_cells_visual()
                self._update_slot_display()
                
                self._show_message("Pattern imported successfully!")
            else:
                self._show_message("Invalid pattern file format", error=True)
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import pattern: {e}")
    
    def _update_tempo(self, value):
        """Update tempo value."""
        self.tempo = int(float(value))
        self.tempo_display.config(text=f"{self.tempo} BPM")
    
    def _show_message(self, message, error=False):
        """Display a status message."""
        color = "#dc2626" if error else "#16a34a"
        self.status_label.config(text=message, fg=color)
        
        # Auto-clear after 2.5 seconds
        self.root.after(2500, lambda: self.status_label.config(text=""))
    
    def _on_close(self):
        """Handle window close event."""
        self._stop_playback()
        self.root.destroy()


class SynthEngine:
    """Simple synthesizer using pygame."""
    
    def __init__(self):
        self.sample_rate = 22050
        self.note_freqs = {
            "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23,
            "G4": 392.00, "A4": 440.00, "B4": 493.88, "C5": 523.25
        }
    
    def play_note(self, note, duration=0.2, volume=0.3):
        """Play a single note."""
        if not PYGAME_AVAILABLE:
            return
        
        freq = self.note_freqs.get(note, 440)
        
        # Generate simple sine wave
        num_samples = int(self.sample_rate * duration)
        arr = np.linspace(0, freq * 2 * np.pi * duration, num_samples)
        
        # Envelope: fade in and out
        envelope = np.hanning(num_samples)
        wave = np.sin(arr) * envelope * volume
        
        # Convert to 16-bit audio
        wave = (wave * 32767).astype(np.int16)
        
        # Create stereo sound
        stereo_wave = np.zeros((len(wave), 2), dtype=np.int16)
        stereo_wave[:, 0] = wave
        stereo_wave[:, 1] = wave
        
        try:
            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.play()
        except Exception as e:
            print(f"Error playing note {note}: {e}")


def main():
    """Main entry point."""
    root = tk.Tk()
    app = MusicSequencer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
