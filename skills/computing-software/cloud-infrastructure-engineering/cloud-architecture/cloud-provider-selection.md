---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-provider-selection
name: cloud-provider-selection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-ecosystem, cloud-provider-selection, vendor-evaluation, weighted-scoring, rfp, proof-of-concept]
level: advanced
status: draft
description: "Select a cloud provider with a weighted, evidence-based evaluation: requirements, scoring model, proof of concept, commercial terms and exit criteria."
sources: ["https://www.nist.gov/publications/nist-cloud-computing-reference-architecture", "https://learn.microsoft.com/azure/cloud-adoption-framework/strategy/", "https://cloudsecurityalliance.org/research/cloud-controls-matrix"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud provider evaluation and selection

Choose a primary (and possibly secondary) provider on evidence tied to your workloads, not
on brand preference or a single feature demo.

## Steps
1. **Write the requirements first**, grouped: regions and data residency, required managed
   services (by workload, not wish list), compliance attestations (SOC 2, ISO 27001, PCI DSS,
   FedRAMP, sector schemes), identity integration, network connectivity options, support
   tiers, sustainability data, skills already in the organisation.
2. **Separate gates from scores.** Gates are pass/fail (region in country X, HIPAA BAA
   available). Only providers passing every gate get scored.
3. **Weighted scoring** (weights agreed with stakeholders before seeing vendor answers):
   technical fit, security and compliance, commercial (3-year modelled cost with realistic
   discounts), operational fit (tooling, support, partner ecosystem), strategic (roadmap,
   lock-in exposure). Score 1-5 with written evidence per cell.
4. **Proof of concept** on 1-2 representative workloads with exit criteria defined upfront:
   deploy via IaC, measure latency and throughput, run a failover, read a real bill.
5. **Commercial**: model list price then negotiated price (commit discounts, credits,
   migration funding programmes); compare 3-year TCO on the same architecture.
6. **Record the decision** as an ADR including runner-up and what would reopen the decision.

## Gotchas
- Feature checklists hide maturity differences; ask for GA status, SLA and region availability per service.
- Migration credits are front-loaded; do not let them dominate a 3-year comparison.
- Weights tuned after scoring to get the preferred answer destroy credibility.

## Verify
- [ ] Gates, weights and evidence documented before final scoring.
- [ ] PoC results and modelled TCO attached to the decision record.
