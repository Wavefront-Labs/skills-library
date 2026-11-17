---
id: computing-software.software-engineering.ada.spark-mode-subset
name: spark-mode-subset
category: computing-software
field: software-engineering
product: ada
tags: [ada, spark-mode-subset, spark-intro]
level: practitioner
status: docs-checked
description: "Mark Ada code SPARK_Mode, know the main SPARK restrictions (exceptions, access types, backward goto, controlled types) and per-part On/Off placement."
sources:
  - https://docs.adacore.com/spark2014-docs/html/lrm/
  - https://learn.adacore.com/courses/intro-to-spark/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPARK_Mode and the SPARK subset
```ada
package Acc with SPARK_Mode is ... end Acc;
package body Acc with SPARK_Mode => Off is ... end;   -- hide non-SPARK body
```
- The most notable restrictions relate to exceptions and access types; backward `goto` and controlled types are unsupported; others concern side effects in expressions and aliasing. Access types are allowed with ownership: assignment transfers ownership and only benign aliasing is allowed.
- `SPARK_Mode => Off` on the body lets the spec be analysed while the body uses full Ada.
- SPARK_Mode can be set On or Off on the visible and private parts of a spec and the declarative and statement parts of a body; once Off, it cannot be switched On again in the same part.
- Check conformance: `gnatprove -P proj.gpr --mode=check` (`check_all` is the full check).
## Gotchas
- Switching SPARK_Mode back On after Off within the same part is rejected.
## Self-check
Add a controlled type inside a SPARK_Mode body and read the diagnostic.

## Checked
2026-11-03. Confirmed in Introduction to SPARK (Overview: restrictions, ownership, SPARK_Mode granularity) and the SPARK User's Guide (`--mode=check`, `check_all`). Removed tasking limits and the spec/body consistency claim (not on the pages read) and the specific statement about exception handlers.
Method: documentation only; no commands were run.
