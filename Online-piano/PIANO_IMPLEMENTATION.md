# Online Piano - Implementation Guide

## Overview
The Online Piano uses a modular, configuration-driven approach to handle piano keys and keyboard mapping. This makes it easy to customize, extend, and maintain.

---

## Architecture

### 1. **Central Configuration** (`PIANO_CONFIGURATION`)
All piano-related settings are centralized in a single object at the top of the script:

```javascript
const PIANO_CONFIGURATION = {
    NOTES: ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
    START_OCTAVE: 4,
    NUM_OCTAVES: 2,
    WHITE_KEYS: ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    BLACK_KEYS_POSITIONS: { /* ... */ },
    KEYBOARD_MAP: { /* ... */ },
    KEYBOARD_VISUAL_MAP: { /* ... */ }
};
```

### 2. **Piano Components**

#### White Keys
- Displayed in order: C, D, E, F, G, A, B
- Span 48px width, 180px height
- CSS classes: `piano-key white-key`

#### Black Keys
- Positioned between white keys using `BLACK_KEYS_POSITIONS`
- Span 28px width, 100px height
- CSS classes: `piano-key black-key`
- Positioned absolutely for proper layering

#### Key Visual Guide
- Shows keyboard shortcut on each piano key
- Positioned at the top of each key
- Uses `.key-guide` CSS class

---

## Keyboard Mapping System

### Understanding the Mapping

The `KEYBOARD_MAP` connects computer keyboard keys to piano notes:

```javascript
KEYBOARD_MAP: {
    'KeyA': { note: 'C', octaveOffset: 0 },      // Current octave
    'KeyW': { note: 'C#', octaveOffset: 0 },     // Current octave
    'KeyK': { note: 'C', octaveOffset: 1 },      // Next octave (+1)
    // ... more mappings
}
```

