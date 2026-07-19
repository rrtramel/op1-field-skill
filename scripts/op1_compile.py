#!/usr/bin/env python3
"""
op1_compile.py — OP-1 Field recipe compiler.

Takes an intermediate recipe object (YAML or JSON), validates it against the
canonical compiler reference + validation rules, and DETERMINISTICALLY renders
the final Telegram/mobile recipe text.

This is the enforcement layer described in the skill architecture: the LLM fills
the recipe object, but it does NOT freehand the final text — this renderer does,
and it refuses to render an invalid object.

Usage:
    python3 op1_compile.py RECIPE.yaml            # validate + render one recipe
    python3 op1_compile.py RECIPE.yaml --json     # machine-readable result
    python3 op1_compile.py --selftest             # internal sanity check

Exit codes: 0 = valid & rendered, 1 = validation errors, 2 = usage/IO error.

Stdlib only (json, argparse, sys, pathlib) + a tiny built-in YAML subset loader
with PyYAML fallback, so it runs anywhere.
"""
from __future__ import annotations
import sys, json, argparse
from pathlib import Path

REF_DIR = Path(__file__).resolve().parent.parent / "references"
COMPILER_REF = REF_DIR / "op1_recipe_compiler_reference.yaml"

CANON_COLORS = ["blue", "ochre", "grey", "orange"]
COLOR_DISPLAY = {"blue": "Blue", "ochre": "Ochre", "grey": "Grey", "orange": "Orange"}
COLOR_ALIASES = {
    "blue": "blue", "t1": "blue",
    "ochre": "ochre", "beige": "ochre", "t2": "ochre",
    "grey": "grey", "gray": "grey", "t3": "grey",
    "orange": "orange", "red": "orange", "t4": "orange",
}
GRAPHIC_TYPES = {"graphic_only", "visual_curve"}
SPEED_TYPES = {"relative_speed"}  # may carry a number OR a relative word — both valid
NUMERIC_TYPES = {"numeric_0_99", "numeric_small_discrete", "numeric_decimal", "numeric_hz", "numeric_ms", "bipolar_signed"}
# numeric_plus_graphic ([B]): screen shows BOTH a number and a graphic.
# Value is required (numeric, range-checked); visual_target is optional flavor text.
BOTH_TYPES = {"numeric_plus_graphic"}

ENGINE_EMOJI = {
    "cluster": "🌊", "digital": "💎", "dimension": "📐", "dna": "🧬", "dr_wave": "🩺",
    "dsynth": "🎛️", "fm": "📻", "phase": "🌀", "pulse": "⚡", "string": "🎸",
    "voltage": "🔋", "vocoder": "🤖", "sampler": "📼", "amp": "🎚️",
}
FX_EMOJI = {
    "cwo": "🐄", "delay": "🔁", "grid": "🕸️", "mother": "🚪", "nitro": "🏎️",
    "phone": "☎️", "punch": "🥊", "spring": "🪀", "terminal": "💻", "fazer": "👽",
}
LFO_EMOJI = {
    "value": "〰️", "element": "⚡", "random": "🎲", "tremolo": "🌊",
    "velocity": "🎹", "midi": "🎹",
}


# --------------------------------------------------------------------------
# YAML loading: prefer PyYAML; fall back to JSON for .json inputs.
# --------------------------------------------------------------------------
def load_yaml(path: Path):
    text = path.read_text()
    if path.suffix in (".json",):
        return json.loads(text)
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text)
    except ModuleNotFoundError:
        # Try JSON as a last resort (a recipe object can be valid JSON).
        try:
            return json.loads(text)
        except Exception:
            raise SystemExit(
                "PyYAML not installed and input is not JSON. "
                "Install pyyaml (uv pip install --system pyyaml) or pass a .json recipe."
            )


