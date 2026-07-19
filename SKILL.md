---
name: op1-field
description: >
  OP-1 Field portable assistant. TWO modes, ONE skill (do not split): (1) sound vibe →
  phone text dial recipe for engines/FX/envelope/LFO; (2) emotional vibe → ONE PNG harmony
  guide card (key/scale/chords lit on the real OP-1 24-key F–E keyboard). Trigger sound
  mode with pad/bass/lead/engine language; trigger harmony mode with key/scale/chord/mood-
  for-a-song language ("melancholy but hopeful", "pirate adventure keys"). Both paths
  use constrained compilers — model never freehands recipe text or keyboard images.
version: 3.5.0
author: Remi Tramel (remingtontramel.com)
license: MIT
tags: [creative, music, synth, op1, teenage-engineering, sound-design, harmony, mobile]
---

# OP-1 Field — Sound Recipes + Harmony Guide

> **⚠️ MAINTAINERS / FUTURE MODELS — READ FIRST.** This is a **public, MIT-licensed skill**
> published under the author's name. When authoring, editing, or extending it, write ONLY
> OP-1 Field / sound-design / harmony content + the compiler code. **Do NOT inject any personal
> context about the user or owner** — no names (beyond the existing author credit + dedication),
> no quotes, career/employer/sales details, machine-specific paths beyond `~/.hermes/skills/...`,
> no API keys, no third-person commentary about the user. Provenance notes stay in gitignored
> private local notes. Before publish: `grep -rinE "api_key|secret|token|/home/|@|akash|gpu|sales|prospect|career"`
> should surface nothing but synth terms. Repo = synth knowledge + code + the author's four
> intentional credits (frontmatter author, README footer, dedication, LICENSE).

**What it does:** Two modes for the OP-1 Field on your phone:
1. **Sound design** — describe a vibe → compact, *physically dialable* text recipe
   (which page, which colored knob, what to watch on screen)
2. **Harmony guide** — describe a mood → one PNG card with key/scale/chords lit on
   the real OP-1 keyboard (24 keys, F–E)

**What changed in v3:** both paths are **constrained compilers**, not freehand
generators. The model fills a validated intermediate object; real Python validators
+ deterministic renderers refuse invalid output. That kills freehanded recipe text
and freehanded keyboard drawings.

## Architecture

### Sound path
```
USER VIBE
  ↓  Intent parser            (match aliases in op1_intent_mapping.yaml)
  ↓  Sound target model       (brightness/width/density/motion/space/articulation)
  ↓  Candidate ranker         (rank engines / FX / LFOs by score_bias)
  ↓  OP-1 semantic translator (map target → params via op1_recipe_compiler_reference.yaml)
  ↓  Structured recipe object (op1_recipe_schema.yaml shape)
  ↓  Validator                (op1_recipe_validation.yaml rules, enforced by op1_compile.py)
  ↓  Deterministic renderer   (op1_compile.py render() → fixed Telegram format)
  ↓  FINAL TEXT RECIPE
```

### Harmony path
```
USER VIBE
  ↓  Mode router              (key/scale/chord/song-mood language → this path)
  ↓  Taxonomy resolve         (op1_vibe_intent.py → op1_vibe_taxonomy.yaml)
  ↓  Harmony object           ({root, scale, progression, reference, vibe})
  ↓  Validator                (op1_keys.validate — roots/scales/romans)
  ↓  Deterministic PNG        (op1_keys.render_guide → OP-1 F–E keyboard + chord cards)
  ↓  FINAL IMAGE              (deliver with MEDIA:/abs/path.png on Telegram)
```

**The LLM does NOT write the final recipe text or draw the keyboard.** It fills the
object. The renderer produces the output. If the object is invalid, the compiler errors
out instead of rendering.

## Files

