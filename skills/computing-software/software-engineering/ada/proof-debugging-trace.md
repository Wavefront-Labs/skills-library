---
id: computing-software.software-engineering.ada.proof-debugging-trace
name: proof-debugging-trace
category: computing-software
field: software-engineering
product: ada
tags: [ada, proof-debugging-trace]
level: advanced
status: docs-checked
description: "Diagnose unproved SPARK checks with GNATprove: classify the cause, run the code with assertions, add contracts, narrow with --limit-line, raise --level."
sources:
  - https://docs.adacore.com/spark2014-docs/html/ug/en/source/how_to_investigate_unproved_checks.html
  - https://docs.adacore.com/spark2014-docs/html/ug/en/source/how_to_run_gnatprove.html
  - https://docs.adacore.com/spark2014-docs/html/ug/en/source/how_to_view_gnatprove_output.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging unproved checks
```
gnatprove -P p.gpr --level=3 --info -u f.adb
gnatprove -P p.gpr --limit-line=f.adb:42
```
The SPARK User's Guide (section 7.8) classifies an unproved check as: [CODE] the code is wrong, [ASSERT] the assertion is wrong, [SPEC] a needed annotation is missing, [MODEL] a GNATprove modelling limit, [TIMEOUT] the prover timed out, or [PROVER] the prover is not smart enough. Work through them in that order.
1. CODE or ASSERT: run the program on representative inputs with `-gnata` (check assertions at run time), `-gnato` (check intermediate overflows) and `-gnat-p` (re-enable checks if `-gnatp` suppressed them).
2. SPEC: the usual culprits are a weak precondition of the enclosing subprogram, a weak postcondition of a called subprogram, or a weak loop invariant (the enclosing loop or an earlier loop). GNATprove does not look into subprogram bodies, so everything a caller needs must be in the contracts. It may print `possible fix:` lines naming a precondition, loop invariant or postcondition. GNAT Studio can display the path on which the proof failed, and a counterexample may be generated on the path. Inserting smaller assertions at intermediate points helps tell an unprovable property from a prover shortcoming; keep only the ones that help the automatic proof.
3. MODEL: floating-point elementary operations (square root, trigonometry) and the `Value` and `Image` attributes may give checks that are true but unprovable; `--info` emits a warning for most such imprecisely supported features. `pragma Assume` can supply the missing fact.
4. TIMEOUT/PROVER: raise `--level` (0 to 4). Level 0 suits only simple proofs; levels 1 to 4 try the provers cvc5, z3 and altergo (level 1 timeout 1 s, 2 is 5 s, 3 is 20 s, 4 is 60 s; counterexamples on from level 2). `--level` is shorthand for combinations of `--timeout`, `--prover`, `--memlimit`, `--steps` and `--counterexamples`, which can be set individually.
- Raising limits only helps if the message says a limit was reached (provers reached time limit); if it says the provers gave up before completing the proof, try a different prover or strategy.
- Provers handle floating-point, non-linear arithmetic (multiplication, division, modulo, exponentiation) and induction poorly; for induction use a lemma from the SPARK lemma library, a user lemma, an assumption, or a justification with `pragma Annotate`.
- Narrowing: `-u file` analyses only the units containing the given files; `--limit-line=file:line` proves only that line; `--limit-region=file:first:last` a range of lines. In GNAT Studio use SPARK > Prove Line or Prove Subprogram.
- `--info` also reports loops that could not be unrolled or subprograms that could not be analysed contextually.
- With `-d`, GNATprove keeps its proof files under the `gnatprove` subdirectory of the object directory (name pattern `<file>_<line>_<column>_<check>_<num>.<ext>`, Why3 format for Alt-Ergo and SMTLIB2 for cvc5).
## Gotchas
- Raising `--level` without adding the contracts the proof needs only burns time.
## Self-check
Fix an unproved range check by adding a precondition and re-run until it proves.

## Checked
Checked against the SPARK 2014 User's Guide pages "How to Investigate Unproved Checks", "How to Run GNATprove" and "How to View GNATprove Output".
Removed: `--proof-warnings` (not found in the pages read), the "check order" list as written before (replaced by the guide's own classification), and the cvc4 note.
Method: docs-only read of cited pages, 2026-11-08
