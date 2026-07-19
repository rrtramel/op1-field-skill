# OP-1 Field — Complete Engine & Effect Reference

> All parameter names are the EXACT labels shown on the OP-1 Field screen. See the README for OP-1 & sound design resources.

## How the Encoders Work
- **4 color-coded encoders**: Blue (T1), Beige/Ochre (T2), Gray (T3), Orange/Red (T4)
- Each section (Engine/ENV/FX/LFO) shows its params on screen, color-matched to encoders
- **Shift + encoder** = fine-tune control
- **Tap encoder** = reset to default / toggle options
- **Shift + T1** = browse engines | **Shift + T3** = browse effects | **Shift + T4** = select LFO type

## How Values Work
- Parameters display as **integers (0-99)** on a pop-up overlay when you turn an encoder
- **NOT percentages** — the screen shows "42" not "42%"
- Some parameters have **center detents** (e.g., PULSE at 49 = neutral)
- Some parameters **wrap around** (e.g., FILTER sweeps HP→LP continuously)
- MIDI CC range is 0-127 internally, but screen shows 0-99 for most params
- Each engine has **unique visual graphics** on screen — not generic bars

## Non-Linear Parameters (from SON WU tutorials)
- **DR. Wave PULSE (gray)**: Center at 49. Left of 49 = pulse width modulation. Right of 49 = oscillator sync effect.
- **DR. Wave FILTER (beige)**: Wraps around. 0 = open. Turning right: HP filter → LP filter → back to open.
- **DR. Wave WAVE (blue)**: Cycles through Sawtooth → Square → Triangle continuously, then into sample rate reduction.
- **Dimension waveform (blue)**: Morphs smoothly: Noise+Pulse → Pulse → Square → Saw → Saw+Sub → Saw+Sub+Noise.
- **FM Topology (gray)**: Adjacent values can jump between harmonic and discordant — sweep carefully.

---

## SYNTH ENGINES (T1 page)

### Cluster
`type: multi layered oscillator cluster`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Waves (WAVES) | Number of waves/oscillators in cluster (up to 6). Fully CW = all |
| T2 (ochre) | Envelope (WAVE ENV) | Filter envelope amount. Non-linear: 0-9 inverted, 10-49 sine, 50+ supersaw |
| T3 (gray) | Spread (SPREAD) | Pitch detuning spread across oscillators |
| T4 (orange) | Unison (UNISON) | Modulation drift speed/range of pitch detuning. Works with Spread |

**Shift row**: (fine-tune on all)
**Best for**: Massive leads, wide pads, trance stabs, supersaw
**Tips**: 3-4 waves = musical. 6 = huge but muddy. Sweep T3 for instant width.

---

### Digital
`type: true digital synthesis`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Wave Shaper (WAVE) | Wave shape adding noise/distortion. 0 = square, moves toward saw |
| T2 (ochre) | Octave (SHAPER) | Sub oscillator octave 0-6. 3 = same as main oscillator |
| T3 (gray) | Detune & Ring Mod | 0-49: detunes sub. 50+: ring modulation ON. Higher octave = narrower detune range |
| T4 (orange) | Digitalness | Digital harshness / bit reduction |

**Shift row**: Ring Mod toggle (T3), fine-tune on others
**Best for**: All-rounder. Leads, clean bass, chiptune, digital textures
**Tips**: Low T4 = warm. High T4 = 8-bit/glitchy. Ring mod more noticeable at high Digitalness.

---

### String
`type: waveguide string model`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Tension (TENSION) | String tightness. Higher = tighter, pluckier, less sustained |
| T2 (ochre) | Decay (IMP) | Impulse decay. Low = short pluck. High = longer bow/strum |
| T3 (gray) | Detune | Phase detuning between strings. Subtle tone changes |
| T4 (orange) | Impulse (IMP TYPE) | How strings struck. Low = hard (nails/plectrum). High = soft (fingers/bow) |

**Shift row**: Fine-tune on all
**Best for**: Warm plucks, acoustic bass, ambient drones, organic textures
**Tips**: Tension (T1) is the main character control. Waveguide string model based on Karplus-Strong principles.

---

