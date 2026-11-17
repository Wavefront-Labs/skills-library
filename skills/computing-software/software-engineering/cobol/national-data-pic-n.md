---
id: computing-software.software-engineering.cobol.national-data-pic-n
name: national-data-pic-n
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, national-data-pic-n, cobol-unicode, national-data, pic-n, utf-16, usage-national]
level: advanced
status: docs-checked
description: "Use USAGE NATIONAL (PIC N) for UTF-16 text in Enterprise COBOL and convert with FUNCTION NATIONAL-OF and DISPLAY-OF; LENGTH vs BYTE-LENGTH."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PIC N national and UTF-16 data
**Goal:** handle multilingual text correctly in IBM Enterprise COBOL for z/OS 6.4.

```cobol
01 WS-UNI  PIC N(20) USAGE NATIONAL.
MOVE FUNCTION NATIONAL-OF(WS-UTF8-TEXT 1208) TO WS-UNI
MOVE FUNCTION DISPLAY-OF(WS-UNI 1208) TO WS-OUT-UTF8
```
- National data (USAGE NATIONAL, `PIC N(m)`) and national literals are UTF-16BE (big endian), CCSID 1200, regardless of the CODEPAGE compiler option. One encoding unit is 2 bytes. UTF-8 data (`PIC U`, USAGE UTF-8) is CCSID 1208.
- Literals: `N'...'` or `N"..."` are national literals when the NSYMBOL(NATIONAL) option is in effect; `NX'hhhh...'` is hexadecimal notation (four hex digits per character, 4 to 320 digits) and is not affected by NSYMBOL.
- `FUNCTION NATIONAL-OF(arg-1 [arg-2])` converts alphabetic, alphanumeric, UTF-8 or DBCS text to national; arg-2 is the source CCSID. If omitted, the source is the CODEPAGE-option code page, or 1208 when arg-1 is UTF-8.
- `FUNCTION DISPLAY-OF(arg-1 [arg-2])` converts national or UTF-8 text to alphanumeric in the CCSID given as arg-2 (default: the CODEPAGE code page). Unconvertible characters become substitution characters and no exception is raised.
- `FUNCTION LENGTH` of a national item counts national character positions; `FUNCTION BYTE-LENGTH` (and `LENGTH OF`) always returns bytes. Example from the manual: a `PIC 9(3)` USAGE NATIONAL item has LENGTH 3 but 6 bytes.
- DBCS is the older double-byte facility: `PIC G(n) USAGE DISPLAY-1`; with PIC N and the NSYMBOL(DBCS) option, DISPLAY-1 is implied.
- Moving alphanumeric data to a national item converts it from the CODEPAGE code page; a VALUE clause on a national item may be an alphanumeric literal, which is converted to UTF-16.

## Gotchas
- Each 2-byte encoding unit is one "character" to COBOL. A surrogate pair is two units (4 bytes) and a combining sequence is two or more; the runtime does not check for splits, so take care with reference modification and truncating MOVEs.
- If the z/OS Unicode conversion services lack the table for the CCSID pair, NATIONAL-OF raises a severe run-time error.
- RECORD CONTAINS and BLOCK CONTAINS counts are in bytes: 10 national characters is 20 CHARACTERS.

## Self-check
Convert a UTF-8 string containing an accented letter to national and back; the round trip must be identical, and BYTE-LENGTH of the national item must be twice its LENGTH.

## Checked
2026-11-08. Confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference (Chapter 2 character encoding units and Unicode UTF-16; national literals incl. NX; PICTURE G/N and USAGE clause notes; Chapter on NATIONAL-OF, DISPLAY-OF, LENGTH and BYTE-LENGTH functions; FD RECORD clause). Removed: GnuCOBOL national-support claims (source not read), the statement that CCSID 1208 and 1200 are only "IBM conventions", and the ISO source.
Method: documentation only; no commands were run.
