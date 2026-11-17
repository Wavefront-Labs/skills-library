---
id: computing-software.software-engineering.ada.global-depends-contracts
name: global-depends-contracts
category: computing-software
field: software-engineering
product: ada
tags: [ada, global-depends-contracts, spark-flow]
level: advanced
status: docs-checked
description: "SPARK Global (Input, Output, In_Out, Proof_In) and Depends contracts so gnatprove checks data and information flow."
sources:
  - https://docs.adacore.com/spark2014-docs/html/lrm/
  - https://learn.adacore.com/courses/intro-to-spark/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global and Depends contracts
```ada
procedure Inc with Global => (In_Out => Counter), Depends => (Counter => Counter);
function Get return Integer with Global => (Input => Counter);
procedure Reset with Global => (Output => Counter), Depends => (Counter => null);
```
- `Global => null` means the subprogram references no global.
- Modes are `Input`, `Output`, `In_Out`, `Proof_In`; a bare list is shorthand for `Input`. `Proof_In` marks entities referenced only in assertions. A function without side effects cannot have `Output` or `In_Out`.
- Depends: `Out => (In1, In2)`; `X => null` says an output depends on no input, and `X =>+ null` is the self-dependent shorthand.
- Without a Depends aspect the default is that each output depends on every input; a tool may synthesize a more accurate relation from the body.
## Gotchas
- When a Global item is a state abstraction whose refinement is visible, `Refined_Global` must name constituents of it.
## Self-check
Remove a read variable from Depends and read the flow error.

## Checked
2026-11-03. Confirmed in the SPARK Reference Manual, Subprograms (Global and Depends aspects: mode selectors, `Global => null`, Proof_In, defaults, `null` and `=>+` forms, Refined_Global rule). Removed the claim that flow analysis requires contracts on specs (the manual says a tool may synthesize them) and the vague Initializes gotcha.
Method: documentation only; no commands were run.
