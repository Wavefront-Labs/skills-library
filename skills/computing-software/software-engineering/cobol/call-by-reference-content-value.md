---
id: computing-software.software-engineering.cobol.call-by-reference-content-value
name: call-by-reference-content-value
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, call-by-reference-content-value, call-statement, cobol-subprograms, by-value, returning]
level: intro
status: docs-checked
description: "Pass parameters with the right mechanism and understand who can change what."
sources:
  - https://www.ibm.com/docs/en/cobol-zos/6.4?topic=statements-call-statement
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CALL BY REFERENCE, BY CONTENT and BY VALUE
**Goal:** pass data without surprise side effects (Enterprise COBOL for z/OS rules).

```cobol
CALL 'CALCTAX' USING BY REFERENCE WS-AMOUNT
                     BY CONTENT   WS-RATE
                     BY VALUE     WS-FLAG-N
                     RETURNING    WS-RESULT
    ON EXCEPTION PERFORM NO-MODULE
END-CALL
```
- BY REFERENCE (assumed before the first parameter if none is given): the caller's data item occupies the same storage as the callee's, so changes are visible to the caller.
- BY CONTENT: the callee cannot change the argument as the caller sees it; changes to the parameter in the callee do not affect the caller's argument. Literals and figurative constants (except ALL literal and NULL/NULLS) are allowed.
- BY VALUE: the value is passed, not a reference, and the callee works on a temporary copy. Meant mainly for non-COBOL callees such as C but allowed COBOL to COBOL if both the CALL and the callee's PROCEDURE DIVISION USING specify BY VALUE. Allowed items include binary (BINARY, COMP, COMP-4, COMP-5), COMP-1/COMP-2, pointers and one single-byte alphanumeric character; a fixed-point numeric literal must have nine or fewer digits.
- A BY CONTENT / BY REFERENCE / BY VALUE phrase applies to the parameters that follow it until another is coded.
- `RETURNING` stores the called program's return value in the named item; a COBOL callee must code RETURNING on its PROCEDURE DIVISION header with matching PICTURE, USAGE, SIGN, SYNCHRONIZE, JUSTIFIED and BLANK WHEN ZERO clauses, and must initialize it before using it. CALL ... RETURNING does not set RETURN-CODE.
- `ON EXCEPTION` runs when the called program cannot be made available; `ON OVERFLOW` has the same effect.

## Gotchas
- The number of operands in the CALL USING and the callee's USING must be identical and are matched by position; the callee's items must describe the same number of character positions as the caller's.
- A LINKAGE SECTION or FILE SECTION item used as an argument needs addressability first (SET ADDRESS OF or being a PROCEDURE DIVISION USING parameter).

## Self-check
Pass a counter BY REFERENCE and BY CONTENT to a routine that adds 1; only the BY REFERENCE one changes.

## Checked
Date: 2026-11-08. Read the whole IBM docs CALL statement page (Enterprise COBOL for z/OS 6.4): the USING, BY REFERENCE, BY CONTENT, BY VALUE, RETURNING, ON EXCEPTION and END-CALL sections. Confirmed the phrase scope rule, default, copy semantics, permitted BY VALUE items, nine-digit literal limit, RETURNING matching rules and RETURN-CODE note. Removed as unconfirmed: "(2002+/IBM)" for RETURNING, ABI size wording, the claim that literals passed BY REFERENCE are passed by content on many compilers, and the statement that PICTURE/USAGE mismatches are never checked. Removed the unread ISO and GnuCOBOL root sources; GnuCOBOL behaviour is not covered.
Method: documentation only; no commands were run.
