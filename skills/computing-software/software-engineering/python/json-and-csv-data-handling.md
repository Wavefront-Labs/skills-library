---
id: computing-software.software-engineering.python.json-and-csv-data-handling
name: json-and-csv-data-handling
category: computing-software
field: software-engineering
product: python
tags: [python, python-stdlib, python-json, python-csv, serialization, encoding, decimal]
level: practitioner
status: verified
description: "Read and write JSON and CSV correctly with the stdlib: custom encoders, Decimal and datetime handling, newline and encoding traps, dialects, streaming large files."
sources:
  - https://docs.python.org/3/library/json.html
  - https://docs.python.org/3/library/csv.html
  - https://www.rfc-editor.org/rfc/rfc8259
  - https://www.rfc-editor.org/rfc/rfc4180
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON and CSV data handling

**Goal:** lossless, encoding-safe interchange that works with Excel, other languages and large files.

## 1. JSON
```python
import json
from decimal import Decimal
data = json.loads(text)                               # str or bytes (UTF-8/16/32)
with open(p, encoding="utf-8") as f: data = json.load(f)
json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True)
json.loads(text, parse_float=Decimal)                 # money without float rounding
```
Custom types:
```python
def default(o):
    if isinstance(o, datetime): return o.isoformat()
    if isinstance(o, Decimal): return str(o)
    if isinstance(o, set): return sorted(o)
    raise TypeError(f"not JSON serialisable: {type(o).__name__}")
json.dumps(obj, default=default)
```
- Python allows `NaN`/`Infinity`, which are invalid JSON; use `allow_nan=False` when producing for other systems.
- Dict keys become strings: `{1: "a"}` round-trips as `{"1": "a"}`.
- Duplicate keys: last wins silently; detect with `object_pairs_hook`.
- Large files: JSON Lines (one object per line) streams with a simple loop; `ijson` for huge single documents.
- For speed: `orjson`/`msgspec` (bytes output, datetime support).

## 2. CSV reading
```python
import csv
with open(p, newline="", encoding="utf-8-sig") as f:      # newline="" is required; -sig strips Excel BOM
    for row in csv.DictReader(f):
        amount = Decimal(row["amount"])
```
- Everything is a string; convert explicitly and handle empty strings.
- Sniff unknown dialects: `csv.Sniffer().sniff(sample)`; Excel in many European locales writes `;` delimited files.
- `csv.field_size_limit(...)` if fields exceed 128 KB.

## 3. CSV writing
```python
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["id", "name", "amount"], extrasaction="raise")
    w.writeheader()
    w.writerows(rows)
```
Quoting: default `QUOTE_MINIMAL` handles commas, quotes and newlines inside fields. For Excel to open UTF-8 correctly, write `utf-8-sig`.

## Gotchas
- Without `newline=""`, Windows writes blank lines between rows and embedded newlines in quoted fields break.
- CSV injection: fields starting with `=`, `+`, `-`, `@` execute as formulas in spreadsheets; prefix with `'` when exporting user data for Excel.
- `json.load` on untrusted input is safe (no code execution) but can be memory-heavy; cap size.
- Float precision: `0.1 + 0.2` artefacts in JSON output; use Decimal or round at the edge.

## Verify
- Round-trip tests: `loads(dumps(x)) == x` for sample payloads; a CSV with commas, quotes, newlines and non-ASCII names opens correctly in Excel and re-reads identically.

## Checked
- Python 3.14.0 on Windows: `json.loads` of UTF-16 bytes, `ensure_ascii`/`indent`/`sort_keys`, `parse_float=Decimal`, the `default` hook (datetime, Decimal, set) and its `TypeError`, `NaN`/`Infinity` written by default and rejected by `allow_nan=False`, `[NaN]` accepted on read, integer keys becoming strings, duplicate keys last-wins and `object_pairs_hook` detecting them; CSV: `utf-8-sig` strips the BOM (plain `utf-8` leaves `﻿id` in the first header), quoted commas, quotes and newlines read back, `Sniffer` finds `;`, `DictWriter` quoting and `extrasaction="raise"`, writing without `newline=""` produced `
` on Windows, `utf-8-sig` writes a BOM, `field_size_limit()` is 131072 and a 200,000-character field raises `field larger than field limit`, and `csv` does not neutralise `=1+1`. `orjson`, `msgspec`, `ijson` and Excel opening were not run.
