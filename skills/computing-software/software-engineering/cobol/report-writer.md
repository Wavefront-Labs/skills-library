---
id: computing-software.software-engineering.cobol.report-writer
name: report-writer
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, report-writer, cobol-report, report-section, rd-entry, generate-statement]
level: advanced
status: draft
description: "Describe reports declaratively with RD/TYPE entries and drive them with INITIATE, GENERATE and TERMINATE."
sources:
  - https://www.iso.org/
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Report Writer module (RD, TYPE IS, GENERATE)
**Goal:** produce control-break reports without hand-coded totals.

```cobol
REPORT SECTION.
RD  SALES-RPT
    CONTROLS ARE FINAL, DEPT
    PAGE LIMIT 60 HEADING 1 FIRST DETAIL 5 LAST DETAIL 55.
01  TYPE PAGE HEADING.
    05 LINE 1 COLUMN 20 PIC X(12) VALUE 'SALES REPORT'.
01  DETAIL-LINE TYPE DETAIL.
    05 LINE PLUS 1 COLUMN 1 PIC X(10) SOURCE EMP-NAME.
    05 COLUMN 20 PIC ZZZ,ZZ9 SOURCE EMP-SALES.
01  TYPE CONTROL FOOTING DEPT.
    05 LINE PLUS 2 COLUMN 20 PIC ZZZ,ZZ9 SUM EMP-SALES.
```
Procedure: `INITIATE SALES-RPT`, `GENERATE DETAIL-LINE` per record, `TERMINATE SALES-RPT`.
- Report Writer is part of the ISO standard and GnuCOBOL support is partial/evolving. IBM Enterprise COBOL for z/OS does not include Report Writer (older VS COBOL II/OS/VS had it); unconfirmed for the very latest release.

## Gotchas
- Control fields must change in the stated hierarchy order.
- On IBM, hand-code control breaks (see the control-break skill).

## Self-check
Generate a report over a sorted file with two departments and verify each department total equals the sum of its detail lines.
