# Community Tips & Recipes

> Real-world technique and recipes. See the README for OP-1 & sound design resources.

---

## Engine Tips from the Community

### FM Engine — Deep Tips
- **Start at pure sine** (blue fully CCW) as init patch, then slowly raise FM Amount
- **Cycle Freq. (ochre)** and **Topology (gray)** carefully — adjacent values jump between harmonic and discordant
- **Detune (orange)** adds inharmonicity/movement — great for organic FM
- Excellent for: bass, piano, strings, organ, percussion, pads (Attack Magazine deep-dive)
- **Sweet spot technique**: Find a harmonic Freq. ratio, then slowly add FM Amount until it starts to bite

### Cluster Engine — Deep Tips
- Strong for: smooth sines, meaty plucks, synth brass, supersaw leads
- **Supersaw technique**: Spread + Unison both around 50-70%, add Random LFO to Spread for movement
- **Sketch sequencer trick**: Sustain a C note with slight per-line pitch offsets (+1/-1 encoder clicks) at /4 division + Unison mode = detuned supersaw arpeggiation (from GitHub op1tips)

### String Engine — Deep Tips
- Most intuitive starting point for organic sounds
- **Shift+T1** to switch impulse model — changes the entire character
- Works beautifully processed through effects or layered on tape
- **Drone technique**: High Decay (T3) + long attack/release on envelope = infinite sustain
- Great for ambient when combined with Mother or Spring reverb

### Digital Engine — Deep Tips
- The all-rounder — if you're not sure which engine, start here
- **Ring mod** (Shift+T3 toggle) adds metallic bell tones instantly
- High Digitalness + Phone FX = lo-fi digital destruction
- Clean settings (low Digitalness) rival expensive VSTs for pure tones

### D-Synth Engine — Deep Tips
- **Multi-envelope concept**: Envelope crossfader (T1) + Decay together define final envelope per oscillator
- Gray line on screen = OSC 1, blue = OSC 2
- Crossfader sets envelope type and amplitude per oscillator
- Straight line on crossfader = continuous tone
- Complex but rewarding — the "advanced" engine

### Voltage Engine — Deep Tips
- The "hoover machine" — aggressive analog-style sounds
- High Ampere Modulation (T1) = warm saturation
- Excellent for bass (Reddit bass thread consensus)
- Slight imperfections are the point — lean into the instability

### Phase Engine — Deep Tips
- Casio CZ-style phase distortion
- Harder to intuit than other engines — hands-on preset exploration recommended
- **Pro tip**: Swap engines while keeping LFO/FX settings to discover new combinations
- Sweet for retro 80s leads and warm digital pads

### DNA Engine — Deep Tips
- CPU-ID noise synthesis — unique noisy/glitchy textures
- Combine with Phone FX or LFO for maximum character
- Less discussed in community but beloved by experimental users
- **Sweep Wave Number (T2) slowly** for evolving alien landscapes

### Dimension Engine (Field-exclusive) — Deep Tips
- Assign smooth sine LFO to waveform parameter for evolving timbre movement
- Great for ambient pads that slowly shift
- The "set and forget" engine — dial in a sound and let it breathe

---

## Effect Tips from the Community

### CWO — Deep Tips
- **Ambient/drone staple**: CWO on Synth FX (T3) + Spring on Master FX (Mixer T3)
- **Value LFO modulating CWO parameters** → chorus-like movement
- **Stack with Delay** on synth FX for spacey/trippy input processing
- **Live input trick**: Feed audio through sampler with CWO active for real-time processing
- Best paired with: Spring (master), Delay (stacked), slow tape speed

### Delay — Deep Tips
- **Synth FX for time-based thickening** — subtle delay adds dimension
- **Combine with Spring master reverb** for dub/ambient
- **Resampled loops**: Apply delay to loops recorded at low tape speed for stretched echoes
- **Dub technique**: Medium Size, moderate Feedback, Spring on master = classic dub

### Grid — Deep Tips
- X/Y grid control for rhythmic/sequenced modulation
- **Visual effect shaping** — the grid metaphor helps you think spatially
- Great for precise, pattern-based effects
- Less community coverage than other effects but powerful for sound design

### Mother — Deep Tips (Field-exclusive)
- **Master FX for balanced, natural reverb** — apply to entire mix
- **Print reverb technique**: Record reverb to a spare track, then you have non-destructive reverb you can adjust later
- Good for gluing mixes together
- **80s gated reverb**: Gate parameter high = classic Phil Collins/80s snare effect

### Nitro — Deep Tips
- **Mic scratching technique**: Max mic sensitivity, Nitro on master, white knob forward, green right — rub mic while tweaking encoders
- **Acid sweeps**: LFO on cutoff-like parameters for classic acid lines
- Pairs well with drive for aggressive filtering
- **Dual frequency** creates complex filter shapes — experiment with both freq params

