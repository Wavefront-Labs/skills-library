---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.non-functional-requirements
name: non-functional-requirements
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-vision, togaf, non-functional-requirements, quality-attributes, iso-25010, nfr-catalogue]
level: practitioner
status: draft
description: "Elicit measurable non-functional requirements for a cloud workload using quality-attribute scenarios: availability, latency, scale, security, cost and operability."
sources: ["https://iso25000.com/index.php/en/iso-25000-standards/iso-25010", "https://insights.sei.cmu.edu/library/quality-attribute-workshops-qaws-third-edition/", "https://learn.microsoft.com/azure/well-architected/reliability/identify-flows"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Eliciting non-functional requirements

## Steps
1. **Use a checklist** so nothing is forgotten (ISO/IEC 25010 qualities plus cloud specifics):
   availability, RTO/RPO, latency, throughput and peak scale, data volume growth, security
   and data classification, residency, compliance, observability, operability (deploy
   frequency, maintenance windows), cost ceiling, sustainability, accessibility.
2. **Write quality-attribute scenarios** (SEI): source, stimulus, environment, artefact,
   response, response measure. Example: "When traffic reaches 5x baseline during a campaign
   (stimulus), the checkout API (artefact) keeps p99 latency under 400 ms (measure) with
   no manual intervention."
3. **Make each measurable**: numbers, percentiles, time windows. "Fast" and "highly
   available" are not requirements.
4. **Prioritise with stakeholders** (quality attribute workshop): rank by business
   importance and architectural difficulty; high/high scenarios drive the design.
5. **Expose trade-offs**: 99.99% multi-region vs cost ceiling; strict residency vs global latency.
6. **Trace** each NFR to design decisions, tests (load test, DR drill) and SLOs.

## Gotchas
- Asking stakeholders "what availability do you need?" yields 100%; ask about the cost of an
  hour of downtime and the tolerable data loss instead.
- NFRs written once and never tested become fiction.

## Verify
- [ ] Every NFR has a response measure and a verification method.
- [ ] Top scenarios linked to ADRs.