def load_compiler_ref():
    if not COMPILER_REF.exists():
        raise SystemExit(f"Compiler reference not found: {COMPILER_REF}")
    return load_yaml(COMPILER_REF)


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------
class Validator:
    def __init__(self, ref: dict):
        self.ref = ref
        self.synths = ref["modules"]["synths"]
        self.effects = ref["modules"]["effects"]
        self.lfos = ref["modules"]["lfos"]
        self.envelope = ref["modules"]["envelope"]
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, rule, msg):
        self.errors.append(f"[{rule}] {msg}")

    def warn(self, rule, msg):
        self.warnings.append(f"[{rule}] {msg}")

    @staticmethod
    def norm_color(c: str) -> str:
        return COLOR_ALIASES.get(str(c).strip().lower(), str(c).strip().lower())

    def _check_param_colors(self, params, where, rule):
        if params is None:
            return False
        keys = {self.norm_color(k) for k in params.keys()}
        missing = [c for c in CANON_COLORS if c not in keys]
        if missing:
            self.err(rule, f"{where} missing colors: {', '.join(missing)}.")
            return False
        return True

    def _norm_params(self, params):
        """Return params keyed by canonical color name."""
        return {self.norm_color(k): v for k, v in (params or {}).items()}

    def _check_param_values(self, params, module_def, where):
        ref_params = (module_def or {}).get("params") or {}
        np = self._norm_params(params)
        for color in CANON_COLORS:
            if color not in np:
                continue
            p = np[color] or {}
            vt = p.get("value_type")
            label = p.get("label", "")
            val = p.get("value", None)
            vis = p.get("visual_target", None)
            # graphic-only: no fake number, must have visual target
            if vt in GRAPHIC_TYPES:
                if val not in (None, "", "null"):
                    self.err("graphic_only_no_fake_number",
                             f"{where}.{color} ({label}) is {vt} — must not carry a number (got {val!r}).")
                if not vis:
                    self.err("graphic_only_no_fake_number",
                             f"{where}.{color} ({label}) is {vt} — needs a visual_target.")
            # relative_speed (LFO SPEED): screen shows a number, but a relative word
            # ("slow"/"fast") is also acceptable. Require at least ONE of value/visual_target.
            elif vt in SPEED_TYPES:
                if val in (None, "", "null") and not vis:
                    self.err("speed_needs_value_or_word",
                             f"{where}.{color} ({label}) is {vt} — needs a number (e.g. 8) or a relative word (e.g. 'slow').")
            elif vt in NUMERIC_TYPES or vt in BOTH_TYPES:
                if val is None:
                    self.err("numeric_has_value",
                             f"{where}.{color} ({label}) is numeric but has no value.")
                else:
                    rng = (ref_params.get(color) or {}).get("range")
                    if rng and isinstance(val, (int, float)):
                        lo, hi = rng
                        if not (lo <= val <= hi):
                            self.err("numeric_in_range",
                                     f"Value {val} for {where}.{color} ({label}) outside range {rng}.")
            # discrete_selector / tap_selector / shift_layer / split_range:
            # value may be int or string; if split_range numeric, range-check when numeric.
            elif vt == "split_range":
                rng = (ref_params.get(color) or {}).get("range")
                if isinstance(val, (int, float)) and rng:
                    lo, hi = rng
                    if not (lo <= val <= hi):
                        self.err("numeric_in_range",
                                 f"Value {val} for {where}.{color} ({label}) outside range {rng}.")

    def validate(self, recipe: dict):
        r = recipe.get("recipe", recipe)

        # engine_exists
        eng = r.get("engine", {})
        eng_id = eng.get("id")
        engine_def = self.synths.get(eng_id)
        if engine_def is None:
            self.err("engine_exists", f"Engine '{eng_id}' is not a known engine.")
        # engine not recipe-eligible (e.g. amp: no envelope, external-input processor)
        if engine_def and engine_def.get("recipe_eligible") is False:
            self.err("engine_recipe_eligible",
                     f"Engine '{eng_id}' is excluded from recipes: "
                     f"{engine_def.get('recipe_exclusion_reason', 'not recipe-eligible')}")
        # sampler has null params; skip param checks for it
        engine_has_params = engine_def and engine_def.get("params") is not None

        if engine_has_params:
            if self._check_param_colors(eng.get("params"), f"engine '{eng_id}'", "engine_param_colors_complete"):
                self._check_param_values(eng.get("params"), engine_def, "engine")

        # shift layer rules
        ref_shift = (engine_def or {}).get("shift_params")
        rec_shift = eng.get("shift_params")
        if rec_shift and not ref_shift:
            self.err("shift_params_only_if_supported",
                     f"Engine '{eng_id}' has no shift layer; shift_params must be null.")
        if eng_id == "dsynth":
            if not self._check_param_colors(rec_shift, "DSynth shift layer", "dsynth_requires_shift"):
                pass

        # labels match reference (engine)
        if engine_has_params:
            self._check_labels(eng.get("params"), engine_def, "engine")

        # envelope
        env = r.get("envelope", {})
        vshape = env.get("visual_shape", {})
        for k, v in (vshape or {}).items():
            if isinstance(v, (int, float)) or (isinstance(v, str) and v.strip().isdigit()):
                self.err("envelope_visual_only",
                         f"Envelope {k} must be visual language, not a number ({v}).")
        arche = env.get("archetype")
        if arche and arche not in (self.envelope.get("archetypes") or {}):
            self.warn("envelope_archetype_known", f"Envelope archetype '{arche}' unknown.")

        # play mode
        cat = r.get("category")
        pm = r.get("play_mode", {})
        if cat in ("pad", "chord", "bass", "lead") and not pm.get("mode"):
            self.err("play_mode_when_relevant",
                     f"Category '{cat}' requires a play mode.")

        # FX
        fx = r.get("fx", {})
        fx_id = fx.get("id")
        if fx_id != "none" and fx_id not in self.effects:
            self.err("fx_exists_or_none", f"Effect '{fx_id}' not known (and not 'none').")
        if fx_id == "none":
            if fx.get("enabled", False):
                self.err("fx_or_explicit_dry", "FX 'none' must have enabled=false (explicit dry).")
        else:
            if self._check_param_colors(fx.get("params"), f"FX '{fx_id}'", "fx_param_colors_complete"):
                self._check_param_values(fx.get("params"), self.effects.get(fx_id), "fx")
                self._check_labels(fx.get("params"), self.effects.get(fx_id), "fx")
            si = fx.get("selection_instruction") or ""
            if "[T3]" not in si:
                self.err("selection_instructions_present",
                         "FX selection_instruction must include [T3] enable/select.")

        # LFO
        lfo = r.get("lfo", {})
        lfo_id = lfo.get("id")
        if lfo_id != "none" and lfo_id not in self.lfos:
            self.err("lfo_exists_or_none", f"LFO '{lfo_id}' not known (and not 'none').")
        if lfo_id == "none":
            if lfo.get("enabled", False):
                self.err("lfo_or_explicit_static", "LFO 'none' must have enabled=false (explicit static).")
        else:
            lfo_def = self.lfos.get(lfo_id, {})
            if self._check_param_colors(lfo.get("params"), f"LFO '{lfo_id}'", "lfo_param_colors_complete"):
                self._check_param_values(lfo.get("params"), lfo_def, "lfo")
                self._check_labels(lfo.get("params"), lfo_def, "lfo")
            si = lfo.get("selection_instruction") or ""
            if "[T4]" not in si:
                self.err("selection_instructions_present",
                         "LFO selection_instruction must include [T4] enable/select.")
            dest = lfo.get("destination")
            tgt = lfo.get("target_parameter")
            if lfo_id in ("value", "element", "random", "velocity"):
                if not dest or not tgt:
                    self.err("lfo_destination_required",
                             f"LFO '{lfo_id}' requires destination + target_parameter.")
            # value_lfo_complete: SPEED/AMOUNT/DEST/PARAMETER labels present
            if lfo_id == "value":
                lp = self._norm_params(lfo.get("params"))
                labels = {c: str((lp.get(c) or {}).get("label", "")).upper() for c in CANON_COLORS}
                if "SPEED" not in labels.get("blue", ""):
                    self.err("value_lfo_complete", "Value LFO Blue must be SPEED.")
                if "AMOUNT" not in labels.get("ochre", ""):
                    self.err("value_lfo_complete", "Value LFO Ochre must be AMOUNT.")
                if "DEST" not in labels.get("grey", ""):
                    self.err("value_lfo_complete", "Value LFO Grey must be DEST.")
                if "PARAMETER" not in labels.get("orange", ""):
                    self.err("value_lfo_complete", "Value LFO Orange must be PARAMETER.")
            if lfo_id == "random":
                amt = (self._norm_params(lfo.get("params")).get("ochre") or {}).get("value")
                if isinstance(amt, (int, float)) and amt < 0:
                    self.err("random_lfo_amount_non_negative", "Random LFO amount must be >= 0.")
            if lfo_id == "tremolo":
                if dest or tgt:
                    self.err("tremolo_no_destination",
                             "Tremolo LFO is hardwired to pitch+volume — clear destination/target_parameter.")
                # tremolo_pitch_volume_split: Ochre = PITCH AMOUNT, Grey = VOLUME AMOUNT
                lp = self._norm_params(lfo.get("params"))
                ochre_label = str((lp.get("ochre") or {}).get("label", "")).upper()
                grey_label = str((lp.get("grey") or {}).get("label", "")).upper()
                if "PITCH" not in ochre_label:
                    self.err("tremolo_pitch_volume_split",
                             f"Tremolo Ochre must be PITCH AMOUNT (got '{ochre_label}').")
                if "VOLUME" not in grey_label:
                    self.err("tremolo_pitch_volume_split",
                             f"Tremolo Grey must be VOLUME AMOUNT (got '{grey_label}').")
            # velocity_lfo_fields: Blue=VOLUME AMOUNT, Ochre=DEST AMOUNT, Grey=DEST, Orange=PARAMETER
            if lfo_id == "velocity":
                lp = self._norm_params(lfo.get("params"))
                blue_label = str((lp.get("blue") or {}).get("label", "")).upper()
                ochre_label = str((lp.get("ochre") or {}).get("label", "")).upper()
                if "VOLUME" not in blue_label and "AMP" not in blue_label:
                    self.err("velocity_lfo_fields",
                             f"Velocity LFO Blue must be VOLUME AMOUNT (got '{blue_label}').")
                if "AMOUNT" not in ochre_label:
                    self.err("velocity_lfo_fields",
                             f"Velocity LFO Ochre must be DEST AMOUNT (got '{ochre_label}').")
            # midi_lfo_cc_channels: params must be labeled CC 1-4, not speed/amount/dest/param
            if lfo_id == "midi":
                lp = self._norm_params(lfo.get("params"))
                expected = {"blue": "CC 1", "ochre": "CC 2", "grey": "CC 3", "orange": "CC 4"}
                for color, want in expected.items():
                    got = str((lp.get(color) or {}).get("label", "")).upper().strip()
                    if got != want:
                        self.err("midi_lfo_cc_channels",
                                 f"MIDI LFO {color} must be labeled '{want}' (got '{got}').")

        # engine selection instruction
        if not (eng.get("selection_instruction") or "").strip():
            self.err("selection_instructions_present", "Engine selection_instruction is required.")

        # correction macros
        if not r.get("correction_macros"):
            self.err("correction_macro_present", "At least one correction macro is required.")

        # split-range + special warnings must be present in provenance.warnings
        warns = " ".join(r.get("provenance", {}).get("warnings", [])).lower()
        if eng_id == "dr_wave" and ("hp" not in warns and "high-pass" not in warns and "silence" not in warns):
            self.err("dr_wave_filter_warning", "Dr. Wave FILTER split-range warning missing from provenance.warnings.")
        if eng_id == "digital" and ("ring" not in warns and "detune" not in warns):
            self.err("digital_ringmod_warning", "Digital Grey detune/ring-mod warning missing from provenance.warnings.")
        if eng_id == "pulse" and "50" not in warns:
            self.err("pulse_mod_warning", "Pulse MOD center-50 warning missing from provenance.warnings.")
        if fx_id == "terminal" and "model" not in warns and "hp" not in warns:
            self.err("terminal_model_warning", "Terminal MODEL split-range warning missing from provenance.warnings.")
        if eng_id == "vocoder" and ("input" not in warns and "mic" not in warns):
            self.err("vocoder_input_note", "Vocoder audio-input requirement missing from provenance.warnings.")

        return not self.errors

    def _check_labels(self, params, module_def, where):
        ref_params = (module_def or {}).get("params") or {}
        np = self._norm_params(params)
        for color in CANON_COLORS:
            if color not in np or color not in ref_params:
                continue
            got = str((np[color] or {}).get("label", "")).strip().upper()
            expected = str((ref_params[color] or {}).get("label", "")).strip().upper()
            if not expected:
                continue
            # tolerant: allow the recipe label to be a prefix/substring of the
            # reference label or vice-versa (handles "FREQ" vs "FREQ (FM AMOUNT)").
            if got and got not in expected and expected not in got:
                self.err("labels_match_reference",
                         f"{where}.{color} label '{got}' != reference '{expected}'.")


