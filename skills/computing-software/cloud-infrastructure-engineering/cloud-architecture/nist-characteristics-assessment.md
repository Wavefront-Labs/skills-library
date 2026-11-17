---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.nist-characteristics-assessment
name: nist-characteristics-assessment
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, service-models, nist-essential-characteristics, nist-sp-800-145, on-demand-self-service, rapid-elasticity, measured-service, cloud-washing]
level: practitioner
status: draft
description: "Assess whether an offering is really cloud: score it against the five NIST SP 800-145 essential characteristics with evidence, and expose cloud-washed hosting."
sources: ["https://csrc.nist.gov/pubs/sp/800/145/final", "https://csrc.nist.gov/pubs/sp/500/292/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Assessing an offering against the NIST essential characteristics

## When
A vendor, an internal "private cloud" or a managed-hosting deal is sold as cloud and the business
case assumes cloud economics (pay per use, scale on demand). Test the claim before you rely on it.

## Steps
1. **Score each characteristic with evidence**, not marketing copy:
   - *On-demand self-service*: can a consumer provision via API/portal with no ticket? Measure
     time-to-provision (minutes = yes; days with a human approval = no).
   - *Broad network access*: standard protocols (HTTPS APIs, standard clients), reachable from
     the networks you need.
   - *Resource pooling*: multi-tenant pool, location abstracted (region/zone choice, not rack).
   - *Rapid elasticity*: scale out and back in automatically; check quota ceilings and the lead
     time to raise them. "Elastic up to the hardware we bought" is not elastic.
   - *Measured service*: metered usage exposed to the consumer, billed on that metering at a
     useful granularity (per second/hour/request), not a flat monthly fee.
2. **Rate each 0-2** (absent / partial / full) and attach the evidence (API doc link, test log).
3. **Map gaps to business-case risk**: no elasticity means you pay for peak; no metering means
   no showback; ticketed provisioning kills developer velocity claims.
4. **Classify the service model** honestly (IaaS/PaaS/SaaS) per NIST: what the consumer controls
   vs the provider.
5. **Decide**: accept, accept with contractual remedies (quota SLAs, metering exports), or treat
   it as hosting and re-cost it as such.

## Gotchas
- Private clouds commonly fail elasticity and metering; that is fine if priced as fixed capacity.
- A portal that opens a ticket behind the scenes is not self-service; time it.
- Quota increases that need a support case can turn "elastic" into weeks at peak season.

## Verify
- [ ] Five characteristics scored with linked evidence.
- [ ] Business-case assumptions reconciled with the gaps found.
