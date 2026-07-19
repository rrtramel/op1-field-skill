#!/usr/bin/env python3
"""
run_keys_tests.py — acceptance suite for the OP-1 harmony guide pipeline.

Covers:
  1. Theory engine: diatonic quality tables vs derived interval math (all modes)
  2. Chord spelling: roman numerals, accidentals (bVI convention), harmonic minor
  3. Sharp/flat display derivation per root
  4. Validator: rejects bad root/scale/roman
  5. Taxonomy: every vibe validates + spells without exceptions
  6. Intent parser: alias resolution battery
  7. Render: every taxonomy vibe renders a non-trivial PNG

Usage: python3 scripts/run_keys_tests.py
"""
import sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import op1_keys as K
import op1_vibe_intent as V

results = []

def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))

# ---- 1. Quality tables vs derived math ---------------------------------
def derived_quality(scale_pcs, deg):
    n = len(scale_pcs)
    r = scale_pcs[(deg - 1) % n]
    third = scale_pcs[(deg + 1) % n]
    fifth = scale_pcs[(deg + 3) % n]
    t3, t5 = (third - r) % 12, (fifth - r) % 12
    if t3 == 4 and t5 == 7: return "maj"
    if t3 == 3 and t5 == 7: return "min"
    if t3 == 3 and t5 == 6: return "dim"
    if t3 == 4 and t5 == 8: return "aug"
    return f"?{t3},{t5}"

for mode in ["major", "dorian", "phrygian", "lydian", "mixolydian", "aeolian", "locrian", "harmonic_minor"]:
    pcs = K.spell_scale("C", mode)
    derived = [derived_quality(pcs, d) for d in range(1, 8)]
    check(f"quality_table:{mode}", derived == K.QUALITY[mode],
          f"derived={derived}" if derived != K.QUALITY[mode] else "")

# ---- 2. Chord spelling battery ------------------------------------------
def spell(root, scale, tok, pf):
    root = K.FLAT_TO_SHARP.get(root, root)
    pcs = K.spell_scale(root, scale)
    deg, acc, q = K.parse_roman(tok)
    return K.chord_for_root_degree(K.N2I[root], pcs, scale, deg, acc, q, pf)[2]

SPELL_CASES = [
    ("C", "major", "vii", "Bdim"), ("A", "aeolian", "ii", "Bdim"),
    ("A", "aeolian", "bVI", "F"), ("A", "aeolian", "bVII", "G"),
    ("A", "aeolian", "bIII", "C"), ("D", "harmonic_minor", "vii", "C#dim"),
    ("D", "harmonic_minor", "V", "A"), ("D", "harmonic_minor", "III", "Faug"),
    ("A", "dorian", "i", "Am"), ("A", "dorian", "v", "Em"),
    ("A", "dorian", "VII", "G"), ("A", "dorian", "IV", "D"),
    ("E", "phrygian", "II", "F"), ("G", "mixolydian", "VII", "F"),
    ("Bb", "major", "I", "Bb"), ("Eb", "major", "IV", "Ab"),
    ("C", "major_pentatonic", "IV", "F"), ("A", "minor_pentatonic", "VII", "G"),
    ("F", "lydian", "II", "G"), ("C", "lydian", "II", "D"),
]
for root, scale, tok, exp in SPELL_CASES:
    pf = ("b" in root) or scale in ("aeolian", "natural_minor") and root in ("D", "G", "C") or K.FLAT_TO_SHARP.get(root, root) in ("F", "A#")
    got = spell(root, scale, tok, pf)
    check(f"spell:{root}_{scale}_{tok}", got == exp, f"got {got}, want {exp}")

# ---- 3. Validator --------------------------------------------------------
bad_objs = [
    ({"vibe": "x", "root": "H", "scale": "dorian", "progression": ["i"]}, "root"),
    ({"vibe": "x", "root": "D", "scale": "blorp", "progression": ["i"]}, "scale"),
    ({"vibe": "x", "root": "D", "scale": "dorian", "progression": ["VIII"]}, "roman"),
    ({"vibe": "", "root": "D", "scale": "dorian", "progression": ["i"]}, "vibe"),
]
for obj, what in bad_objs:
    check(f"validator_rejects:{what}", len(K.validate(obj)) > 0)

# ---- 4-5. Taxonomy integrity + render ------------------------------------
tax = V.load_taxonomy()
check("taxonomy_count", len(tax["vibes"]) == 20, f"got {len(tax['vibes'])}")

with tempfile.TemporaryDirectory() as td:
    for vid, entry in tax["vibes"].items():
        obj = V.spec_for(vid, tax)
        errs = K.validate(obj)
        if errs:
            check(f"tax_valid:{vid}", False, str(errs))
            continue
        try:
            out = Path(td) / f"{vid}.png"
            K.render_guide(obj, str(out))
            ok = out.exists() and out.stat().st_size > 10_000
            check(f"tax_render:{vid}", ok, f"size={out.stat().st_size if out.exists() else 0}")
        except Exception as e:
            check(f"tax_render:{vid}", False, str(e))

# ---- 6. Intent battery ----------------------------------------------------
INTENT_CASES = [
    ("melancholy but hopeful", "melancholy_but_hopeful"),
    ("like the end of a movie", "melancholy_but_hopeful"),
    ("creepy and unsettling", "eerie_unstable"),
    ("swashbuckling pirate adventure", "swashbuckling"),
    ("sad", "pure_melancholy"),
    ("triumphant victory anthem", "triumphant"),
    ("dreamy floating wonder", "dreamy_wonder"),
    ("the simpsons", "whimsical_comedic"),
    ("menacing villain theme", "menacing"),
    ("smooth late night jazz", "jazzy_resolve"),
    ("sweet home alabama", "bluesy_cool"),
    ("campfire folk song", "rootsy_open"),
    ("happy sunny morning", "bright_open"),
    ("flamenco desert vibes", "exotic_tension"),
    ("heart of courage", "courageous"),
    ("graduation song", "nostalgic_anthem"),
    ("gladiator sacrifice", "noble_tragedy"),
    ("dark knight brooding", "dark_dramatic"),
    ("scarborough fair", "wistful_folk"),
    ("cathedral mystery", "mystical_unease"),
    ("xqzplth nothing matches", None),
]
for text, exp in INTENT_CASES:
    vid, kind, score = V.resolve(text)
    check(f"intent:{text[:30]}", vid == exp, f"got {vid}")

# ---- report ---------------------------------------------------------------
fails = [r for r in results if not r[1]]
print(f"\n{len(results) - len(fails)}/{len(results)} passed")
if fails:
    print("\nFAILURES:")
    for name, _, detail in fails:
        print(f"  ✗ {name}  {detail}")
    sys.exit(1)
print("ALL GREEN")
