---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.platform-service-catalogue
name: platform-service-catalogue
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, service-models, platform-service-catalogue, platform-engineering, service-catalogue, golden-paths]
level: practitioner
status: draft
description: "Build an internal platform service catalogue mapped to IaaS/PaaS/SaaS/FaaS: offering, consumer responsibilities, SLOs, guardrails and how teams request each."
sources: ["https://csrc.nist.gov/pubs/sp/800/145/final", "https://tag-app-delivery.cncf.io/whitepapers/platforms/", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Internal platform service catalogue mapped to service models

## Steps
1. **Inventory what the platform actually offers**: VMs, container runtime, managed databases,
   functions, messaging, SaaS tools. One entry per consumable offering, not per cloud service.
2. **Tag each with its service model and responsibility split**: for IaaS the team patches the
   OS; for the platform's managed Postgres the platform team patches, the app team owns schema
   and queries. Write the split as a short RACI per entry.
3. **Per entry record**: owner team, supported regions, SLO, backup/DR default, security
   baseline (private endpoint, CMK), cost model (showback rate or pass-through), request path
   (self-service module, portal template, ticket), lifecycle state (preview/GA/deprecated).
4. **Prefer higher service models by default**: catalogue order steers choice; list the PaaS or
   serverless option first and require a reason for IaaS.
5. **Expose it** in the developer portal (Backstage software templates or similar) backed by
   IaC modules so each entry is provisionable, not just documented.
6. **Review quarterly**: usage per entry, deprecations, new provider services promoted from the
   technology radar.

## Gotchas
- A catalogue of raw provider services duplicates the provider docs; catalogue the curated,
  guard-railed offerings.
- Entries without an owner rot; deprecate them.

## Verify
- [ ] Every entry has service model, owner, SLO and responsibility split.
- [ ] Each GA entry is provisionable self-service.
