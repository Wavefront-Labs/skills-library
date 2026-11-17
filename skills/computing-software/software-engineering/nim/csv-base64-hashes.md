---
id: computing-software.software-engineering.nim.csv-base64-hashes
name: csv-base64-hashes
category: computing-software
field: software-engineering
product: nim
tags: [csv-base64-hashes, stdlib-json-and-data, parsecsv, csv, base64, md5, sha1, hashes, checksums, encoding, nim]
level: practitioner
status: docs-checked
description: "Parse CSV with parsecsv, encode with base64, and build Hash values for table keys with std/hashes."
sources:
  - https://nim-lang.org/docs/parsecsv.html
  - https://nim-lang.org/docs/base64.html
  - https://nim-lang.org/docs/hashes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSV, Base64 and checksums

Goal: handle common data encodings.

- CSV: `import std/parsecsv`; `var p: CsvParser; p.open("a.csv"); p.readHeaderRow(); while p.readRow(): echo p.rowEntry("name")`; `p.close()`. `open(..., separator=';')` sets delimiter. For writes build lines with `join` and quote fields containing separators.
- Base64: `import std/base64`; `encode(data)`, `decode(s)`, `encode(data, safe=true)` for URL-safe.
- Hash for tables: `import std/hashes`; `hash(x)`, `x !& y` mixes, `!$` finalises; define `proc hash(o: MyObj): Hash` for table keys.
- `hashes` computes `Hash` values for tables and sets, not cryptographic digests; its page points to separate cryptographic and hashing modules in the standard library.

Gotchas:
- CSV parser lacks type conversion; call parseInt yourself.

Verify: decode(encode(x)) == x.

## Checked

2026-11-03. Confirmed against the parsecsv, base64 and hashes pages: CsvParser open(filename, separator), readHeaderRow, readRow, rowEntry, close; base64 encode(s, safe) and decode; hash, `!&`, `!$`. Removed: the `checksums` package claim and the md5/sha1 advice (not on these pages).

Method: documentation only; no commands were run.
