---
id: computing-software.software-engineering.cobol.reference-modification
name: reference-modification
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, reference-modification, substring, ref-mod, string-handling, bound-ref-mod]
level: practitioner
status: docs-checked
description: "Take substrings with name(start:length) and avoid out-of-range reference modification."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reference modification and substrings
**Goal:** read and write part of a field.

```cobol
MOVE WS-DATE(1:4) TO WS-YEAR
MOVE 'ZZ' TO WS-REC(10:2)
MOVE WS-NAME(WS-I:) TO WS-REST      *> to end of field
MOVE TAB OF TABLE-1 (3) (4:2) TO SUFFIX    *> subscript first, then ref-mod
```
- Offsets are 1-based. The start must be a positive nonzero integer no larger than the item's length; the length, if given, must be a positive nonzero integer and start + length - 1 must not exceed the item's size. If length is omitted, the substring runs to the end of the item.
- Start and length are arithmetic expressions, so `WS-NAME(WS-I + 1 : WS-N)` is allowed.
- The target may be a USAGE DISPLAY, DISPLAY-1, NATIONAL or UTF-8 item (qualified or subscripted), a group item (a national group is treated as category national), or an alphanumeric/national function result. A numeric, numeric-edited or external floating-point DISPLAY item is treated as alphanumeric for reference modification, so it works on the characters, and a SEPARATE sign counts as a position.
- For NATIONAL and DISPLAY-1 items positions are whole characters (2 bytes each), not bytes.
- The result is an elementary item without JUSTIFIED. With a subscript, the subscript is evaluated first, then the reference modification.

## Gotchas
- A start or length outside the rules above is invalid, and checking is a compiler/runtime option: on GnuCOBOL `--debug` (`-d`) enables all runtime checks, and `-fec=EC-BOUND-REF-MOD` enables the reference-modification check alone. Without checking, a bad offset can touch neighbouring storage; enable checks while developing.
- Zero length is not allowed by the language rules. GnuCOBOL has `-fref-mod-zero-length` to allow it, and that flag only matters with `EC-BOUND-REF-MOD` active.
- On an edited numeric item, ref-mod addresses the edited characters (the item is treated as alphanumeric).

## Self-check
Compile with `--debug` (GnuCOBOL), set start beyond the item's size and confirm a runtime error is reported.

## Checked
2026-11-08. Confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference PDF (Reference modification section and examples) and the GnuCOBOL Programmer's Guide (--debug, -fec, -fref-mod-zero-length, EC-BOUND-REF-MOD). Removed: IBM SSRANGE as the checking option (the Language Reference only points to the Programming Guide for it, which was not read), and the claim that ref-mod length expressions work only in "recent compilers".
Method: documentation only; no commands were run.
