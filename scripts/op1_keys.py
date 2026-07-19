#!/usr/bin/env python3
"""
op1_keys.py — OP-1 Field harmony guide renderer.

Input: a validated harmony object (key/scale/progression/vibe/reference).
Output: ONE composed PNG "guide card" sized for a phone screen, designed to
sit next to the OP-1: full 24-key (F-to-E) keyboard with the scale lit,
the chord progression as mini-keyboards, chord names, mode note, and the
reference-song citation.

The model NEVER draws and NEVER spells notes. This module owns all theory.
Stdlib + Pillow only.

Layout of the OP-1 Field keyboard (device layout: 2 octaves starting at F):
  24 keys, F..E, 14 white / 10 black, standard 2-3 black groups.
"""
from __future__ import annotations
import json, argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ----------------------------------------------------------------------
# Theory tables (deterministic — the LLM never computes these)
# ----------------------------------------------------------------------
CHROMA = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
N2I = {n: i for i, n in enumerate(CHROMA)}
# flat spellings for readability in minor/flat keys
FLAT_NAME = {"C#": "Db", "D#": "Eb", "F#": "Gb", "G#": "Ab", "A#": "Bb"}
# accept flat input roots by normalizing to sharp
FLAT_TO_SHARP = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}

SCALES = {
    # name: (semitone offsets from root, degree qualities for triads)
    "major":            [0, 2, 4, 5, 7, 9, 11],
    "ionian":           [0, 2, 4, 5, 7, 9, 11],
    "dorian":           [0, 2, 3, 5, 7, 9, 10],
    "phrygian":         [0, 1, 3, 5, 7, 8, 10],
    "lydian":           [0, 2, 4, 6, 7, 9, 11],
    "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    "aeolian":          [0, 2, 3, 5, 7, 8, 10],
    "natural_minor":    [0, 2, 3, 5, 7, 8, 10],
    "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
    "locrian":          [0, 1, 3, 5, 6, 8, 10],
    "minor_pentatonic": [0, 3, 5, 7, 10],
    "major_pentatonic": [0, 2, 4, 7, 9],
}

# Triad quality per scale degree (1-indexed), for diatonic chord spelling.
QUALITY = {
    "major":            ["maj", "min", "min", "maj", "maj", "min", "dim"],
    "ionian":           ["maj", "min", "min", "maj", "maj", "min", "dim"],
    "dorian":           ["min", "min", "maj", "maj", "min", "dim", "maj"],
    "phrygian":         ["min", "maj", "maj", "min", "dim", "maj", "min"],
    "lydian":           ["maj", "maj", "min", "dim", "maj", "min", "min"],
    "mixolydian":       ["maj", "min", "dim", "maj", "min", "min", "maj"],
    "aeolian":          ["min", "dim", "maj", "min", "min", "maj", "maj"],
    "natural_minor":    ["min", "dim", "maj", "min", "min", "maj", "maj"],
    "harmonic_minor":   ["min", "dim", "aug", "min", "maj", "maj", "dim"],
    "locrian":          ["dim", "maj", "min", "min", "maj", "maj", "min"],
    # Pentatonics: chords are spelled against the PARENT mode (major / aeolian).
    # Pentatonic tones don't stack into clean tertian triads — that's their charm.
    # The parent table has 7 entries so full roman numerals work in progressions.
    "minor_pentatonic": ["min", "dim", "maj", "min", "min", "maj", "maj"],
    "major_pentatonic": ["maj", "min", "min", "maj", "maj", "min", "dim"],
}
QUAL_SUFFIX = {"maj": "", "min": "m", "dim": "dim", "aug": "aug"}

# Mode flavor one-liners (from the 2026-07 taxonomy research).
MODE_NOTE = {
    "dorian": "raised 6th — melancholy with a hopeful lift",
    "lydian": "raised 4th — floaty, dreamy, never quite resolves",
    "phrygian": "flat 2nd — tense, exotic, foreboding",
    "mixolydian": "flat 7th — bluesy major, longing under brightness",
    "aeolian": "natural minor — straight melancholy, no leading-tone pull",
    "natural_minor": "natural minor — straight melancholy, no leading-tone pull",
    "harmonic_minor": "raised 7th — dramatic minor, classical tension",
    "major": "resolved, bright, triumphant",
    "ionian": "resolved, bright, triumphant",
    "locrian": "flat 2nd + flat 5th — unstable, eerie, ungrounded",
    "minor_pentatonic": "5-note minor — open, rootsy, forgiving",
    "major_pentatonic": "5-note major — open, bright, forgiving",
}

