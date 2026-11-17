---
id: computing-software.software-engineering.ada.aunit-gnattest
name: aunit-gnattest
category: computing-software
field: software-engineering
product: ada
tags: [ada, aunit-gnattest, ada-testing]
level: practitioner
status: draft
description: "Unit-test Ada with AUnit test cases and suites, generate harnesses with gnattest, run and report."
sources:
  - https://learn.adacore.com/
  - https://docs.adacore.com/gnat_ugn-docs/html/gnat_ugn/gnat_ugn.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AUnit and GNATtest
```
alr with aunit
gnattest -P app.gpr                 # creates tests/ harness with stubs
gprbuild -P tests/test_driver/test_runner.gpr && ./test_runner
```
- AUnit: derive from `AUnit.Test_Cases.Test_Case`, register routines, `AUnit.Assertions.Assert (Cond, "msg")`.
- gnattest generates a skeleton per public subprogram; fill the `Test_` bodies.
## Gotchas
- gnattest regenerates only stubs; keep hand-written tests outside generated dirs or in the marked sections.
## Self-check
Create a test for a function and make it fail on purpose.
