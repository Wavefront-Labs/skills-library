---
id: computing-software.software-engineering.ada.lemma-assume-axiomatization
name: lemma-assume-axiomatization
category: computing-software
field: software-engineering
product: ada
tags: [ada, lemma-assume-axiomatization]
level: sme
status: draft
description: "Provide proof hints: ghost lemma procedures with Annotate => Automatic_Instantiation, pragma Assume, external axiomatization."
sources:
  - https://docs.adacore.com/spark2014-docs/html/ug/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lemmas, Assume and axiomatization
```ada
procedure Lemma_Mul_Mono (X, Y, Z : Natural) with Ghost, Post => X <= Y => X*Z <= Y*Z;
pragma Annotate (GNATprove, Automatic_Instantiation, Lemma_Mul_Mono);
pragma Assume (Hyp);   -- trusted, unproven; review every use
```
- `pragma Assume` obliges you to justify the claim; audit with `--report=all`.
- `Annotate (GNATprove, False_Positive/Intentional, ...)` justifies accepted messages.
## Gotchas
- Wrong Assume statements silently unsound the analysis.
## Self-check
Replace an Assume by a proven lemma.
