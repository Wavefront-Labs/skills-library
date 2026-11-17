#!/usr/bin/env python3
"""check - Level-2 (fields) coverage check.
- Every Level-1 category has a fields/<category>.yaml file.
- Every field id is unique within its category, kebab-case, and matches the file's own
  `category:` key.
- Every (category, field) pair already live in skills.index.jsonl (built by tools/reindex.py)
  is present here with status: live — a field already carrying real skills can never be
  silently dropped or renamed.
Run: python taxonomy/fields/check.py   (exit 1 on any problem)"""
import json, re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
FIELDS = ROOT / "taxonomy" / "fields"
CATS = yaml.safe_load((ROOT / "taxonomy" / "categories.yaml").read_text(encoding="utf-8"))["categories"]
KEBAB = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')

live = set()
manifest = ROOT / "skills.index.jsonl"
if manifest.exists():
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if line.strip():
            s = json.loads(line)
            live.add((s["category"], s["field"]))

problems = []
seen_fields = {}
for cat in CATS:
    f = FIELDS / f"{cat}.yaml"
    if not f.exists():
        problems.append(f"{cat}: no taxonomy/fields/{cat}.yaml")
        continue
    doc = yaml.safe_load(f.read_text(encoding="utf-8"))
    if doc.get("category") != cat:
        problems.append(f"{cat}.yaml: category '{doc.get('category')}' != filename '{cat}'")
    ids = set()
    for field in doc.get("fields", []):
        fid = field.get("id")
        if not fid or not KEBAB.match(fid):
            problems.append(f"{cat}.yaml: bad or missing field id {fid!r}")
            continue
        if fid in ids:
            problems.append(f"{cat}.yaml: duplicate field id '{fid}'")
        ids.add(fid)
        if not field.get("scope"):
            problems.append(f"{cat}.yaml/{fid}: missing scope")
        seen_fields[(cat, fid)] = field.get("status")
    for cat2, fid2 in live:
        if cat2 == cat and (cat2, fid2) not in seen_fields:
            problems.append(f"{cat}.yaml: live field '{fid2}' (has real skills) is missing")
        elif cat2 == cat and seen_fields.get((cat2, fid2)) != "live":
            problems.append(f"{cat}.yaml/{fid2}: has real skills but status is not 'live'")

n_cats = sum(1 for cat in CATS if (FIELDS / f"{cat}.yaml").exists())
n_fields = len(seen_fields)
print(f"{n_cats}/{len(CATS)} categories drafted, {n_fields} fields total")
if problems:
    print(f"PROBLEMS ({len(problems)}):")
    for p in problems:
        print("  ", p)
    sys.exit(1)
print("ok")
