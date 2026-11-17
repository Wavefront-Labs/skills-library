---
id: computing-software.software-engineering.cobol.user-defined-names
name: user-defined-names
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, user-defined-names, cobol-lexical, name-qualification, of-in-qualifier]
level: intro
status: docs-checked
description: "Choose valid Enterprise COBOL data, paragraph and file names (30 bytes, hyphens, letters) and disambiguate duplicates with OF/IN qualification."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rules for user-defined names and qualification
**Goal:** name things so they compile under IBM Enterprise COBOL for z/OS 6.4 (other compilers differ; check theirs).

- A COBOL word is built from A-Z, a-z, 0-9, hyphen and underscore. The hyphen cannot be the first or last character; the underscore cannot be the first.
- The maximum length of a user-defined word is 30 bytes (except level-numbers and priority-numbers, which are one or two digits).
- Most user-defined words must contain at least one alphabetic character; the exceptions are section-names, paragraph-names, priority-numbers and level-numbers.
- Lowercase and uppercase single-byte letters are equivalent in COBOL words (not inside literals).
- A reserved word cannot be used as a user-defined word.
- A given user-defined word belongs to one set only (data-name, file-name, condition-name, paragraph-name and so on), and each word within a set must be unique, except as qualification allows.
- The same data name may appear under different groups; qualify with `OF` or `IN` (logically equivalent):
```cobol
01 OLD-REC.  05 CUST-ID PIC 9(6).
01 NEW-REC.  05 CUST-ID PIC 9(6).
MOVE CUST-ID OF OLD-REC TO CUST-ID OF NEW-REC
```
- Qualifiers must be higher-level names in the same hierarchy; you need only enough of them to make the name unique (more is allowed but unnecessary). A name in a REDEFINES clause must not be qualified.
- Level-01 and level-77 names cannot be qualified, so they must be unique if referenced.
- A paragraph-name can be qualified only by its section-name (`PARA-A OF SEC-1`, without the word SECTION).
- `FILLER` (or omitting the name) marks an item that is not explicitly referred to in the program.

## Gotchas
- Heavy reliance on duplicate names plus MOVE CORRESPONDING hides bugs (FILLER items are ignored by CORRESPONDING); prefer prefixes (`OLD-`, `NEW-`) in new code.
- The QUALIFY(EXTEND) compiler option relaxes the qualification rules for a name with a single 01 level; do not depend on it across shops.

## Self-check
Compile and confirm there are no diagnostics for names that are too long, start or end with a hyphen, or are ambiguous references.

## Checked
2026-11-08. Confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference (Chapter 3 COBOL words and user-defined words; Chapter 8 Referencing data names, Qualification, References to PROCEDURE DIVISION names; Chapter 24 level-77 and 01 qualification; DATA DESCRIPTION FILLER): 30-byte limit, permitted characters, hyphen and underscore rules, alphabetic-character rule and its exceptions, case equivalence, OF/IN equivalence, qualification rules, paragraph qualification. Removed: the claim of 31 characters on IBM (the manual says 30), the ISO 63-character claim, the `cobc -Xref` self-check, and ISO/GnuCOBOL generalisations the manual does not state.
Method: documentation only; no commands were run.
