---
id: computing-software.firmware-embedded-development.freertos.rate-monotonic-priority-assignment
name: rate-monotonic-priority-assignment
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-scheduler, rate-monotonic, deadline-monotonic, response-time-analysis, schedulability, task-priority, freertos, firmware-embedded-development]
level: advanced
status: draft
description: "Assign FreeRTOS task priorities by rate-monotonic or deadline-monotonic rules and check schedulability with the utilisation bound and response-time analysis."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book
  - https://doi.org/10.1145/321738.321743
  - https://www.cs.york.ac.uk/rts/books/RTSBookFourthEdition.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rate-monotonic priority assignment

**Rule:** for periodic tasks with deadline = period, give **shorter period = higher priority**.
Liu and Layland (1973) proved this is optimal among fixed-priority schemes: if any fixed
priority order meets all deadlines, rate-monotonic does. When deadline < period, use
**deadline-monotonic** (shorter deadline = higher priority).

## Step 1: build the task table
| Task | Period T | WCET C | Deadline D | U = C/T |
|---|---|---|---|---|
| motor_ctrl | 1 ms | 0.2 ms | 1 ms | 0.20 |
| sensor | 10 ms | 1.5 ms | 10 ms | 0.15 |
| comms | 20 ms | 4 ms | 20 ms | 0.20 |
| ui | 100 ms | 10 ms | 100 ms | 0.10 |

Use **measured** worst-case execution times (GPIO/DWT timing under worst-case load, plus margin).
Average times are useless here.

## Step 2: quick utilisation test
Sufficient (not necessary) bound: `U_total <= n(2^(1/n) - 1)`.
n=1: 1.0, n=2: 0.828, n=3: 0.780, n=4: 0.757, n to infinity: 0.693.
Example: U = 0.65 <= 0.757, so it is schedulable. Above the bound it may still be schedulable;
do step 3.

## Step 3: response-time analysis (exact for this model)
For task i, iterate until R stops changing:
```
R_i = C_i + B_i + sum over higher-priority j of ceil(R_i / T_j) * C_j
```
Start with R_i = C_i. Schedulable if R_i <= D_i. `B_i` = longest blocking by a lower-priority
task holding a mutex task i needs (with priority inheritance, the longest critical section).
Example, comms: R = 4 -> 4 + ceil(4/1)*0.2 + ceil(4/10)*1.5 = 6.3 -> 4 + 7*0.2 + 1.5 = 6.9 ->
4 + 7*0.2 + 1.5 = 6.9. 6.9 ms <= 20 ms, so it passes.

## Mapping to FreeRTOS
- Highest RM rank = highest numeric priority (FreeRTOS: larger number = higher priority,
  unlike NVIC).
- Use distinct priorities for periodic tasks; equal priorities make the analysis
  depend on time slicing.
- Implement each task with `xTaskDelayUntil` (see periodic-tasks-with-vtaskdelayuntil).
- **ISRs** run above all tasks: add each ISR as a highest-priority "task" with its own C and
  minimum inter-arrival time T. Include the tick ISR and the timer daemon if its callbacks matter.
- Aperiodic/background tasks (logging, UI) go below all periodic ones, or are modelled as
  sporadic tasks with a minimum inter-arrival time.
- Kernel overhead: add context switch cost (about 2x switch time per job) to each C.

## Verify
- [ ] Task table with measured WCETs is kept in the repo and updated when code changes.
- [ ] RTA spreadsheet/script passes for every task including ISR load and blocking terms.
- [ ] On target, a deadline-miss monitor (xTaskDelayUntil returning pdFALSE) stays at zero under worst-case load.
