---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.preventing-operational-underload
name: preventing-operational-underload
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [operational-underload, on-call, wheel-of-misfortune, dirt, shadowing, skills-maintenance]
level: practitioner
status: docs-checked
description: "Keep on-call skills sharp on quiet services: on-call frequency, Wheel of Misfortune, DiRT, shadowing and deliberate exercises so the first real page is not a surprise."
sources: ["https://sre.google/sre-book/being-on-call/", "https://sre.google/sre-book/accelerating-sre-on-call/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preventing operational underload

The SRE Book calls operational underload undesirable: being out of touch with production for long periods leads to
confidence issues (both over- and underconfidence), and knowledge gaps are discovered only when an incident occurs.

## Countermeasures the Book names
| Practice | Source detail |
|---|---|
| Size the team so everyone is on-call often | every engineer on-call at least once or twice a quarter |
| Wheel of Misfortune | a game master runs a scenario for a primary and secondary on-call; see `running-a-wheel-of-misfortune-exercise` |
| DiRT (Disaster Recovery Training) | Google's company-wide annual event combining theoretical and practical multiday drills |
| Shadowing and reverse shadowing | a student shadows the on-caller before taking primary; a reverse shadow has the experienced engineer watch without changing state; see `on-call-learning-paths` |
| Break and fix real things | hands-on practice on a diverted instance or a staging stack under synthetic load, before the first on-call shift |
| Burn-down exercise | gradually impair a known-good stack and have participants predict the effects; Google Search SRE runs one quarterly |

## Gotchas
- The same scenario every time turns the drill into theatre; the Book suggests scenarios from past outages, hypothetical
  breakages of new features, or newly found production breakage.
- Limiting the rotation size also keeps engineers in touch with production (Book, on multi-site teams).

## Checked
2026-11-01. Confirmed against the SRE Book chapters "Being On-Call" (underload section, once or twice a quarter, Wheel of
Misfortune, DiRT, rotation size) and "Accelerating SREs to On-Call and Beyond" (disaster role playing, shadow and reverse
shadow, break real things, quarterly burn-down). Removed: the underload signals with page, 3-month and 6-month
thresholds, the biweekly and monthly cadences, the runbook-per-shift practice, the numbered Wheel format and the verify
list; none is on these pages. The Workbook source was dropped (not read this batch).
Method: documentation only; no commands were run.
