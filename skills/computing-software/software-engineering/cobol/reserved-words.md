---
id: computing-software.software-engineering.cobol.reserved-words
name: reserved-words
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, reserved-words, cobol-lexical, reserved-word-clash, context-sensitive-words]
level: practitioner
status: docs-checked
description: "Avoid clashes between your data names and COBOL reserved words, and find the reserved-word list for your dialect."
sources:
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reserved words (GnuCOBOL)
**Goal:** stop "name is a reserved word" compile errors and surprise parses.
- A reserved word may be part of a longer name you create, but your own word may not exactly duplicate one (case ignored). Reserved words include intrinsic functions, mnemonic names, system routines and the other classes. Hyphenated names such as `WS-DATE` avoid clashes.
- The default list is large (over 1130 words) and covers many dialects. `-std=<dialect>` (with `-strict` variants) limits it, and `--conf=<file>` swaps the configuration.
- `cobc --list-reserved` prints the current set; `--list-intrinsics`, `--list-system` and `--list-mnemonics` print the other lists. The output depends on `-std`.
- Add or remove words with `-freserved=<word>`, `-freserved=<word>:<alias>` and `-fnot-reserved=<word>`; special registers with `-fregister=<word>` and `-fnot-register=<word>`.
- Using `FUNCTION ALL INTRINSIC` in REPOSITORY adds 100+ more reserved words.

## Gotchas
- A reserved word used as a paragraph name often gives a confusing error some lines later.
- Copybooks from other teams may use names that are reserved in your dialect; `COPY ... REPLACING` is a stopgap.

## Self-check
Run `cobc --list-reserved` with the same `-std` you compile with and search the output for every top-level name in a new program.

## Checked
2026-11-02. Checked against the GnuCOBOL Programmer's Guide (reserved words, cobc option summary, Appendix B reference). Removed: all IBM Language Reference statements and the claim that specific words like DATE, STATUS or COUNT are reserved.

Method: documentation only; no commands were run.
