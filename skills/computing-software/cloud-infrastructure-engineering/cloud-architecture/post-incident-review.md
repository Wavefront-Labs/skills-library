---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.post-incident-review
name: post-incident-review
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, operational-excellence, post-incident-review, blameless-postmortem, incident-timeline, contributing-factors, action-items]
level: practitioner
status: draft
description: "Run blameless post-incident reviews: timeline, impact, contributing factors (not one root cause), what went well, and tracked actions that change systems not people."
sources: ["https://sre.google/sre-book/postmortem-culture/", "https://www.atlassian.com/incident-management/postmortem", "https://learn.microsoft.com/azure/well-architected/operational-excellence/incident-response"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Blameless post-incident reviews

## Triggers
User-visible outage or SLO breach, data loss, security incident, on-call intervention beyond
threshold, near misses worth learning from, significant error budget consumption.

## Document structure
1. Summary: what happened, impact (users, duration, revenue/SLO), severity.
2. **Timeline** (UTC): detection, escalation, key decisions, mitigation, resolution - from chat,
   alerts, deploy logs.
3. **Contributing factors**: technical (latent bug, config, capacity), process (missing review),
   detection gaps, response friction. Ask "how did it make sense at the time?"
4. What went well / where we got lucky.
5. **Actions**: specific, owned, dated; prioritised (prevent, detect faster, mitigate faster).
6. Lessons for other teams.

## Running the meeting
Within ~5 working days; facilitator not involved in the incident; focus on systems and decisions,
no blame or naming as fault; review draft async first.

## Gotchas
- "Human error" as root cause - always ask why the system allowed it.
- Action items like "be more careful"; replace with guardrails/automation.
- Actions never completed; track closure rate.

## Verify
- [ ] Action closure rate reported monthly; overdue actions escalated.
