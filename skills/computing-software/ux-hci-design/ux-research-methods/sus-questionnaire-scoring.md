---
id: computing-software.ux-hci-design.ux-research-methods.sus-questionnaire-scoring
name: sus-questionnaire-scoring
category: computing-software
field: ux-hci-design
product: ux-research-methods
tags: [system-usability-scale, sus-scoring, ur-surveys-metrics]
level: practitioner
status: draft
description: "Score the 10-item SUS questionnaire to a 0-100 value and interpret against the roughly 68 average."
sources:
  - https://measuringu.com/sus/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SUS scoring
10 statements, 5-point agree scale, alternating positive and negative wording.
- Odd items: score = response - 1. Even items: score = 5 - response.
- Sum the ten contributions and multiply by 2.5 = 0-100.
- The commonly cited average is about 68; SUS is not a percentage. It diagnoses overall perceived usability, not specific problems.
- Administer after tasks, one system at a time; wording "system" can be replaced by product name.

```python
def sus(r): return 2.5*sum((x-1) if i%2==0 else (5-x) for i,x in enumerate(r))
```

## Verify
- [ ] Sample [3]*10 scores 50.
