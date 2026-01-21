# Piano Implementation - Developer Cheat Sheet

## 📋 Quick File Map

| File | Purpose |
|------|---------|
| [index.html](index.html) | Main implementation + frontend |
| [PIANO_IMPLEMENTATION.md](PIANO_IMPLEMENTATION.md) | Full technical documentation |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Quick lookup for common tasks |
| [VISUAL_GUIDE.md](VISUAL_GUIDE.md) | Diagrams and visual explanations |
| [CHEAT_SHEET.md](CHEAT_SHEET.md) | This file - quick snippets |

---

## 🎹 Core Configuration (Top of Script)

```javascript
const PIANO_CONFIGURATION = {
    START_OCTAVE: 4,
    NUM_OCTAVES: 2,
    KEYBOARD_MAP: {
        'KeyA': { note: 'C', octaveOffset: 0 },
        'KeyW': { note: 'C#', octaveOffset: 0 },
        // ... more mappings
    },
    KEYBOARD_VISUAL_MAP: {
        'C4': 'A',
        'C#4': 'W',
        // ... more mappings
    }
};
```

---

## ⌨️ Adding New Keyboard Shortcuts

### Single Note
```javascript
// In KEYBOARD_MAP:
'KeyZ': { note: 'C', octaveOffset: -1 }  // Lower octave C

// In KEYBOARD_VISUAL_MAP:
'C3': 'Z'  // Show 'Z' label on C3 key
```

### Multiple Notes (Chord Mapping)
```javascript
// Not directly supported, but can be added with custom handler:
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        // Play C major chord
        synth.triggerAttack(['C4', 'E4', 'G4']);
    }
});
```

---

## 🎛️ Keyboard Layouts

### Current Layout
```
A S D F G H J    = C D E F G A B (octave 4)
W E T Y U        = C# D# F# G# A# (octave 4)
K L ; P [        = C D E F G (octave 5)
O 0              = C# D# (octave 5)
```

### To Add Octave 3
```javascript
// Update config:
START_OCTAVE: 3,
NUM_OCTAVES: 3,

// Add keyboard mappings:
'Digit1': { note: 'C', octaveOffset: -1 },
'Digit2': { note: 'D', octaveOffset: -1 },
'Digit3': { note: 'E', octaveOffset: -1 },
// etc.
```

---

## 🔍 Finding & Debugging

### Find a Note's Keyboard Shortcut
```javascript
// In browser console:
const note = 'C4';
const shortcut = PIANO_CONFIGURATION.KEYBOARD_VISUAL_MAP[note];
console.log(`${note} keyboard shortcut: ${shortcut}`);  // Output: A
```

### Find a Key's Piano Note
```javascript
// In browser console:
const keyCode = 'KeyA';
const mapping = PIANO_CONFIGURATION.KEYBOARD_MAP[keyCode];
const note = mapping.note + (4 + mapping.octaveOffset);
console.log(`${keyCode} plays: ${note}`);  // Output: C4
```

### Test Keyboard Mapping
```javascript
// In browser console:
pianoInstance.noteForKey({ code: 'KeyA' });  // Returns: 'C4'
pianoInstance.noteForKey({ code: 'KeyW' });  // Returns: 'C#4'
pianoInstance.noteForKey({ code: 'KeyZ' });  // Returns: null (not mapped)
```

### Check All Pressed Notes
```javascript
// In browser console:
console.log(pianoInstance.pressedNotes);  // Set { 'C4', 'E4', 'G4' }
```

### Trigger Note Manually
```javascript
// In browser console:
pianoInstance.synth.triggerAttack('C4');   // Play C4
pianoInstance.synth.triggerRelease('C4');  // Stop C4

// Or play a chord:
pianoInstance.synth.triggerAttack(['C4', 'E4', 'G4']);  // C major
pianoInstance.synth.triggerRelease(['C4', 'E4', 'G4']);
```

---

## 🎵 Note Conversion Snippets

### Keyboard Code → Note Name
```javascript
function getNote(keyCode, currentOctave = 4) {
    const config = PIANO_CONFIGURATION.KEYBOARD_MAP[keyCode];
    if (!config) return null;
    return config.note + (currentOctave + config.octaveOffset);
}

getNote('KeyA');  // Returns: 'C4'
getNote('KeyW');  // Returns: 'C#4'
```