### Pulse
`type: dual pulsetrain oscillator`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Filtero (FILTERO) | Filter cutoff with envelope follower pushing pulse shape |
| T2 (ochre) | Amplitude (AMPL) | Pulse train amplitude/volume |
| T3 (gray) | 2nd Pulse (TIME) | Pulse width of second pulse. Good LFO target for PWM |
| T4 (orange) | Modulation (MOD) | PWM amount+speed. 49→0 = depth+speed inc. 50 = off. 51-99 = faster PWM |

**Shift row**: Fine-tune on all
**Best for**: Funky bass, hollow leads, PWM pads, chiptune-ish
**Tips**: Modulate T3 (gray) with LFO for classic PWM. T4 center (50) = no modulation. Wraps around center.

---

### FM
`type: four operator FM synthesis`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | FM Amount (FREQ) | Modulation intensity. 0 = minimum (fully CCW) |
| T2 (ochre) | Frequency | Operator frequency ratios. 8 discrete values per operator |
| T3 (gray) | Topology | Algorithm config. Determines operator roles as carrier/modulator |
| T4 (orange) | Detune | Detunes operators for movement and harmonic character |

**Shift row**: Fine-tune on all
**Best for**: Bells, EPiano, metallic bass, aggressive leads, DX7 sounds
**Tips**: Low T1 + specific T2 ratios = bell/EPiano. High T1 = aggressive. T3 changes operator routing topology.

---

### Phase
`type: phase distortion`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Phase Shift (PHASE) | Shifts wave adding harmonics. 0 = sine, increasing → square |
| T2 (ochre) | Distortion Amount (DIST) | Distorts wave shape affecting timbre |
| T3 (gray) | Phase Filter (FILTER) | Filters wave amplitude, emphasising distortion. Not a traditional freq filter |
| T4 (orange) | Phase Tilt (TILT) | Wave folding distortion creating noise |

**Shift row**: Fine-tune on all
**Best for**: Warm leads, Casio CZ-style tones, retro 80s, phat bass
**Tips**: Starts from sine wave at 0. Increasing Phase Shift adds harmonics toward square. Similar to Casio CZ-101.

---

### Dr. Wave
`type: frequency domain synthesis`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Type & Length (PHASE) | 0-50: morphs saw→square→triangle. 50+: sample rate reduction |
| T2 (ochre) | Filter | 0 = no filter. 1-49 = high pass. 50 = silence. 51-99 = low pass |
| T3 (gray) | Phase | 0-49: pulse width. 50+: adds wave cycles (sync) + harmonics. Formant effects |
| T4 (orange) | Chorus | 0 = off. 1-99 = modulation speed for chorus-like effect |

**Shift row**: Fine-tune on all
**Best for**: Leads, evolving textures, 80s digital, classic wavetable
**Tips**: T2 is special: wraps HP→LP around center (50=silence). Sweep T1 for evolving timbre.

---

### DNA
`type: CPU Id Noise synthesis`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Filter (FILTER) | Filter cutoff. Does not fully close. Screen shows animated modulation |
| T2 (ochre) | Wave Number (CPU ID) | CPU noise segments. Not traditional wave shapes |
| T3 (gray) | Wave Modifier | Modulates waves. Affects pitch detuning and timbre. Use with Wave Number |
| T4 (orange) | Noise | Noise mixed into audio |

**Shift row**: Fine-tune on all
**Best for**: Experimental textures, ambient drones, weird FX, evolving pads
**Tips**: Set T1 low first as starting point. Sweep T2 slowly for evolving textures. T3 works iteratively with T2.

---

### Voltage
`type: multi oscillator electric synthesis`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Modulation (AMPERE) | Amplitude modulation between sine wave oscillators |
| T2 (ochre) | Ground Noise | Distorts sine wave adding harmonics, later stages add noise |
| T3 (gray) | Phase Filter (VOLT) | Low pass filter cutoff. Works with noise to distort wave |
| T4 (orange) | Detune | Detunes sub-oscillator from main. 0 = matched |

**Shift row**: Fine-tune on all
**Best for**: Warm bass, analog leads, vintage pads, Moog-ish
**Tips**: High T1 = warm amplitude modulation. Works with 1 Oscillator + 1 Sub-Oscillator with cross modulation.

---

### D-Synth
`type: multi envelope dual oscillator synth`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Envelope / Crossfader | Layer envelope + crossfade |
| T2 (ochre) | Waveform / Envelope | Wave shape per layer |
| T3 (gray) | Cross Mod. | Cross-modulation between layers |
| T4 (orange) | Frequency / Filter Cutoff Freq. | Pitch + filter |