```
~/.hermes/skills/creative/op1-field/
├── SKILL.md                                  ← this file
├── CHANGELOG.md                              ← v3 architecture change notes
├── TEST_REPORT.md                            ← recipe pass/fail report (regenerate any time)
├── references/
│   ├── op1_recipe_compiler_reference.yaml    ← CANONICAL merged source of truth (engines, FX,
│   │                                           envelope, play modes, LFOs, screen/action maps,
│   │                                           value types, split-ranges, shift layers, confidence)
│   ├── op1_adjective_index.yaml              ← ADJECTIVE→PARAMETER REVERSE INDEX (95 sound-design
│   │                                           adjectives mapped to concrete params with audible_tendency
│   │                                           evidence; used by the fallback strategy when no alias matches.
│   │                                           v3.1 adds 46 new descriptors: material textures (velvety,
│   │                                           creamy, crystalline, molten, brittle, rubbery, plastic,
│   │                                           papery, ceramic, tubular, corroded, dilapidated), motion
│   │                                           verbs (breathing, bouncing, crawling, seeping, cascading,
│   │                                           trickling, dripping, blooming, wilting, erupting, imploding,
│   │                                           shattering, melting, freezing), atmospheres (underwater,
│   │                                           feathered, gnarly, feral, pointillist, smeared, pristine,
│   │                                           sterile, saturated, compressed), and genre archetypes
│   │                                           (boards_of_canada, aphex_twin, shoegaze, dub_techno,
│   │                                           vaporwave, lofi_hip_hop, dungeon_synth, darksynth,
│   │                                           chillwave, drone).)
│   ├── op1_intent_mapping.yaml               ← vibe → ranked engine/FX/LFO candidates (20 archetypes, 85+ aliases)
│   ├── op1_recipe_schema.yaml                ← the intermediate recipe object shape + worked example
│   ├── op1_recipe_validation.yaml            ← deterministic validation rules (mirrored in op1_compile.py)
│   ├── op1_recipe_examples.yaml              ← 23 worked recipe objects (also the test corpus)
│   ├── display_format.md                     ← READ FIRST. LFO encoder maps, MIDI CC, non-linear behavior
│   ├── screen_behavior.yaml                  ← per-param [N]/[G]/[B] + visual descriptions (native-vision)
│   ├── screen_animation_behavior.yaml        ← what ANIMATES when you turn each encoder
│   │                                           (many entries still inferred; device photos win on conflict)
│   ├── engines_effects_v2.yaml               ← param NAMES + ranges (device + TE guide + community refs)
│   ├── engines_effects.md                    ← human-readable engine/effect reference
│   ├── community_tips.md                     ← real-world technique + correction-macro material
│   ├── harmony-renderer-notes.md             ← op1_keys.py conventions: roman-numeral rules (dim table wins,
│   │                                           bVI-relative-to-major), OP-1 keyboard geometry (24 keys F-to-E),
│   │                                           mode-first emotion taxonomy, test battery. READ before touching harmony output.
│   ├── harmony-card-design.md                ← phone PNG layout defaults (2×2 grid, integer keys, contrast,
│   │                                           MEDIA: delivery). Re-check with native vision after design edits.
│   └── op1_vibe_taxonomy.yaml                ← 20 vibe→{root,scale,progression,reference} seeds for harmony mode
├── scripts/
│   ├── op1_compile.py                        ← validator + deterministic renderer (the enforcement layer)
│   ├── op1_keys.py                           ← harmony guide renderer: vibe→{root,scale,progression}→ONE PNG
│   │                                           guide card (OP-1 24-key keyboard + chord cards). Phone layout v2.
│   │                                           See references/harmony-renderer-notes.md + harmony-card-design.md.
│   ├── op1_vibe_intent.py                    ← fuzzy alias resolver for taxonomy (exact→substring→tokens)
│   ├── run_keys_tests.py                     ← 74 harmony checks (theory + taxonomy + render smoke + intent)
│   └── run_tests.py                          ← compiles + checks all 23 example recipes
└── output/
    └── training_log.jsonl                    ← vibe→recipe log (RAG/fine-tune corpus)
```

`op1_recipe_compiler_reference.yaml` is the **main normalized source**. The older files
(`screen_behavior.yaml`, `display_format.md`, `engines_effects_v2.yaml`) remain as upstream
provenance — the compiler reference is built from them and is what you read first when generating.
Runtime does NOT need any PDFs, YouTube downloads, or build-time verification tools.
The screen facts already live in the YAML.

**Public surface rule:** ship only what a stranger needs to *generate* a recipe or
card. Build-time verification tools (frame dumps, PDF renderers, audit diaries,
research dumps) stay out of the published tree — they do **not** run at skill-use
time. Private source notes stay local/unpublished. Before adding any verification
package back into the published tree, ask: "Does a stranger with only the git
clone need this file to produce a recipe/card?" If no → omit it.

## How to Use

```
# Sound-design mode (text recipe)
"Load op1-field. I want a lush 80s pad."
"Load op1-field. Warm bass, no reverb."
"Load op1-field. Something weird on the DNA engine."
"Load op1-field. Tell me about the FM engine."   ← research mode

# Harmony mode (ONE PNG guide card on Telegram)
"Load op1-field. Melancholy but hopeful — end of the movie."
"Load op1-field. Show me the keys for a pirate adventure in G."
"Load op1-field. Dorian loop like Time from Inception."
```

## Mode router (do this BEFORE A–H)

**Keep these as ONE skill.** Same device, same on-the-go audience, same discipline
(vibe → validated object → deterministic render). Do NOT split into a second skill —
shared OP-1 layout/pitfalls/provenance would fork and drift.

