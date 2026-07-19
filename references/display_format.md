# OP-1 Field Display Format — CRITICAL REFERENCE

> ⚠️ **SOURCE PRIORITY:** This file was built from web research + native-vision screen extraction and
> has been found to contain hallucinations (Random LFO encoder map, Velocity Ochre "unused", and an
> over-broad "values typically 0-99" claim). The **OP-1 Field Notebook** PDF is the authoritative
> verified source and OVERRIDES this file wherever they disagree. LFO AMOUNT is bipolar **−100 → +100**
> on Value/Element/Velocity (NOT 0-99). Several knobs that are "filter cutoffs" by function show NO
> number on screen (graphic_only) — do not assume a numeric display from the function. See SKILL.md
> pitfalls for the function-vs-display rule.
>
> Verified through multiple independent references. See the README for OP-1 & sound design resources.

## How Values Are Actually Displayed

### The Screen
- The OP-1 Field has a **custom color LCD** (not OLED on Field)
- Each engine has **unique, engine-specific graphics** — NOT generic bar charts or labeled parameters
- When you turn an encoder, a **pop-up appears** showing the parameter name and numeric value
- Values are **integers** (0-99 or 0-127 depending on parameter)
- The main screen shows **visual representations** (waveforms, shapes, curves) that change as you turn encoders

### Encoders Are Identified by COLOR
The community and tutorials refer to encoders by color, NOT by T1/T2/T3/T4:
- **Blue** = T1 (leftmost)
- **Beige/Ochre** = T2
- **Gray** = T3
- **Orange/Red** = T4 (rightmost)

In recipes, use BOTH: "Blue (T1)" for clarity.

### Value Ranges
- **MIDI CC**: All parameters map to 0-127 (confirmed from official MIDI reference)
- **On-screen**: Values appear as integers, typically 0-99 (per SON WU tutorials showing values like 49, 99)
- **NOT percentages**: The OP-1 never shows "50%" — it shows "50" or a graphical position
- **Some parameters have special ranges**:
  - Number of waves (Cluster): 0-6 (discrete, not continuous)
  - Octave (Digital): -5 to +5 (bipolar)
  - Filter style: discrete options (LP/BP/HP/Notch)

### Non-Linear Parameters
Some parameters have non-obvious behavior:
- **DR. Wave Pulse**: Center detent at 49. Counterclockwise = PWM. Clockwise = oscillator sync.
- **DR. Wave Filter**: 0 = open. Turning right goes HP→LP in one continuous sweep.
- **DR. Wave Blue knob**: Cycles through waveforms (Saw→Square→Triangle) then into sample rate reduction.
- **FM Freq.**: Adjacent values can jump between harmonic and discordant.

## Recipe Format Rules

### DO:
- Use **integer values** (0-99 or 0-127), NOT percentages
- Use **color names** alongside T1-T4: "Blue (T1) Waves = 5"
- Describe **what the screen shows** when relevant: "Blue knob cycles through waveforms: noise+pulse → pulse → square → saw → saw+sub"
- Note **non-linear behavior**: "Gray knob: 0=open, sweep goes HP→LP"
- Use **Hz or tempo divisions** for LFO speed: "~0.5 Hz" or "🕐 1/8"
- Reference the **SON WU tutorials** for engine-specific visual behavior

### DON'T:
- Use percentages for parameter values
- Assume all parameters are linear 0-100
- Use bar charts (▓░) for parameter values — the OP-1 doesn't show bars
- Assume T1-T4 labels are universal — LFO types have DIFFERENT T1-T4 layouts
- Give LFO speed as a percentage

## LFO Type Differences (CRITICAL)

Each LFO type has a COMPLETELY DIFFERENT T1-T4 layout. You MUST specify the type first.

### Value LFO
- Blue (T1): Speed (Hz or tempo-synced)
- Beige (T2): Amount (modulation depth)
- Gray (T3): Destination Category (Engine/Envelope/FX)
- Orange (T4): Destination Parameter (specific param within category)

### Random LFO
- Blue (T1): **Speed** (random update rate) — CORRECTED per OP-1 Field Notebook p.137
- Beige (Ochre) (T2): **Amount** (randomization intensity, 0 → +100) — CORRECTED per book p.137
- Gray (T3): Destination Category (Engine/Envelope/FX)
- Orange (T4): Parameter / Envelope (param selector + AD envelope shaping)
- NOTE: this file PREVIOUSLY had Blue=Amount/Ochre=Speed — that was WRONG. The book (the verified
  source) confirms Blue=Speed, Ochre=Amount. Do not revert.

### Tremolo LFO
- Blue (T1): Speed
- Beige (Ochre) (T2): Pitch Amount (negative = invert)
- Gray (T3): Volume Amount (negative = invert)
- Orange (T4): Envelope (attack/decay shaping)
- Shift+Orange: Waveform select (sine, saw, exp, square, blip)

### Velocity LFO
- Blue (T1): **Volume Amount** (0 → +100) — how much velocity affects master volume
- Beige (Ochre) (T2): **Destination Amount** (−100 → +100) — CORRECTED: Ochre is NOT unused
  (this file previously said "(unused)" — WRONG per OP-1 Field Notebook p.145)
- Gray (T3): Destination Category
- Orange (T4): Destination Parameter

### Element LFO
- Blue (T1): Source (G-force/Radio/Line-in/Mic/Synth Env/Synth Level)
- Beige (Ochre) (T2): Amount
- Gray (T3): Destination Category
- Orange (T4): Destination Parameter

### MIDI LFO
- Blue (T1): CC 1
- Beige (Ochre) (T2): CC 2
- Gray (T3): CC 3
- Orange (T4): CC 4

## MIDI CC Reference (for programmatic control)
| CC | Function | Range |
|----|----------|-------|
| 46-49 | Synth params 1-4 (T1-T4 engine) | 0-127 |
| 50-53 | Envelope A/D/S/R | 0-127 |
| 54-57 | FX params 1-4 | 0-127 |
| 58-61 | LFO params 1-4 | 0-127 |
| 62 | Randomize patch | ≥64 |
| 63 | Reset patch | ≥64 |
| 70-73 | Master FX params 1-4 | 0-127 |
| 74-77 | Master compressor params 1-4 | 0-127 |
