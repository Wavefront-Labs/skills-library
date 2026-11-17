---
id: computing-software.software-engineering.cobol.configuration-section
name: configuration-section
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, configuration-section, cobol-environment, special-names, decimal-point-comma, currency-sign]
level: practitioner
status: docs-checked
description: "Use SOURCE-COMPUTER, OBJECT-COMPUTER and SPECIAL-NAMES for decimal-comma, currency sign, mnemonic names and collating sequence."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CONFIGURATION SECTION and SPECIAL-NAMES
**Goal:** tune a program's environment without changing business logic (Enterprise COBOL for z/OS rules).

```cobol
ENVIRONMENT DIVISION.
CONFIGURATION SECTION.
SPECIAL-NAMES.
    DECIMAL-POINT IS COMMA
    CURRENCY SIGN IS 'L'
    CLASS HEX-DIGIT IS '0' THRU '9' 'A' THRU 'F'
    SYSIN IS INPUT-STREAM.
```
- The configuration section can relate environment-names to mnemonic names, set the collating sequence, set a currency sign value and symbol, swap the comma and period in PICTURE strings and numeric literals, define alphabets, symbolic characters and classes, and name classes (repository paragraph).
- `DECIMAL-POINT IS COMMA` exchanges the functions of the period and the comma in PICTURE character-strings and in numeric literals. A program called as a function must match the invoked function on this setting.
- `CURRENCY SIGN IS literal` sets the currency sign value and symbol used in PICTURE strings. Without a PICTURE SYMBOL phrase, the literal must be a single character and must not be a digit, one of A B C D E G N P R S U V X Z (either case) or space, or one of + - , . * / ; ( ) " = '. Currency symbols are case sensitive and each CURRENCY SIGN clause needs a different symbol. With `PICTURE SYMBOL literal-7`, the sign value can be several characters (for example 'EUR') and literal-7 is the one-character symbol. A CURRENCY SIGN clause overrides the CURRENCY and NOCURRENCY compiler options; with neither, `$` is the default.
- Mnemonic names tie IBM environment-names (such as SYSIN, SYSOUT, CONSOLE) to your own names.
- SOURCE-COMPUTER and OBJECT-COMPUTER are syntax checked, but only `WITH DEBUGGING MODE` (source-computer) and `PROGRAM COLLATING SEQUENCE IS alphabet-name` (object-computer) affect execution. Without the collating sequence clause, EBCDIC is used. MEMORY SIZE and SEGMENT-LIMIT are checked but have no effect.
- Do not specify the configuration section in a program contained within another program; the outer program's entries apply to it.

## Gotchas
- DECIMAL-POINT IS COMMA affects every numeric literal in the program: write `1,5` for one and a half.
- Under DECIMAL-POINT IS COMMA, the NUMVAL and NUMVAL-C argument must use a comma rather than a decimal point.
- A one-character CURRENCY SIGN literal cannot be a letter from the excluded list, so `'E'` is invalid; use PICTURE SYMBOL for a multi-character sign.

## Self-check
Compile a program with `DECIMAL-POINT IS COMMA` and a numeric-edited field such as `PIC 9.999,99`; the comma should be the decimal point and the period the separator.

## Checked
Date: 2026-11-08. Read, in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted), the Configuration section introduction, SOURCE-COMPUTER, OBJECT-COMPUTER, CURRENCY SIGN and DECIMAL-POINT IS COMMA clauses, and the NUMVAL notes by search. Corrected: the example `CURRENCY SIGN IS 'E'` is invalid on IBM (E is excluded). Removed: the claim that the 2002 standard marks SOURCE-COMPUTER and OBJECT-COMPUTER obsolete, the paragraph-order claim, and the unread ISO and GnuCOBOL sources. GnuCOBOL and ISO behaviour are not covered.
Method: documentation only; no commands were run.
