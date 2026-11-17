---
id: computing-software.data-science-and-analytics.experiment-design.experiment-duration-power
name: experiment-duration-power
category: computing-software
field: data-science-and-analytics
product: experiment-design
tags: [experiment-duration, novelty-effect, weekly-seasonality]
level: practitioner
status: draft
description: "Size the test for the minimum detectable effect, run whole weeks and watch for novelty and primacy effects before deciding."
sources:
  - https://experimentguide.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Duration
- Compute n per variant from baseline rate, MDE, alpha=0.05, power=0.8 (see power-and-sample-size).
- Run at least one full business cycle (usually 1-2 weeks) so weekday mix is balanced.
- Novelty: plot the daily effect; a decaying lift suggests a transient effect.
## Gotchas
- Stopping the moment p<0.05 inflates false positives (see sequential testing).
- Underpowered tests produce exaggerated significant effects.
## Verify
- [ ] Daily effect plot is stable in the final days.
