# OP-1 Field — a weird, super-specific Hermes skill

> Hey — here's a weird super-specific skill for [Hermes Agent](https://hermes-agent.nousresearch.com). Do what you want with it.

It helps you use a **Teenage Engineering OP-1 Field** from your phone:

1. **Sound design** — describe a vibe → screen-actionable **text dial recipe**
2. **Harmony guide** — describe a mood → **one PNG** with key/scale/chords lit on the real OP-1 keyboard (24 keys, F–E)

Sitting outside with the OP-1 and a sound (or song feeling) in your head? Tell the agent. No menu-diving, no freehand fake keyboards.

Works with **any model** Hermes is pointed at — nothing hardwired to a specific LLM. MIT. Fork it, break it, ignore it.

---

## A note on what this is

**Inspiration for you to design with — not a patch generator that replaces your ears.** Free and open. If you can do better, fork it or open a PR.

---

## What makes it different

It's not a chatbot guessing. Both paths are **constrained compilers**:

```
# Sound
your vibe → intent match → fill recipe object → VALIDATE → deterministic text render

# Harmony
your vibe → taxonomy match → fill harmony object → VALIDATE → deterministic PNG render
```

The model only fills structured data. Real Python validators + renderers produce the final output and **refuse invalid recipes / bad theory**. Same clean output regardless of which model is driving.

**Coverage**
- Sound: 14 engines (Amp is reference-only), 10 effects, envelope, play modes, 6 LFOs
- Harmony: 12 scales/modes, diatonic chord tables, 20 vibe→harmony seeds with real song citations

---

## Sample — sound recipe (text)

```
🎛️ CYBERPUNK FM BASS 📻
━━━━━━━━━━━━━━
1) ENGINE — FM
Press [Synth] → [T1]. Hold [Shift]+[T1], choose FM.
Blue   FREQ        65  (raise until it growls/bites hard)
Ochre  FREQUENCY RATIO step to a low harmonic ratio (1 or 1/2)
Grey   TOPOLOGY    step until it sounds metallic/gnarly
Orange DETUNE      35
━━━━━━━━━━━━━━
2) 📈 ENVELOPE — stab (curve, no numbers)
Blue   ATTACK    instant
Ochre  DECAY     fast punchy drop
Grey   SUSTAIN   low-mid plateau
Orange RELEASE   short fade
━━━━━━━━━━━━━━
3) PLAY — mono · [Shift]+[T2], set MONO. Portamento low (slight glide).
━━━━━━━━━━━━━━
4) ✨ FX — TERMINAL 💻 ON
...
💡 Too harsh → lower FM FREQ (Blue) or raise Terminal MODEL (Grey)
⚠️ starting point — tweak by ear
```

Encoders are named by **color** (Blue / Ochre / Grey / Orange = T1–T4). Knobs with no on-screen number get a *watch-the-graphic* cue — never a made-up number.

---

## Sample — harmony guide (image)

```
Load op1-field. Melancholy but hopeful — end of the movie.
```

→ matches the Inception “Time” loop (A Dorian, i–v–VII–IV)  
→ renders one phone PNG: scale lit on the OP-1 F–E keyboard + progression cards + reference citation  
→ delivered inline on Telegram as a photo

Optional transpose:

```
Load op1-field. Pirate adventure keys in G.
```

---

## Install

This is a **multi-file skill** (needs `references/` + `scripts/`). Install the whole folder — a raw single-file `SKILL.md` URL will break it.

**Option A — clone (simplest)**
```bash
git clone https://github.com/rrtramel/op1-field-skill \
  ~/.hermes/skills/creative/op1-field
```

**Option B — GitHub tap (auto-updates)**
```bash
hermes skills tap add rrtramel/op1-field-skill
hermes skills install op1-field
```

Then start a new session (or `/reset`) and try:
```
Load op1-field. Give me a warm plucky bass.
Load op1-field. Melancholy but hopeful.
```

### Requirements
- **PyYAML** for the compilers (JSON fallback exists but YAML is the real path)
- **Pillow** for harmony PNG cards

```bash
uv pip install --system pyyaml pillow
# or: pip install pyyaml pillow
```

---

## Run the tests yourself

```bash
cd ~/.hermes/skills/creative/op1-field
python3 scripts/run_tests.py            # 23/23 sound recipes
python3 scripts/op1_compile.py --selftest
python3 scripts/run_keys_tests.py       # 74/74 harmony (theory + taxonomy + render)
```

Manual harmony card:
```bash
python3 scripts/op1_keys.py --vibe "melancholy but hopeful" -o /tmp/guide.png
python3 scripts/op1_keys.py --vibe "swashbuckling pirate adventure" --root G -o /tmp/guide.png
```

---

## Honest limitations

- **Inspiration while you're outside**, not a studio-final patch sheet. The OP-1 Field is a *差不多* (“close enough”) machine — values are launch points; tweak by ear.
- **Encoders are infinite/endless.** Instructions are “turn until the screen shows X,” never “to 3 o’clock.”
- **LFO SPEED is a one-knob, two-mode control** (tempo-synced numbers, then free-run clock face). Recipes name the zone; fine speed is by ear.
- **Harmony moods are conventions, not laws.** Tempo, orchestration, and context change the feel. Every taxonomy entry cites a real reference track so you can hear the shape yourself.
- **Amp is reference-only** (external input + tuner, no envelope recipe path).
- Exact sweet-spots vary by note, envelope, and taste.

---

## Contributing

PRs welcome. **If you know synths, harmony, or the OP-1 better than me, make it better.**

Good places to dig in:
- tighten parameter semantics from real device testing
- add sound intents to `references/op1_intent_mapping.yaml`
- add sound examples to `references/op1_recipe_examples.yaml` (test corpus)
- add harmony vibes to `references/op1_vibe_taxonomy.yaml` (must cite a real reference track)
- phone-card layout in `scripts/op1_keys.py` + `references/harmony-card-design.md`

Before a PR:
```bash
python3 scripts/run_tests.py
python3 scripts/run_keys_tests.py
```

---

## License

[MIT](./LICENSE). Use it, fork it, improve it.

---

*Designed by Remi Tramel — [remingtontramel.com](https://remingtontramel.com)*

*In memory of Dick Tramel, 1941–2026.*