**Shift row**: Accesses second oscillator params (frequency, waveform, envelope, filter cutoff)
**Best for**: Complex pads, layered sounds, thick leads, evolving textures
**Tips**: High T3 = complex intermodulation. Two oscillators interacting = rich timbres.

---

### D-Box
`type: teenage drum synthesizer`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Pitch | Drum pitch |
| T2 (ochre) | Waveform | Oscillator wave shape |
| T3 (gray) | Envelope | Amplitude envelope |
| T4 (orange) | Cross Mod. | Cross-modulation |

**Shift row**: Accesses second oscillator (pitch, waveform, envelope, filter cutoff freq.)
**Best for**: Kick drums, snares, hi-hats, percussion synthesis
**Tips**: Shift reveals full dual-oscillator control. Great for designing custom drum sounds.

---

### Dimension (Field-exclusive)
`type: subtractive synthesis with wavetable`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Waveform (WAVEFORM) | Wavetable position. Morphs Noise→Pulse→Square→Saw→Sub Saw |
| T2 (ochre) | Stereo (STEREO) | Modulation width / chorus-type effect |
| T3 (gray) | Filter Frequency (FILTER FREQ) | Filter cutoff. 0% = silent, 100% = 18kHz pass-through |
| T4 (orange) | Resonance (RES) | Filter resonance at cutoff. Classic filter sweep at high levels |

**Shift row**: Fine-tune on all
**Best for**: Acid sounds, leads, chords, plucks, classic subtractive
**Tips**: Sweep T3+T4 together for classic filter sweeps. Wavetable position (T1) is great for modulation targets.

---

### Synth Sampler
`type: teenage sample player`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Start | Sample start point |
| T2 (ochre) | Loop In | Loop start point |
| T3 (gray) | Loop Out | Loop end point |
| T4 (orange) | End | Sample end point |

**Shift row**: Reverse ON/OFF (T1 shift), Loop In Fine Tune (T2 shift), Loop Out Fine Tune (T3 shift), Gain (T4 shift)
**Best for**: Custom sounds, vocal chops, field recordings, granular textures
**Tips**: Record from mic, line in, or FM radio. Use Start/End to isolate parts.

---

### Drum Sampler
`type: teenage percussion sample player`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Note/Pitch | Chromatic pitch |
| T2 (ochre) | In | Sample start point |
| T3 (gray) | Out | Sample end point |
| T4 (orange) | Loop Off/Once/On | Loop mode |

**Shift row**: Reverse ON/OFF, In Fine Tune, Out Fine Tune, Gain
**Best for**: Drum kits, one-shot samples, sliced breaks
**Tips**: Assign different samples to each key. Loop modes: Off (one-shot), Once (play through), On (loop).

---

## EFFECTS (T3 page)

> Shift + encoder = fine-tune.
> One effect active at a time. **Shift + T3** to browse. **T3** to toggle on/off.

### CWO
`type: pitch shifting delay`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Frequency | Pitch shift / carrier frequency |
| T2 (ochre) | Delay | Delay time |
| T3 (gray) | Feedback | Repeat amount |
| T4 (orange) | Sideband | Sideband modulation (the weird factor) |

**Best for**: Alien textures, metallic destruction, pitch-shifted echoes, aggressive FX
**Tips**: High T4 = extreme sideband weirdness. T1 sweeps the pitch-shifted signal. Most "out there" effect.

---

### Delay
`type: solid state delay`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Size | Delay time / size |
| T2 (ochre) | Speed | Modulation speed |
| T3 (gray) | Feedback | Number of repeats |
| T4 (orange) | Mix | Dry/wet mix |

**Shift row**: Fine-tune on all
**Best for**: Slapback, rhythmic echoes, ambient tails, dub delays
**Tips**: T2 adds modulation (chorus-like on short delays). T3 past 70% = self-oscillation.

---

### Grid
`type: three dimensional feedback plate`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | X Size | X-axis grid size |
| T2 (ochre) | Y Size | Y-axis grid size |
| T3 (gray) | Z Feedback | Z-axis feedback depth |
| T4 (orange) | Mix | Dry/wet mix |

**Shift row**: Fine-tune on all
**Best for**: Rhythmic chops, glitchy textures, stutter effects, metallic plates
**Tips**: X and Y create different delay grid patterns. High Z = complex self-oscillating textures.

---