# ----------------------------------------------------------------------
# Roman numeral -> chord spelling
# ----------------------------------------------------------------------
def parse_roman(tok: str):
    """Parse e.g. 'i', 'VI', 'bVII', 'iv', 'III', '#ivdim'. Returns (degree, acc, explicit_quality|None).

    explicit_quality is only a HINT from suffix ('dim'/'aug'/'m') or letter case —
    the diatonic table wins for in-scale degrees (acc == 0). It only decides
    quality for chromatic (accidentalled) chords.
    """
    acc = 0
    tok = tok.strip()
    while tok.startswith(("b", "♭")):
        acc -= 1; tok = tok[1:]
    while tok.startswith(("#", "♯")):
        acc += 1; tok = tok[1:]
    explicit = None
    for suf, q in (("dim", "dim"), ("aug", "aug"), ("m", "min")):
        if tok.lower().endswith(suf):
            explicit = q
            tok = tok[: -len(suf)]
            break
    roman = tok.upper()
    degs = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7}
    if roman not in degs:
        raise ValueError(f"bad roman numeral: {tok!r}")
    if explicit is None:
        explicit = "min" if tok.islower() else "maj"
    return degs[roman], acc, explicit


# Parent scale for chord spelling when the scale is pentatonic (5-tone scales
# don't carry tertian harmony; progressions are spelled against the parent mode).
PENT_PARENT = {"minor_pentatonic": "aeolian", "major_pentatonic": "major"}


def chord_for_root_degree(key_root_pc, scale_pcs, scale_key, degree, acc, explicit_q, prefer_flats):
    """Spell a chord from a roman numeral against a key.

    Diatonic (acc == 0): root from the scale (or the pentatonic's PARENT mode),
    quality from the quality table. Chromatic (acc != 0): root = MAJOR-scale
    degree pitch of the key root + acc (standard roman convention: bVI in minor
    = VI-in-major flattened once — e.g. bVI in A minor = F natural).
    """
    if scale_key in PENT_PARENT:
        parent = PENT_PARENT[scale_key]
        scale_pcs = spell_scale(CHROMA[key_root_pc], parent)
        scale_key = parent
    quals = QUALITY.get(scale_key, QUALITY["natural_minor"])
    if acc == 0:
        root_pc = scale_pcs[degree - 1]
        q = quals[degree - 1]
    else:
        major_degree_pitch = (key_root_pc + SCALES["major"][degree - 1]) % 12
        root_pc = (major_degree_pitch + acc) % 12
        q = explicit_q or quals[degree - 1]
    third = 4 if q in ("maj", "aug") else 3
    fifth = 7 if q in ("maj", "min") else (8 if q == "aug" else 6)
    tones = {root_pc, (root_pc + third) % 12, (root_pc + fifth) % 12}
    name = display_name(root_pc, prefer_flats) + QUAL_SUFFIX[q]
    return root_pc, q, name, tones


def spell_scale(root: str, scale: str):
    offs = SCALES[scale]
    return [(N2I[root] + o) % 12 for o in offs]


def display_name(pc: int, prefer_flats: bool) -> str:
    n = CHROMA[pc]
    return FLAT_NAME.get(n, n) if prefer_flats else n


# ----------------------------------------------------------------------
# Keyboard geometry — OP-1 Field: 24 keys, F..E
# ----------------------------------------------------------------------
# White sequence F G A B C D E F G A B C D E ; blacks sit between
WHITES = ["F", "G", "A", "B", "C", "D", "E"] * 2
# black after white index i? pattern per octave F# G# A# _ C# D# _
BLACK_AFTER = {0: "F#", 1: "G#", 2: "A#", 4: "C#", 5: "D#", 7: "F#", 8: "G#", 9: "A#", 11: "C#", 12: "D#"}
KB_LOW, KB_HIGH = N2I["F"], N2I["E"]  # wraps: F..E ascending within one octave numbering


def kb_key_positions(x0, y0, w, h):
    """Return list of (pc, is_black, x, y, kw, kh) for the 24-key OP-1 bed."""
    wk = w / 14.0
    bk_w, bk_h = wk * 0.62, h * 0.62
    keys = []
    octave = 0
    for i, name in enumerate(WHITES):
        pc = (N2I[name] + 12 * octave) % 12 if False else N2I[name]
        keys.append((N2I[name], False, x0 + i * wk, y0, wk, h))
        if i == 6:
            octave = 1
    octave = 0
    for i in range(14):
        if i in BLACK_AFTER:
            name = BLACK_AFTER[i]
            keys.append((N2I[name], True, x0 + (i + 1) * wk - bk_w / 2, y0, bk_w, bk_h))
    return keys


