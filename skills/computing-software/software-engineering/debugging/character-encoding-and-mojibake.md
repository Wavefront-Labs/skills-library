---
id: computing-software.software-engineering.debugging.character-encoding-and-mojibake
name: character-encoding-and-mojibake
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, character-encoding, mojibake, utf-8, unicode, byte-order-mark]
level: practitioner
status: verified
description: "Debug encoding bugs and mojibake: identify the wrong decode from byte patterns, check each hop (files, HTTP, DB, terminal), fix at the boundary, and repair already-corrupted data."
sources: ["https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/", "https://ftfy.readthedocs.io/", "https://dev.mysql.com/doc/refman/8.4/en/charset-unicode-utf8mb4.html", "https://docs.python.org/3/howto/unicode.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Character encoding and mojibake bugs

## Recognise the pattern
| You see | Likely cause |
|---|---|
| `Ã©` for `é`, `â€™` for `'` | UTF-8 bytes decoded as Windows-1252/Latin-1 |
| `Ã‚Â`, `Ã©` becoming `ÃƒÂ©` | double (or triple) mis-decoding and re-encoding (run: `é` decoded twice as cp1252 gives `ÃƒÂ©`) |
| `�` (U+FFFD) | invalid bytes for the decoder; data already lost at that hop |
| `?` in place of characters | encoded to a charset lacking them (e.g. MySQL `utf8`/latin1 column) |
| `ï»¿` at file start | UTF-8 BOM read as Latin-1 |
| Emoji fail, accents fine | MySQL `utf8` (3-byte utf8mb3) instead of `utf8mb4` |

## Find the hop: inspect bytes, not rendered text
```
printf '%s' "$value" | xxd | head         # é should be c3 a9 in UTF-8
python -c "print(repr(open('f.csv','rb').read(60)))"
file -i data.csv                           # guess, not proof
```
Check each boundary in order: source file/editor -> HTTP request (`Content-Type: ...; charset=`) ->
app decode -> DB connection charset -> column charset/collation -> export/CSV -> terminal/viewer.
`SELECT HEX(name) FROM t WHERE id=1` shows what the DB actually stores.

## Fix at the boundaries
- Decode bytes to text once on input, encode once on output; text inside the program is Unicode.
- Always specify the encoding: Python `open(p, encoding="utf-8")` (default is locale-dependent
  before 3.15, where PEP 686 makes UTF-8 the default; `PYTHONUTF8=1` forces UTF-8 mode earlier), Java `Files.readString(p, UTF_8)` (default UTF-8 since JDK 18),
  .NET `Encoding.UTF8`, Node `fs.readFile(p, 'utf8')`.
- HTTP: send `charset=utf-8`; HTML `<meta charset="utf-8">`.
- MySQL: `utf8mb4` columns (`utf8` is a deprecated alias of the 3-byte `utf8mb3`), `utf8mb4_0900_ai_ci` collation (MySQL 8.0+, listed in the 8.4 manual; MariaDB does not have it), connection `charset=utf8mb4`.
  Postgres: database `ENCODING 'UTF8'`, client_encoding UTF8.
- CSV for Excel: write UTF-8 **with BOM** (`utf-8-sig`) or desktop Excel often falls back to the ANSI code page (behaviour not tested here; check your Excel version).
- Terminals/logs: `LANG=C.UTF-8`; Windows console `chcp 65001`.

## Repair corrupted data
- Single mis-decode: `s.encode("cp1252").decode("utf-8")` reverses it (test on samples first; run: `Ã©` -> `é` works, but text whose UTF-8 bytes include 0x81, 0x8D, 0x8F, 0x90 or 0x9D, such as `Á` (C3 81), was decoded by the wrong tool as Latin-1 and needs `.encode("latin-1")`, and cp1252 raises on those bytes).
- Mixed/multiple layers: `ftfy.fix_text(s)` (Python) detects and fixes common mojibake (run on ftfy 6.3.1: `cafÃ©` -> `café`, `â€™` -> `'`).
- MySQL latin1 columns holding UTF-8 bytes: convert via `BINARY`/`VARBINARY` then to utf8mb4
  (`ALTER TABLE ... MODIFY col VARBINARY(...)` then `... MODIFY col VARCHAR(...) CHARACTER SET utf8mb4`).
- `�` replacement characters can't be recovered; go back to the source.

## Related traps
Normalisation (NFC vs NFD: `é` as one or two code points breaks equality and filenames on macOS),
string length in bytes vs code points vs grapheme clusters, case-folding with locale (Turkish i).
