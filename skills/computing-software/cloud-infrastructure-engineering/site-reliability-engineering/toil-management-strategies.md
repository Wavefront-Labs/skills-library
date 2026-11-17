---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.toil-management-strategies
name: toil-management-strategies
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [toil-management-strategies, automation-prioritisation, toil, eliminating-toil, automation-roi]
level: practitioner
status: docs-checked
description: "Apply the Workbook's toil management strategies: identify and measure, engineer toil out at the source, reject toil, use SLOs, standardise, and prioritise automation by ROI."
sources: ["https://sre.google/workbook/eliminating-toil/", "https://sre.google/sre-book/eliminating-toil/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Toil management strategies

The Workbook says toil reduction can take weeks or quarters, so it needs an overarching strategy. This lists its
strategies as a checklist for choosing what to do with each toil item.

## The strategies (Workbook)
1. **Identify and measure toil**: take a data-driven approach; Google SRE teams often track toil in bugs and rank it by
   cost to fix and time saved. If a team is overloaded, treat toil reduction as its own project.
2. **Engineer toil out of the system**: the Workbook calls eliminating toil at its source the optimal strategy. Work with
   product developers on operationally friendly software.
3. **Reject the toil**: the Workbook says rejecting a toil-intensive task should be the first option considered. Compare
   the cost of responding with the cost of not doing so; or delay tasks so they accumulate for batch processing.
4. **Use SLOs to reduce toil**: you may ignore operational tasks that do not consume or exceed the error budget; an SLO
   on overall service health rather than individual devices scales better.
5. **Start with human-backed interfaces**: take structured requests through a defined API while engineers still handle
   some operations behind it, then move toward full automation.
6. **Provide self-service methods**: a web form, script, API or documented pull-request flow; let it degrade to a ticket
   for specialised requests or failures.
7. **Get support from management and colleagues**, and **promote toil reduction as a feature** coupled with goals such as
   security, scalability or reliability.
8. **Start small and then improve**: automate a few high-priority items first and pick clear metrics such as MTTR.
9. **Increase uniformity**: treat devices as interchangeable ("pets versus cattle") with a consistent interface.
10. **Assess risk within automation**: validate input, add safeguards such as timeouts and checks of current metrics,
    remember that naive read operations can spike load, and default to human operators on an unsafe condition.
11. **Automate toil response**: do not transcribe a human workflow literally; build composable components.
12. **Use open source and third-party tools**, and **use feedback to improve** (latency, error rate, rework rate, human
    time saved).

## Choosing
Eliminate or reject first. Automate only when the measured cost justifies it: the Workbook says to weigh the measurable
costs of designing and implementing automation using metrics, ROI analysis, risk assessment and iterative development.

## Gotchas
- Eliminating toil is not always the best solution; do the ROI analysis first.
- Automation with admin-level powers can cause outages; safety checks are crucial.

## Checked
2026-11-01. Confirmed against the SRE Workbook chapter "Eliminating Toil" (Toil Management Strategies section and the
closing note on ROI) and the SRE Book chapter "Eliminating Toil". Corrected: the skill ranked "engineer out" above
"reject"; the Workbook says reject should be considered first and engineering out is the optimal outcome. Removed: the
scoring formulas and risk multiplier, the one-year payback rule, the O(n) rule, the 50 percent line and the xkcd source
(not read).
Method: documentation only; no commands were run.
