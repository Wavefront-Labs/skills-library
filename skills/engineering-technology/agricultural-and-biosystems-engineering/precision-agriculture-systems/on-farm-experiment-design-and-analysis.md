---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.on-farm-experiment-design-and-analysis
name: on-farm-experiment-design-and-analysis
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, on-farm-trials, on-farm-experimentation, strip-trial, replication, randomization, yield-monitor-trials, spatial-analysis, farm-data-management]
level: advanced
status: draft
description: "Run reliable on-farm experiments: question, treatments, randomised replicated strips, yield monitor data checks, spatial and ANOVA analysis, and decision rules."
sources:
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "Hunt & Wilson, Farm Power and Machinery Management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# On-farm experiment design and analysis

**Goal:** a result from the farmer's own fields that can support a management decision, with a stated level of confidence.

## Design
1. State one clear question (for example: nitrogen rate A versus B, hybrid comparison, seeding rate, a product trial) and the decision rule: what difference is worth acting on?
2. Choose treatments that fit the machinery (full-width strips or passes of the planter, sprayer or spreader) and are easy to apply correctly.
3. Randomise treatment positions within blocks and replicate each treatment at least three or four times; a single side-by-side strip cannot separate treatment from soil differences. Set the strip length to cover the variability and be long enough for the monitor to log steady data, and put buffer areas at the ends.
4. Put the blocks across the field gradients (soil, slope, EC).
5. Record planting, input rates and operations accurately (as-applied maps, `as-applied-maps-and-verification`), weather and anything else that changed.

## Data
Use yield monitor data after calibration and cleaning (`yield-monitor-calibration-procedure`, `yield-data-cleaning-and-error-removal`); delete the ends of each strip; use the data within the strip excluding the edges; compare with weigh-wagon or truck scale checks.

## Analysis
- Strip means by treatment and block, then ANOVA for a randomised block design; report the mean difference, its standard error or confidence interval, and the p-value or a decision-oriented summary. For large datasets, use spatial statistical models to account for spatial correlation; farmers and advisers can use software that fits these models.
- Check the difference against the cost of the treatment to give an economic result (`variable-rate-economics-and-break-even`).
- Repeat for more than one year or in more fields before changing the whole-farm practice, because weather interacts with treatments.

## Verify
- [ ] Layout map and randomisation recorded.
- [ ] Analysis includes uncertainty, not only the means.
- Unconfirmed: software options; choose one that handles spatial models.