# --------------------------------------------------------------------------
# Deterministic renderer
# --------------------------------------------------------------------------
SEP = "━━━━━━━━━━━━━━"


def _row(color: str, label: str, value, visual, value_type) -> str:
    name = COLOR_DISPLAY[Validator.norm_color(color)]
    if value_type in GRAPHIC_TYPES or value in (None, "", "null"):
        detail = visual if visual else ""
    else:
        detail = str(value)
        if visual:
            detail = f"{value}  ({visual})"
    return f"{name:<6} {label:<11} {detail}"


def render(recipe: dict, ref: dict) -> str:
    r = recipe.get("recipe", recipe)
    out = []
    eng = r.get("engine", {})
    eng_id = eng.get("id")
    emoji = ENGINE_EMOJI.get(eng_id, "🎛️")
    title = r.get("title", "OP-1 PATCH").upper()
    out.append(f"🎛️ {title} {emoji}")
    out.append(SEP)

    # 1) ENGINE
    out.append(f"1) ENGINE — {eng_id.upper()}")
    out.append(eng["selection_instruction"])
    np = {Validator.norm_color(k): v for k, v in (eng.get("params") or {}).items()}
    if np:
        for c in CANON_COLORS:
            p = np.get(c, {}) or {}
            out.append(_row(c, p.get("label", ""), p.get("value"), p.get("visual_target"), p.get("value_type")))
    # shift layer
    if eng.get("shift_params"):
        out.append("⇧ SHIFT (hold [Shift] while turning)")
        sp = {Validator.norm_color(k): v for k, v in eng["shift_params"].items()}
        for c in CANON_COLORS:
            if c in sp:
                p = sp[c] or {}
                out.append(_row(c, p.get("label", ""), p.get("value"), p.get("visual_target"), p.get("value_type")))
    out.append(SEP)

    # 2) ENVELOPE
    env = r.get("envelope", {})
    vs = env.get("visual_shape", {})
    out.append(f"2) 📈 ENVELOPE — {env.get('archetype','')} (curve, no numbers)")
    out.append(f"Blue   ATTACK    {vs.get('blue_attack','')}")
    out.append(f"Ochre  DECAY     {vs.get('ochre_decay','')}")
    out.append(f"Grey   SUSTAIN   {vs.get('grey_sustain','')}")
    out.append(f"Orange RELEASE   {vs.get('orange_release','')}")
    out.append(SEP)

    # 3) PLAY MODE (single compact line)
    pm = r.get("play_mode", {})
    if pm.get("mode"):
        porta = pm.get("portamento")
        porta_txt = f" Portamento {porta}." if porta not in (None, "", "null") else ""
        out.append(f"3) PLAY — {pm['mode']} · [Shift]+[T2], set {str(pm['mode']).upper()}.{porta_txt}")
        out.append(SEP)

    # 4) FX
    fx = r.get("fx", {})
    fx_id = fx.get("id")
    if fx_id and fx_id != "none":
        fe = FX_EMOJI.get(fx_id, "✨")
        out.append(f"4) ✨ FX — {fx_id.upper()} {fe} ON")
        out.append(fx["selection_instruction"])
        fp = {Validator.norm_color(k): v for k, v in (fx.get("params") or {}).items()}
        for c in CANON_COLORS:
            p = fp.get(c, {}) or {}
            out.append(_row(c, p.get("label", ""), p.get("value"), p.get("visual_target"), p.get("value_type")))
    else:
        out.append("4) ✨ FX — none (dry)")
    out.append(SEP)

    # 5) LFO
    lfo = r.get("lfo", {})
    lfo_id = lfo.get("id")
    if lfo_id and lfo_id != "none":
        le = LFO_EMOJI.get(lfo_id, "🔄")
        out.append(f"5) 🔄 LFO — {lfo_id.upper()} {le} ON")
        out.append(lfo["selection_instruction"])
        lp = {Validator.norm_color(k): v for k, v in (lfo.get("params") or {}).items()}
        for c in CANON_COLORS:
            p = lp.get(c, {}) or {}
            out.append(_row(c, p.get("label", ""), p.get("value"), p.get("visual_target"), p.get("value_type")))
    else:
        out.append("5) 🔄 LFO — none (static patch)")
    out.append(SEP)

    # Correction macros
    for m in r.get("correction_macros", [])[:2]:
        out.append(f"💡 {m.get('symptom','').capitalize()} → {m.get('screen_action','')}")

    # Single simple honesty line — values are starting points, tweak by ear.
    out.append("⚠️ starting point — tweak by ear")

    return "\n".join(out)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def compile_recipe(recipe: dict, ref: dict):
    v = Validator(ref)
    ok = v.validate(recipe)
    rendered = render(recipe, ref) if ok else None
    # post-render checks
    if rendered:
        if "%" in rendered:
            ok = False
            v.errors.append("[no_percentages] Rendered output contains a percentage.")
            rendered = None
        else:
            lines = rendered.count("\n") + 1
            # DSynth's shift block legitimately adds ~5 lines; budget is higher there.
            r = recipe.get("recipe", recipe)
            budget = 39 if (r.get("engine", {}).get("shift_params")) else 34
            if lines > budget:
                v.warnings.append(f"[output_line_count] Recipe is {lines} lines (budget {budget}).")
    return ok, rendered, v.errors, v.warnings