def draw_keyboard(d: ImageDraw.ImageDraw, box, lit_pcs: set, root_pc: int,
                  palette, small=False, label_root=True):
    """Draw OP-1 F–E keyboard. Uses integer key widths so gaps stay even."""
    x0, y0, w, h = box
    n_white = 14
    # integer white-key width; leftover dead pixels go on the right edge
    wk = max(6, int(w // n_white))
    total_w = wk * n_white
    # center the bed if leftover pixels
    x0 = int(x0 + (w - total_w) / 2)
    bk_w = max(4, int(round(wk * 0.58)))
    bk_h = max(8, int(round(h * (0.58 if small else 0.62))))
    white_pcs = [N2I[n] for n in WHITES]
    outline = palette["line"]
    # whites first
    for i, pc in enumerate(white_pcs):
        x = x0 + i * wk
        lit = pc in lit_pcs
        is_root = pc == root_pc
        fill = palette["root"] if is_root else (palette["lit"] if lit else palette["white"])
        # leave 1px gutter between whites
        d.rectangle([x, y0, x + wk - 2, y0 + h - 1], fill=fill, outline=outline, width=1)
        if is_root and label_root and not small:
            r = max(3, int(wk * 0.16))
            cx, cy = x + (wk - 2) / 2, y0 + h - max(10, wk * 0.30)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=palette["root_dot"])
        elif is_root and label_root and small and wk >= 10:
            r = max(2, int(wk * 0.14))
            cx, cy = x + (wk - 2) / 2, y0 + h - max(7, wk * 0.26)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=palette["root_dot"])
    # blacks on top
    for i in range(n_white):
        if i not in BLACK_AFTER:
            continue
        pc = N2I[BLACK_AFTER[i]]
        # center black over the joint between white i and i+1
        mid = x0 + (i + 1) * wk - 1
        x = int(mid - bk_w / 2)
        lit = pc in lit_pcs
        is_root = pc == root_pc
        fill = palette["root"] if is_root else (palette["lit_dark"] if lit else palette["black"])
        d.rectangle([x, y0, x + bk_w - 1, y0 + bk_h - 1], fill=fill, outline=outline, width=1)
        if is_root and label_root and (not small or wk >= 10):
            r = max(2, int(bk_w * 0.22))
            cx, cy = x + bk_w / 2, y0 + bk_h - max(6, bk_w * 0.35)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=palette["root_dot"])


# ----------------------------------------------------------------------
# Palette + fonts
# ----------------------------------------------------------------------
PAL = {
    "bg": (12, 12, 16),
    "panel": (26, 26, 32),
    "line": (72, 72, 84),
    "text": (245, 245, 248),
    "dim": (176, 176, 190),          # brighter grey — was too dim on phone
    "accent": (255, 176, 64),
    "white": (246, 244, 238),
    "black": (22, 22, 28),
    "lit": (88, 176, 255),           # brighter blue for white-key hits
    "lit_dark": (56, 140, 230),      # deeper blue for black-key hits (contrast)
    "root": (255, 140, 36),
    "root_dot": (18, 18, 22),
}

def _font(sz, bold=False):
    for p in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""),
        "/usr/share/fonts/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""),
    ):
        if Path(p).exists():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


