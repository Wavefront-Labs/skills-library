---
id: computing-software.software-engineering.ada.adoption-levels
name: adoption-levels
category: computing-software
field: software-engineering
product: ada
tags: [ada, adoption-levels, spark-levels]
level: practitioner
status: draft
description: "Plan SPARK adoption: Stone (subset), Bronze (flow), Silver (AoRTE proof), Gold (functional contracts); what each requires."
sources:
  - https://docs.adacore.com/spark2014-docs/html/ug/
  - https://learn.adacore.com/courses/intro-to-spark/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stone, Bronze, Silver, Gold adoption levels
- Stone: code conforms to the SPARK subset (`SPARK_Mode`).
- Bronze: flow analysis clean, no uninitialised data, correct Global/Depends.
- Silver: absence of run-time errors proven.
- Gold: key functional properties proven via contracts.
- Platinum: full functional correctness (the user guide names it; scope varies).
Progress by module: raise `--level` and add contracts only where risk justifies.
## Gotchas
- Mix: SPARK_Mode on critical packages, plain Ada elsewhere.
## Self-check
State the level a given package reaches given gnatprove output.