### Phone — Deep Tips
- **Glitch/scratching favorite**: High Baud/Phonic/Telematic + moderate Attack + some Delay + zero Sustain + low Release
- **Apply Value LFO to blue FX knob** — play manually to tape for glitch patterns
- **Granular pitch-shifting** for lo-fi/vocal chops or vinyl-like degradation
- **Alternative scratching**: Portamento + LFO on mono synth + Sketch sequencer
- Best paired with: LFO (glitch), Delay (spacey), tape layering

### Punch — Deep Tips
- **Functions as lo-pass filter** in many uses (not just compression)
- **Stereo phase trick**: Blue ~10 o'clock + free-running LFO on blue param — record same loop to two hard-panned tracks with offset LFO timing
- **Vinyl emulation**: Max Drive + Punch master (99 power, 0 punch, 5 rounds) = instant vinyl
- **LFO modulation** on Punch params for movement and width
- Essential for live performance — makes everything louder and punchier

### Spring — Deep Tips
- **Master FX staple for dub/ambient**: Pair with CWO/Delay on synth FX
- **Slow everything down** + long EG + Spring = huge washy spaces
- **Print reverb to spare track** for non-destructive use
- Classic surf guitar sound — small Turns + bright Tone
- **Dub technique**: High Send + high Turns + low Damping = bouncy dub springs

---

## LFO Tips from the Community

### General LFO Wisdom
- **Modulate FX knobs** — this is the #1 community recommendation for adding movement
- **Value LFO** on CWO/Delay/Phone/Punch = chorus, glitch, or phase effects
- **Tremolo LFO in sonic range** = metallic/growly textures (push past normal LFO speeds)
- **Element LFO with mic/radio** as external mod source = unpredictable, organic modulation
- **Free-running LFO on Punch** = stereo width

### Specific LFO Tricks
- **Square/pulse Tremolo**: Green ±40-41 + White 100/-100 = stereo octave-jumping arpeggiation
- **Sine Tremolo**: Rhodes-style panning
- **Full-frequency Tremolo**: Metallic AM/FM effects
- **Random LFO to pitch**: Adds organic instability, arcade character
- **Random LFO to "All"**: Increases unison spread, wild textures
- **Smooth sine LFO to Dimension waveform**: Evolving timbre movement

---

## Effect Combinations (Community Favorites)

| Combo | Synth FX | Master FX | Result |
|-------|----------|-----------|--------|
| **Ambient/Drone** | CWO or Delay | Spring | Huge washy space |
| **Lo-Fi/Glitch** | Phone + LFO | Mother (subtle) | Degraded texture with space |
| **Acid** | Nitro | Spring (light) | Squelch with space |
| **Dub** | Delay | Spring | Classic dub echoes |
| **Aggressive** | CWO | Punch | Destroyed + loud |
| **Vinyl** | — | Punch (99/0/5) + max Drive | Instant vinyl emulation |
| **Chorus** | CWO + Value LFO | — | Chorus-like movement |
| **Phase** | Any + free-running LFO | — | Stereo phase effect |

---

## Tape & Workflow Tips

- **Layering for depth**: Record same part multiple times with deliberate variation — global detune ~10 cents, different octaves, slow free-running LFO, varying FX amounts, slight delay on one layer, hard-pan L/R
- **Tape speed tricks**: Record at low tape speed, play back at normal = time-stretching effect
- **Resample with FX active**, then lift/drop or re-process for effect stacking without permanent commitment
- **M1/M2 memories** store differences — clever offsetting creates a "third" patch slot
- **Lift/drop between patches** to transfer LFO/envelope/FX settings
- **Detune globally** (Shift + Metronome) for warmth/chorus on doubled tracks
- **Drum sampler for tuned instruments**: 2-octave range, great for bass or melodic percussion
- **Workflow**: Design on synth → record to tape at varying speeds → resample with FX → use Sketch or Finger sequencer for ideas

---

## Dial-In Cheat Sheet (what to listen for + sweet spots)

> Practical per-knob guidance for writing recipes that actually land on the sound. Sourced from
> SON WU's per-engine tutorials, OP Forums, op1.fun, and the magazinmehatronika review. The OP-1
> Field is a 差不多 ("close enough") machine — these are starting points to tweak by ear, not exact
> science. For graphic-only knobs (no on-screen number) the cue is **what to listen for / watch**.

### Dimension (numeric filter — the one with real Hz)
- **Blue WAVEFORM**: morphs Noise→Pulse→Square→Saw→Saw+Sub→Noise. Glides smoothly, so it's a great
  LFO target. Saw = classic analog lead; Pulse/Square = hollow/retro; Sub = beefy bass.
- **Ochre STEREO**: chorus/width. 0 = dry/centered; high = wide shimmer. Watch the scope line thicken/double.
- **Grey FILTER FREQ (Hz, 0–18000)**: **default 500 is DARK.** Landmarks → dark pad ~800–1500,
  warm mid ~2000–4000, **bright lead ~5000–9000**, wide open ~12000+. Below ~300 = near silent.
