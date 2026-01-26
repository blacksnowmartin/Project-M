# AI Coding Agent Instructions for Project-M

## Project Overview
Project-M is a music production toolkit focused on **melody extraction from audio and music creation/sequencing**. It's a multi-technology project combining Python audio processing with web-based music composition tools.

### Core Components
- **Melody Extraction**: `Melody.py` + `melody_extractor_gui.py` — Extract pitch data from audio files using librosa's piptrack
- **Music Grid Sequencer**: `Music-Grid-Sequencer/index.html` — Web-based 8-step piano grid sequencer using Tone.js
- **Online Piano**: `Online-piano/` — Interactive piano keyboard (see PIANO_SOLUTION.md for architecture)
- **Utilities**: `quantize.py` (MIDI quantization), `video-viewer.py` (YouTube link browser)
- **Audio Processing**: `Spleeter/` (vocal separation reference)

## Critical Architecture Patterns

### Python Audio Processing (Melody.py & melody_extractor_gui.py)
**Pattern**: Load → Extract → Visualize → Export

```python
# Standard workflow for audio files
y, sr = librosa.load(audio_path)  # Load with sample rate
pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)  # Extract pitches
midi_notes = librosa.hz_to_midi(pitch_values)  # Convert Hz → MIDI
```

- Use **librosa.core.piptrack()** for melody extraction (not other methods)
- Filter out zero pitches: `if pitch > 0`
- GUI uses **Tkinter** + **matplotlib FigureCanvasTkAgg** for embedding plots
- Support audio formats: `.wav`, `.mp3`

### Web-Based Sequencer (Music-Grid-Sequencer/index.html)
**Pattern**: Grid-based note sequencing with Tone.js playback

- **Note Range**: C4-C5 (8 notes, high to low)
- **Grid Size**: 16 steps (columns) × 8 notes (rows)
- **Sound Engine**: Tone.js PolySynth with envelope: `{attack: 0.04, release: 0.2}`
- **Persistence**: LocalStorage with 5 pattern slots (`melodyPattern_slot_0` through `slot_4`)
- **Tempo Control**: Stored in BPM, synced with Tone.Transport
- **Color Scheme**: Yellow highlight (current step), Indigo-500 (note on), White (note off)

### Online Piano (Online-piano/)
**Architecture**: Configuration-driven system (see PIANO_SOLUTION.md for full details)

- Centralized **PIANO_CONFIGURATION** object controls all mappings
- Maps computer keyboard → piano notes via KEYBOARD_MAP
- Supports multiple octaves with configurable start octave and count
- White/black key positioning uses CSS Grid or Flexbox

## Developer Workflows

### Testing Audio Features
```bash
# Requires librosa, numpy, matplotlib
python3 melody_extractor_gui.py  # Launch GUI for manual testing
```

### Web Tools Testing
- Open `Music-Grid-Sequencer/index.html` in browser (no server needed, uses localStorage)
- Open `Online-piano/index.html` for keyboard/mouse piano interaction

### Dependencies
- **Python**: librosa, numpy, matplotlib, tkinter (standard library)
- **Web**: Tone.js (CDN), Tailwind CSS (CDN)

## Project-Specific Conventions

### File Organization
- Python tools are at root level with `_gui` suffix for GUI versions
- Markdown documents describe implementation approach (PIANO_SOLUTION.md pattern)
- HTML files are self-contained with embedded scripts (no separate JS files currently)

### Naming & Comments
- Function names use snake_case (Python) or camelCase (JS)
- Audio variables: `y` (waveform), `sr` (sample rate), standard librosa conventions
- State variables in sequencer: `grid`, `currentStep`, `currentSlot`, `notes` (note names)

### Data Formats
- **Pitch data**: Arrays of Hz values (float)
- **MIDI notes**: Arrays of 0-127 (librosa.hz_to_midi output)
- **Quantized notes**: Rounded MIDI values
- **Sequencer patterns**: `{notes: Array<Array<boolean>>, tempo: number, timestamp: number}`

## Integration Points & External Dependencies

### Audio Processing Chain
- **librosa** → Extract raw pitches → MIDI conversion → Optional quantization
- Real-time playback: Tone.js for web, no Python playback in current tools

### Storage
- Web tools use **browser localStorage** (no backend)
- Patterns saved with 2.5s success/error notification

### Tone.js Sequencing Pattern
```javascript
// Used in Music-Grid-Sequencer
const synth = new Tone.PolySynth(Tone.Synth, {
    envelope: {attack: 0.04, release: 0.2},
    volume: -8
}).toDestination();

// Standard step callback
loop = new Tone.Loop((time) => {
    // Play notes at current step based on grid state
    notes[pitch].forEach(col => {
        if (grid[pitch][col] === true) synth.triggerAttackRelease(note, "8n", time);
    });
}, "16n");
```

## Non-Obvious Gotchas & Tips

1. **Librosa sample rate**: Always capture `sr` from `librosa.load()` — it may not be 22050 Hz
2. **Piptrack is compute-heavy**: Processing long audio files in GUI will freeze the UI
3. **MIDI note range**: 0-127 standard, but Project-M focuses on melodic range (middle C and above)
4. **LocalStorage size limits**: ~5MB per domain — adequate for pattern slots but not audio data
5. **Tone.js Transport**: Must call `Tone.start()` before playback, especially after user interaction
6. **Piano key visual alignment**: Black keys require negative margin/offset positioning to appear between white keys
7. **Audio file paths**: GUI uses `filedialog.askopenfilename()` — relative paths won't work in deployed GUIs

## When Adding New Features

- **Audio processing**: Add to Python tools following the "Load → Extract → Visualize" pattern
- **Sequencing features**: Extend the grid-based approach with new Tone.js parameters (reverb, filter, etc.)
- **Piano improvements**: Modify PIANO_CONFIGURATION object, document in PIANO_SOLUTION.md
- **Web UI**: Use Tailwind CSS (already in CDN imports), maintain current color/layout conventions

## Documentation Conventions
- Complex implementations get a detailed `.md` file (see PIANO_SOLUTION.md as template)
- Include "What You Got" summary, implementation code, and technical reference
- Provide copy-paste code examples and ASCII diagrams for clarity
