---
id: computing-software.data-science-and-analytics.experiment-design.sequential-testing-peeking
name: sequential-testing-peeking
category: computing-software
field: data-science-and-analytics
product: experiment-design
tags: [sequential-testing, peeking-problem, alpha-spending, ab-pitfalls]
level: advanced
status: draft
description: "Explain why repeated looks inflate false positives and apply alpha-spending or always-valid methods when early stopping is needed."
sources:
  - https://experimentguide.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Peeking
- Looking daily and stopping at the first p<0.05 can push the false-positive rate several times above 5%; simulate it to convince stakeholders.
- Options: fixed horizon (do not peek); group-sequential boundaries (O'Brien-Fleming, alpha spending); always-valid p-values/mSPRT; Bayesian decision rules with loss thresholds.
```python
rng = np.random.default_rng(0)   # A/A simulation: count how often any daily look gives p<0.05
```
## Gotchas
- Platform dashboards that show live p-values invite peeking.
## Verify
- [ ] A/A simulation of the planned procedure holds about 5% false positives.