### Mother (Field-exclusive)
`type: gated reverb`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Distance | Room size / proximity (close → massive) |
| T2 (ochre) | Gate | Gating intensity (door-like cutoff) |
| T3 (gray) | Color | Reverb tonal color (dark → bright) |
| T4 (orange) | Mix | Dry/wet mix |

**Shift row**: Fine-tune on all
**Best for**: Ambient pads, deep space, large halls, cinematic, 80s gated reverb
**Tips**: Low T1 = intimate room. High T1 = massive cathedral. T2 for 80s gated reverb effect. Unique to Field.

---

### Nitro
`type: dual resonant turbo filter`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Frequency | Filter center frequency |
| T2 (ochre) | Filter Follow | Keyboard tracking amount |
| T3 (gray) | Resonance | Peak emphasis (squelch) |
| T4 (orange) | Frequency | Second frequency (dual filter / fine-tune) |

**Shift row**: Fine-tune on all
**Best for**: Filter sweeps, auto-wah, vowel sounds, acid squelch, resonant peaks
**Tips**: High T3 = acid squelch. T2 makes filter follow pitch (more natural). Dual frequencies for complex filter shapes.

---

### Phone
`type: hacked telephone system`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Tone | Telephone tone character |
| T2 (ochre) | Phonic | Vocal/phonetic quality |
| T3 (gray) | Baud | Data rate / bit crushing |
| T4 (orange) | Telematic | Transmission artifacts / noise |

**Shift row**: Fine-tune on all
**Best for**: Lo-fi textures, telephone voice, 8-bit crunch, vintage digital, glitch
**Tips**: Low T3 = extreme lo-fi. T4 adds transmission noise. Great for lo-fi hip-hop vocal chops.

---

### Punch
`type: hard hitting low pass filter`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Frequency | Filter cutoff frequency |
| T2 (ochre) | Punch | Punch intensity / transient snap |
| T3 (gray) | Rounds | Number of filter rounds / resonance character |
| T4 (orange) | Power | Overall power / drive |

**Shift row**: Fine-tune on all
**Best for**: Drum punch, bass tightness, transient shaping, aggressive filtering
**Tips**: T2 + T4 together = maximum impact. T1 sets where the punch hits. Essential for live performance.

---

### Spring
`type: mathematic reverb`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Tone | Spring tonal character (dark → bright) |
| T2 (ochre) | Turns | Number of spring turns (reverb complexity) |
| T3 (gray) | Damping | High-frequency damping |
| T4 (orange) | Send | Effect send amount (dry/wet) |

**Shift row**: Fine-tune on all
**Best for**: Guitar-like reverb, retro surf, lo-fi space, dub, bouncy springs
**Tips**: Low T1 = dark splash. High T2 = complex spring character. Classic surf guitar sound.

---

### Fazer (Easter Egg — unlockable)
`type: phaser`
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Rate | Sweep speed |
| T2 (ochre) | Depth | Sweep depth |
| T3 (gray) | Feedback | Feedback intensity |
| T4 (orange) | Mix | Dry/wet mix |

**Best for**: Sweeping leads, psychedelic textures, synthwave, funk
**Tips**: Discovered via community Easter egg. Adds phaser to the effect list.

---

## ENVELOPE (T2 page)

### Synth Envelope — ADSR
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Attack | Time to reach full volume (instant → slow swell) |
| T2 (ochre) | Decay | Time to fall to sustain level |
| T3 (gray) | Sustain | Held volume level while key is pressed |
| T4 (orange) | Release | Time to fade after key release |

**Shift + T2**: Play modes (Poly/Mono/Legato/Unison + Portamento)

### Drum Envelope — Transient Shaper
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Attack | Transient snap (soft → hard) |
| T2 (ochre) | Gain | Overall volume |
| T3 (gray) | Release | Tail length (short → long) |
| T4 (orange) | Smooth/Timing | Smoothing / time stretch |

**Tips**: Optimized for percussion. T1 for snap, T3 for tail. Shape drums to be aggressive or laid-back.

---

## LFO (T4 page)

> **Shift + T4** to select LFO type. **T4** to toggle on/off.
> White (T3) = destination category, Orange (T4) = destination parameter within category.
> Clock icon = tempo-synced. "F" suffix = no retrigger.
> 
> **IMPORTANT**: LFO Speed is NOT a percentage. It's either:
> - **Free-running**: Hz values (~0.1 Hz very slow → ~30 Hz very fast)
> - **Tempo-synced**: note divisions (1/1, 1/2, 1/4, 1/8, 1/16, 1/32)
> Amount/depth IS a percentage with ▓░ bars.

