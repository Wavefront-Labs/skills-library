---
id: computing-software.software-engineering.cobol.jcl-conditional-steps
name: jcl-conditional-steps
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, jcl-conditional-steps, cobol-jcl, jcl-cond, jcl-if-then-else, step-return-code]
level: practitioner
status: draft
description: "Run steps conditionally on earlier return codes with IF/THEN/ELSE and COND."
sources:
  - https://www.ibm.com/docs/en/zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# COND, IF/THEN/ELSE and return-code handling
**Goal:** branch a batch stream correctly.

```jcl
//S1 EXEC PGM=EDIT
//   IF (S1.RC <= 4) THEN
//S2 EXEC PGM=UPDATE
//   ELSE
//S3 EXEC PGM=ALERT
//   ENDIF
```
- IF/THEN/ELSE/ENDIF tests RC, ABEND, ABENDCC and `stepname.RUN` conditions.
- `COND=(4,LT)` on an EXEC means bypass this step if 4 is less than any previous step's RC (the test is inverted from intuition: the step is skipped when the condition is true). `COND=EVEN` / `COND=ONLY` control runs after an abend.
- The COBOL program sets RC via RETURN-CODE.

## Gotchas
- Prefer IF/THEN; the COND logic is read as "bypass if", which is a frequent mistake.
- A step that abends has no RC; use ABEND tests.

## Self-check
Make S1 return RC=8 and verify S3 runs, S2 is skipped.
