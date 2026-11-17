#!/usr/bin/env python3
"""harvest - turn the local report log into a worklist for maintainers and contributors.

The librarian's `report(id, outcome)` calls append to a local log (default ~/.wavefront-skills/reports.jsonl,
override with WAVEFRONT_SKILLS_LOG or --log). This reads it and prints:

  GAPS          tasks nobody could find coverage for, grouped by wording, most frequent first: skills to write
  FIX FIRST     skills reported `wrong`: re-check against the source before anything else
  WEAK          skills reported `not_useful` more often than `used`: improve the description, tags or body
  WORKING       most used skills: do not break these

    python tools/harvest.py [--log FILE] [--top 15]

Nothing here edits the library. Self-improvement is a proposal loop: harvest produces candidates, a human (or an
agent working through a normal pull request) drafts the change, and it merges only after review and, for retrieval
changes, only if the held-out retrieval tests (`tools/retrieval_eval.py`) do not get worse.
"""
import argparse, collections, json, os, re


def norm(task):
    w = [x for x in re.findall(r"[a-z0-9]+", task.lower()) if len(x) > 3]
    return " ".join(sorted(set(w))[:8])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default=os.environ.get("WAVEFRONT_SKILLS_LOG") or os.path.join(os.path.expanduser("~"), ".wavefront-skills", "reports.jsonl"))
    ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args()
    if not os.path.exists(a.log):
        return print(f"no reports yet ({a.log})")
    recs = [json.loads(l) for l in open(a.log, encoding="utf-8") if l.strip()]
    by = collections.defaultdict(collections.Counter)
    gaps = collections.defaultdict(list)
    for r in recs:
        by[r["id"]][r["outcome"]] += 1
        if r["outcome"] == "gap":
            gaps[norm(r.get("task") or r.get("note") or "")].append(r.get("task") or r.get("note"))
    print(f"{len(recs)} reports\n")
    print("GAPS (skills to write)")
    for k, v in sorted(gaps.items(), key=lambda x: -len(x[1]))[: a.top]:
        print(f"  {len(v):3}x  {v[0][:110]}")
    print("\nFIX FIRST (reported wrong)")
    for sid, c in sorted(((s, c) for s, c in by.items() if c["wrong"]), key=lambda x: -x[1]["wrong"])[: a.top]:
        print(f"  {c['wrong']:3}x  {sid}")
    print("\nWEAK (not_useful > used)")
    for sid, c in sorted(((s, c) for s, c in by.items() if c["not_useful"] > c["used"]), key=lambda x: -x[1]["not_useful"])[: a.top]:
        print(f"  {c['not_useful']:3} not useful / {c['used']} used  {sid}")
    print("\nWORKING (most used)")
    for sid, c in sorted(((s, c) for s, c in by.items() if c["used"]), key=lambda x: -x[1]["used"])[: a.top]:
        print(f"  {c['used']:3}x  {sid}")


if __name__ == "__main__":
    main()
