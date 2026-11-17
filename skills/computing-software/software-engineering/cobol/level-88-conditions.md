---
id: computing-software.software-engineering.cobol.level-88-conditions
name: level-88-conditions
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, level-88-conditions, cobol-conditions, condition-names, set-to-true, 88-level]
level: intro
status: docs-checked
description: "Replace magic values with level-88 condition names and flip them with SET ... TO TRUE."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Level-88 condition names and SET TO TRUE
**Goal:** readable flags and status checks. Rules below are from the Enterprise COBOL for z/OS 6.4 Language Reference.

```cobol
05 WS-STATE PIC X.
   88 STATE-NEW    VALUE 'N'.
   88 STATE-DONE   VALUE 'D' 'X'.
   88 STATE-ANY    VALUE 'A' THRU 'Z'
                   WHEN SET TO FALSE IS ' '.
...
SET STATE-DONE TO TRUE
IF STATE-DONE ...
SET STATE-ANY TO FALSE
```
- A level-88 entry has VALUE as its only clause and must end with a period. It must immediately follow its conditional variable (or another 88 of the same variable) and takes that variable's PICTURE characteristics.
- Values can be single literals or ranges with `THROUGH`/`THRU` (the lower literal must be less than the upper). Several values can be listed, separated by a space, comma or semicolon.
- The conditional variable can be any elementary item except another condition name, a level-66 item, or an INDEX, POINTER, PROCEDURE-POINTER, FUNCTION-POINTER or OBJECT REFERENCE item. If it needs subscripts or indexes, every reference to the condition name must supply them. Condition names may also be attached to alphanumeric, national and UTF-8 group items.
- `SET cond TO TRUE` moves the first listed literal of the VALUE clause into the conditional variable; listing several condition names in one SET behaves as separate SET statements in order.
- `SET cond TO FALSE` requires a `WHEN SET TO FALSE` phrase on that condition name; that single false value is moved to the variable. Testing the condition is false for every non-true value, not only the one named in the phrase.

## Gotchas
- With a `THRU` range or several values, SET TO TRUE uses only the first literal.
- Setting FALSE does not mean "any value outside the 88": only the one WHEN SET TO FALSE value is stored.

## Self-check
SET each condition and DISPLAY the parent; it must equal the first listed value.

## Checked
2026-11-08. Confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference PDF: condition-name VALUE clause format, Rules for condition-name entries, and Format 4 of the SET statement. Removed: the claims about ISO 2002 availability of SET TO FALSE, EVALUATE ordering with duplicate values, and numeric comparison of 88 values on `9(2)` items, none of which the sections state.
Method: documentation only; no commands were run.