- **Orange RES**: resonance/squelch at the cutoff. Tame by design (built-in compressor, won't
  self-oscillate or hurt). Acid = low cutoff + RES near max. Watch the red triangle grow.

### Cluster (supersaw / pads)
- **Blue WAVES (0–99 on screen)**: number of stacked detuned oscillators. Low = thin/single; high
  on the dial = thick supersaw/pad. Volume auto-normalizes.
- **Ochre WAVE ENV (split)**: filter-envelope presets, not ADSR. ~noon = static/open; lower = down
  sweeps; 50+ = aggressive supersaw up-sweeps. Listen for the direction/speed of the sweep on chords.
- **Grey SPREAD**: detune depth. Under ~30 = musical/controlled; higher = chaotic beating.
- **Orange UNISON**: detune drift speed (interacts with Spread). Low Spread + moderate Unison = subtle
  living movement; both high = unstable/icy textures.

### Digital (all-rounder)
- **Blue WAVE SHAPER (number)**: clean→edgy→heavy digital distortion as you turn up. Low = pure tones
  that rival VSTs; high = gritty.
- **Ochre OCTAVE (0–6, 3 = unison)**: sub-osc octave. 1–2 = fat bass; 3 = clean unison.
- **Grey DETUNE / RING MOD**: 0–49 = downward detune (fat); cross 50 = ring mod ON (metallic/clangy).
  The 49→50 switch is the big timbre jump.
- **Orange DIGITALNESS**: digital noise/grit. Use sparingly; pairs with detune/ring for harshness.

### FM (bells, EPiano, metallic)
- **Blue FM AMOUNT (0–99, 0 = pure sine)**: modulation depth = brightness/bite. Start at 0, raise
  until it just starts to bite for musical tones; high = aggressive/clangy.
- **Ochre FREQUENCY (8 discrete ratios)**: steps jump between harmonic (musical) and discordant
  (metallic/bell). Step it, don't sweep — watch the operator cubes/ratio change.
- **Grey TOPOLOGY (discrete algorithms)**: changes which operators are carriers vs modulators. Watch
  cubes reconnect; each algo = different harmonic character.
- **Orange DETUNE**: offsets operators for movement/inharmonicity — great for organic bells.

### Dr Wave (buzzy leads, lo-fi, formant)
- **Blue TYPE & LENGTH (split)**: 0–50 morphs saw→square→triangle; 50+ adds sample-rate reduction
  (pixelated crunch). Listen for grit creeping in past halfway.
- **Ochre FILTER (split)**: 0 = off/open, 1–49 = high-pass, **50 = silence (avoid)**, 51–99 = low-pass.
- **Grey PHASE (split)**: 0–49 = pulse width (thin to clicky); 50+ = added harmonics / sync / vocal
  formant character.
- **Orange CHORUS**: 0 = off; higher = thicker/wider but saps energy at the top — use in moderation.

### Effects — numeric landmarks + listen-for cues
- **Delay** — RANGE shows **ms**: slapback ~80–150 ms, rhythmic ~200–350 ms, dub/ambient ~400–800+ ms.
  SPEED = time multiplier (lower = longer). FEEDBACK 30–60 = clean repeats, 70+ = self-oscillating
  drone. INPUT = wet send (40–70 typical; back off to avoid runaway).
- **Terminal** (bitcrush) — KHZ (sample rate): gentle 8–12, crunchy 4–8, extreme glitch <4. BITS:
  gentle 8–12, heavy 3–6 (very low = dropouts on quiet bits). MODEL: <3 high-pass, ~3 none, >3 low-pass.
- **Mother** (gated reverb) — DISTANCE (room size): intimate 10–30, room 40–60, hall 70–99. GATE high =
  80s gated-snare chop; low = natural tail. COLOR = tone (dark↔bright). MIX 25–60 typical.
- **Nitro** (dual resonant filter, all graphic) — LOWS = high-pass (clears mud), HIGHS = low-pass
  (darkens), Q = resonance (moderate avoids harsh self-osc), FREQ FOLLOW = auto-wah that tracks input
  level (great on drums). Listen for the filter "singing" at the cutoff.
- **Spring** (reverb, all graphic) — TONE bright↔dark, TURNS = size + metallic character (low+bright =
  surf, high+low-damping = dub), DAMPING = how fast highs die, MIX 20–50 typical.
- **CWO** (delay + freq shifter) — FREQ (graphic) = subtle detune→wild metallic shift; DELAY (number)
  low = rhythmic, high = long echo; FEEDBACK (number) higher = self-oscillating drone; SIDEBAND
  (graphic) adds metallic overtones. Low DELAY + low rate = phaser-like.

---

## Community Resources

_The full resource list (community + official + paid references) lives in the README under
"Additional OP-1 & sound design resources."_
