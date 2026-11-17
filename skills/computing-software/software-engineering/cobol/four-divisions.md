---
id: computing-software.software-engineering.cobol.four-divisions
name: four-divisions
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, four-divisions, cobol-structure, division-order, identification-division, procedure-division]
level: intro
status: draft
description: "Lay out a COBOL program in its four divisions, in the required order, with the minimum entries that compile."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Identification, Environment, Data and Procedure divisions
**Goal:** write a correct skeleton and know what each division owns.

Order is fixed: IDENTIFICATION, ENVIRONMENT, DATA, PROCEDURE. ENVIRONMENT and DATA may be omitted if empty; PROCEDURE is needed for an executable program.
```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. HELLO.
ENVIRONMENT DIVISION.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 WS-MSG PIC X(12) VALUE 'HELLO, WORLD'.
PROCEDURE DIVISION.
MAIN-PARA.
    DISPLAY WS-MSG
    STOP RUN.
```
- Identification: PROGRAM-ID (required), optional AUTHOR/DATE-WRITTEN paragraphs (obsolete in the 2002+ standard; compilers still accept them).
- Environment: CONFIGURATION and INPUT-OUTPUT sections (files, special names).
- Data: FILE, WORKING-STORAGE, LOCAL-STORAGE, LINKAGE sections.
- Procedure: sections, paragraphs, sentences, statements.

## Gotchas
- A sentence ends at a period; a stray period inside an IF ends the IF early. Prefer scope terminators (END-IF) and a single period per paragraph.
- Division headers need the period after the word DIVISION; sections need SECTION. too.

## Self-check
Compile the skeleton (`cobc -x hello.cob` with GnuCOBOL, or your z/OS compile proc) and run it; it must print the message with no warnings.
