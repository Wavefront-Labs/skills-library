---
id: engineering-technology.biomedical-engineering.device-verification-validation.fault-tree-analysis
name: fault-tree-analysis
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [fault-tree, iso-14971, risk-management, fault-tree-analysis, fta, minimal-cut-set, common-cause-failure, top-down-analysis]
level: advanced
status: gated
description: "Build and quantify a fault tree for a device hazard: top event, gates, minimal cut sets, probability combination, common-cause failures and links to ISO 14971."
sources: ["IEC 61025:2006 Fault tree analysis (FTA) (2006 edition listed as current by national standards bodies; an edition 3 is in development; clause content (gated: unconfirmed, source is paywalled or blocked))", "ISO 14971 Medical devices - Application of risk management (FTA as a technique; confirm edition)", "NASA Fault Tree Handbook with Aerospace Applications"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fault tree analysis (FTA)

**Goal:** a top-down map of the combinations of failures that can cause a hazardous situation, to find weak points and verify redundancy.

## Steps
1. **Define the top event** precisely and the system boundary (for example "Infusion pump delivers more than 20% over-dose for more than 5 minutes").
2. **Decompose** downwards: ask what is necessary and sufficient to cause the event. Use **OR gates** when any input is enough and **AND gates** when all inputs are required (for example a runaway motor drive AND failure of the independent overspeed monitor).
3. Continue to **basic events** (component failures, human errors, software faults, environment) at the level where failure data are available or the cause is not developed further.
4. **Find minimal cut sets:** the smallest combinations of basic events that cause the top event; single-event cut sets are single points of failure, a red flag for serious harm.
5. **Quantify** with probabilities per unit time or per demand: AND gates multiply (P = P1 x P2 for independent events); OR gates sum approximately for small values (P about P1 + P2). Example: motor driver runaway 1e-4 per year and monitor failure 1e-3 per demand gives about 1e-7 per year for the AND path (1e-4 x 1e-3 = 1e-7 computed; the product is a per-year rate only if the monitor failure probability applies per runaway demand).
6. **Common-cause failures:** events that fail multiple branches together (shared power supply, same software, same temperature stress) invalidate independence; add them explicitly (beta-factor models or explicit common events).
7. **Importance measures** (Fussell-Vesely, Birnbaum) show which events dominate and where to apply design effort.
8. **Link to risk control:** add measures (redundancy, monitors, interlocks), update the tree and show the new cut sets.

## Software and human factors
Software defects are systematic, so do not assign random failure rates; represent them as events with a design control (see software-risk-control), and quantify use errors with human reliability data and usability evidence.

## Verify
- [ ] Top event matches the hazardous situation in the risk file.
- [ ] No single-point cut set for severe harm without a justified control.
- [ ] Failure rates cited from a source (field data, handbook, supplier) with uncertainty.
