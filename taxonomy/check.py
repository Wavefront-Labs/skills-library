#!/usr/bin/env python3
"""check - Level-1 coverage check. Every source entry maps to at least one category, every
mapped category exists, and every category is backed by at least two sources.
Run: python taxonomy/check.py   (exit 1 on any problem)"""
import sys
from pathlib import Path
import yaml


class _NoDupLoader(yaml.SafeLoader):
    """Raises instead of silently keeping only the last value when a mapping key repeats
    (e.g. a category with two `tie_breaks:` entries) — plain safe_load drops the first one."""


def _no_dup_construct_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                None, None, f"duplicate key {key!r}", key_node.start_mark)
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_NoDupLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_dup_construct_mapping)

HERE = Path(__file__).resolve().parent
cats = yaml.load((HERE / "categories.yaml").read_text(encoding="utf-8"), Loader=_NoDupLoader)["categories"]
srcs = yaml.load((HERE / "crosswalk.yaml").read_text(encoding="utf-8"), Loader=_NoDupLoader)["sources"]

problems, backing = [], {c: set() for c in cats}
for src, entries in srcs.items():
    for entry, mapped in entries.items():
        if not mapped:
            problems.append(f"{src} / {entry}: maps to no category")
        for c in mapped or []:
            if c not in cats:
                problems.append(f"{src} / {entry}: unknown category '{c}'")
            else:
                backing[c].add(src)
for c, s in backing.items():
    if len(s) < 2:
        problems.append(f"category '{c}' is backed by {len(s)} source(s): {sorted(s)}")

n = sum(len(e) for e in srcs.values())
print(f"{len(cats)} categories, {len(srcs)} sources, {n} source entries")
for c in sorted(cats, key=lambda c: len(backing[c])):
    print(f"  {c:26} backed by {len(backing[c]):2} sources")
if problems:
    print("PROBLEMS:"); [print("  ", p) for p in problems]; sys.exit(1)
print("every source entry has a home")