# ----------------------------------------------------------------------
# The guide card
# ----------------------------------------------------------------------
def render_guide(obj: dict, out_path: str):
    vibe = obj["vibe"]
    root = obj["root"]
    root = FLAT_TO_SHARP.get(root, root)  # accept 'Bb' etc., normalize to sharp
    scale_key = obj["scale"].lower().replace(" ", "_")
    progression = obj["progression"]
    reference = obj.get("reference", "")
    # Sharp/flat spelling: derive from the ROOT's home key signature, not the mode.
    # Flat-side roots (F and all flat keys) spell with flats; everything else sharps.
    # So A dorian spells F# (not Gb); Bb major spells Bb; D minor spells Bb.
    FLAT_SIDE_ROOTS = {"F", "A#"}  # F major and all flat-key roots (Bb=A#, Eb=D#, etc.)
    if "prefer_flats" in obj:
        prefer_flats = obj["prefer_flats"]
    else:
        flat_key = ("b" in obj["root"]) or root in FLAT_SIDE_ROOTS
        minor_flat = (scale_key in ("aeolian", "natural_minor") and root in ("D", "G", "C"))
        prefer_flats = flat_key or minor_flat
    root_disp = display_name(N2I[root], prefer_flats)

    scale_pcs = spell_scale(root, scale_key)
    root_pc = N2I[root]
    scale_names = [display_name(pc, prefer_flats) for pc in scale_pcs]

    # spell progression chords
    # Accidentals follow standard roman-numeral convention: relative to the MAJOR
    # scale degree of the same root. So bVI in A minor = F natural (A major's VI
    # is F#, flat it once = F), matching how "bVI-bVII-i" is used in pop analysis.
    chords = []
    for tok in progression:
        deg, acc, q = parse_roman(tok)
        c_root, qual, c_name, tones = chord_for_root_degree(
            root_pc, scale_pcs, scale_key, deg, acc, q, prefer_flats)
        chords.append({
            "roman": tok,
            "name": c_name,
            "tones": tones, "root": c_root, "quality": qual,
        })

    # ---- canvas: portrait phone card, phone-first
    W = 1080
    pad = 36
    # components: title ~100, mode+scale "~70+50", main kb ~210, progression 2x2 ~440, footer ~110
    kb_h = 200
    card_h = 200
    gap = 18
    # 2x2 for 4 chords; 1xN for 2-3; single wide for 1; 2+ for 5+
    n = len(chords)
    if n <= 1:
        cols, rows = 1, 1
    elif n == 2:
        cols, rows = 2, 1
    elif n == 3:
        cols, rows = 3, 1
    elif n == 4:
        cols, rows = 2, 2
    else:
        cols, rows = 3, (n + 2) // 3
    prog_h = rows * card_h + (rows - 1) * gap + 40  # label + cards
    H = pad + 110 + 70 + 50 + (kb_h + 50) + prog_h + 110 + pad
    img = Image.new("RGB", (W, H), PAL["bg"])
    d = ImageDraw.Draw(img)

    f_mode = _font(34, bold=True)
    f_small = _font(24)
    f_chord = _font(34, bold=True)
    f_roman = _font(22)
    f_legend = _font(20)

    y = pad
    # header — vibe title, shrink until it fits one line (never truncate)
    vibe_text = f"“{vibe}”"
    vibe_size = 48
    while vibe_size > 26 and d.textlength(vibe_text, font=_font(vibe_size, bold=True)) > W - 2 * pad:
        vibe_size -= 2
    f_vibe = _font(vibe_size, bold=True)
    d.text((pad, y), vibe_text, font=f_vibe, fill=PAL["text"])
    y += vibe_size + 14
    scale_title = {"major": "Major", "ionian": "Ionian", "dorian": "Dorian", "phrygian": "Phrygian",
                   "lydian": "Lydian", "mixolydian": "Mixolydian", "aeolian": "Aeolian",
                   "natural_minor": "Natural Minor", "harmonic_minor": "Harmonic Minor",
                   "locrian": "Locrian", "minor_pentatonic": "Minor Pentatonic",
                   "major_pentatonic": "Major Pentatonic"}[scale_key]
    d.text((pad, y), f"{root_disp} {scale_title}", font=f_mode, fill=PAL["accent"])
    y += 42
    note = MODE_NOTE.get(scale_key, "")
    if note:
        d.text((pad, y), note, font=f_small, fill=PAL["dim"])
        y += 34
    else:
        y += 8

    # scale degrees strip as pill chips
    x = pad
    chip_h = 36
    for i, nm in enumerate(scale_names):
        tw = d.textlength(nm, font=f_small)
        chip_w = tw + 22
        fill = PAL["root"] if i == 0 else PAL["panel"]
        tc = PAL["root_dot"] if i == 0 else PAL["text"]
        d.rounded_rectangle([x, y, x + chip_w, y + chip_h], radius=10, fill=fill)
        d.text((x + 11, y + 6), nm, font=f_small, fill=tc)
        x += chip_w + 10
    y += chip_h + 22

    # main keyboard (scale lit)
    d.rounded_rectangle([pad - 4, y, W - pad + 4, y + kb_h + 44], radius=16, fill=PAL["panel"])
    d.text((pad + 8, y + 10), "SCALE on the OP-1  ·  F–E, both octaves", font=f_roman, fill=PAL["dim"])
    draw_keyboard(d, (pad + 12, y + 40, W - 2 * pad - 24, kb_h - 8), set(scale_pcs), root_pc, PAL)
    y += kb_h + 60

    # progression — 2x2 when 4 chords so keys stay readable on a phone
    d.text((pad, y), "PROGRESSION", font=f_roman, fill=PAL["dim"])
    y += 28
    cw = (W - 2 * pad - gap * (cols - 1)) / cols
    for i, c in enumerate(chords):
        r_i, c_i = divmod(i, cols)
        cx = pad + c_i * (cw + gap)
        cy = y + r_i * (card_h + gap)
        d.rounded_rectangle([cx, cy, cx + cw, cy + card_h], radius=14, fill=PAL["panel"])
        d.text((cx + 16, cy + 12), c["roman"], font=f_roman, fill=PAL["dim"])
        d.text((cx + 16, cy + 38), c["name"], font=f_chord, fill=PAL["accent"])
        draw_keyboard(d, (cx + 14, cy + 84, cw - 28, card_h - 100), c["tones"], c["root"], PAL, small=True)
    y += rows * card_h + (rows - 1) * gap + 24

    # footer
    d.line([pad, y, W - pad, y], fill=PAL["line"], width=1)
    y += 16
    if reference:
        # wrap long references to avoid microscopic footer / off-edge text
        prefix = "Sounds like: "
        max_w = W - 2 * pad
        words = (prefix + reference).split()
        line, lines = "", []
        for w in words:
            trial = (line + " " + w).strip()
            if d.textlength(trial, font=f_small) <= max_w:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
        for ln in lines[:3]:
            d.text((pad, y), ln, font=f_small, fill=PAL["dim"])
            y += 30
        y += 4
    d.text((pad, y), "orange = root  ·  blue = chord/scale tones  ·  [Left]/[Right] shift octave",
           font=f_legend, fill=PAL["dim"])

    img.save(out_path, optimize=True)
    return out_path


