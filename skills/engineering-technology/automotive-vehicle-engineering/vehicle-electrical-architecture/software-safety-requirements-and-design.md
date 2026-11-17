---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.software-safety-requirements-and-design
name: software-safety-requirements-and-design
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [software-safety, iso-26262-part-6, freedom-from-interference, defensive-programming, misra-c, unit-verification]
level: practitioner
status: gated
description: "Apply ISO 26262-6 software practices: safety requirements, architectural principles, freedom from interference, coding rules, unit and integration verification."
sources:
  - "ISO 26262-6:2018 (software) and ISO 26262-8 tool qualification; MISRA C guidelines (misra.org.uk); confirm editions"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Software safety requirements and design

Professional practice guidance; follow ISO 26262 with your functional safety manager and assessor.

1. Software safety requirements derive from the technical safety concept: e.g. plausibility check of input within a given time, program-flow monitoring, memory integrity checks, safe state transition; each with ASIL, timing and verification criteria.
2. Architecture principles (from the standard's tables): hierarchical structure, restricted size and complexity of components, restricted size of interfaces, strong cohesion, loose coupling, appropriate scheduling, restricted use of interrupts.
3. **Freedom from interference** between software of different ASIL on the same ECU: memory protection (MPU), timing protection (OS execution budgets), controlled communication; partition QM and safety software.
4. Mechanisms: watchdog with program flow monitoring (e.g. alive, deadline and logical supervision), CRC and E2E protection of signals (AUTOSAR E2E library), RAM/ROM tests at start-up and runtime, stack monitoring, lockstep core diagnostics.
5. Coding rules: MISRA C (or C++ guidelines), no dynamic memory, no recursion, defensive programming and range checks, static analysis.
6. Verification: requirements-based unit tests with structural coverage appropriate to the ASIL (statement, branch, MC/DC; confirm the table in ISO 26262-6 (gated: unconfirmed, source is paywalled or blocked)), integration tests, fault injection tests, and resource usage tests (CPU, stack).
7. Tools: qualify or justify tools (compiler, test, code generator) per ISO 26262-8 (gated: unconfirmed, source is paywalled or blocked).
8. Traceability from safety goals through software requirements to tests.

**Gotchas:** coverage tests without checking expected values; unqualified code generators.

## Verify
- [ ] Each safety requirement has a verification case and passes.
- [ ] Freedom-from-interference measures demonstrated by a test (memory violation test).