**Components:**
- `note`: The note name (C, C#, D, etc.)
- `octaveOffset`: Relative to current octave (0 = same, 1 = next, -1 = previous)

### Layout

```
Row 1 (White keys):  A S D F G H J K L ;
                     C D E F G A B C D E

Row 2 (Black keys):  W E T Y U O
                     C# D# F# G# A#
```

### Visual Display Map

The `KEYBOARD_VISUAL_MAP` shows which keyboard key displays on which piano key:

```javascript
KEYBOARD_VISUAL_MAP: {
    'C4': 'A',          // Piano key C4 shows "A" keyboard shortcut
    'C#4': 'W',
    'D4': 'S',
    // ...
}
```

---

## How Piano Keys Are Created

### 1. **Initialization**
```javascript
createPiano() {
    const startOctave = PIANO_CONFIGURATION.START_OCTAVE;  // 4
    const numOctaves = PIANO_CONFIGURATION.NUM_OCTAVES;    // 2
    const whiteNotes = PIANO_CONFIGURATION.WHITE_KEYS;     // ['C','D','E'...]
    const blackKeysPositions = PIANO_CONFIGURATION.BLACK_KEYS_POSITIONS;
    // ...
}
```

### 2. **Loop Through Octaves**
For each octave from `START_OCTAVE` to `START_OCTAVE + NUM_OCTAVES`:
- Iterate through each white key
- Create white key DOM element
- Check if black key exists at this position
- Create black key DOM element if needed

### 3. **Element Creation**
```html
<div class="piano-key white-key" data-note="C4">
    <div class="key-guide">A</div>
    <div class="note-label">C4</div>
</div>

<div class="piano-key black-key" data-note="C#4" style="left: 36px; top: 0;">
    <div class="key-guide">W</div>
    <div class="note-label">C#4</div>
</div>
```

---

## Input Methods

### 1. **Computer Keyboard**
- Maps keyboard keys to piano notes using `noteForKey()`
- Respects current octave with `octaveOffset`
- Shift octave with Arrow Up/Down

### 2. **Mouse/Touch**
- Click/tap on piano key directly
- Uses `data-note` attribute to identify key
- Supports multi-touch

### 3. **MIDI Controller**
- Converts MIDI note numbers (0-127) to note names
- MIDI 60 = C4
- Formula: `note = NOTES[midiNote % 12] + (Math.floor(midiNote / 12) - 1)`

---

## Key Methods

### `noteForKey(event)`
Converts keyboard event to piano note:
```javascript
noteForKey(e) {
    const code = e.code;                              // e.g., "KeyA"
    const keyConfig = this.keyMap[code];              // Get mapping
    const note = keyConfig.note;                      // e.g., "C"
    const octave = this.currentOctave + keyConfig.octaveOffset;
    return note + octave;                             // e.g., "C4"
}
```

### `buildKeyboardMap()`
Constructs keyboard map from configuration:
```javascript
buildKeyboardMap() {
    const map = {};
    for (const [key, config] of Object.entries(PIANO_CONFIGURATION.KEYBOARD_MAP)) {
        map[key] = config;
    }
    return map;
}
```

### `createPiano()`
Generates all piano keys and sets up event handlers:
- Creates DOM elements for white and black keys
- Stores references in `keyElements` object
- Attaches mouse, touch, and keyboard event listeners

### `onKeyDown(note, keyElement)` / `onKeyUp(note, keyElement)`
Handles note playing:
- Triggers attack/release on synth
- Adds/removes "pressed" CSS class
- Updates visual feedback

---

## Customization Guide

### Add More Keyboard Keys
Edit `PIANO_CONFIGURATION.KEYBOARD_MAP`:
```javascript
KEYBOARD_MAP: {
    // ... existing mappings
    'KeyZ': { note: 'C', octaveOffset: -1 },  // Lower octave
    'KeyX': { note: 'D', octaveOffset: -1 },
}
```

Update visual map `KEYBOARD_VISUAL_MAP`:
```javascript
KEYBOARD_VISUAL_MAP: {
    // ... existing mappings
    'C3': 'Z',
    'D3': 'X',
}
```

### Change Piano Range
Modify `START_OCTAVE` and `NUM_OCTAVES`:
```javascript
START_OCTAVE: 3,      // Start from C3
NUM_OCTAVES: 3,       // Show 3 octaves (C3-B5)
```

### Add Custom Black Key Positions
Modify `BLACK_KEYS_POSITIONS`:
```javascript
BLACK_KEYS_POSITIONS: {
    0: 'C#',  // After white key index 0 (C)
    1: 'D#',  // After white key index 1 (D)
    // ... etc
}
```

### Adjust Key Dimensions
In `createPiano()`:
```javascript
white.style.width = '60px';      // Wider white keys
white.style.height = '200px';    // Taller white keys
black.style.width = '35px';      // Wider black keys
black.style.height = '120px';    // Taller black keys
```

---

## Event Flow

### Keyboard Press
```
Computer Key Pressed
  ↓
keydown event listener triggered
  ↓
noteForKey() resolves to note name (e.g., "C4")
  ↓
synth.triggerAttack("C4")
  ↓
Piano key element highlighted
  ↓
Note display updated
  ↓
Visual guide advanced (if in guide mode)
  ↓
Note saved to recording
```

### Piano Key Click
```
Mouse down on piano key
  ↓
mousedown event listener triggered
  ↓
Element identified via data-note attribute
  ↓
onKeyDown() called with note and element
  ↓
synth.triggerAttack(note)
  ↓
"pressed" class added (visual feedback)
  ↓
... same as above
```

---

## Data Structure Reference

### `keyElements` Object
Fast lookup map of all piano keys:
```javascript
{
    'C4': HTMLElement,
    'C#4': HTMLElement,
    'D4': HTMLElement,
    // ... all keys
}
```

### `pressedNotes` Set
Tracks currently playing notes:
```javascript
Set {
    'C4',
    'E4',
    'G4'  // Chord playing
}
```

### `keyMap` Object
Keyboard to note mapping:
```javascript
{
    'KeyA': { note: 'C', octaveOffset: 0 },
    'KeyW': { note: 'C#', octaveOffset: 0 },
    // ... more
}
```

---

## CSS Classes

| Class | Purpose | Element |
|-------|---------|---------|
| `.piano-key` | Base styling for all keys | white-key, black-key |
| `.white-key` | White key styling | White keys |
| `.black-key` | Black key styling | Black keys |
| `.pressed` | Visual feedback when pressed | Any key |
| `.key-guide` | Keyboard shortcut display | Top of each key |
| `.piano-container` | Scrollable container | Parent div |
| `.visual-suggestion` | Guide highlight | Active guide key |

---

## Troubleshooting

### Keys Not Responding
- Check browser console for errors
- Verify `PIANO_CONFIGURATION` is properly formatted
- Ensure `keyElements` object is populated after `createPiano()`

### Octave Shifts Wrong
- Check `octaveOffset` in `KEYBOARD_MAP`
- Verify `currentOctave` is between 1 and 7
- Test with keyboard arrows (↑/↓)

### Visual Guide Not Showing
- Check `.visual-suggestion` CSS class is applied
- Verify `showVisualGuide()` is being called
- Check console for element lookup errors

### MIDI Not Working
- Verify browser supports Web MIDI API
- Check system MIDI connections
- Look for "MIDI not available" in console

---

## Future Enhancements

1. **Extended Range**: Add more octaves or configurable ranges
2. **Alternative Layouts**: QWERTY, Dvorak, custom layouts
3. **Velocity Sensitivity**: Support for MIDI velocity on keyboard
4. **Key Bindings UI**: User-configurable keyboard shortcuts
5. **Virtual MIDI**: Send MIDI output to other applications
6. **Key Animation**: Custom animations for key presses
7. **Sound Visualization**: Frequency spectrum analyzer

---

## Testing Checklist

- [ ] All white keys play correct notes
- [ ] All black keys play correct notes
- [ ] Keyboard shortcuts work as labeled
- [ ] Octave shifts work with Arrow keys
- [ ] Sustain pedal (Space) works
- [ ] MIDI controller input works
- [ ] Touch works on mobile
- [ ] Visual feedback (key highlights) works
- [ ] Recording captures correct notes
- [ ] Visual guide shows correct notes
- [ ] Dark mode displays keys properly
- [ ] Performance is smooth with full octaves

