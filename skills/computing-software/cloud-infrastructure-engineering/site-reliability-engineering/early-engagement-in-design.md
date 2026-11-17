---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.early-engagement-in-design
name: early-engagement-in-design
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [early-engagement, design-phase-sre, sre-engagement, design-review, reliability-requirements]
level: practitioner
status: docs-checked
description: "SRE early engagement as the Google SRE Book describes it: which services qualify, SRE contributions in design, build, launch and post-launch, and disengaging."
sources: ["https://sre.google/sre-book/evolving-sre-engagement-model/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Early engagement in design

Source: SRE Book "The Evolving SRE Engagement Model", Early Engagement Model. The book says the earlier an SRE consultation happens, the better the service will be and the quicker it benefits; engaged in the earliest design stages, onboarding time is lower and the service is more reliable "out of the gate".

## Which services qualify
Applying the model needs an early view of the service's importance or business value and whether it will have enough scale or complexity to benefit. The book's candidate characteristics:
- significant new functionality that will be part of an existing system already managed by SRE;
- a significant rewrite or alternative to an existing system with the same use cases;
- the development team sought SRE advice or approached SRE for takeover on launch.
SRE can take over any time during or after the Build phase. The model is based on active collaboration between development and SRE.

## Contributions by phase (from the book)
- Design: prevents incidents that would otherwise occur; later design changes are costly. SRE is aware of trade-offs up front and part of the decision to pick a less-than-ideal option, minimising later disputes.
- Build and implementation: production aspects such as instrumentation and metrics, operational and emergency controls, resource usage and efficiency. SRE can recommend existing libraries and components or help build controls, and gains operational experience before launch.
- Launch: help implement launch patterns such as a dark launch (a share of existing traffic sent to the new service with its responses discarded), giving operational insight without affecting users.
- Post-launch: a stable launch means fewer conflicting priorities between reliability and features; SRE can be ready to take over sooner than under the Simple PRR model.

## Costs and limits
The simple PRR model's costs include communication overhead, availability of the right SRE reviewers, and the need for SRE work to be visible and reviewed so SREs work as part of the development team. Early engagement has the same constraint that SRE bandwidth is limited; the book says development team requests exceed SRE capacity.

## Disengaging
The book treats it as a positive outcome when a service engineered to be reliable and low-maintenance stays with the development team. If an early-engaged service does not reach projected usage, the SRE effort is part of normal business risk, the team can be reassigned and lessons incorporated.

## Verify
- [ ] The service meets at least one of the candidate characteristics and has an SRE contact during design.
- [ ] Reliability trade-offs accepted in design are written down with SRE participation.

## Checked
Confirmed against the SRE Book "The Evolving SRE Engagement Model" (Candidates for Early Engagement, Benefits by phase, Disengaging from a service). Removed: the reliability design-doc template, the 20% quarter staffing example, the phase table items not in the book (load tests, rollout tooling), and the "veto" gotcha.
Method: docs-only read of cited pages, 2026-11-08
