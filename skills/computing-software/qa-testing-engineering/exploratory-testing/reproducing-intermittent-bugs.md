---
id: computing-software.qa-testing-engineering.exploratory-testing.reproducing-intermittent-bugs
name: reproducing-intermittent-bugs
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [intermittent-bugs, bug-investigation, heisenbug, reproduction, race-conditions]
level: practitioner
status: draft
description: "Reproduce intermittent bugs: record frequency, vary one factor at a time (timing, load, data, environment), amplify with loops and stress, and capture evidence on failure."
sources:
  - https://www.istqb.org/certifications/test-analyst
  - https://rr-project.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reproducing intermittent bugs

**Goal:** turn "sometimes it fails" into a repeatable recipe, or at least enough evidence to fix it.

## First, measure
- Frequency: run N times, record failures (e.g. 3/50). Without a rate you cannot tell if a change helped.
- Collect everything per occurrence: timestamp, build, environment, user, data, request id, logs.

## Common causes and how to provoke them
| Cause | Provoke by |
|---|---|
| Race condition | add load/parallel users, CPU throttling, run on slower machine, insert delays in suspected spots |
| Timing/timeouts | throttle network (DevTools, `tc netem`), slow dependencies (toxiproxy) |
| Order/state dependence | randomise order, run after a specific other action, reuse vs fresh session |
| Data dependence | compare failing vs passing records; look at nulls, unicode, sizes, time zones |
| Time dependence | run near midnight/month end/DST change; freeze clock at those moments |
| Caching | cold vs warm cache, cache expiry boundary |
| Environment | specific node/pod/region, browser version, memory pressure |
| Resource leaks | long-running sessions, repeated actions (all-nighter) |

## Amplify
```bash
for i in $(seq 1 200); do ./run-scenario.sh || echo "fail $i"; done
npx playwright test checkout.spec.ts --repeat-each=100 --workers=8
pytest tests/test_sync.py --count=200 -x      # pytest-repeat
stress-ng --cpu 4 --timeout 300s &            # background CPU pressure
```

## Narrow down
Vary one factor at a time and track the rate. Look for correlations in logs across failures (same pod, same time window, same data). Record-and-replay debuggers (rr) help for native code.

## When you cannot reproduce
Report anyway with all occurrences, rate and conditions tried; add logging/telemetry around the suspected area so the next occurrence carries more evidence.

## Gotchas
- Debuggers and extra logging change timing (heisenbugs); prefer lightweight tracing.
- "Fixed" after a few clean runs: verify with enough runs for the original rate (3/50 needs hundreds of clean runs).

## Verify
A recipe reproduces the failure at a known rate, or the report lists rate, conditions tried and the added telemetry.