| User language | Path | Deliverable |
|---|---|---|
| pad / bass / lead / engine / FX / LFO / "dial" / "knobs" | sound recipe (`op1_compile.py`) | Telegram **text** |
| key / scale / chords / progression / "fingering" / song-mood / film cue / roman numerals | harmony guide (`op1_keys.py` + taxonomy) | Telegram **PNG** via `MEDIA:/abs/path.png` |
| ambiguous | ask one short clarifier OR default to sound recipe if any engine word appears | — |

Harmony path (when routed there):
```bash
python3 scripts/op1_keys.py --vibe "…" [-o /tmp/op1_guide.png]
# optional transpose: --root G
# deliver: include MEDIA:/tmp/op1_guide.png in the reply (Telegram native photo)
python3 scripts/run_keys_tests.py   # 74 checks — run after any keys/taxonomy edit
```
If `op1_vibe_intent.resolve()` returns no match: pick the nearest `vibe_id` from
`references/op1_vibe_taxonomy.yaml` (or a documented transpose of one), emit a JSON
spec, validate via `op1_keys.validate`, re-render. **Never invent a progression**
outside the taxonomy without a real reference-song citation.

## Workflow (for the agent) — sound-recipe path, follow in order

**A. Parse the request.** Pull vibe adjectives, sound type, and any explicit engine/FX preference.

**B. Build the `sound_target`.** brightness / width / density / motion / space / articulation.

**C. Rank candidates.** Match the request against `op1_intent_mapping.yaml` aliases. Take the
candidates. Honor any explicit user pick;
otherwise take the highest `score_bias`. If nothing matches, use the `fallback` strategy — which now
looks up the user's adjectives in `op1_adjective_index.yaml` first (concrete params + directions),
falling back to the `best_for` tag overlap method only if adjectives are ambiguous or absent.

**D. Select one plan** (engine + envelope archetype + play mode + FX-or-dry + LFO-or-static).

**E. Compile the structured recipe object** per `op1_recipe_schema.yaml`. Fill every param
block from `op1_recipe_compiler_reference.yaml`:
  - Use the **exact `label`** from the reference for each color.
  - Use the reference's **`value_type`** for each control.
  - For numeric controls, put a provisional integer/decimal in range (prefer ~centers or ranges).
  - For graphic-only / visual-curve controls, set `value: null` and write a **`visual_target`**
    (what to watch) — never a number. **Keep `visual_target` SHORT (≤ ~6 words)** so the recipe row
    scans on a phone: prefer "thickens for width", "darker", "red triangle grows" over full sentences
    like "moderate — oscilloscope line thickens slightly". Terse + true beats wordy.
  - Copy split-range / input-required / conflict **warnings** into `provenance.warnings`.
  - Add the page **selection_instruction** (engine select; FX must include `[T3]`; LFO must include `[T4]`).
  - Add **1–2 correction macros**.

**F. Validate.** Run the object through the compiler:
```bash
python3 scripts/op1_compile.py RECIPE.yaml          # human output
python3 scripts/op1_compile.py RECIPE.yaml --json   # {valid, errors, warnings, rendered}
```
If it reports errors, fix the object and re-run. Do not hand the user an unvalidated recipe.
(You can also validate by writing the object to a temp `.yaml`/`.json` and invoking the script,
or by importing `op1_compile` and calling `compile_recipe(obj, ref)`.)

**G. Render.** The compiler's `render()` produces the final Telegram text deterministically.
Send exactly that — do not rewrite it.

**H. Optional context** below the recipe: one line on why this engine, 2–3 tweak ideas, a
community pro-tip from `community_tips.md`. And log to `output/training_log.jsonl`.

### Quick path (no temp file)
For a one-off, you can fill the object mentally and reproduce the renderer's format directly —
**but only if** you mirror the exact structure the renderer emits (title, `━` separators,
5 numbered sections, color rows, two `💡` macros, the provisional line). When in doubt, run the
compiler; it is the source of truth for format.

## Scope — what this skill IS and IS NOT

**This skill is a portable sound design recipe compiler.** The user is outside with their
OP-1 Field. They describe a sound → the skill tells them which page to open, which colored
knob to turn, and what to watch on screen. That's the entire workflow.

**What this skill is NOT:**
- ❌ NOT a MIDI CC / DAW automation tool. The user is on the go — no laptop, no DAW, no
  external controller. Do not research or add MIDI CC mappings, NRPN charts, or DAW
  integration. Even if firmware updates add new MIDI capabilities, that is a different
  workflow and does not belong in this skill.
- ❌ NOT a firmware changelog tracker. Do not add firmware version requirements to
  engine/FX entries unless a specific param's screen behavior changed across versions.
- ❌ NOT a community tips collection. Tape tricks, sequencer hacks, and button combos
  belong in `community_tips.md` as reference, not in the recipe pipeline.