def main(argv=None):
    ap = argparse.ArgumentParser(description="OP-1 Field recipe compiler")
    ap.add_argument("recipe", nargs="?", help="Path to recipe object (.yaml/.json)")
    ap.add_argument("--json", action="store_true", help="Machine-readable output")
    ap.add_argument("--selftest", action="store_true", help="Run internal sanity test")
    args = ap.parse_args(argv)

    ref = load_compiler_ref()

    if args.selftest:
        sample = REF_DIR / "op1_recipe_schema.yaml"
        data = load_yaml(sample)
        ex = data.get("example", {})
        ok, rendered, errs, warns = compile_recipe(ex, ref)
        print("SELFTEST", "PASS" if ok else "FAIL")
        if errs:
            print("\n".join(errs))
        if rendered:
            print(rendered)
        return 0 if ok else 1

    if not args.recipe:
        ap.error("recipe path required (or use --selftest)")
    path = Path(args.recipe)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2
    recipe = load_yaml(path)
    ok, rendered, errs, warns = compile_recipe(recipe, ref)
    if args.json:
        print(json.dumps({"valid": ok, "errors": errs, "warnings": warns, "rendered": rendered}, indent=2))
        return 0 if ok else 1
    if warns:
        print("WARNINGS:\n" + "\n".join(warns) + "\n", file=sys.stderr)
    if not ok:
        print("VALIDATION FAILED:\n" + "\n".join(errs), file=sys.stderr)
        return 1
    print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
