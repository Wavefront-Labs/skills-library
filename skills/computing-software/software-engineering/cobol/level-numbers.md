---
id: computing-software.software-engineering.cobol.level-numbers
name: level-numbers
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, level-numbers, cobol-data-description, level-77, group-items, elementary-items]
level: intro
status: docs-checked
description: "Build record layouts with group and elementary items using level numbers 01-49 and the special levels 66, 77 and 88."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Level numbers 01-49, 66, 77 and 88
**Goal:** read and write hierarchical data definitions (Enterprise COBOL for z/OS 6.4).

```cobol
01 CUSTOMER-REC.
   05 CUST-ID        PIC 9(6).
   05 CUST-NAME.
      10 FIRST-NAME  PIC X(15).
      10 LAST-NAME   PIC X(20).
   05 CUST-STATUS    PIC X.
      88 ACTIVE      VALUE 'A'.
77 WS-COUNT          PIC 9(4) COMP.
```
- A level number is a one- or two-digit integer 01-49, or 66, 77, 88. 01 and 77 must start in Area A; 02-49 may start in Area A or B.
- 01 is the most inclusive record level. Less inclusive items get higher, not necessarily consecutive, numbers. A group includes every following item until a level number less than or equal to the group's own appears. Items at the same depth may use different numbers (05 and 04 under one 01); the compiler renumbers them relatively.
- 77: an independent item in WORKING-STORAGE, LOCAL-STORAGE or LINKAGE, not subdivided. 66: regrouping item that must carry a RENAMES clause. 88: condition-name tied to values of a conditional variable.
- 01 and 77 names cannot be qualified, so those referenced must be unique; subordinate names must be unique or qualified.
- Indentation is documentation only.

## Gotchas
- A group move (an alphanumeric group as sender or receiver) acts like an alphanumeric-to-alphanumeric move with no conversion, ignoring the elementary items inside. Moving a group holding packed or binary fields into a DISPLAY layout does not convert them.
- A VALUE on a group initializes the whole group area without regard to subordinates; subordinate entries then must not have VALUE, and all items under an alphanumeric group with VALUE must be USAGE DISPLAY.
- A level-66 entry cannot rename another 66, nor a 01, 77 or 88.

## Self-check
Compile with the compiler's data map listing (see the Programming Guide for the option) and compare offsets and total length with the intended record length.

## Checked
2026-11-08. Confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference (Chapter 24 Levels of data in a record description entry, Special level-numbers, Indentation; Chapter 26 data description entry formats and VALUE clause; Group moves; Area A rules). Removed: "step levels by 4 or 5" advice, the claim that groups are "always alphanumeric" (national and UTF-8 groups exist), the specific MAP/LIST/XREF and `cobc -t` option claims (Programming Guide and GnuCOBOL docs not read), and the ISO source.
Method: documentation only; no commands were run.
