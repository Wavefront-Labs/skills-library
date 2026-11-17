---
id: computing-software.software-engineering.cobol.paragraph-section-structure
name: paragraph-section-structure
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, paragraph-section-structure, cobol-control-flow, paragraph-naming, section-performs, fall-through, exit-paragraph]
level: practitioner
status: docs-checked
description: "Organize the procedure division in numbered paragraphs, avoid fall-through, and use EXIT paragraphs correctly."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Paragraphs, sections, fall-through and EXIT
**Goal:** a layout that is easy to read and to PERFORM.

```cobol
0000-MAIN.
    PERFORM 1000-INIT
    PERFORM 2000-PROCESS UNTIL AT-EOF
    PERFORM 3000-TERM
    GOBACK.
1000-INIT.
    ...
2000-PROCESS.
    ...
2000-EXIT.
    EXIT.
```
- Execution begins at the first statement of the PROCEDURE DIVISION (declaratives excluded) and statements run in source order unless a statement redirects it; a paragraph ends only at the next paragraph-name or section header, so control falls into the next paragraph unless a GOBACK/STOP RUN/GO TO stops it. Put the main logic in a driver paragraph that ends with GOBACK.
- Number paragraphs in ascending order that reflects call hierarchy; one exit paragraph per THRU range.
- A section is a section-header followed by optional paragraphs and ends before the next section header. PERFORM of a section returns after the last statement of its last paragraph; PERFORM a THRU b returns after the last statement of b (or of b's last paragraph if b is a section).
- Declaratives require the whole PROCEDURE DIVISION to be divided into sections. SORT INPUT/OUTPUT PROCEDURE names a section or a paragraph (a first and optional last procedure-name), so sections are not required for SORT.
- Paragraphs need not be inside sections, and paragraph-names are not required at all when there are no declaratives.
- Format 1 `EXIT` is treated as CONTINUE and only gives a procedure-name an end point. In Enterprise COBOL 6.4 `EXIT PARAGRAPH` and `EXIT SECTION` leave the current paragraph or section without running its remaining statements (`EXIT SECTION` only inside a section), and `EXIT PERFORM [CYCLE]` leaves an inline PERFORM (ignored outside one).

## Gotchas
- A paragraph name is also a label: renaming breaks GO TO and PERFORM THRU ranges.
- A paragraph-name used in a reference must not be duplicated within its section; a section-name must be unique in the program. Paragraph and section names cannot be referenced from another program.
- Code placed after the last PERFORM'd paragraph runs by fall-through when you meant to stop.

## Self-check
Add a distinct DISPLAY in each paragraph and confirm the execution order matches the call tree.

## Checked
2026-11-08: confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference: "Procedures" and "Declaratives" (Procedure division structure), PERFORM return points, SORT INPUT PROCEDURE, EXIT statement formats 1, 5 and 6, and paragraph-name qualification rules. Removed the claim that sections are required for SORT procedures and the "verify" hedge on EXIT PARAGRAPH/SECTION. GnuCOBOL behaviour was not checked.
Method: documentation only; no commands were run.