### MIDI Number → Note Name
```javascript
function midiToNote(midiNumber) {
    const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    const noteName = notes[midiNumber % 12];
    const octave = Math.floor(midiNumber / 12) - 1;
    return noteName + octave;
}

midiToNote(60);   // Returns: 'C4'
midiToNote(64);   // Returns: 'E4'
midiToNote(72);   // Returns: 'C5'
```

### Note Name → MIDI Number
```javascript
function noteToMidi(noteName) {
    const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    const match = noteName.match(/([A-G]#?)(\d+)/);
    if (!match) return null;
    const [, note, octave] = match;
    const noteIndex = notes.indexOf(note);
    return (parseInt(octave) + 1) * 12 + noteIndex;
}

noteToMidi('C4');   // Returns: 60
noteToMidi('E4');   // Returns: 64
noteToMidi('C5');   // Returns: 72
```

---

## 🎨 Styling Customizations

### Resize Piano Keys
```javascript
// In createPiano() method, find these lines:
white.style.width = '48px';      // Adjust width
white.style.height = '180px';    // Adjust height
black.style.width = '28px';
black.style.height = '100px';
```

### Change Key Colors (CSS)
```css
.white-key {
    background: linear-gradient(to bottom, #ffffff 0%, #f8f9fa 100%);
    border: 1px solid #d1d5db;
}

.black-key {
    background: linear-gradient(to bottom, #374151 0%, #1f2937 100%);
    border: 1px solid #111827;
}

.piano-key.pressed {
    transform: translateY(2px);
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
}
```

### Customize Keyboard Label Position
```javascript
// In createPiano(), find:
let guide = `<div class="key-guide">${this.overlayMap[note]}</div>`;

// Edit CSS class to change position:
// .key-guide is currently positioned at: top: 10px; left: 50%
```

---

## 🔊 Sound Customization

### Change Instrument Sound
```javascript
// In createSynth() method:
const synthConfigs = {
    piano: {
        oscillator: { type: "triangle" },      // Try: sine, square, sawtooth
        envelope: { attack: 0.02, decay: 0.1, sustain: 0.3, release: 0.5 },
        volume: Tone.gainToDb(this.volume)
    }
};
```

### Add New Instrument
```javascript
// In PIANO_CONFIGURATION or createSynth():
synth: {
    oscillator: { type: "square" },
    envelope: { attack: 0.1, decay: 0.15, sustain: 0.6, release: 0.3 },
    volume: Tone.gainToDb(this.volume * 0.9)
},
harpsichord: {
    oscillator: { type: "sawtooth" },
    envelope: { attack: 0.001, decay: 0.3, sustain: 0, release: 0.1 },
    volume: Tone.gainToDb(this.volume * 0.8)
}
```

### Adjust Volume
```javascript
// In browser console:
pianoInstance.volume = 0.5;  // Set to 50%
pianoInstance.synth.volume.value = Tone.gainToDb(0.5);

// Or use the UI slider
```

---

## 📱 Input Method Implementations

### Keyboard Input
```javascript
noteForKey(e) {
    const code = e.code;
    const keyConfig = this.keyMap[code];
    if (!keyConfig) return null;
    return keyConfig.note + (this.currentOctave + keyConfig.octaveOffset);
}
```

### Mouse Input
```javascript
keyboard.addEventListener('mousedown', (e) => {
    const key = e.target.closest('.piano-key');
    if (key) this.onKeyDown(key.dataset.note, key);
});
```

### Touch Input
```javascript
keyboard.addEventListener('touchstart', (e) => {
    for (const t of e.changedTouches) {
        const el = document.elementFromPoint(t.clientX, t.clientY);
        const key = el && el.closest('.piano-key');
        if (key) this.onKeyDown(key.dataset.note, key);
    }
});
```

### MIDI Input
```javascript
handleMIDIMessage(event) {
    const [command, note, velocity] = event.data;
    const isNoteOn = (command & 0xF0) === 0x90 && velocity > 0;
    if (isNoteOn) {
        const midiNote = this.midiNoteToNoteName(note);
        this.synth.triggerAttack(midiNote);
    }
}
```

---

## 📊 State Management

### Get Current State
```javascript
// In browser console:
console.log({
    octave: pianoInstance.currentOctave,
    sustain: pianoInstance.sustainPedal,
    volume: pianoInstance.volume,
    instrument: pianoInstance.currentInstrument,
    pressed: Array.from(pianoInstance.pressedNotes),
    recording: pianoInstance.recording,
    midiAvailable: !!pianoInstance.midiAccess
});
```

