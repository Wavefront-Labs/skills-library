---
id: computing-software.systems-network-administration.patch-management.change-risk-assessment
name: change-risk-assessment
category: computing-software
field: systems-network-administration
product: patch-management
tags: [change-risk-assessment, risk-matrix, change-enablement, change-collision, impact-assessment, itil-4]
level: practitioner
status: draft
description: "Assess change risk consistently with a likelihood-by-impact model and questionnaire: complexity, testing, track record, reversibility, service impact, timing and collisions."
sources:
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-change-enablement
  - https://www.servicenow.com/docs/bundle/xanadu-it-service-management/page/product/change-management/concept/c_RiskAssessment.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Change risk assessment

**Goal:** a repeatable risk rating that decides the change authority and the safeguards required.

## Two axes
**Likelihood of failure**, raised by:
- Complexity (number of steps, systems, teams).
- Novelty (first time on this platform or version).
- Testing quality (none / lab / production-like / previous successful run).
- Track record of this change class (historical failure rate).
- Automation vs manual execution.

**Impact if it fails**, raised by:
- Services and users affected; tier of CIs.
- Loss of redundancy during the change (single node remains).
- Reversibility (snapshot rollback in minutes vs irreversible schema/firmware change).
- Timing (business hours, peak periods, regulatory deadlines).
- Data at risk.

## Questionnaire (score 0-3 each, example)
1. Has this exact change succeeded before in production? (3 = never)
2. Is there a tested rollback taking under 30 minutes? (3 = no rollback)
3. Will any service be unavailable or non-redundant? (3 = customer-facing outage)
4. How many CIs are touched? (3 = more than 50 or cross-site)
5. Is the change executed by automation with validation? (3 = fully manual)
6. Does it fall during a high-impact period? (3 = yes)
Sum maps to Low / Medium / High, which maps to the change authority.

## Collision check
Look at the change schedule for other changes on the same CIs, shared infrastructure (network, storage, identity) or the same team in the same window. Collisions raise risk or force rescheduling.

## Gotchas
- Self-assessed risk tends to be low; calibrate by comparing predicted risk with outcomes quarterly.
- A "low risk" patch on a Tier 0 system still deserves its redundancy plan.

## Verify
Quarterly review: failed changes were mostly rated Medium/High; if many Low-rated changes failed, adjust the questionnaire weights.
