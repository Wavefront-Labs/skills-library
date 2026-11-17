---
id: computing-software.software-engineering.ada.loop-invariants-variants
name: loop-invariants-variants
category: computing-software
field: software-engineering
product: ada
tags: [ada, loop-invariants-variants, spark-proof]
level: advanced
status: docs-checked
description: "Write Loop_Invariant, Loop_Variant and Assert in SPARK so provers handle loops; preserve facts across iterations."
sources:
  - https://docs.adacore.com/spark2014-docs/html/ug/
  - https://learn.adacore.com/courses/intro-to-spark/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loop invariants and variants
```ada
for I in A'Range loop
   pragma Loop_Invariant (for all J in A'First .. I - 1 => A (J) = 0);
   A (I) := 0;
end loop;
```
- A loop invariant is a Boolean expression true at every iteration; GNATprove checks it holds in the first iteration, then in an arbitrary iteration assuming it held in the previous one (proof by induction). It can also be checked at run time with assertions enabled.
- `pragma Loop_Variant` can be used to ensure termination of loops.
- `pragma Assert` statements can guide the prover.
## Gotchas
- A too-weak invariant leaves later checks (e.g. a postcondition) unproved; GNATprove reports when the invariant is not proved in the first iteration.
## Self-check
Prove a zeroing loop, then delete the invariant and see checks fail.

## Checked
2026-11-03. Confirmed in Introduction to SPARK (Proof of Functional Correctness: loop invariants and proof by induction, `pragma Assert`) and the SPARK Reference Manual (`pragma Loop_Variant` for termination). Removed `Increases =>` syntax and the frame-condition claims (not on the pages read).
Method: documentation only; no commands were run.
