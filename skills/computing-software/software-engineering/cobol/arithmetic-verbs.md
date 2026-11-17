---
id: computing-software.software-engineering.cobol.arithmetic-verbs
name: arithmetic-verbs
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, arithmetic-verbs, cobol-arithmetic, add-subtract, compute-statement, divide-remainder]
level: intro
status: docs-checked
description: "Choose between ADD/SUBTRACT/MULTIPLY/DIVIDE and COMPUTE and use GIVING, REMAINDER and CORRESPONDING forms."
sources:
  - https://www.ibm.com/docs/en/cobol-zos/6.4?topic=statements-add-statement
  - https://www.ibm.com/docs/en/cobol-zos/6.4?topic=statements-divide-statement
  - https://www.ibm.com/docs/en/cobol-zos/6.4?topic=statements-compute-statement
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ADD, SUBTRACT, MULTIPLY, DIVIDE and COMPUTE
**Goal:** write arithmetic that is clear and correctly typed (Enterprise COBOL for z/OS wording; other compilers differ in detail).

```cobol
ADD 1 TO WS-COUNT
ADD A B C GIVING WS-SUM
SUBTRACT DISC FROM PRICE GIVING NET
MULTIPLY QTY BY UNIT-PRICE GIVING LINE-AMT
DIVIDE TOTAL BY CNT GIVING AVG REMAINDER REM
COMPUTE WS-NET ROUNDED = (WS-GROSS - WS-TAX) * 0.9
```
- Without GIVING, the operands before TO are summed and added to the receiver (`ADD A TO B` updates B); with GIVING the result replaces each GIVING item and the operands are unchanged. A GIVING item can be numeric-edited.
- COMPUTE stores an arithmetic expression into one or more items and avoids the receiver restrictions of the four verbs. Operators are `+ - * / **`, each preceded and followed by a space. Evaluation order without parentheses: unary operator, then `**`, then `*` and `/`, then `+` and `-`, equal levels left to right.
- `ADD CORRESPONDING` / `SUBTRACT CORRESPONDING` operate on same-named elementary numeric items of two group items; other items are ignored.
- DIVIDE with REMAINDER: the quotient used for the remainder is truncated, not rounded; floating-point operands are not allowed with REMAINDER.
- Composite of operands is limited to 30 digits under ARITH(COMPAT) and 31 under ARITH(EXTEND).

## Gotchas
- Division by zero is a size error condition. With ON SIZE ERROR the receiver is left unchanged and your imperative runs; without it, truncation rules apply and a value is still computed, so test divisors or code ON SIZE ERROR.
- The size error condition applies to final results only, not intermediate results. When both ROUNDED and size checking apply, rounding happens first.
- Excess fraction digits are truncated unless ROUNDED is given.

## Self-check
Compute 10 / 3 into `9V99` and `9V9999`; expect 3.33 and 3.3333 (excess digits truncated unless ROUNDED).

## Checked
Date: 2026-11-08. Read the IBM docs pages for ADD, SUBTRACT, MULTIPLY, DIVIDE and COMPUTE (rendered HTML, full text) and, in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted), the sections Arithmetic operators, CORRESPONDING phrase, GIVING phrase, ROUNDED phrase and SIZE ERROR phrases. Confirmed: GIVING and CORRESPONDING semantics, the 30/31 digit composite limits, the operator list, operand spacing and precedence, REMAINDER truncation, size error rules. Trimmed: the claim that division by zero without SIZE ERROR abends "on most platforms" (IBM says truncation rules apply and a value is computed) and the claim that results are truncated only in receiving fields. Removed the unread ISO and GnuCOBOL root sources.
Method: documentation only; no commands were run.
