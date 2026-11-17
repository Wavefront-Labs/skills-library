---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.prr-checklist-and-questionnaire
name: prr-checklist-and-questionnaire
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [prr-checklist-sections, prr-questionnaire, production-readiness-review, launch-checklist, sre-engagement]
level: practitioner
status: docs-checked
description: "Build a production readiness review checklist from the Google SRE Book: PRR phases, the production areas SRE reviews, sample checklist items and the launch checklist themes."
sources: ["https://sre.google/sre-book/evolving-sre-engagement-model/", "https://sre.google/sre-book/launch-checklist/", "https://sre.google/sre-book/reliable-product-launches/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PRR checklist sections and questionnaire

## What a PRR is (SRE Book "The Evolving SRE Engagement Model")
A Production Readiness Review identifies a service's reliability needs and is a prerequisite for SRE to accept production responsibility. Its objectives: verify the service meets accepted standards of production setup and operational readiness, and improve reliability and minimise the number and severity of expected incidents. Phases: Engagement, Analysis, Improvements and Refactoring, Training, Onboarding, Continuous Improvement.

## Areas SRE reviews (the book's "production" aspects)
System architecture and interservice dependencies; instrumentation, metrics and monitoring; emergency response; capacity planning; change management; performance (availability, latency, efficiency).

## Checklist items the book gives for the Analysis phase
- Do updates impact an unreasonably large percentage of the system at once?
- Does the service connect to the appropriate serving instance of its dependencies (end-user requests should not depend on a batch-processing system)?
- Does it request a sufficiently high network quality of service when talking to a critical remote service?
- Does it report errors to central logging, including all exceptional conditions that cause degraded responses or failures?
- Are all user-visible request failures well instrumented and monitored, with suitable alerting?
The book says the checklist is service-specific, based on domain expertise, experience with similar systems and the Production Guide. SREs also review recent incidents, postmortems and follow-ups.

## Launch checklist themes (SRE Book launch chapters)
The "Reliable Product Launches" chapter's themes: architecture and dependencies, integration, capacity planning, failure modes, client behaviour, processes and automation, development process, external dependencies, rollout planning. The 2005 checklist appendix sections: architecture; machines and datacenters; volume estimates, capacity and performance; system reliability and failover; monitoring and server management; security; automation and manual tasks; growth issues; external dependencies; schedule and rollout planning.

Example questions and actions from the chapter: request flow user to frontend to backend; single points of failure; manual processes required to keep the service running (document them); back off exponentially and jitter client requests; are you storing persistent data (implement backups); check code and config into version control; cut each release on a new release branch.

## Using it as a questionnaire
Your own format: question, answer, evidence, status, owner. The book requires every question's importance to be substantiated and every instruction to be concrete, practical and reasonable. It also says experienced engineers customise the process per launch and warns that burdensome checklists get bypassed.

## Verify
- [ ] Each answer points to evidence, not opinion.
- [ ] The checklist is curated from incidents and reviewed periodically (the book says once or twice a year).

## Checked
Confirmed against the SRE Book "The Evolving SRE Engagement Model" (PRR phases, objectives, Analysis checklist), "Reliable Product Launches at Scale" and the "Launch Coordination Checklist" appendix. Removed: the invented per-section sample questions (burn-rate alerts, N+2 headroom, rollback in minutes), the cross-references to skills not read here, and the table format claims.
Method: docs-only read of cited pages, 2026-11-08
