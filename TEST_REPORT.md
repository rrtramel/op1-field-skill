# OP-1 Field Recipe Compiler — Test Report

Suite: `references/op1_recipe_examples.yaml` (23 prompts)

| # | Prompt | Status | Notes |
|---|--------|--------|-------|
| 1 | lush 80s pad | PASS | all checks pass |
| 2 | warm plucky bass | PASS | all checks pass |
| 3 | glassy bell | PASS | all checks pass |
| 4 | Boards of Canada-ish detuned keys | PASS | all checks pass |
| 5 | dark evolving drone | PASS | all checks pass |
| 6 | weird DNA glitch | PASS | all checks pass |
| 7 | acid lead | PASS | all checks pass |
| 8 | surf spring lead | PASS | all checks pass |
| 9 | lo-fi chip lead | PASS | all checks pass |
| 10 | metallic percussion | PASS | all checks pass |
| 11 | soft string pluck | PASS | all checks pass |
| 12 | dreamy pad with spring reverb | PASS | all checks pass |
| 13 | warm bass, no reverb | PASS | all checks pass |
| 14 | mono lead with glide | PASS | all checks pass |
| 15 | wide synthwave lead | PASS | all checks pass |
| 16 | robotic vocoder voice | PASS | all checks pass |
| 17 | aggressive industrial stab | PASS | all checks pass |
| 18 | subtle ambient texture | PASS | all checks pass |
| 19 | FM bell with delay | PASS | all checks pass |
| 20 | Pulse PWM pad | PASS | all checks pass |
| 21 | thick dsynth lead | PASS | all checks pass |
| 22 | lo-fi organ chords | PASS | all checks pass |
| 23 | retro 80s phase lead | PASS | all checks pass |

**Result: 23/23 passed.**

## Acceptance checks applied per prompt

- engine present
- envelope present
- play mode (pad/bass/lead)
- FX or explicit dry
- LFO or explicit static
- screen actions ([Synth]/[T1-4]/[Shift])
- mobile readable (<=34 lines)
- no percentages
- (validator) colors valid, labels match, graphic-only no fake numbers,
- split-range warnings present, LFO destination+parameter, numeric in range

## Sample rendered output (prompt 1)

```
🎛️ LUSH 80S PAD 🌊
━━━━━━━━━━━━━━
1) ENGINE — CLUSTER
Press [Synth] → [T1]. Hold [Shift]+[T1], choose CLUSTER.
Blue   WAVES       6
Ochre  WAVE ENV    60  (upper zone)
Grey   SPREAD      80
Orange UNISON      55
━━━━━━━━━━━━━━
2) 📈 ENVELOPE — pad (curve, no numbers)
Blue   ATTACK    gradual rise (dot ~halfway)
Ochre  DECAY     slow gentle drop
Grey   SUSTAIN   high plateau (dot near top)
Orange RELEASE   long right tail
━━━━━━━━━━━━━━
3) PLAY — poly · [Shift]+[T2], set POLY. Portamento off or low.
━━━━━━━━━━━━━━
4) ✨ FX — MOTHER 🚪 ON
Press [T3]. Hold [Shift]+[T3], choose MOTHER. Press [T3] so FX is ON.
Blue   DISTANCE    70
Ochre  GATE        moderate; don't fully choke the tail
Grey   COLOR       slightly dark
Orange MIX         medium, not washed out
━━━━━━━━━━━━━━
5) 🔄 LFO — VALUE 〰️ ON
Press [T4]. Hold [Shift]+[T4], choose VALUE. Press [T4] so LFO is ON.
Blue   SPEED       slow
Ochre  AMOUNT      18
Grey   DEST        Synth (engine)
Orange PARAMETER   SPREAD
━━━━━━━━━━━━━━
💡 Too bright → lower Mother COLOR (Grey) or reduce WAVE ENV (Ochre)
💡 Too static → raise LFO AMOUNT (Ochre)
⚠️ starting point — tweak by ear
```
