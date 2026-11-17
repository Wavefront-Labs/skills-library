---
id: computing-software.qa-testing-engineering.exploratory-testing.system-usability-scale-and-usability-metrics
name: system-usability-scale-and-usability-metrics
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [system-usability-scale, usability-metrics, sus, task-success-rate, usability-testing]
level: practitioner
status: draft
description: "Measure usability with SUS questionnaires, task success, time on task and error rate; score SUS correctly and interpret it against the 68 benchmark."
sources:
  - https://www.usability.gov/how-to-and-tools/methods/system-usability-scale.html
  - https://measuringu.com/sus/
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SUS and usability metrics

**Goal:** turn usability sessions into comparable numbers alongside the qualitative findings.

## Core metrics (ISO 9241-11: effectiveness, efficiency, satisfaction)
- **Task success rate:** completed without help / attempted. Define success criteria before sessions.
- **Time on task:** median, not mean (skewed); successful attempts only.
- **Error rate:** slips and mistakes per task.
- **Satisfaction:** SUS after the session, or the single ease question (SEQ, 1-7) after each task.

## SUS scoring
Ten statements, 1 (strongly disagree) to 5 (strongly agree), alternating positive (odd) and negative (even).
- Odd items: score - 1. Even items: 5 - score.
- Sum the ten contributions (0-40) and multiply by 2.5 to get 0-100.

```python
def sus(r):  # r = list of 10 responses 1..5
    return 2.5 * sum((x - 1) if i % 2 == 0 else (5 - x) for i, x in enumerate(r))
assert sus([5,1]*5) == 100 and sus([1,5]*5) == 0
```

## Interpreting
- The average across published studies is about 68; above 80 is good, below 50 signals serious problems (Sauro, MeasuringU).
- SUS is neither a percentage nor a percentile.
- Five users find most qualitative issues, but metrics need more: report confidence intervals; with n < 20 treat SUS as directional.
- Compare like with like: same tasks, same user profile, before and after a redesign.

## Gotchas
- Do not reword items beyond swapping "system" for the product name.
- Administer before any debrief discussion, which biases answers.

## Verify
Each study report lists per-task success, median time and errors, the SUS mean with interval, and the qualitative issues behind low scores.