- ❌ NOT a general OP-1 Field encyclopedia. If a feature doesn't help the user dial in
  a sound from a vibe description, it doesn't belong here.

**When researching improvements, the productive direction is:**
better vibe descriptors → parameter mappings drawn from how producers describe sounds,
mapped to real OP-1 Field params (cite compiler-reference `audible_tendency` strings).
The adjective index is the main growth surface.

## Hard prohibitions (the renderer/validator enforces these — do not fight them)

- ❌ **No fake percentages.** Values are integers/decimals on screen, never `%`.
- ❌ **No fake envelope numbers.** The envelope screen shows NO numbers — use curve/dot language only.
- ❌ **No fake numbers on graphic-only controls.** If `screen_behavior` says `[G]`, describe what
  to watch; never invent a precise value. (String, Pulse, Phase, Voltage, DNA, DSynth, Vocoder,
  and most reverb/filter FX knobs are graphic-only.)
- ✅ **LFO SPEED = ONE knob, TWO modes (synced number ⇄ free-run clock).** Verified on the real
  device (owner photos): turning SPEED sweeps between (1) a TEMPO-SYNCED side showing a NUMBER (1, 8…
  = note division locked to tempo) and (2) a FREE-RUNNING side showing a CLOCK-FACE with a needle (no
  number, LFO at its own rate). Fast/slow is NOT readable off the icon — synced divisions are
  tempo-relative, the clock is free-rate. Tell the user to **dial by ear while the LFO moves**; if
  giving a value, say "synced ~8 (in-time)" or "free-run, dial by ear". Don't fake a precise rate.
- ❌ **No generic synth advice without an OP-1 screen action.** Every param row maps to a page +
  colored knob + what to watch.
- ❌ **No LFO without a destination AND target parameter** (except Tremolo, which is hardwired to
  pitch+volume, and MIDI, which uses CC channels).
- ❌ **No effect named without its `[T3]` enable/select instruction**, and no LFO without `[T4]`.
- ❌ **No recipe that only covers engine params.** Every recipe includes engine, envelope, play
  mode (for pad/bass/lead/chord), FX-or-explicit-dry, and LFO-or-explicit-static.
- ❌ **Never silently omit FX or LFO.** State "none (dry)" / "none (static patch)" explicitly.

## Required content per recipe (validator checks all of these)

- Engine exists; all four colors present with matching labels.
- FX exists or is `none` (explicit dry); LFO exists or is `none` (explicit static).
- Numeric values in range; graphic-only controls carry a visual target, not a number.
- Split-range warnings present when relevant:
  - **Dr. Wave FILTER (Ochre):** 1–49 HP / 50 silence / 51–99 LP.
  - **Digital DETUNE/RING MOD (Grey):** 0–49 detune / 50+ ring mod.
  - **Pulse MOD (Orange):** 50 = no modulation (center).
  - **Terminal MODEL (Grey):** <3 HP / >3 LP.
- DSynth recipes include the **shift layer** (OSC 2 / OSC 2 wav / ENV osc2 / FILTER).
- Vocoder recipes include the **audio-input-required** note (Mic/Headset/FM Radio/USB; not Out-In).
- Value LFO includes shape/speed, amount, destination, target parameter. Random LFO amount ≥ 0.
  Tremolo distinguishes pitch amount vs volume amount and has no destination. Velocity LFO leaves
  Ochre/T2 unused. MIDI LFO uses CC1–CC4, not speed/amount/dest/param.
- At least one correction macro.

## Final output format (deterministic)

```text
🎛️ LUSH 80s PAD 🌊
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
Blue   SPEED       12
Ochre  AMOUNT      18
Grey   DEST        Synth (engine)
Orange PARAMETER   SPREAD
━━━━━━━━━━━━━━
💡 Too bright → lower Mother COLOR (Grey) or reduce WAVE ENV (Ochre)
💡 Too static → raise LFO AMOUNT (Ochre)
⚠️ starting point — tweak by ear
```

Recipes run ~22–32 lines (budget ≤ 34). Clarity beats arbitrary compression, but stay scannable
on a phone. DSynth recipes add a `⇧ SHIFT` block.

## Naming convention