def validate(obj: dict):
    errs = []
    root = FLAT_TO_SHARP.get(obj.get("root", ""), obj.get("root", ""))
    if root not in N2I:
        errs.append(f"unknown root {obj.get('root')!r} (e.g. 'C', 'F#', 'Bb')")
    sk = obj.get("scale", "").lower().replace(" ", "_")
    if sk not in SCALES:
        errs.append(f"unknown scale {obj.get('scale')!r}; known: {sorted(SCALES)}")
    if not obj.get("vibe"):
        errs.append("vibe is required (it's printed at the top)")
    for tok in obj.get("progression", []):
        try:
            parse_roman(tok)
        except ValueError as e:
            errs.append(str(e))
    if not obj.get("progression"):
        errs.append("progression is required (list of roman numerals)")
    return errs


EXAMPLE = {
    "vibe": "melancholy but hopeful — end of the movie",
    "root": "A", "scale": "dorian",
    "progression": ["i", "v", "VII", "IV"],
    "reference": "“Time” — Inception (Am–Em–G–D loop; the D major IV is the dorian raised-6th sunlight)",
}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Render an OP-1 Field harmony guide card.")
    ap.add_argument("spec", nargs="?", help="JSON harmony object file, or omit for demo")
    ap.add_argument("--vibe", help='free-text vibe, e.g. --vibe "melancholy but hopeful"')
    ap.add_argument("--root", help="transpose: override the taxonomy root, e.g. --root F#")
    ap.add_argument("-o", "--out", default="/tmp/op1_guide.png")
    args = ap.parse_args()

    if args.vibe:
        import op1_vibe_intent as V
        vid, kind, score = V.resolve(args.vibe)
        if vid is None:
            print(f"NO TAXONOMY MATCH for {args.vibe!r} — the LLM caller should pick the")
            print("nearest vibe_id from references/op1_vibe_taxonomy.yaml, then re-run with")
            print("a JSON spec. The parser never invents harmony.")
            raise SystemExit(2)
        obj = V.spec_for(vid, vibe_label=args.vibe)
        if args.root:
            obj["root"] = args.root
        print(f"[vibe match] {vid} ({kind}, {score}) → {obj['root']} {obj['scale']} "
              f"{'-'.join(obj['progression'])}")
    elif args.spec:
        obj = json.loads(Path(args.spec).read_text())
    else:
        obj = EXAMPLE

    errs = validate(obj)
    if errs:
        print("INVALID:\n" + "\n".join(f"  - {e}" for e in errs))
        raise SystemExit(1)
    print(render_guide(obj, args.out))
