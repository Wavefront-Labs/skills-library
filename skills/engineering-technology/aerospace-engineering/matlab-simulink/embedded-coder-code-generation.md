---
id: engineering-technology.aerospace-engineering.matlab-simulink.embedded-coder-code-generation
name: embedded-coder-code-generation
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, model-based-verification, embedded-coder, code-generation, ert, sil, fixed-step-solver, slbuild]
level: practitioner
status: docs-checked
description: "Generate embedded C code from a Simulink model with Embedded Coder: fixed-step solver, ert target, data dictionary, code report and SIL equivalence check."
sources:
  - "https://www.mathworks.com/help/simulink/slref/slbuild.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Embedded code generation

**Goal:** production-style C code with verified equivalence to the model.

## Configuration
- Solver: fixed-step discrete, with the step size chosen for the target rate.
- System target file: `ert.tlc` (Embedded Coder); code interface packaging per the integration need.
- Hardware implementation: set word sizes and integer division behaviour to match the target.

## Procedure
1. `slbuild('controller')` builds the model: depending on configuration it generates code only, or generates and compiles it. With "Create code generation report" selected, a report links to the generated files.
2. Run a SIL equivalence test: the generated code executes on the host and the output is compared to the model.
3. Review report for unexpected code (for example math library calls, dynamic memory).
4. Integrate with the target build and run PIL if hardware is available.

## Gotchas
- Model Advisor checks (for example the modelling standards) should be clean before generation.
- Floating-point differences between host and target compilers need tolerance.
- For airborne software, the code generator and verification tools may need qualification; the certification plan governs.

## Verify
- [ ] SIL outputs match the model within the stated tolerance for all test cases.

## Checked
2026-11-01. Confirmed on the MathWorks slbuild page: `slbuild(mdl)` behaviour, code generation report option, `ert.tlc` as a system target file. Removed: 0.01 s step, menu path, data dictionary and storage-class advice, `sim` SIL mode, DO-330 citation (not on the page read).
Method: documentation only; no commands were run.