### LFO Types

#### Element
External source modulates one parameter. Use accelerometer (G-force), mic, line-in, radio, synth envelope, or synth level.
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Source | G-force / Radio / Line-in / Mic / Synth Env / Synth Level |
| T2 (ochre) | Amount | Modulation depth |
| T3 (gray) | Destination Category | Engine / Envelope / FX |
| T4 (orange) | Destination Param | Specific parameter within category |

**Tips**: Tilt the OP-1 with G-force for physical modulation. Use mic input for vocal-controlled effects.

#### Value
Classic single-parameter LFO with waveform control.
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Speed | LFO rate (free or tempo-synced) |
| T2 (ochre) | Amount | Modulation depth |
| T3 (gray) | Destination Category | Engine / Envelope / FX |
| T4 (orange) | Destination Param | Specific parameter within category |

**Tips**: The workhorse LFO. Select destination with T3+T4. Use Shift+T1 for tempo sync.

#### Tremolo
Pitch + volume modulation with envelope shaping.
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Speed | LFO rate |
| T2 (ochre) | Pitch Amount | Pitch modulation depth (negative = invert) |
| T3 (gray) | Volume Amount | Volume modulation depth (negative = invert) |
| T4 (orange) | Envelope | Attack/decay shaping |

**Shift + T4**: Waveform select (sine, saw, exp, square, blip)
**Tips**: Negative amounts = inverted phase. Great for vibrato + tremolo combos.

#### Random
Randomizes destination parameters with envelope control.
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Amount | Randomization intensity |
| T2 (ochre) | Speed | Random update rate |
| T3 (gray) | Destination Category | Engine / Envelope / FX |
| T4 (orange) | Envelope | Attack/decay shaping |

**Tips**: Slow speed = evolving textures. Fast = glitchy. Great for organic movement.

#### Velocity
Responds to key playing dynamics.
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | Amount | Velocity sensitivity |
| T2 (ochre) | — | — |
| T3 (gray) | Destination Category | Engine / Envelope / FX |
| T4 (orange) | Destination Param | Specific parameter |

**Tips**: Makes sounds respond to how hard you play. Essential for expressive performance.

#### MIDI
Maps external MIDI CCs to parameters.
| Encoder | Param | Notes |
|---------|-------|-------|
| T1 (blue) | CC 1 | First MIDI CC number |
| T2 (ochre) | CC 2 | Second MIDI CC number |
| T3 (gray) | CC 3 | Third MIDI CC number |
| T4 (orange) | CC 4 | Fourth MIDI CC number |

**Tips**: Map up to 4 external MIDI CCs to any parameter. Use with external controllers.

---

## SECTION NAVIGATION

| Button | Section | What It Controls |
|--------|---------|-----------------|
| T1 | Engine | Synth oscillator / waveshaping params |
| T2 | Envelope | ADSR (synth) or transient (drum) |
| T3 | Effects | One active effect at a time |
| T4 | LFO | Modulation source |
| Shift+T1 | Browse | Cycle through synth engines |
| Shift+T3 | Browse | Cycle through effects |
| Shift+T4 | LFO Type | Select LFO mode |
| Shift+T2 | Play Mode | Poly/Mono/Legato/Unison + Portamento |

## MIXER (Mixer mode — T3)
Master FX in Mixer mode uses the same effect pool as synth/drum T3. Applies to the entire mix.

## OP-1 FIELD TIPS
- **Snapshot**: Hold sound key 1-8 for 3 seconds to save preset
- **FM Radio**: Sample radio transmissions as source material
- **Mic**: Record directly for sampler/vocoder
- **G-Force LFO**: Tilt the OP-1 to control parameters (Element LFO type)
- **Battery**: ~24 hours, charge via USB-C
- **4-track tape**: Record ideas directly
- **7 sequencers**: Arpeggio, Endless, Hold, Pattern, Tombola, Sketch, Finger
- **Tape styles**: Studio, Vintage (7.5 ips), Porta (3.75 ips cassette), Disc Mini
- **Disk mode**: Transfer files via USB-C (COM → Disk Mode)

---

_For OP-1 & sound design resources, see the README._
