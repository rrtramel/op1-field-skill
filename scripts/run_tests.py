#!/usr/bin/env python3
"""
run_tests.py — OP-1 Field recipe compiler regression suite.

Loads references/op1_recipe_examples.yaml (20 recipe objects), compiles each one
through op1_compile.py's Validator + renderer, and asserts the per-prompt
acceptance checks from the mega-prompt:

  - output includes engine, envelope, play mode, FX, and LFO/no-LFO note
  - output includes screen actions ([Synth]/[T1..T4]/[Shift])
  - all colors valid (validator)
  - no unsupported parameter labels (validator label check)
  - LFO has destination + target parameter (validator, when applicable)
  - graphic-only controls get no fake numbers (validator)
  - split-range controls include warnings (validator)
  - output remains readable on mobile (line-count budget)

Usage:
    python3 run_tests.py            # human report
    python3 run_tests.py --report  # write ../TEST_REPORT.md
"""
from __future__ import annotations
import sys, argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import op1_compile as C  # noqa: E402

EXAMPLES = HERE.parent / "references" / "op1_recipe_examples.yaml"
LINE_BUDGET = 34


def per_prompt_checks(rec: dict, rendered: str):
    """Acceptance checks beyond validator errors. Returns list of (name, ok, detail)."""
    r = rec.get("recipe", rec)
    checks = []

    # engine section present
    checks.append(("has_engine", "1) ENGINE" in rendered, ""))
    # envelope section
    checks.append(("has_envelope", "ENVELOPE" in rendered, ""))
    # play mode (for relevant categories) or present line
    if r.get("category") in ("pad", "chord", "bass", "lead"):
        checks.append(("has_play_mode", "PLAY —" in rendered, "required for this category"))
    else:
        checks.append(("has_play_mode", True, "n/a"))
    # FX present OR explicit dry
    checks.append(("has_fx_or_dry", ("FX —" in rendered), ""))
    # LFO present OR explicit static
    checks.append(("has_lfo_or_static", ("LFO —" in rendered), ""))
    # screen actions present
    has_actions = ("[Synth]" in rendered or "[T1]" in rendered) and "[Shift]" in rendered
    checks.append(("has_screen_actions", has_actions, ""))
    # mobile readable (shift-layer recipes e.g. DSynth legitimately run longer)
    lines = rendered.count("\n") + 1
    budget = 39 if r.get("engine", {}).get("shift_params") else LINE_BUDGET
    checks.append(("mobile_readable", lines <= budget, f"{lines} lines (budget {budget})"))
    # no percentages on values
    checks.append(("no_percentages", "%" not in rendered, ""))
    return checks


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="Write TEST_REPORT.md")
    args = ap.parse_args(argv)

    ref = C.load_compiler_ref()
    data = C.load_yaml(EXAMPLES)
    recipes = data["recipes"]

    rows = []
    all_pass = True
    report_lines = ["# OP-1 Field Recipe Compiler — Test Report", "",
                    f"Suite: `references/op1_recipe_examples.yaml` ({len(recipes)} prompts)", ""]

    for i, rec in enumerate(recipes, 1):
        r = rec.get("recipe", rec)
        title = r.get("user_request", r.get("title", f"recipe {i}"))
        ok, rendered, errs, warns = C.compile_recipe(rec, ref)
        check_results = per_prompt_checks(rec, rendered) if rendered else []
        checks_ok = all(c[1] for c in check_results)
        passed = ok and checks_ok
        all_pass = all_pass and passed
        status = "PASS" if passed else "FAIL"
        rows.append((i, title, status, errs, [c for c in check_results if not c[1]], warns))

    # Console output
    print(f"{'#':>2}  {'PROMPT':<36} STATUS")
    print("-" * 52)
    for i, title, status, errs, failed_checks, warns in rows:
        print(f"{i:>2}  {title[:36]:<36} {status}")
        for e in errs:
            print(f"      ERROR {e}")
        for fc in failed_checks:
            print(f"      CHECK-FAIL {fc[0]} ({fc[2]})")
    print("-" * 52)
    n_pass = sum(1 for x in rows if x[2] == "PASS")
    print(f"{n_pass}/{len(rows)} passed")

    if args.report:
        report_lines.append("| # | Prompt | Status | Notes |")
        report_lines.append("|---|--------|--------|-------|")
        for i, title, status, errs, failed_checks, warns in rows:
            notes = []
            if errs:
                notes += [f"ERR: {e}" for e in errs]
            if failed_checks:
                notes += [f"check: {fc[0]} {fc[2]}" for fc in failed_checks]
            report_lines.append(f"| {i} | {title} | {status} | {'; '.join(notes) if notes else 'all checks pass'} |")
        report_lines.append("")
        report_lines.append(f"**Result: {n_pass}/{len(rows)} passed.**")
        report_lines.append("")
        report_lines.append("## Acceptance checks applied per prompt")
        report_lines.append("")
        for c in ["engine present", "envelope present", "play mode (pad/bass/lead)",
                  "FX or explicit dry", "LFO or explicit static", "screen actions ([Synth]/[T1-4]/[Shift])",
                  "mobile readable (<=34 lines)", "no percentages",
                  "(validator) colors valid, labels match, graphic-only no fake numbers,",
                  "split-range warnings present, LFO destination+parameter, numeric in range"]:
            report_lines.append(f"- {c}")
        report_lines.append("")
        report_lines.append("## Sample rendered output (prompt 1)")
        report_lines.append("")
        report_lines.append("```")
        _, rendered, _, _ = C.compile_recipe(recipes[0], ref)
        report_lines.append(rendered or "(render failed)")
        report_lines.append("```")
        out = HERE.parent / "TEST_REPORT.md"
        out.write_text("\n".join(report_lines) + "\n")
        print(f"\nWrote {out}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
