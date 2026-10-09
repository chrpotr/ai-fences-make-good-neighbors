#!/usr/bin/env python3
"""Count fences in a plan. A fixed pattern list flags candidates; a person judges every line.

    python count.py flag plans/<run_id>.md          -> writes plans/<run_id>.count.md
    python count.py tally plans/<run_id>.count.md   -> writes the seven counts into runs.csv

The sheet has one line per plan line:

    012 | ? | fence=  | bucket=         | kind=dont | <the line>

Fill in: fence=y or n; bucket=prompt, standing, or invented (only when fence=y); kind=do, dont, or blank.
`?` marks a line the pattern list flagged. Pre-filled values are guesses to edit, not findings.
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs.csv"

FENCE_PATTERNS = [
    r"\bnever\b", r"\bdo not\b", r"\bdon't\b", r"\bmust not\b", r"\bmay not\b", r"\bshould not\b", r"\bavoid\b",
    r"\bonly\b", r"\bexcept\b", r"\brequire[sd]? (?:approval|sign-off|permission|confirmation)\b",
    r"\bask (?:before|first|for approval|for permission)\b", r"\bbefore (?:you|proceeding|any)\b",
    r"\bat most\b", r"\bat least\b", r"\bno more than\b", r"\bno fewer than\b", r"\bmaximum\b", r"\bminimum\b",
    r"\blimit\b", r"\bstop if\b", r"\bhalt\b", r"\bprohibit", r"\bforbid", r"\bnot allowed\b", r"\bout of scope\b",
    r"\bguardrail", r"\bconstraint", r"\bmust\b",
]
FENCE_RE = re.compile("|".join(FENCE_PATTERNS), re.IGNORECASE)
STEP_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)]|step \d+)", re.IGNORECASE)


def flag(plan_path):
    plan_path = Path(plan_path)
    out = plan_path.with_suffix(".count.md")
    lines = plan_path.read_text(encoding="utf-8").splitlines()
    rows = ["# Count sheet for " + plan_path.name,
            "# fence=y/n; bucket=prompt/standing/invented; kind=do/dont. '?' = flagged by pattern. Edit, then run tally.", ""]
    flagged = 0
    for i, line in enumerate(lines, 1):
        hit = bool(FENCE_RE.search(line))
        flagged += hit
        kind = "dont" if hit else ("do" if STEP_RE.match(line) and line.strip() else "")
        rows.append("%03d | %s | fence=%s | bucket= | kind=%s | %s" % (i, "?" if hit else " ", "y" if hit else "", kind, line))
    out.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print("wrote " + str(out) + ": " + str(len(lines)) + " lines, " + str(flagged) + " flagged for judgement")


ROW_RE = re.compile(r"^(\d{3}) \| (.) \| fence=(\w*) \| bucket=(\w*) \| kind=(\w*) \| (.*)$")


def tally(sheet_path, write=True):
    sheet_path = Path(sheet_path)
    run_id = sheet_path.name.replace(".count.md", "")
    total = fences = do = dont = 0
    buckets = {"prompt": 0, "standing": 0, "invented": 0}
    for raw in sheet_path.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(raw)
        if not m:
            continue
        _, _, fence, bucket, kind, text = m.groups()
        if not text.strip():
            continue
        total += 1
        if fence.lower() == "y":
            fences += 1
            if bucket.lower() in buckets:
                buckets[bucket.lower()] += 1
            else:
                print("line " + m.group(1) + ": fence=y but bucket is '" + bucket + "' (want prompt, standing, or invented)")
        if kind.lower() == "do":
            do += 1
        elif kind.lower() == "dont":
            dont += 1
    counts = {"lines_total": total, "fence_lines": fences, "fence_prompt": buckets["prompt"],
              "fence_standing": buckets["standing"], "fence_invented": buckets["invented"],
              "do_lines": do, "dont_lines": dont}
    print(run_id + ": " + ", ".join(k + "=" + str(v) for k, v in counts.items()))
    if write:
        write_counts(run_id, counts)
    return counts


def write_counts(run_id, counts):
    if not RUNS.exists():
        print("runs.csv not found; counts not written")
        return
    with RUNS.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)
    hit = False
    for r in rows:
        if r.get("run_id") == run_id:
            r.update({k: str(v) for k, v in counts.items()})
            hit = True
    if not hit:
        print("run_id " + run_id + " not in runs.csv; counts not written")
        return
    with RUNS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print("runs.csv updated for " + run_id)


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("flag", "tally"):
        print(__doc__)
        sys.exit(1)
    if sys.argv[1] == "flag":
        flag(sys.argv[2])
    else:
        tally(sys.argv[2])


if __name__ == "__main__":
    main()
