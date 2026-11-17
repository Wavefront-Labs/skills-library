---
id: computing-software.ux-hci-design.ux-research-methods.ab-testing-ux-pitfalls
name: ab-testing-ux-pitfalls
category: computing-software
field: ux-hci-design
product: ux-research-methods
tags: [ab-testing-ux, sample-ratio-mismatch, ur-quant-experiments]
level: advanced
status: draft
description: "Define hypothesis, metric and sample size up front; check sample ratio mismatch and avoid peeking."
sources:
  - https://www.nngroup.com/articles/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# A/B tests
- Pre-register hypothesis, primary metric, guardrail metrics, minimum detectable effect and sample size (power analysis).
- Randomise at user level; run whole weekly cycles.
- Check **sample ratio mismatch** (chi-square on assignment counts) before reading results; mismatch indicates a bug.
- Do not peek and stop early on significance; use sequential methods if you must monitor.
- Beware multiple comparisons and novelty effects.
- A/B tells what, not why; pair with qualitative research.

## Verify
- [ ] Sample sizes and SRM check documented before the decision.
