#!/usr/bin/env python3
"""check - Level-3 (products) validation.
- Every products/<category>/<field>.yaml has matching category/field keys, and the field
  exists in taxonomy/fields/<category>.yaml.
- Product ids unique within the field, kebab-case; kind is application|craft|method; scope present.
- Every (category, field, product) live in skills.index.jsonl appears with status: live.
Fields without a products file are counted, not errors (Level 3 fills in gradually).
Run: python taxonomy/products/check.py   (exit 1 on any problem)"""
import json, re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
PRODUCTS = ROOT / "taxonomy" / "products"
FIELDS_DIR = ROOT / "taxonomy" / "fields"
KEBAB = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
KINDS = {"application", "craft", "method"}

fields_by_cat = {}
for f in FIELDS_DIR.glob("*.yaml"):
    doc = yaml.safe_load(f.read_text(encoding="utf-8"))
    fields_by_cat[doc["category"]] = {fl["id"] for fl in doc["fields"]}

live = set()
manifest = ROOT / "skills.index.jsonl"
if manifest.exists():
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if line.strip():
            s = json.loads(line)
            live.add((s["category"], s["field"], s["product"]))

problems, seen = [], {}
n_files = 0
for f in sorted(PRODUCTS.glob("*/*.yaml")):
    n_files += 1
    cat, field = f.parent.name, f.stem
    doc = yaml.safe_load(f.read_text(encoding="utf-8"))
    rel = f"{cat}/{field}.yaml"
    if doc.get("category") != cat:
        problems.append(f"{rel}: category key '{doc.get('category')}' != folder '{cat}'")
    if doc.get("field") != field:
        problems.append(f"{rel}: field key '{doc.get('field')}' != filename '{field}'")
    if field not in fields_by_cat.get(cat, set()):
        problems.append(f"{rel}: field '{field}' not in taxonomy/fields/{cat}.yaml")
    ids = set()
    for p in doc.get("products", []):
        pid = p.get("id")
        if not pid or not KEBAB.match(pid):
            problems.append(f"{rel}: bad or missing product id {pid!r}"); continue
        if pid in ids:
            problems.append(f"{rel}: duplicate product id '{pid}'")
        ids.add(pid)
        if p.get("kind") not in KINDS:
            problems.append(f"{rel}/{pid}: kind must be application|craft|method, got {p.get('kind')!r}")
        if not p.get("scope"):
            problems.append(f"{rel}/{pid}: missing scope")
        seen[(cat, field, pid)] = p.get("status")

for cat, field, prod in live:
    if (cat, field, prod) not in seen:
        problems.append(f"{cat}/{field}.yaml: live product '{prod}' (has real skills) is missing"
                        if (PRODUCTS / cat / f"{field}.yaml").exists()
                        else f"{cat}/{field}.yaml missing but has live products ({prod})")
    elif seen[(cat, field, prod)] != "live":
        problems.append(f"{cat}/{field}.yaml/{prod}: has real skills but status is not 'live'")

total_fields = sum(len(v) for v in fields_by_cat.values())
print(f"{n_files}/{total_fields} fields have products files, {len(seen)} products total")
if problems:
    print(f"PROBLEMS ({len(problems)}):")
    for p in problems:
        print("  ", p)
    sys.exit(1)
print("ok")
