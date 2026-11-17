---
id: computing-software.software-engineering.cobol.class-condition-names
name: class-condition-names
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, class-condition-names, special-names, class-clause, alphabet-clause, symbolic-characters]
level: advanced
status: docs-checked
description: "Define user classes, alphabets and symbolic characters in SPECIAL-NAMES for validation and collating."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CLASS, ALPHABET and SYMBOLIC CHARACTERS
**Goal:** declare reusable character sets once (Enterprise COBOL for z/OS rules).

```cobol
SPECIAL-NAMES.
    CLASS VALID-ID IS 'A' THRU 'Z' '0' THRU '9'
    SYMBOLIC CHARACTERS SEP-CH IS 10
    ALPHABET MY-SEQ IS EBCDIC.
...
IF WS-ID IS VALID-ID ...
```
- The clauses of SPECIAL-NAMES can appear in any order, and the paragraph ends with a period after the last clause.
- `CLASS name IS ...` defines the exclusive set of characters of the class; the name can be used only in a class condition: `IF field IS name` or `IS NOT name`. The tested identifier must be USAGE DISPLAY. Literals are numeric (unsigned integers giving ordinal positions) or alphanumeric; `THRU` ranges may run ascending or descending, and a literal with a THRU must be one character.
- `SYMBOLIC CHARACTERS` names single characters by ordinal position, numbered from 1, so `IS 10` is the 10th character of the native character set, not byte value 10. With an `IN alphabet-name` phrase the position refers to that alphabet. Each symbolic character needs a matching integer and must contain at least one letter.
- `ALPHABET name IS` NATIVE, STANDARD-1 (ASCII), STANDARD-2 (ISO/IEC 646), EBCDIC, or a list of literals. The name can then be a collating sequence in the PROGRAM COLLATING SEQUENCE clause or the COLLATING SEQUENCE phrase of SORT and MERGE, or a character code set in CODE-SET and SYMBOLIC CHARACTERS. Alphabets apply to alphanumeric data only, not DBCS or national.
- In a literal list, characters you do not name sort after those you do; THROUGH and ALSO assign ranges or equal positions.

## Gotchas
- A class condition is true only if the whole item consists of characters in the class, so trailing spaces fail the test unless SPACE is in the class.
- The CLASS, SYMBOLIC CHARACTERS and ALPHABET clauses cannot be used in a function prototype definition.

## Self-check
Test a value with one illegal character and one with all legal characters; only the second satisfies the class.

## Checked
Date: 2026-11-08. Read, in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted), the SPECIAL-NAMES paragraph format, the ALPHABET, CLASS and SYMBOLIC CHARACTERS clauses in full, and the Class condition section. Confirmed every bullet. Resolved the earlier hedge on SYMBOLIC CHARACTERS: positions are numbered from 1. Removed: the claim that using an alphabet for comparisons changes sort order (replaced with the documented SORT/MERGE and PROGRAM COLLATING SEQUENCE uses), the name TAB-CH in the example (the page does not say which character position 10 is), and the unread ISO source. GnuCOBOL and ISO behaviour are not covered.
Method: documentation only; no commands were run.
