# Piano Implementation - Visual Guide

## 1. Piano Layout Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Online Piano (2 Octaves)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ╔════╗   ╔════╗   ╔════╗   ╔════╗   ╔════╗   ╔════╗   ╔════╗ │
│  ║ C4 ║   ║ D4 ║   ║ E4 ║   ║ F4 ║   ║ G4 ║   ║ A4 ║   ║ B4 ║ │
│  ╚════╝   ╚════╝   ╚════╝   ╚════╝   ╚════╝   ╚════╝   ╚════╝ │
│    A       S       D       F       G       H       J            │
│                                                                 │
│    ╔═══╗   ╔═══╗         ╔═══╗   ╔═══╗   ╔═══╗                 │
│    ║C# ║   ║D# ║         ║F# ║   ║G# ║   ║A# ║                 │
│    ║ 4 ║   ║ 4 ║         ║ 4 ║   ║ 4 ║   ║ 4 ║                 │
│    ╚═══╝   ╚═══╝         ╚═══╝   ╚═══╝   ╚═══╝                 │
│      W       E               T       Y       U                  │
│                                                                 │
│  ╔════╗   ╔════╗   ╔════╗   ╔════╗   ╔════╗   ╔════╗   ╔════╗ │
│  ║ C5 ║   ║ D5 ║   ║ E5 ║   ║ F5 ║   ║ G5 ║   ║ A5 ║   ║ B5 ║ │
│  ╚════╝   ╚════╝   ╚════╝   ╚════╝   ╚════╝   ╚════╝   ╚════╝ │
│    K       L       ;       P       [       O       0            │
│                                                                 │
│    ╔═══╗   ╔═══╗         ╔═══╗   ╔═══╗   ╔═══╗                 │
│    ║C# ║   ║D# ║         ║F# ║   ║G# ║   ║A# ║                 │
│    ║ 5 ║   ║ 5 ║         ║ 5 ║   ║ 5 ║   ║ 5 ║                 │
│    ╚═══╝   ╚═══╝         ╚═══╝   ╚═══╝   ╚═══╝                 │
│      O       0               (none)    (none)  (none)           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Keyboard Mapping Layers

```
Physical Keyboard Layout (QWERTY)
═════════════════════════════════════════════════════════════════

Number Row:  1  2  3  4  5  6  7  8  9  0
             ├─────────────────────────────────────────────┐
             │ Future extension (can add octave 3/6 here) │
             └─────────────────────────────────────────────┘

Letter Row 1: Q W E R T Y U I O P
             ├─────────────────────────────────────────┐
             │ W E T Y U = Black keys (Octave 4/5)    │
             │ O 0 = Black keys (Octave 5)            │
             └─────────────────────────────────────────┘

Letter Row 2: A S D F G H J K L ;
             ├──────────────────────────────────────────────┐
             │ A S D F G H J = White keys (Octave 4)      │
             │ K L ; = White keys (Octave 5)              │
             │ P [ = White keys (Octave 5)                │
             └──────────────────────────────────────────────┘

Letter Row 3: Z X C V B N M , . /
             └─ Available for future mappings
```

## 3. PIANO_CONFIGURATION Object Structure

```
PIANO_CONFIGURATION
│
├─ NOTES (Chromatic scale)
│  └─ ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
│
├─ START_OCTAVE
│  └─ 4 (display starts at octave 4)
│
├─ NUM_OCTAVES
│  └─ 2 (show octaves 4 and 5)
│
├─ WHITE_KEYS
│  └─ ['C', 'D', 'E', 'F', 'G', 'A', 'B']
│
├─ BLACK_KEYS_POSITIONS
│  ├─ 0 → 'C#'  (after C)
│  ├─ 1 → 'D#'  (after D)
│  ├─ 3 → 'F#'  (after F)
│  ├─ 4 → 'G#'  (after G)
│  └─ 5 → 'A#'  (after A)
│
├─ KEYBOARD_MAP (Computer key → Note mapping)
│  ├─ 'KeyA': { note: 'C', octaveOffset: 0 }
│  ├─ 'KeyW': { note: 'C#', octaveOffset: 0 }
│  ├─ 'KeyS': { note: 'D', octaveOffset: 0 }
│  ├─ ...
│  └─ 'Digit0': { note: 'D#', octaveOffset: 1 }
│
└─ KEYBOARD_VISUAL_MAP (Piano note → Keyboard label)
   ├─ 'C4': 'A'
   ├─ 'C#4': 'W'
   ├─ 'D4': 'S'
   └─ ...
```

## 4. Data Flow - Keyboard Input

```
┌──────────────────┐
│ User presses 'A' │
└────────┬─────────┘
         │
         ↓
    ┌────────────────────────┐
    │ 'keydown' Event        │
    │ event.code = 'KeyA'    │
    └────────┬───────────────┘
             │
             ↓
    ┌──────────────────────────────────────┐
    │ noteForKey(event)                    │
    │ - Lookup: keyMap['KeyA']             │
    │ - Get: { note: 'C', octaveOffset:0 } │
    │ - Calculate: 'C' + currentOctave     │
    │ - Return: 'C4'                       │
    └────────┬─────────────────────────────┘
             │
             ↓
    ┌───────────────────────────────────────┐
    │ synth.triggerAttack('C4')             │
    │ Sound produced by synthesizer         │
    └────────┬────────────────────────────┬─┘
             │                            │
             ↓                            ↓
    ┌──────────────────┐      ┌──────────────────────┐
    │ UI Updates       │      │ Record Note          │
    │ - Highlight key  │      │ - Add to recordings  │
    │ - Show label     │      │ - Check guide        │
    │ - Update status  │      │ - Save cache         │
    └──────────────────┘      └──────────────────────┘
```

## 5. Data Flow - Mouse/Touch Input

```
┌─────────────────────────┐
│ User clicks piano key   │
└────────┬────────────────┘
         │
         ↓
    ┌──────────────────────────┐
    │ 'mousedown' Event        │
    │ on piano-keyboard div    │
    └────────┬─────────────────┘
             │
             ↓
    ┌──────────────────────────────┐
    │ Find closest .piano-key      │
    │ Get data-note attribute      │
    │ Result: 'C#4'                │
    └────────┬─────────────────────┘
             │
             ↓
    ┌──────────────────────────────┐
    │ onKeyDown(note, element)     │
    │ - synth.triggerAttack('C#4') │
    │ - Add 'pressed' class        │
    │ - Update display             │
    └──────────────────────────────┘
```

## 6. Piano Key Creation Algorithm

```
createPiano()
    │
    ├─ Get config:
    │  ├─ startOctave = 4
    │  ├─ numOctaves = 2
    │  ├─ whiteNotes = ['C','D','E','F','G','A','B']
    │  └─ blackKeysPositions = { 0:'C#', 1:'D#', ... }
    │
    ├─ Clear keyboard div
    │
    ├─ FOR octave 4 TO 5:
    │  │
    │  └─ FOR each white note (C-B):
    │     │
    │     ├─ Create white key <div>
    │     │  ├─ Set class: 'piano-key white-key'
    │     │  ├─ Set data-note: 'C4' (or D4, etc.)
    │     │  ├─ Add keyboard label if exists
    │     │  └─ Add note label
    │     │
    │     ├─ Check if black key exists at this position
    │     │
    │     └─ If yes, create black key <div>
    │        ├─ Set class: 'piano-key black-key'
    │        ├─ Set position: absolute (overlaid)
    │        ├─ Set data-note: 'C#4' (or D#4, etc.)
    │        ├─ Add keyboard label if exists
    │        └─ Add note label
    │
    └─ Store all keys in keyElements map
       ├─ keyElements['C4'] = HTMLElement
       ├─ keyElements['C#4'] = HTMLElement
       └─ ...
```

## 7. Input Method Comparison

```
┌─────────────┬──────────────────┬───────────────┬─────────────────┐
│   METHOD    │   RESOLUTION     │   ATTRIBUTES  │   PROS/CONS     │
├─────────────┼──────────────────┼───────────────┼─────────────────┤
│ Keyboard    │ noteForKey()     │ octaveOffset  │ Fast, labels    │
│             │ KEYBOARD_MAP     │ configurable  │ Configurable    │
├─────────────┼──────────────────┼───────────────┼─────────────────┤
│ Mouse       │ data-note attr   │ Direct note  │ Intuitive, no   │
│             │ DOM lookup       │ (no offset)  │ octave shift    │
├─────────────┼──────────────────┼───────────────┼─────────────────┤
│ Touch       │ coordinate →     │ Touch ID     │ Mobile support  │
│             │ element lookup   │ tracking     │ Multi-touch OK  │
├─────────────┼──────────────────┼───────────────┼─────────────────┤
│ MIDI        │ midiNoteToNote   │ Velocity 0-  │ Full instrument │
│             │ Name()           │ 127 supported│ Professional    │
└─────────────┴──────────────────┴───────────────┴─────────────────┘
```

## 8. Note Naming Convention

```
MIDI Number → Note Name Conversion
═══════════════════════════════════

MIDI 60 = C4 (Middle C)

Formula:
  noteName = NOTES[midiNote % 12]  // Gets C, C#, D, etc.
  octave = floor(midiNote / 12) - 1

Examples:
  MIDI 60 → NOTES[0] + (5-1) = 'C4'       ✓
  MIDI 61 → NOTES[1] + (5-1) = 'C#4'      ✓
  MIDI 72 → NOTES[0] + (6-1) = 'C5'       ✓
  MIDI 48 → NOTES[0] + (4-1) = 'C3'       ✓

Note: Octave changes at C
  B3 (MIDI 59) → NOTES[11] + (4-1) = 'B3'
  C4 (MIDI 60) → NOTES[0] + (5-1) = 'C4'
```

## 9. State Management

```
OnlinePiano Instance State
═══════════════════════════════════════════

Current State Variables:
├─ currentOctave: 4 (1-7 range)
├─ sustainPedal: false (true/false)
├─ volume: 0.7 (0-1 range)
├─ currentInstrument: 'piano'
├─ pressedNotes: Set { 'C4', 'E4', 'G4' }
├─ recording: false
├─ recordedNotes: ['C4', 'E4', 'G4', ...]
├─ guideTuneNotes: ['C4', 'E4', 'G4', ...]
├─ tunePlaybackIdx: 0
└─ activeMidiNotes: Set { 60, 64, 67 }

Key UI References:
├─ synth: Tone.PolySynth instance
├─ keyElements: { 'C4': HTMLElement, ... }
├─ midiAccess: Web MIDI API instance
└─ visualGuideNotes: ['C4', 'E4']
```

## 10. Customization Examples

### Example 1: Add 'Z' for C3
```javascript
// In KEYBOARD_MAP:
'KeyZ': { note: 'C', octaveOffset: -1 }

// In KEYBOARD_VISUAL_MAP:
'C3': 'Z'

// Visual result: When user presses 'Z', plays C3
// When octave is 4: calculates C + (4-1) = C3 ✓
```

### Example 2: Extend to 3 Octaves
```javascript
// Change configuration:
START_OCTAVE: 3
NUM_OCTAVES: 3

// Add keyboard shortcuts for octave 3:
'KeyV': { note: 'C', octaveOffset: -1 }
'KeyB': { note: 'D', octaveOffset: -1 }
// etc.

// Result: Display C3 to B5 (3 octaves)
```

### Example 3: Resize Keys
```javascript
// In createPiano():
white.style.width = '60px';      // was 48px
white.style.height = '200px';    // was 180px
black.style.width = '35px';      // was 28px
black.style.height = '120px';    // was 100px

// Result: Larger, easier to click keys
```