### Change State Programmatically
```javascript
// Change octave:
pianoInstance.currentOctave = 5;

// Toggle sustain:
pianoInstance.sustainPedal = !pianoInstance.sustainPedal;

// Change instrument:
pianoInstance.createSynth('organ');

// Update volume:
pianoInstance.volume = 0.8;
pianoInstance.synth.volume.value = Tone.gainToDb(0.8);
```

---

## 🧪 Common Issues & Fixes

### Keys Not Responding After Config Change
```javascript
// Solution: Recreate the piano
pianoInstance.createPiano();
pianoInstance.setupUIEvents();
```

### Wrong Octave When Playing
```javascript
// Check keyboard map:
const mapping = pianoInstance.keyMap['KeyA'];
console.log(mapping);  // Should show { note: 'C', octaveOffset: 0 }

// Verify calculation:
const note = 'C' + (pianoInstance.currentOctave + 0);
console.log(note);  // Should show correct octave
```

### Visual Guide Not Showing
```javascript
// Debug visual guide:
pianoInstance.showVisualGuide(['C4', 'E4', 'G4']);

// Check CSS:
document.querySelectorAll('.visual-suggestion').length;  // Should be 3

// Check elements exist:
console.log(pianoInstance.keyElements['C4']);  // Should not be undefined
```

### MIDI Not Connecting
```javascript
// Check MIDI availability:
console.log(navigator.requestMIDIAccess);  // Should not be undefined

// Check current connections:
console.log(pianoInstance.midiAccess);  // Should not be null

// List MIDI inputs:
if (pianoInstance.midiAccess) {
    Array.from(pianoInstance.midiAccess.inputs.values()).forEach(input => {
        console.log(`MIDI Input: ${input.name}`);
    });
}
```

---

## 📈 Performance Tips

### Reduce Key Elements
```javascript
// Instead of 2 octaves:
NUM_OCTAVES: 2

// Use 1 octave for faster rendering:
NUM_OCTAVES: 1

// Or extend if needed:
NUM_OCTAVES: 3  // 21 white + 15 black = 36 DOM elements
```

### Optimize Event Handlers
```javascript
// Current: Event delegation (efficient)
keyboard.addEventListener('mousedown', handler);

// Not recommended: Individual handlers
for (each key) {
    key.addEventListener('mousedown', handler);  // Many listeners!
}
```

### Cache DOM Queries
```javascript
// Good: Store reference
this.keyElements = keyElements;
const key = this.keyElements['C4'];  // O(1) lookup

// Avoid: Repeated queries
const key = document.querySelector('[data-note="C4"]');  // Slower
```

---

## 🐛 Debugging Console Commands

```javascript
// Dump entire configuration
console.table(PIANO_CONFIGURATION);

// Test note conversion
for (let midi = 48; midi <= 84; midi++) {
    console.log(`MIDI ${midi} = ${pianoInstance.midiNoteToNoteName(midi)}`);
}

// Play all piano keys
Object.keys(pianoInstance.keyElements).forEach(note => {
    setTimeout(() => {
        pianoInstance.synth.triggerAttack(note);
    }, 100);
});

// Record performance
performance.mark('piano-init-start');
pianoInstance.createPiano();
performance.mark('piano-init-end');
performance.measure('piano-init', 'piano-init-start', 'piano-init-end');
console.log(performance.getEntriesByName('piano-init')[0].duration);

// Monitor events
document.addEventListener('keydown', (e) => {
    if (e.target === document.body) {
        console.log(`Key pressed: ${e.code}`);
    }
}, true);
```

---

## 📚 Related Files & Resources

- [Tone.js Documentation](https://tonejs.org/)
- [Web MIDI API](https://www.w3.org/TR/webmidi/)
- [Keyboard Event Code Reference](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/code)
- [MIDI Note Number Standard](https://en.wikipedia.org/wiki/MIDI_note)

---

## 🚀 Quick Start for Contributors

1. **Read this file first** ← You are here
2. **Review [QUICK_REFERENCE.md](QUICK_REFERENCE.md)** for common tasks
3. **Check [VISUAL_GUIDE.md](VISUAL_GUIDE.md)** for understanding flows
4. **Consult [PIANO_IMPLEMENTATION.md](PIANO_IMPLEMENTATION.md)** for deep dives
5. **Test changes** in browser console first before editing files

