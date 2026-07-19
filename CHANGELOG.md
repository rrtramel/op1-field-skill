# Changelog — op1-field

## v3.5.0 — Harmony guide mode (vibe → key/scale/chords → image)

### Why
Harmony mode: vibe → key/scale/chords → one phone PNG on the real OP-1 keyboard.
Same constrained-compiler discipline as the synth path.


### What changed
**New mode:** describe a vibe → get back a single composed PNG "harmony guide
card" (1080×940) with the key, mode, scale lit on the OP-1 keyboard (24 keys,
F–E, both octaves), a 4-chord progression as mini-keyboards, and a reference-
song citation. Designed to sit next to the OP-1 on a phone screen.

**New files:**
- `references/op1_vibe_taxonomy.yaml` — 20 vibe → spec mappings, each citing a
  real reference track (Inception "Time", Yoda's Theme, Simpsons, Scarborough
  Fair, Pirates of the Caribbean, Heart of Courage, Gladiator, Dark Knight,
  Creep, etc.). The citation prints on the card.
- `scripts/op1_keys.py` — theory engine + PNG renderer. 12 scales/modes,
  diatonic chord tables per mode (verified against derived interval math),
  roman-numeral parser with the standard pop-analysis accidental convention
  (bVI in minor = VI-in-major flattened once). OP-1 keyboard layout verified
  against book p.65.
- `scripts/op1_vibe_intent.py` — fuzzy alias resolver (exact → substring →
  token-overlap). Returns None on no match; the LLM caller picks the nearest
  vibe_id. Never invents harmony.
- `scripts/run_keys_tests.py` — 74 checks: quality tables vs derived math,
  chord spelling battery (incl. harmonic minor edge cases), validator
  rejections, taxonomy integrity + render smoke tests, intent battery.

**Bugs caught by testing before they shipped:**
- Diatonic quality table was being overridden by roman-numeral case (every
  `vii` came out `min` instead of `dim`). Fixed: table wins in-scale.
- Lydian degree 2 was tagged `min` — actually `maj` (D-F#-A in C lydian).
  Fixed and audited all 8 mode tables against interval math.
- Pentatonic "chords" don't exist (5-tone scales don't stack into triads).
  Progressions over pentatonic keys now spell against the parent mode via
  `PENT_PARENT`.
- Sharp/flat spelling was derived from the mode family (A dorian spelled
  Gb). Fixed: derives from the ROOT's key signature (A dorian → F#).

### Sources
2026-07 taxonomy research: Musical U modes guide, Inside the Score "What Are
Modes" (YouTube), Shockwave-Sound major/minor modes series, Filipe Leitão
film progression analysis, Kevin Kuschel "9 cinematic chord patterns,"
Soundfly Yoda's Theme analysis, Hooktheory cinematic progressions. OP-1
OP-1 keyboard layout F–E confirmed.

### Tests
`python3 scripts/run_keys_tests.py` → 74/74 passed. `run_tests.py` → 23/23
(synth recipes, unchanged).

## v3.4.0 — Full-Book Reconciliation + Validator Hardening

### Why
A complete 270-page read of device documentation + screen verification — not just the 29
rendered mockup pages — settled every contested data item in the compiler reference, and a
validator audit found documented rules with no enforcement. Key lesson: static screen
mockups show the steady-state screen only; split-ranges, tap/shift layers, and transient
popups live in the book's Control Knobs tables and Observed Behaviour prose. Several
mockup-only "errors" turned out to be correct data (Dr. Wave FILTER/PHASE splits, Pulse
MOD center-50, Tremolo dual amounts, Velocity LFO fields).

