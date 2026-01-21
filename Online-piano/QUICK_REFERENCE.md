# Quick Reference - Piano Implementation

## File Structure
```
Online-piano/
├── index.html                 # Main implementation
├── PIANO_IMPLEMENTATION.md    # Full documentation
└── QUICK_REFERENCE.md         # This file
```

---

## Central Configuration

Located at the top of the `<script>` section in `index.html`:

```javascript
const PIANO_CONFIGURATION = {
    NOTES: ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
    START_OCTAVE: 4,        // First visible octave
    NUM_OCTAVES: 2,         // Number of octaves to display
    WHITE_KEYS: ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    BLACK_KEYS_POSITIONS: { /* position mappings */ },
    KEYBOARD_MAP: { /* computer key → piano note */ },
    KEYBOARD_VISUAL_MAP: { /* piano key → keyboard label */ }
};
```

---

## Current Keyboard Layout

### Row 1: White Keys (A-S-D-F-G-H-J)
```
Keyboard: A  S  D  F  G  H  J
Piano:    C  D  E  F  G  A  B  (current octave)
```

### Row 2: Black Keys (W-E-T-Y-U)
```
Keyboard: W  E  T  Y  U
Piano:    C# D# F# G# A#  (current octave)
```

### Row 3: Next Octave (K-L-;-P-[)
```
Keyboard: K  L  ;  P  [
Piano:    C  D  E  F  G  (next octave)
```

### Row 4: Black Keys in Next Octave (O-0)
```
Keyboard: O  0
Piano:    C# D#  (next octave)
```

---

## Key Methods

### Keyboard Input
```javascript
noteForKey(event)              // Converts keyboard event → note name
buildKeyboardMap()             // Creates keyboard mapping from config
```

### Piano Creation
```javascript
createPiano()                  // Generates all piano keys
```

### Key Events
```javascript
onKeyDown(note, element)       // Triggers note attack
onKeyUp(note, element)         // Triggers note release
highlightPianoKey(note, bool)  // Adds/removes visual highlight
```

### User Feedback
```javascript
showNotePlayed(note)           // Display current note
showVisualGuide(notes)         // Highlight guide notes
clearVisualGuide()             // Remove guide highlights
```

---

## To Add a Keyboard Shortcut

**Example: Add 'Z' key for C3 (lower octave C)**

1. **Add to `KEYBOARD_MAP`:**
   ```javascript
   KEYBOARD_MAP: {
       // ... existing ...
       'KeyZ': { note: 'C', octaveOffset: -1 },
   }
   ```

2. **Add to `KEYBOARD_VISUAL_MAP`:**
   ```javascript
   KEYBOARD_VISUAL_MAP: {
       // ... existing ...
       'C3': 'Z',
   }
   ```

3. **Test** - Press 'Z' key, should play C3

---

## To Extend Piano Range

**Example: Show 3 octaves instead of 2**

```javascript
const PIANO_CONFIGURATION = {
    START_OCTAVE: 3,        // Changed from 4
    NUM_OCTAVES: 3,         // Changed from 2
    // ... rest unchanged
};
```

**Add keyboard shortcuts for octave 3:**
```javascript
KEYBOARD_MAP: {
    // Existing mappings for octaves 4-5...
    
    // New mappings for octave 3
    'Digit1': { note: 'C', octaveOffset: -1 },
    'Digit2': { note: 'D', octaveOffset: -1 },
    // ... etc
}
```

---

## To Change Key Dimensions

In `createPiano()` method:

```javascript
// White keys
white.style.width = '48px';    // Wider/narrower
white.style.height = '180px';  // Taller/shorter

// Black keys
black.style.width = '28px';    // Wider/narrower
black.style.height = '100px';  // Taller/shorter
```

---

## Input Methods Supported

| Method | Implementation | Config |
|--------|---|---|
| **Keyboard** | `noteForKey()` → `KEYBOARD_MAP` | `PIANO_CONFIGURATION.KEYBOARD_MAP` |
| **Mouse** | Direct element click | `.data-note` attribute |
| **Touch** | `touchstart`/`touchend` events | Built-in |
| **MIDI** | `handleMIDIMessage()` | Web MIDI API |

---

## Data Structures

### `keyElements`
```javascript
{
    'C4': HTMLElement(div.white-key),
    'C#4': HTMLElement(div.black-key),
    'D4': HTMLElement(div.white-key),
    // ... all keys
}
```
Used for quick DOM access during playback.

### `pressedNotes`
```javascript
Set { 'C4', 'E4', 'G4' }
```
Tracks which notes are currently held down.

### `keyMap`
```javascript
{
    'KeyA': { note: 'C', octaveOffset: 0 },
    'KeyW': { note: 'C#', octaveOffset: 0 },
    // ...
}
```
Maps keyboard codes to note information.

---

## CSS Classes for Styling

```css
.piano-key          /* All keys */
.white-key          /* White keys */
.black-key          /* Black keys */
.pressed            /* Key currently pressed */
.key-guide          /* Keyboard shortcut label */
.visual-suggestion  /* Highlighted guide note */
```

---

## Common Customizations

| Need | Location | Change |
|------|----------|--------|
| Add keyboard shortcut | `KEYBOARD_MAP` | Add `'KeyX': { note: '...', octaveOffset: ... }` |
| Change visual label | `KEYBOARD_VISUAL_MAP` | Update `'NOTE': 'KEY'` |
| Extend octaves | `START_OCTAVE`, `NUM_OCTAVES` | Update numbers |
| Resize keys | `createPiano()` method | Adjust `style.width` / `style.height` |
| Change sound | `createSynth()` method | Modify `synthConfigs` |

---

## Event Flow Example: Press 'A' Key

```
1. User presses 'A' key
   ↓
2. 'keydown' event fires with code='KeyA'
   ↓
3. noteForKey() is called
   - Gets keyMap['KeyA'] = { note: 'C', octaveOffset: 0 }
   - Calculates: 'C' + (4 + 0) = 'C4'
   ↓
4. synth.triggerAttack('C4')
   ↓
5. keyElements['C4'].classList.add('pressed')
   ↓
6. showNotePlayed('C4') → displays "Playing: C4"
```

---

## Debugging Tips

**Piano keys not responding?**
1. Check browser console (F12)
2. Verify `PIANO_CONFIGURATION` syntax
3. Ensure `createPiano()` was called

**Wrong notes playing?**
1. Check `octaveOffset` in `KEYBOARD_MAP`
2. Verify `currentOctave` value
3. Test with arrow keys

**Visual guide not working?**
1. Check if `.visual-suggestion` CSS class exists
2. Verify guide notes are in piano range
3. Look for element lookup errors

**MIDI not working?**
1. Check browser supports Web MIDI API
2. Verify MIDI device is connected and selected
3. Check console for "MIDI not available" message

---

## Performance Notes

- Piano generates **14 white keys + 10 black keys** = **24 DOM elements** (2 octaves)
- Each key has `data-note`, keyboard label, and note label
- Event handlers use event delegation where possible
- `keyElements` object provides O(1) lookup time for DOM access

---

## File References

- **Main file**: [index.html](index.html)
- **Full documentation**: [PIANO_IMPLEMENTATION.md](PIANO_IMPLEMENTATION.md)
- **This file**: QUICK_REFERENCE.md