- **The encoders are INFINITE/ENDLESS rotary encoders — they spin round and round with no start, end,
  or fixed pointer.** NEVER describe a physical knob position ("turn to 2 o'clock", "3/4 up",
  "halfway"). That's meaningless on this hardware. The ONLY reference is what's on the SCREEN. Every
  instruction must be "turn {color} until {screen shows X}": a number where the screen shows one
  ("until FILTER FREQ reads ~6000"), or a direction + what to watch/hear for a graphic ("turn up until
  the line spreads / it sounds brighter"). This is why the skill is screen-action-based, not
  position-based.
- Encoders by **COLOR**: **Blue / Ochre / Grey / Orange** (= T1/T2/T3/T4).
- **Beige** is an accepted *input* alias for Ochre; **Red** for Orange; **Gray** = Grey. Output
  always normalizes to Blue / Ochre / Grey / Orange.
- OP-1 buttons: `[Synth]`, `[T1]`–`[T4]`, `[Shift]`.

## Engine Quick Reference

| Engine | Character | Best For |
|--------|-----------|----------|
| Cluster | Massive supersaw | Huge leads, wide pads |
| Digital | Clean→harsh + ring mod | All-rounder, bass, metallic stabs |
| Dimension | Wavetable through filter | Acid, leads, plucks (Field-only) |
| DNA | CPU-noise glitch | Experimental, percussion, alien |
| Dr. Wave | Wavetable/frequency domain | Buzzy leads, lo-fi pads, organ |
| DSynth | Dual-osc + cross-mod | Complex/thick (needs shift layer) |
| FM | Metallic, bell | Bells, EPiano, percussion, aggressive |
| Phase | Phase distortion | Retro 80s leads, warm pads |
| Pulse | PWM, hollow | Funky bass, PWM pads, brass |
| String | Physical model | Warm, plucky, organic |
| Voltage | Analog-modeled | Vintage pads, gritty bass, metallic perc |
| Vocoder | Voice-controlled | Robot/vocal (needs audio input) |
| Sampler | Sample playback | Custom sounds |
| Amp | Guitar-amp emulation | External input only — reference-only, never a recipe (no envelope; owner ruling) |

## Research mode

When the user asks "tell me about FM" / "FM vs Digital" / "what sounds like [reference]": read the
relevant module block in `op1_recipe_compiler_reference.yaml` + `community_tips.md`, explain the
params and screen behavior, and offer to compile a recipe.

## Pitfalls

- **#1 RULE — VERIFY VISUALLY, EARLY, COMPLETELY. Do not guess from prose; do not half-do it.**
  This skill's data describes WHAT IS ON THE SCREEN, and the only trustworthy way to confirm that is
  render EVERY module page to PNG, then `vision_analyze` each one and read the mockup literally. Hard
  lessons: (a) a text-only/prose pass mislabeled Cluster WAVES as [0,6] when
  the screen shows 99, and missed the LFO SPEED two-mode display entirely; (b) verifying only 9 of 29
  modules and stamping the rest from book prose is not enough — when you
  verify, do ALL of them; (c) real device PHOTOS were the final ground
  truth that corrected three wrong guesses about SPEED. Priority order of authority: **device owner's
  words/photos > screen mockup image > book prose > web research > the old reference files.** When the
  user describes or photographs their own screen, that is ground truth, full stop — reach for it
  EARLY, do not theorize first. And use your full toolset: render images, zoom/crop for tiny details,
  use vision early instead of theorizing from prose alone.
- **Keep recipe OUTPUT simple; no verification badges.** The rendered footer is just
  `⚠️ starting point — tweak by ear`. Provenance (`user_verified`, `source:`) lives in the DATA
  for maintainers, never in the recipe text. Recipe rows stay terse and phone-scannable.
- **READ `references/display_format.md` FIRST** when touching LFO mappings, MIDI CC, or non-linear
  behavior. It is authoritative for encoder→param mapping per LFO type and value ranges. The
  compiler reference already folds it in, but the source is the tiebreaker.
- **Source conflicts are real and documented.** (1) Random LFO encoder map: `display_format.md`
  (Blue=Amount) vs `screen_behavior.yaml` (Blue=Speed) — the compiler reference follows
  `screen_behavior.yaml` and says so. (2) Punch Blue/Ochre (FREQ vs PUNCH) differs between
  `screen_behavior.yaml` and `engines_effects_v2.yaml` — reference follows `engines_effects_v2`
  for param names. Both are flagged `confidence: medium`. Don't "resolve" them silently.
- **LFO SPEED — confirmed two-zone control:** one knob crosses a boundary. Full-left to full-right:
  NUMBERS first (8,7,…,2,1 = TEMPO-SYNCED divisions, 8 = slowest → 1 = fastest synced), then a
  FREE-RUNNING CLOCK-FACE (~1 o'clock → 6 o'clock = faster). Name the zone + feel ("synced ~8, slow"
  or "free-run clock, push toward 6"). Corner "0000" is tempo/fine, NOT SPEED. Uses `relative_speed`
  (number OR word). Device photos beat the manual when they disagree.
- **Live device observation overrides the data file.** If the person using the skill says
  "nothing shows X on screen," treat that as ground truth. Fix at the SOURCE (compiler reference
  + validator) so every future recipe inherits it. No clean 0–99 number on screen → `relative_speed`
  or `graphic_only`.
- **A knob's FUNCTION is not its on-screen REPRESENTATION — this is the #1 data-quality bug.**
  A control can *be* a filter cutoff and still display as a Hz frequency, a 0-99 number, a graphic,
  or nothing. Deciding a value_type from what the knob *does* ("it's a filter, so 0-99") instead of
  what the *screen shows* is exactly what produced silent recipes (Dimension FILTER FREQ is **Hz,
  default ~500, max ~18000** — setting it to 40 or 70 = ~40-70 Hz = filter shut = SILENCE). Caught
  twice by the device owner before it was fixed. Before tagging any numeric value_type, confirm the
  screen literally prints that number. Counter-example from the same audit: Mother COLOR, Nitro
  LOWS/HIGHS, Punch FREQ, Fazer FREQ are ALL filter cutoffs but show NO Hz number on screen (Punch's
  screen shows `20 84 45` for POWER/PUNCH/ROUNDS and nothing for FREQ) → they stay `graphic_only`.
  Use the `numeric_hz` value_type (range [0,18000]) only when the screen shows an actual Hz number.
- **The compiled reference outranks old upstream drafts.** `display_format.md`,
  `screen_behavior.yaml`, and web-research data have held real errors historically
  (Random LFO encoder map flipped, Velocity LFO Ochre marked "unused", Amp missing).
  Preference order when reconciling: **device owner words/photos > official TE guide
  screens > free community device footage > compiler reference > old upstream files.**
  Stamp `user_verified: true` + `source:` only after a real check, never from memory.
- **`user_verified` honesty model (no on-screen stamp).** Modules may carry
  `user_verified` + `source:` in the data for maintainers. The rendered recipe does
  NOT print a verification badge — footer is just `⚠️ starting point — tweak by ear`.
  Keep provenance in the data; keep the output clean. NEVER stamp `user_verified: true`
  from memory or a single web search. `confidence: high` on unverified data is what
  made the early skill feel like gaslighting.
- **Fake-number leaks are the cardinal sin of this skill.** The entire architecture
  exists to stop the recipe from claiming a precise value the screen never shows.
  Any time you're unsure whether a control displays a real number, default to a
  visual/relative description — vague-but-true beats precise-but-fabricated.
- **Function ≠ on-screen display. Do NOT overcorrect.** Separate two questions:
  (1) WHAT the knob *does* (musical hint) vs (2) WHAT the *screen shows* (only this
  decides value_type / whether to print a number). Several FX filter cutoffs (Mother
  COLOR, Nitro LOWS/HIGHS, Punch FREQ, Fazer FREQ) ARE cutoff-frequency controls by
  function but show **no Hz number on screen** — they stay `graphic_only`. Dimension
  FILTER FREQ was special ONLY because the screen literally prints `FILTER FREQ 500`.
  Don't blanket-retag every filter as `numeric_hz`.
- **WRONG-UNIT leaks are just as bad as fake numbers.** A param can have a real
  on-screen number that is NOT a 0-99 knob — e.g. **Dimension FILTER FREQ is Hz**
  (default ~500, max ~18000 = fully open). It was mistagged `numeric_0_99` with
  `confidence: high`, so recipes emitted "FILTER FREQ 40" (= 40 Hz = silent). Fix at
  the source: `value_type: numeric_hz`, range [0,18000]. Sanity-check that a low value
  won't silence the engine before emitting any numeric unit.
- **Screen reading requires NATIVE vision, not a vision proxy.** When reconciling a
  contested param, look at real device photos / official guide figures / free community
  footage yourself. Trust the screen over prose every time they disagree. Known
  screen-caught corrections: Cluster WAVES is 0-99 (not 0-6); LFO SPEED shows a number
  in the synced zone (`relative_speed` accepts number OR relative word); Dimension
  FILTER FREQ is Hz.
- **All modules currently in the compiler reference have been cross-checked against
  device screens** and stamped accordingly. If you add or change a param, re-verify
  against the real screen before trusting it.
- **Recipe shape is intentionally uniform** across all presets (4-row engine/envelope/FX/LFO).
  The OP-1 Field IS a 4-encoder machine; uniform shape = fast color recognition on
  Telegram while sitting outside. Variety comes from CONTENT, not from varying the recipe
  shape. Do not "fix" the uniform format.
- **Never propose manual knob-turning documentation work before checking existing resources**
  (the device itself, the official TE user guide, free community footage, OP Forums, op1.fun).
  Only propose manual verification for edge cases existing public references don't cover.

- **Scope: on-the-go dialing, not DAW integration.** Tell people which knobs to turn on the
  physical device. Do not add MIDI CC automation, NRPN maps, or computer-side workflow features
  even when firmware gains them — that is a different product.
- **`screen_animation_behavior.yaml` is often INFERRED, not device-verified.** Prefer
  `screen_behavior.yaml` and live device observation when they conflict.
- **TE official documentation can contain typos — verify labels against real footage.**
  Confirmed mismatches: Cluster Orange is **UNISON** on device (not UNITOR); Pulse Blue is
  **FILTERO** (not FILTER). Device footage wins. Fix at `op1_recipe_compiler_reference.yaml`.
- **A static screen image often cannot show split-ranges, tap/shift layers, or transient
  popups.** Compiler-reference details for Dr. Wave FILTER/PHASE, Pulse MOD, Tremolo amounts,
  and Velocity LFO fields are the authority over a single mockup freeze-frame.
- **Punch Blue/Ochre = FREQ / PUNCH (settled).** Blue is FREQ (graphic), Ochre is PUNCH (numeric).
- **Amp is reference-only, never a recipe.** External-input processor; no envelope recipe path;
  `recipe_eligible: false`; validator rejects Amp recipes. Screen numbers are bare (no `%`).
- **Improve via better descriptors and dial cues, not feature creep.** Map adjectives to real
  params; refine visual dialing guidance. Skip firmware tours, MIDI deep-dives, and integrations.
- **PyYAML:** compiler prefers PyYAML, falls back to JSON. Install `pyyaml` or pass `.json`.
- **Correction macro field name: `screen_action`** (not `screen_screen_action` or `action`).
  Renderer reads `m.get("screen_action","")`. Match the schema and example recipes.

## Settled data (do not re-litigate)

- `numeric_plus_graphic` validator; LFO completeness rules; Amp excluded from recipes
- Digital OCTAVE unsigned 0–6; Fazer Blue `graphic_only`; Punch FREQ/PUNCH mapping
- UNISON / FILTERO from device footage (over contradictory docs)
- Shift-layer line budget 39; 23 example recipes
- FM ratios; Random / Tremolo / Value LFO field notes; Element source; Pulse MOD inversion

Open (low priority): optional training log; unused `swell` envelope archetype; animation-file stamps.

## When updating data from a reference

1. Read the **full** reference before listing findings — mockup-only samples produce false errors.
2. Conflict authority: live device / photos > official TE screens > free community footage >
   compiler reference > older drafts.
3. If the best available source settles it, fix from that source. Extra photos are for real
   disagreements or gaps — not for re-confirming settled prose.
4. Check CHANGELOG / settled labels before "fixing" (UNISON/FILTERO already decided).
5. Auxiliary/proxy vision is scout-only — confirm value_types and labels with native vision or
   source tables/prose before editing the reference.

## Maintenance

- Re-run the regression suite any time you edit the reference or renderer:
  `python3 scripts/run_tests.py --report` (writes `TEST_REPORT.md`).
- `python3 scripts/op1_compile.py --selftest` validates+renders the schema's worked example.
- When you add a engine/FX/LFO or a new intent, add a matching example to
  `op1_recipe_examples.yaml` so it's covered by the suite.

### Expanding the adjective index

`references/op1_adjective_index.yaml` is the fallback vocabulary when no intent alias matches.
To expand it:

1. Research real producer/community descriptors mapped to concrete synth parameters.
2. Cross-check existing entries to avoid near-duplicates (`warm` / `velvety` / `creamy`).
3. Every new entry MUST cite real params from `op1_recipe_compiler_reference.yaml` with
   those params' `audible_tendency` strings — do not invent names or tendencies.
4. Validate YAML, then `python3 scripts/run_tests.py --report`.

## Harmony guide mode (vibe → key/scale/chords → image)

This skill has a second mode: describe a vibe, get back a single composed PNG
"harmony guide card" with the key, scale, chords, and a reference song —
designed to sit next to the OP-1 on a phone screen. The model never draws and
never spells notes — it maps vibe → taxonomy spec; code does everything else.

**Architecture (same discipline as the synth recipe skill):**

```
"melancholy but hopeful — end of the movie"
  → op1_vibe_intent.resolve()  (fuzzy alias match against the taxonomy)
  → spec {root: A, scale: dorian, progression: [i, v, VII, IV], reference: ...}
  → op1_keys.validate()        (rejects bad roots/scales/romans)
  → op1_keys.render_guide()    (deterministic PNG: keyboard + progression strip)
  → /tmp/op1_guide.png         (deliver inline to Telegram)
```

The model's ONLY job is picking the closest taxonomy entry. It never invents
a progression, never spells a chord, never draws a keyboard. The validator
checks the final spec regardless of where it came from.

**Files:**

- `references/op1_vibe_taxonomy.yaml` — 20 vibes → spec mappings. Every entry
  cites a real reference track (Inception "Time", Yoda's Theme, Simpsons,
  Scarborough Fair, Pirates of the Caribbean, Heart of Courage, etc.). The
  citation IS the explanation — it's printed on the card and doubles as
  user-verifiable ground truth.
- `scripts/op1_keys.py` — theory engine (12 scales/modes, diatonic chord
  tables, roman-numeral parser with proper accidental convention), OP-1
  keyboard renderer (24 keys, F–E, verified against source p.65), PNG composer.
- `scripts/op1_vibe_intent.py` — fuzzy alias resolver (exact → substring →
  token-overlap). Returns `None` on no match; the LLM caller picks the nearest
  vibe_id from the taxonomy and re-runs. Never invents harmony.
- `scripts/run_keys_tests.py` — 74 checks: quality tables vs derived interval
  math, chord spelling battery, validator rejections, taxonomy integrity,
  render smoke tests, intent battery.

**Usage:**

```bash
# free-text vibe → image
python3 scripts/op1_keys.py --vibe "melancholy but hopeful" -o /tmp/guide.png

# transpose to a different root
python3 scripts/op1_keys.py --vibe "swashbuckling pirate adventure" --root G -o /tmp/guide.png

# explicit JSON spec (bypass the taxonomy)
python3 scripts/op1_keys.py spec.json -o /tmp/guide.png

# run the test suite
python3 scripts/run_keys_tests.py
```

**Pitfalls (learned during the v0.1 build):**

- **The OP-1 keyboard starts on F, not C.** Device layout: two octaves starting at F.
  A renderer that assumes C-to-C draws the wrong keyboard. Verify against device layout.
- **Diatonic quality wins over roman-numeral case.** Lowercase `vii` does NOT
  mean "minor" — degree 7 in major is `dim` per the table. The case hint only
  applies to chromatic (accidentalled) chords. Caught by the test battery
  before it shipped.
- **Accidentals follow the MAJOR-scale convention.** `bVI` in A minor = F
  natural (A major's VI is F#, flat once = F). Standard pop/film roman analysis.
- **Pentatonic scales don't carry tertian harmony.** A 5-tone scale's tones
  don't stack into clean triads. Progressions over pentatonic keys are spelled
  against the parent mode (major / aeolian) via `PENT_PARENT`. The pentatonic
  still lights on the keyboard — the chord strip just uses the parent's
  roman numerals.
- **Sharp/flat spelling derives from the ROOT's key signature, not the mode
  family.** A dorian spells F# (A minor has no flats); Bb major spells Eb;
  D aeolian spells Bb. Getting this wrong makes the card look amateur.
- **The reference song is the evidence.** Every taxonomy entry ships with a
  citation; the card prints it. If you can't cite a real track that documents
  the vibe→harmony link, the entry doesn't belong in the taxonomy. Same
  discipline as the synth recipe provenance fields.
- **Emotional associations are CONVENTIONS, not laws.** Tempo, orchestration,
  and context modulate them. The taxonomy maps conventions, not physics —
  carry that caveat; don't fake precision.
- **Phone card design matters.** Defaults: 2×2 grid for 4 chords; integer key widths;
  separate lit blues for white vs black keys; scale notes as pill chips; wrapped reference
  footer; canvas ~1080×1120. Edit `scripts/op1_keys.py` only — never freehand a keyboard.
  See `references/harmony-card-design.md`. Re-check with native vision after design edits.

- **Theory bugs caught by the keys test battery before ship.** Roman-numeral
  case must NOT override diatonic quality (`vii` in major = Bdim, not Bm).
  Accidentals are relative to the MAJOR scale (`bVI` in A minor = F). Pentatonics
  don't stack tertian chords — spell progressions via `PENT_PARENT`. Sharp/flat
  spelling comes from the ROOT's key signature (A dorian → F#, not Gb). Run
  `python3 scripts/run_keys_tests.py` after ANY theory or taxonomy edit.
- **Vision-capable review for card pixels.** Theory/code can land without vision; pixel QA of the PNG needs a vision-capable model or a human.

## Publishing & distribution

MIT licensed (`LICENSE` + `README.md` at root). Notes for redistributors:

- **Data files are source-neutral.** Facts only (param names, ranges, screen behavior).
- **Multi-file skill — install via tap or clone, not a raw `SKILL.md` URL.** A raw URL drops
  `references/` and `scripts/` and breaks the compilers.
- **Model-agnostic.** Nothing hardwired to a specific LLM.
- **Before publishing changes:** `python3 scripts/run_tests.py`,
  `python3 scripts/op1_compile.py --selftest`, `python3 scripts/run_keys_tests.py`.
  Frontmatter must describe both modes.
