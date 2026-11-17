---
id: computing-software.software-engineering.cobol.cobol-input-validation
name: cobol-input-validation
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, cobol-input-validation, cobol-security, input-validation, bounds-checking, numeric-validation, buffer-overflow]
level: advanced
status: draft
description: "Validate every external field before use and keep subscripts, reference modifications and lengths in range."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Input validation, bounds checking and numeric safety
**Goal:** untrusted data cannot corrupt storage or logic.

- Validate before arithmetic: `IF fld IS NUMERIC`, then range checks, then use; use `FUNCTION TEST-NUMVAL` for text.
- Check lengths before ref-mod and before STRING/UNSTRING; use `ON OVERFLOW`.
- Subscripts: check `WS-I >= 1 AND <= table-count` explicitly; do not rely on `SSRANGE`/`-debug` in production.
- Variable-length records: trust `RECORD VARYING ... DEPENDING ON` length only after testing it against the maximum.
- CALL interfaces: validate lengths in parameters; never trust caller-supplied length > buffer.
- Use level-88 whitelists (`88 VALID-TYPE VALUES 'A' 'B' 'C'`).
- Log rejects with record keys, not full sensitive data.

## Gotchas
- COBOL has no automatic bounds checking by default: overruns silently corrupt adjacent storage.
- Pointers from `SET ADDRESS OF` bypass all checks.

## Self-check
Feed deliberately oversized and non-numeric inputs and confirm clean rejection, not abends.
