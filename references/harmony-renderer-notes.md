# Harmony Renderer Notes (op1_keys.py)

Hard-won conventions from building the vibe→harmony guide renderer (2026-07).
Read this before touching `scripts/op1_keys.py` or building any harmony/theory output.
These took three iterations and a test battery to get right — do not relearn them.

## The renderer owns ALL theory

The model NEVER spells notes, computes chord qualities, or draws the keyboard. It emits a
structured object `{vibe, root, scale, progression[], reference}`; code does everything.
This is the same lesson as the recipe compiler: an LLM drawing a keyboard with text
produces wrong key counts, wrong black-key positions, wrong note labels — every time.

## Roman numeral conventions (tested)

- **Diatonic chords (no accidental): quality comes from the scale's QUALITY table, NOT
  the letter case of the roman numeral.** 'vii' in major is Bdim, not Bm; 'ii' in aeolian
  is dim. An early bug let the lowercase case-hint override the table — every dim chord
  came out min. Case/suffix is only a HINT for chromatic chords.
- **Accidentals are relative to the MAJOR scale of the key root** (standard pop-analysis
  convention): bVI in A minor = F natural (A major's VI is F#, flatten once), NOT E.
  This is how "bVI-bVII-i" (Creep, Hurt) is actually spelled in minor keys.
- Harmonic minor keeps its raised 7th as a SHARP (C#dim in D harmonic minor) even when
  the key otherwise prefers flats — sharp/flat spelling derives from the ROOT's key
  signature side (circle of fifths), not the mode family. A dorian spells F# (not Gb);
  Bb major spells Eb; D aeolian spells Bb.
- Accept flat root input ('Bb') and normalize to sharp internally (FLAT_TO_SHARP).

## OP-1 Field keyboard geometry (device layout)

- 24 keys, F-to-E, 2 octaves. 14 white (F G A B C D E ×2), 10 black (F# G# A# | C# D#
  per octave = the 2-3 groups). No note names printed on the physical keys.
- "The keyboard covers 2 octaves starting at 'F'." [Left]/[Right] transpose ±1 octave.
- Chord voicings must fit the 24-semitone window; wider spans get an octave-shift hint.

## Rendering lessons

- One composed PNG per answer (not N keyboard images) — the "guide card": vibe title,
  mode + one-line why, scale row, full keyboard with scale lit, progression as
  mini-keyboard cards, reference-song citation, legend.
- Title text must auto-shrink to fit — never truncate mid-word (caught by aux vision).
- Orange = root (with dot marker), blue = chord/scale tones, on BOTH the main keyboard
  and the mini chord cards. Consistent legend at the bottom.
- Dark panel cards (#1c1c22 bg, #22222a panels) read well on phones in daylight.

## The taxonomy is MODE-first, not key-first

"Key X = emotion Y" is horoscope-tier. The documented unit of emotional function is the
mode's signature interval: dorian raised-6th = melancholy with hope (Rohan/Time),
lydian raised-4th = floaty wonder (Yoda/Simpsons), phrygian flat-2nd = menace/exotic,
mixolydian flat-7th = bluesy longing, locrian flat-2nd+5th = ungrounded. Keys are just
transpositions. Every vibe→harmony mapping must cite a confirmed-positive reference
song (the needle-finder discipline: evidence ships with the match).

## Test battery (run after ANY theory change)

Spell all 7 diatonic chords in each of: C major, A aeolian, D dorian, E phrygian,
F lydian, G mixolydian, D harmonic minor. Plus chromatic: bVI/bVII/bIII in A aeolian.
Plus display: A dorian = F#, D aeolian = Bb, Bb major = Bb/Eb. The session log for
this battery is in the 2026-07 conversation; expected outputs are in the code comments
and were all verified correct at v0.1.
