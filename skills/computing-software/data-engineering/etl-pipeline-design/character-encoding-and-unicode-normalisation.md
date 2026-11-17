---
id: computing-software.data-engineering.etl-pipeline-design.character-encoding-and-unicode-normalisation
name: character-encoding-and-unicode-normalisation
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, character-encoding, unicode-normalization, utf-8, mojibake]
level: advanced
status: gated
description: "Prevent encoding bugs in pipelines: detecting source encodings, decoding explicitly, BOMs, mojibake repair, Unicode NFC/NFKC normalisation and collation for joins."
sources:
  - https://docs.python.org/3/howto/unicode.html
  - https://unicode.org/reports/tr15/
  - https://ftfy.readthedocs.io/en/latest/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Character encoding and Unicode normalisation

**Goal:** text arrives in the warehouse exactly as intended, and equal-looking strings compare equal.

## Decode explicitly
- Never rely on defaults (`open()` uses the platform locale; Windows often cp1252). Always `open(path, encoding="utf-8")` or the documented source encoding.
- Detect unknown encodings on a sample with `charset-normalizer`; confirm with the source owner (charset-normalizer guessed cp1250 for a short cp1252 sample here, so treat detection as a hint; common: UTF-8, cp1252/Windows-1252, ISO-8859-1, UTF-16 LE from Excel exports, Shift_JIS, EBCDIC).
- `encoding="utf-8-sig"` strips a UTF-8 BOM (run); on Windows with Python 3.14 `locale.getpreferredencoding(False)` returned `cp1252` here, confirming that the default is the locale. Without it the first header becomes `\ufeffid`.
- Decide on invalid bytes: `errors="strict"` (fail) for critical data, never silently `ignore`.

Warehouse loaders (option spellings not confirmed here (gated: unconfirmed, source is paywalled or blocked)): Snowflake `FILE_FORMAT = (ENCODING = 'WINDOWS1252')`, BigQuery `--encoding=ISO-8859-1`, Spark `option("encoding", "cp1252")`.

## Mojibake
`CafÃ©` = UTF-8 bytes decoded as cp1252/latin-1. Fix at the source decode step; for already-damaged data `ftfy.fix_text()` repairs common cases (run with ftfy 6.3.1: the mojibake of `Café` came back as `Café`). Double-encoded data needs the reverse transform: `s.encode("cp1252").decode("utf-8")` (test carefully).

## Normalisation
The same visible text can have different code points: `é` as U+00E9 (NFC) or `e` + U+0301 (NFD, common from macOS file names).
```python
import unicodedata
clean = unicodedata.normalize("NFC", s)          # canonical composition: default for storage
key = unicodedata.normalize("NFKC", s).casefold().strip()   # compatibility + case folding: for matching keys
```
- NFKC also maps full-width letters, ligatures (`ﬁ` -> `fi`) and superscripts: good for matching, lossy for display.
- Warehouses: Snowflake/BigQuery have `NORMALIZE()` style functions or use collations; otherwise normalise in the pipeline.

## Other traps
- Zero-width spaces, non-breaking spaces (U+00A0) and trailing whitespace in keys: strip/replace before joins. Python's `str.strip()` removes U+00A0 but not U+200B, and NFKC maps U+00A0 to a plain space but leaves U+200B (all checked).
- Length limits: MySQL `VARCHAR(n)` counts characters, but the 65,535-byte row limit is in bytes and depends on the character set (MySQL docs), so wide tables with utf8mb4 hit it sooner. Other databases count bytes by default or by setting (gated: unconfirmed, source is paywalled or blocked).
- MySQL `utf8` is a deprecated alias for `utf8mb3` (max 3 bytes, BMP only); use `utf8mb4` for supplementary characters such as emoji (MySQL docs). An emoji is 4 bytes in UTF-8 (checked).

## Verify
Test fixtures with accents, emoji, CJK, BOM and NFD input load correctly; join keys normalised in both sides produce expected matches.
