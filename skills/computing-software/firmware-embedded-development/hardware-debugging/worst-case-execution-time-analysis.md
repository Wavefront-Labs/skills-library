---
id: computing-software.firmware-embedded-development.hardware-debugging.worst-case-execution-time-analysis
name: worst-case-execution-time-analysis
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [timing-analysis, wcet, response-time-analysis, measurement-based-timing, static-timing-analysis, ait, rapita, schedulability, firmware-embedded-development]
level: sme
status: draft
description: "Establish worst-case execution and response times for real-time firmware: measurement-based WCET with stress inputs and margins, static analysis tools, and schedulability checks."
sources:
  - https://www.absint.com/ait/
  - https://www.rapitasystems.com/products/rapitime
  - https://www.cs.york.ac.uk/rts/books/RTSbookFourthEdition.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Worst-case execution time (WCET) analysis

**Goal:** an evidence-backed upper bound for how long each task/ISR can take, and proof that
all deadlines are met when everything happens at once.

## Two approaches
| | Measurement-based (MBTA) | Static analysis |
|---|---|---|
| How | run on target with worst-case inputs, record max (DWT, trace) | analyse binary + processor model, compute bound for all paths |
| Pros | real hardware, easy | safe bound without needing worst input |
| Cons | may miss the true worst path; need margin | needs tool support for your exact core/memory; pessimistic with caches |
| Tools | DWT/trace, RapiTime (hybrid), Tracealyzer | AbsInt aiT (Cortex-M, PowerPC, ...), OTAWA, Bound-T |
Safety standards (DO-178C, ISO 26262) accept either with justification; certification work
often uses hybrid tools.

## Measurement-based procedure
1. Identify the timing-critical code and its inputs.
2. Drive **path coverage**: inputs that exercise every branch, maximum loop iterations,
   error-handling paths, largest buffers. Code coverage tools (gcov on target, ETM coverage)
   show which paths were measured.
3. Create worst-case **system conditions**: caches flushed/cold, flash wait states, DMA and
   other bus masters active, highest interrupt load.
4. Record the **high-water mark** over long runs (hours), not a single run.
5. Add an engineering margin (commonly 20-50 %) for unobserved paths.

## Response time analysis (fixed-priority)
For task i with WCET C_i, period T_i, higher-priority set hp(i) and blocking B_i (longest
critical section/lower-priority mutex hold):
```
R_i = C_i + B_i + sum_{j in hp(i)} ceil(R_i / T_j) * C_j      (iterate to a fixed point)
```
Deadline met if R_i <= D_i. Include ISRs as highest-priority "tasks" and RTOS overhead (tick,
context switch). Utilisation bound check (rate-monotonic, U <= n(2^(1/n)-1)) is a quick sanity
test only.

## Make code analysable
Bounded loops (annotate maximum iterations), no recursion, no unbounded dynamic allocation in
time-critical paths, avoid data-dependent algorithms with huge variance (or bound them).

## Verify
- [ ] WCET table per task/ISR with method, conditions and margin.
- [ ] Response-time analysis shows all deadlines met; spreadsheet or script kept with the code.
- [ ] Re-measured after significant code or compiler changes.
