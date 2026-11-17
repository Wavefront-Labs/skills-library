---
id: computing-software.software-engineering.cobol.codepages-ebcdic-ascii
name: codepages-ebcdic-ascii
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, codepages-ebcdic-ascii, cobol-unicode, ebcdic-ascii, collating-sequence, code-page-conversion]
level: practitioner
status: draft
description: "Handle EBCDIC and ASCII differences: sort order, character ranges, and conversion at file transfer."
sources:
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EBCDIC versus ASCII, collating sequence and conversion
**Goal:** keep data correct when it crosses platforms.

- Collating differs: EBCDIC orders lowercase, then uppercase, then digits; ASCII orders digits, uppercase, lowercase. Sorts and comparisons give different orders.
- Character ranges: in EBCDIC `A THRU Z` as a class includes non-letters between I and J and R and S; use explicit lists or `IS ALPHABETIC`.
- Text file transfer (FTP ASCII mode, Zowe, `iconv`) converts text; binary and packed fields must be transferred as binary or fields will be corrupted.
- GnuCOBOL on ASCII systems can use `PROGRAM COLLATING SEQUENCE IS EBCDIC` or ALPHABET definitions to mimic mainframe ordering.
```cobol
ALPHABET EBCDIC-SEQ IS EBCDIC.
OBJECT-COMPUTER. X PROGRAM COLLATING SEQUENCE IS EBCDIC-SEQ.
```

## Gotchas
- Packed/binary content survives only if the whole file is moved without conversion; mixed-format records need field-aware conversion.
- Characters like `[ ] { } | ^` map differently across EBCDIC code pages (e.g. 037 vs 1047).

## Self-check
Sort a small mixed-case dataset on both platforms and document the order differences.