### What changed
**Data corrections (book-settled):**
- **Punch Blue/Ochre swapped to FREQ/PUNCH** (book p.120: "Turn Blue: Frequency / Turn
  Ochre: Punch"; mockup shows FREQ arc graphic, PUNCH 45 numeric). Reverses the older
  screen_behavior.yaml extraction. Fixed in compiler reference, screen_behavior.yaml, and
  8 adjective-index entries moved blue→ochre.
- **Digital OCTAVE**: split_range → numeric_small_discrete [0,6], "3 = unison" (p.83).
- **Fazer FREQ**: numeric_0_99 → graphic_only; transient "34 kP" readout noted as
  unexplained by all sources — no fake values.
- **Amp**: stripped wrong `unit: "%"` (screen shows bare numbers, p.104); flagged
  `recipe_eligible: false` (external-input processor, tuner replaces envelope, p.105);
  validator rejects Amp recipes (`engine_recipe_eligible`). Reference-only, per owner ruling.
- **UNISON/FILTERO kept** (v3.3.0 device-footage verification > book mockup's "UNITOR").
  Recorded as settled; do not re-litigate from mockups alone.

**Book additions:**
- FM ratio tables (p.91) with integer=bell / fractional=harsh guidance on FREQUENCY RATIO.
- Random LFO Orange dual-function: turn = AD envelope (0-50 attack / 50-100 decay),
  tap = parameter (p.138).
- Tremolo Shift+Orange = 5 shapes (Sine/Saw/Exp/Square/Blip, p.142); Value LFO tap-Blue =
  4 shapes (Square/Ramp/Saw/Sine, p.129).
- Element LFO: added missing Envelope source option (p.133).
- Pulse MOD: below-50 runs inverted (p.95).

**Code:**
- Validator: new `BOTH_TYPES` branch so `numeric_plus_graphic` params (Digital WAVE
  SHAPER, Dr. Wave TYPE & LENGTH, FM FREQ) are value-required + range-checked.
- Validator: implemented 5 previously documented-but-unenforced rules —
  `value_lfo_complete`, `tremolo_pitch_volume_split`, `velocity_lfo_fields`,
  `midi_lfo_cc_channels`, plus LFO `_check_labels` and `engine_recipe_eligible`.
- "modern lead" alias collision resolved (kept on acid_lead).
- Line budget 34 → 39 for shift-layer recipes (DSynth) in renderer + test suite.

**Tests:**
- 3 new example recipes: DSynth (first shift-layer coverage), Dr. Wave (both split-range
  warnings), Phase. Suite 20 → 23 recipes, 23/23 pass + selftest.

### Sources
Full device-screen + prose reconciliation pass: engines §4.6-4.18 (p.78-105),
FX §5.3-5.12 (p.114-123), LFOs §5.16-5.21 (p.128-150).

## v3.3.0 — YouTube Screen Verification Pipeline

### Why
The `screen_behavior.yaml` (static screen descriptions) and `screen_animation_behavior.yaml`
(v3.2, inferred from TE user guide + Grok research) had known unverified entries. The most
critical known issue: Cluster engine's Orange param was labeled "UNITOR" in all skill files
(matching the TE official user guide PDF), but real device footage shows "UNISON" on screen.
The `screen_animation_behavior.yaml` was explicitly marked as "INFERRED, not device-verified."

### What changed
Ran a systematic YouTube screen verification pipeline using SON WU's OP-1 Field tutorial
playlist (24 videos). Downloaded 1080p footage, extracted frames at 1-3 fps, and vision-analyzed
the OP-1 Field device screen against existing YAML entries for every engine, FX, and LFO type
covered in the playlist.

**Major corrections:**
- **Cluster Orange param: UNITOR → UNISON** (12 files, 34+ occurrences). The TE official user
  guide PDF (v1.7) says "UNITOR" — this is a TE documentation typo. Real device screen
  consistently shows "UNISON" across 20+ vision-analyzed frames. Fixed at the source
  (`op1_recipe_compiler_reference.yaml`) so all derived files inherit the correction.
- **Pulse Blue param: FILTER → FILTERO** (6 files). Real device screen shows "FILTERO" not
  "FILTER". Verified from SON WU Pulse tutorial (1080p, multiple frames). Fixed in compiler
  reference, screen_behavior, animation, examples, adjective index, engines_effects.
- **Delay effect graphics colors**: ripple circles are teal/cyan (not "black"), center dot is
  orange (not "red"), INPUT dash column is orange (not "red"). Corrected in screen_behavior.yaml.
- **Dr. Wave popup color**: popup box is teal/cyan (not "grey"), waveform line is cyan/light-blue
  (not "white"). Corrected in screen_behavior.yaml.
- **CWO SIDEBAND color**: vertical dash column is cyan (not "red"). Corrected.
- **Phone TONE description**: it's a gauge/arc with needle (not "fader/slider"). Corrected.
- **Nitro display description**: removed incorrect "Both top labels say 'FREQ FOLLOW'" —
  the labels are just "LOWS" and "HIGHS". Removed "labeled 'Q'" from joystick (not labeled).
  "NO numbers" claim confirmed correct.

**Verified correct (no changes needed):**
- String: TENSION/IMP/IMP TYPE labels, all graphic-only, no numbers — confirmed
- Voltage: AMPERE/GROUND NOISE/VOLT labels, all graphic-only, V gauge with needle — confirmed
- Spring Reverb: TONE/TURNS/DAMPING/MIX labels, all graphic-only, no numbers — confirmed
- Grid: X/Y/Z axis labels, FEEDBACK numeric, MIX graphic — confirmed
- Punch: PUNCH/FREQ/ROUNDS/POWER labels and display types — confirmed
- Cluster: WAVES/WAVE ENV/SPREAD labels and [B] display types — confirmed
- **Dimension FILTER FREQ: confirmed Hz (not 0-99)** — footage shows values like 140, 18000.
  The numeric_hz fix from v3.0 is validated against real footage.
- Vocoder: head profiles + purple fan (BANDS) present. Some label detail differences
  (labels may not appear as text on screen — graphics carry the parameter info).

### What didn't change
- No changes to the compiler, validator, renderer, or recipe schema logic.
- All 20 tests still pass (20/20).
- The `screen_animation_behavior.yaml` was updated where YouTube footage confirmed or corrected
  animation descriptions — entries verified against real footage are upgraded from inferred to
  verified status.

### Sources
SON WU OP-1 Field tutorial playlist:
`https://www.youtube.com/playlist?list=PL1ORyz4b29f7R0MGZN6m7Z_bp-Zj0j7kU`
1080p downloads, frame extraction at 1-3 fps, vision analysis of device screen.

## v3.2.0 — Screen Animation Behavior

### Why
The existing `screen_behavior.yaml` describes what's *statically* on screen — labels,
numbers, graphics. But when dialing in a sound, the user needs to know what *moves* —
"what should I watch animate as I turn this knob?" The static descriptions say "vertical
red dash column" but don't say "the column rises as you turn up."

### What changed
Added **`references/screen_animation_behavior.yaml`** — a new reference covering all
14 engines, 10 effects, 6 LFO types, and the envelope page. Each entry has:
- `static:` — one-line summary of the screen layout (matches screen_behavior.yaml)
- `animations:` — per-encoder descriptions of what moves/animates when you turn it,
  including behavior at extreme values (min/max) and visual transitions

Sources: TE OP-1 Field User Guide v1.7 (official PDF, rendered to PNG and vision-analyzed
with native vision), community visual research, cross-referenced against existing screen_behavior.yaml.

### What didn't change
- No changes to the compiler, validator, renderer, or recipe schema.
- No changes to screen_behavior.yaml (the static reference remains as-is).
- All 20 tests still pass (20/20).
- The new file is a supplementary reference for writing better `visual_target` and
  `action` phrases in recipes — the agent reads it when deciding what to tell the
  user to watch on screen.

## v3.1.0 — Expanded Adjective Index (95 descriptors)

### Why
The v3.0 adjective index had 49 entries covering common descriptors (warm, bright, dark,
glassy, etc.) but missed many evocative terms that musicians actually use when describing
sounds. Research surfaced hundreds of sound-design
descriptors used in practice across forums, YouTube tutorials, and production communities.

### What changed
Added **46 new descriptors** to `references/op1_adjective_index.yaml`, nearly doubling the
index from 49 → 95 entries. Every new entry maps to real OP-1 Field params with their
verbatim `audible_tendency` strings from the compiler reference.

New descriptor categories:
- **Material textures (12):** velvety, creamy, crystalline, molten, brittle, rubbery,
  plastic, papery, ceramic, tubular, corroded, dilapidated
- **Motion verbs (14):** breathing, bouncing, crawling, seeping, cascading, trickling,
  dripping, blooming, wilting, erupting, imploding, shattering, melting, freezing
- **Atmospheres (10):** underwater, feathered, gnarly, feral, pointillist, smeared,
  pristine, sterile, saturated, compressed
- **Genre archetypes (10):** boards_of_canada, aphex_twin, shoegaze, dub_techno,
  vaporwave, lofi_hip_hop, dungeon_synth, darksynth, chillwave, drone

### What didn't change
- No changes to the compiler, validator, renderer, or recipe schema.
- No changes to the intent mapping or example recipes.
- All 20 tests still pass (20/20).
- The new descriptors are used by the **fallback strategy** (Step C of the workflow):
  when no intent alias matches, the agent looks up the user's adjectives in this index.

## v3.0.0 — Recipe Compiler architecture

### Why
The v2 skill knew parameter *names* but had three systemic failures:
1. Parameter knowledge was inconsistent across engines / FX / envelope / play modes / LFOs.
2. Recipes didn't reliably tell the user *what to physically do on the screen* — which page,
   which colored knob, what label/value/graphic to watch, when Shift/tap/selector behavior matters.
3. The LLM emitted recipe text directly (freehand), so format and correctness drifted.

### What changed
The skill is now a **constrained recipe compiler**. The LLM reasons and fills a validated
intermediate **recipe object**; a real Python **validator + deterministic renderer** enforces the
final format and refuses to emit an invalid recipe.

```
vibe → intent parse → sound target → candidate ranking → semantic translate →
screen/action plan → recipe object → VALIDATE → deterministic RENDER → final recipe
```

### New / changed files
- **`references/op1_recipe_compiler_reference.yaml`** (NEW) — canonical merged source of truth.
  Every module carries *both* musical semantics and screen/action semantics, plus value-display
  types, split-range warnings, shift layers, graphic-only flags, LFO destination rules, source
  provenance, and confidence levels. Built by merging the authoritative on-disk files:
  `screen_behavior.yaml` (native-vision screen extraction), `display_format.md` (encoder maps /
  MIDI CC / non-linear behavior), `engines_effects_v2.yaml` (param names + ranges), and
  `community_tips.md` (correction-macro material).
- **`references/op1_intent_mapping.yaml`** (NEW) — 20 vibe archetypes; each *ranks* engine/FX/LFO
  candidates (no single hardcoded engine) and ships correction macros. Includes all 15 required
  archetypes plus 5 more (dreamy_spring_pad, warm_bass_no_reverb, mono_glide_lead, fm_bell_delay,
  pulse_pwm_pad).
- **`references/op1_recipe_schema.yaml`** (NEW) — the intermediate recipe object shape + an
  annotated, valid worked example.
- **`references/op1_recipe_validation.yaml`** (NEW) — deterministic validation rules, each with a
  rule id mirrored in the compiler script.
- **`references/op1_recipe_examples.yaml`** (NEW) — 20 worked recipe objects; doubles as the
  regression test corpus.
- **`scripts/op1_compile.py`** (NEW) — the enforcement layer. Validator (`Validator`) + deterministic
  renderer (`render`). `--selftest` and `--json` modes. Stdlib + PyYAML (JSON fallback).
- **`scripts/run_tests.py`** (NEW) — compiles + checks all 20 examples; `--report` writes `TEST_REPORT.md`.
- **`SKILL.md`** (REWRITTEN) — compiler workflow A–H, hard prohibitions, required content,
  deterministic output format, maintenance commands.
- **`TEST_REPORT.md`** (NEW) — generated 20/20 pass report.

### Naming normalization
Canonical encoder names are **Blue / Ochre / Grey / Orange**. `Beige`→Ochre, `Red`→Orange,
`Gray`→Grey are accepted as *input* aliases; output always normalizes.

### Honesty about sources
Two genuine source conflicts are documented rather than hidden, both flagged `confidence: medium`:
- Random LFO encoder map: `display_format.md` (Blue=Amount) vs `screen_behavior.yaml`
  (Blue=Speed). The compiler reference follows `screen_behavior.yaml`.
- Punch Blue/Ochre (FREQ vs PUNCH): `screen_behavior.yaml` vs `engines_effects_v2.yaml`. The
  reference follows `engines_effects_v2` for param names.

Note: the three `op1_engine_semantics_v0_1.yaml` / `op1_sound_design_semantics_v0_2.yaml` /
`op1_screen_action_layer_v0_3.yaml` "layers" referenced by the v3 fix-prompt did **not** exist on
disk in this environment — they were the prompt author's drafts. The compiler reference was built
directly from the real authoritative files instead.

### Guarantees the validator enforces
No fake percentages; no fake envelope numbers (visual curve language only); no fake numbers on
graphic-only controls; LFO destination + target parameter required (except Tremolo/MIDI);
FX requires `[T3]` and LFO requires `[T4]` selection instructions; split-range warnings present;
DSynth shift layer required; Vocoder input note required; ≥1 correction macro; values in range;
mobile-readable line budget.

### Backward compatibility
v2 reference files are retained as upstream provenance. The compiler reference is the new
normalized source; recipes are generated through it.

## v2.0.0
- Native-vision screen extraction into `screen_behavior.yaml`; `display_format.md` authoritative
  for LFO encoder maps; emoji vocabulary; DSynth shift-layer handling.

## v1.x
- Initial vibe→recipe skill with engine/effect reference and mobile formatting.
