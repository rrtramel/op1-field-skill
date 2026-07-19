#!/usr/bin/env python3
"""
op1_vibe_intent.py — map free-text vibe descriptions to taxonomy specs.

Resolution order (first hit wins):
  1. exact alias match (case-insensitive, punctuation-stripped)
  2. substring alias match (longest alias wins)
  3. token-overlap scoring against aliases + emotion_note words
  4. None -> caller falls back to the LLM choosing from the alias list

The parser NEVER invents harmony. It returns a taxonomy vibe_id; the spec
comes from the YAML. LLM fallback picks an id from the same list — the
validator in op1_keys.py checks the final spec regardless.
"""
from __future__ import annotations
import re, string
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

TAX_PATH = Path(__file__).resolve().parent.parent / "references" / "op1_vibe_taxonomy.yaml"

STOP = {"a", "an", "the", "and", "but", "or", "of", "to", "in", "for", "with",
        "like", "that", "this", "it", "is", "feel", "feeling", "feels", "vibe",
        "kind", "kinda", "sort", "sorta", "something", "song", "music", "track",
        "really", "very", "so", "bit", "little", "make", "want", "i", "my", "me"}


def _norm(s: str) -> str:
    s = s.lower().strip()
    s = s.translate(str.maketrans("", "", string.punctuation.replace("-", " ")))
    return re.sub(r"\s+", " ", s).strip()


def _tokens(s: str):
    return [t for t in _norm(s).split() if t not in STOP and len(t) > 2]


def load_taxonomy(path: Path = TAX_PATH):
    with open(path) as f:
        return yaml.safe_load(f)


def build_alias_index(tax: dict):
    """alias -> vibe_id (includes the vibe_id itself as an implicit alias)."""
    idx = {}
    for vid, entry in tax["vibes"].items():
        for a in entry.get("aliases", []):
            idx[_norm(a)] = vid
        idx[_norm(vid.replace("_", " "))] = vid
    return idx


def resolve(text: str, tax: dict | None = None):
    """Return (vibe_id, match_kind, score) or (None, 'no_match', 0.0)."""
    tax = tax or load_taxonomy()
    idx = build_alias_index(tax)
    n = _norm(text)

    # 1) exact
    if n in idx:
        return idx[n], "exact", 1.0

    # 2) substring — longest matching alias wins
    best, blen = None, 0
    for alias, vid in idx.items():
        if len(alias) >= 4 and alias in n and len(alias) > blen:
            best, blen = vid, len(alias)
    if best:
        return best, "substring", min(1.0, blen / max(len(n), 1))

    # 3) token overlap against aliases + emotion notes
    qtok = set(_tokens(text))
    if not qtok:
        return None, "no_match", 0.0
    best, bscore = None, 0.0
    for vid, entry in tax["vibes"].items():
        hay = set()
        for a in entry.get("aliases", []):
            hay |= set(_tokens(a))
        hay |= set(_tokens(entry.get("emotion_note", "")))
        hay |= set(_tokens(vid.replace("_", " ")))
        if not hay:
            continue
        ov = len(qtok & hay)
        score = ov / max(len(qtok), 1)
        if score > bscore:
            best, bscore = vid, score
    if best and bscore >= 0.34:
        return best, "fuzzy", round(bscore, 2)
    return None, "no_match", 0.0


def spec_for(vibe_id: str, tax: dict | None = None, vibe_label: str | None = None):
    """Build the render spec for op1_keys.py from a taxonomy id."""
    tax = tax or load_taxonomy()
    entry = tax["vibes"][vibe_id]
    obj = {"vibe": vibe_label or vibe_id.replace("_", " ")}
    obj.update(entry["spec"])
    return obj


if __name__ == "__main__":
    import argparse, json
    ap = argparse.ArgumentParser()
    ap.add_argument("vibe", help="free-text vibe description")
    ap.add_argument("--json", action="store_true", help="print the full render spec")
    args = ap.parse_args()
    vid, kind, score = resolve(args.vibe)
    if vid is None:
        print(json.dumps({"match": None, "kind": kind}))
        raise SystemExit(2)
    if args.json:
        print(json.dumps({"match": vid, "kind": kind, "score": score,
                          "spec": spec_for(vid, vibe_label=args.vibe)}, indent=2))
    else:
        print(f"{vid}  ({kind}, {score})")
