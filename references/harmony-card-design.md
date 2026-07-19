# Harmony guide card — phone design notes (v3.5)

Single composed PNG for Telegram next to the OP-1. `scripts/op1_keys.py` owns all pixels.
Model never draws keyboards.

## Required layout (do not regress)

- Canvas portrait phone: ~1080×1120 after the 2×2 redesign (taller than the first 940 draft).
- Header: vibe quote (auto-shrink, never truncate) → mode line → mode-note on its **own** line.
- Scale degrees as **pill chips** (root chip orange).
- Main keyboard: full OP-1 bed, 24 keys, **F–E both octaves** (book p.65), integer white widths.
- Progression: **2×2 when 4 chords** (4-across was unreadable on phone). 1 / 2 / 3 / 2×2 / 3×N adaptive.
- Footer: wrapped "Sounds like: {reference}" + orange/blue legend + octave-shift hint.
- Deliver with `MEDIA:/abs/path.png` so Telegram shows a native photo.

## Keyboard geometry

- Whites: F G A B C D E ×2 (14). Blacks: standard 2-3 groups (10).
- Use integer `wk = width // 14`, center leftover pixels — float widths cause uneven keys.
- Black keys centered on white joints; separate fill for lit black keys (`lit_dark`) vs white (`lit`).
- Orange = root (+ sevenwavelength root dot when legible). Blue = other scale/chord tones.

## Theory reminders (see also harmony-renderer-notes.md)

- Diatonic QUALITY table wins over roman case (`vii` major → dim).
- `bVI` accidentals relative to MAJOR.
- Pentatonic progressions → parent mode via `PENT_PARENT`.
- Prefer flats from ROOT key signature, not mode family (A dorian → F#).

## QA

```bash
python3 scripts/run_keys_tests.py
python3 scripts/op1_keys.py --vibe "melancholy but hopeful" -o /tmp/guide.png
# Native vision on top crop + main kb crop + progression crop — not aux alone
```

Aux/proxy vision over-flags and invents defects on these cards the same way it did on
book mockups. Content correctness (chords/scale) can be double-checked in Python; pixel
craft needs native vision or a human.