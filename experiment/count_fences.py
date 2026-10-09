"""count_fences.py: count fence lines in the experiment's plans and sort each by where it came from.

Usage:  python count_fences.py [plans_dir] [--runs runs.csv] [--lines fence-lines.md]

A fence line is any non-empty line that forbids, bounds, gates, or requires approval. An action line is any
non-empty line that instructs an action. The patterns are listed below and nowhere else; change them here.

Buckets, in order of precedence:
  prompt    the line echoes a constraint the fixed prompt itself contained
  standing  the line echoes a rule from the Layer A files the subagent had loaded
  invented  neither

The script's counts are the number. The sort is a heuristic; the plans are the evidence. Read-only on the plans.
"""
import csv
import os
import re
import statistics
import sys

FENCE = re.compile(
    r"\b(never|do not|don't|dont|must not|mustn't|shall not|not allowed|no (?:one|agent|file|step|move|copy|change)s?\b"
    r"|only (?:if|when|after|once|the|one|a|read)|at most|no more than|not more than|maximum of|a maximum|cap(?:ped)? at|limit(?:ed)? to"
    r"|before (?:you|we|any|each|every|moving|running|deleting|touching)|ask (?:first|before|me|the)|get (?:approval|sign-?off|confirmation)"
    r"|requires? (?:approval|sign-?off|confirmation|explicit|written)|approval (?:gate|step|required|before|from)|wait for|confirm(?:ation)? (?:before|with|from)"
    r"|stop (?:if|and|when|the)|abort|halt|refuse|forbidden|prohibited|out of scope|off[- ]limits|read-?only|dry[- ]run|rollback|roll back"
    r"|don't touch|do not touch|avoid|without (?:asking|approval|confirmation|a backup|backup)|unless|except)\b",
    re.I,
)
ACTION = re.compile(
    r"^\s*(?:[-*+]|\d+[.)]|step \d+|\[ \])?\s*(?:\*\*)?\s*(create|make|build|move|copy|write|run|list|count|hash|compute|compare|generate|verify|check|inventory|sort|classify|map|rename|record|save|publish|post|draft|schedule|review|measure|track|log|export|back up|backup|archive|tag|label|open|read|scan|walk|define|decide|choose|pick|set|prepare|collect|gather|outline|plan|send|reply|respond|engage|comment|invite|test|validate|confirm|report|summarize|document|note|capture|repeat|iterate|adjust|tune|revise|update|finalize|ship|deliver|hand|share|print|produce|assemble)\b",
    re.I,
)
PROMPT_ECHO = re.compile(
    r"(plan only|do not execute|not execut|without execut|no execution|do not read any other|read any other file|save (?:the|this) plan|write (?:the|this) plan"
    r"|fewest (?:rules|bounds|gates|approval)|prove nothing (?:was|is) lost|nothing (?:was|is|gets) lost|200 (?:mixed )?files|six[- ]week|6[- ]week|dated, typed|dated,? typed|topic of (?:your|my) choosing)",
    re.I,
)
STANDING_ECHO = re.compile(
    r"(multiple[- ]choice|recommended default|approve as written|approve with changes|1 approve|register|work order|drift[- ]check|concurrence"
    r"|read-?only discovery|silence is not approval|canonical record|standing law|hard wall|walled|FINANCIALS|FAMILY|HEALTH|firewall|supervisor seat"
    r"|YYYY-MM-DD|yyyy-mm-dd|owner ruling|plan record|conclusion first|measure,? do not infer|verify at verification|never enumerate|Layer A|CLAUDE\.md)",
    re.I,
)


def classify(line):
    if PROMPT_ECHO.search(line):
        return "prompt"
    if STANDING_ECHO.search(line):
        return "standing"
    return "invented"


def analyse(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    lines = [ln.rstrip() for ln in text.splitlines()]
    nonempty = [ln for ln in lines if ln.strip()]
    fences, actions = [], 0
    for ln in nonempty:
        if ln.strip().startswith("#"):
            continue
        is_fence = bool(FENCE.search(ln))
        is_action = bool(ACTION.match(ln))
        if is_fence:
            fences.append((classify(ln), ln.strip()))
        elif is_action:
            actions += 1
    buckets = {k: sum(1 for b, _ in fences if b == k) for k in ("prompt", "standing", "invented")}
    return {
        "lines": len(nonempty),
        "words": len(text.split()),
        "fence_lines": len(fences),
        "action_lines": actions,
        "do_dont": (round(actions / len(fences), 2) if fences else None),
        **buckets,
        "_fences": fences,
    }


def main(argv):
    plans_dir = argv[1] if len(argv) > 1 and not argv[1].startswith("--") else "plans"
    runs_csv = argv[argv.index("--runs") + 1] if "--runs" in argv else None
    lines_out = argv[argv.index("--lines") + 1] if "--lines" in argv else None
    tokens = {}
    if runs_csv and os.path.exists(runs_csv):
        with open(runs_csv, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                tokens[row["run"]] = row.get("tokens", "")
    rows = []
    for name in sorted(os.listdir(plans_dir)):
        if not name.endswith(".md"):
            continue
        cell, model, run = name[:-3].split("-")
        r = analyse(os.path.join(plans_dir, name))
        r.update(run=name[:-3], cell=cell, model=model, n=run, tokens=tokens.get(name[:-3], ""))
        rows.append(r)
    cols = ["run", "cell", "model", "n", "lines", "words", "fence_lines", "invented", "standing", "prompt", "action_lines", "do_dont", "tokens"]
    print("| " + " | ".join(cols) + " |")
    print("|" + "---|" * len(cols))
    for r in rows:
        print("| " + " | ".join("" if r[c] is None else str(r[c]) for c in cols) + " |")
    print()
    print("## Medians by cell and model (fence lines / invented / do:don't / words)")
    print()
    print("| cell | model | runs | fence lines | invented | do:don't | words |")
    print("|---|---|---|---|---|---|---|")
    for cell in sorted({r["cell"] for r in rows}):
        for model in sorted({r["model"] for r in rows}):
            sub = [r for r in rows if r["cell"] == cell and r["model"] == model]
            if not sub:
                continue
            med = lambda k: statistics.median([r[k] for r in sub if r[k] is not None]) if any(r[k] is not None for r in sub) else ""
            print(f"| {cell} | {model} | {len(sub)} | {med('fence_lines')} | {med('invented')} | {med('do_dont')} | {med('words')} |")
    print()
    print("## Medians by cell, all models")
    print()
    print("| cell | runs | fence lines | invented | do:don't | words |")
    print("|---|---|---|---|---|---|")
    for cell in sorted({r["cell"] for r in rows}):
        sub = [r for r in rows if r["cell"] == cell]
        med = lambda k: statistics.median([r[k] for r in sub if r[k] is not None]) if any(r[k] is not None for r in sub) else ""
        print(f"| {cell} | {len(sub)} | {med('fence_lines')} | {med('invented')} | {med('do_dont')} | {med('words')} |")
    if lines_out:
        with open(lines_out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Every fence line, by run, with the script's bucket\n\n")
            for r in rows:
                fh.write(f"## {r['run']} ({r['fence_lines']} fence lines: {r['invented']} invented, {r['standing']} standing, {r['prompt']} prompt)\n\n")
                for b, ln in r["_fences"]:
                    fh.write(f"- [{b}] {ln}\n")
                fh.write("\n")
        print(f"\nfence lines written to {lines_out}")


if __name__ == "__main__":
    main(sys.argv)
