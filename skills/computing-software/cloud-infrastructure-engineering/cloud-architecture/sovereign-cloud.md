---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.sovereign-cloud
name: sovereign-cloud
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, deployment-models, sovereign-cloud, data-sovereignty, operational-sovereignty, government-cloud, aws-european-sovereign-cloud, microsoft-cloud-for-sovereignty, google-sovereign-cloud, regulated-workloads]
level: advanced
status: draft
description: "Design for sovereignty: split data, operational and software sovereignty, map them to sovereign regions, gov or partner clouds, and controls in standard regions."
sources: ["https://learn.microsoft.com/industry/sovereignty/overview", "https://aws.amazon.com/compliance/digital-sovereignty/", "https://cloud.google.com/sovereign-cloud", "https://www.enisa.europa.eu/topics/cloud-and-big-data/cloud-security"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sovereign and regulated cloud

## Break "sovereignty" into requirements
1. **Data sovereignty / residency**: data stored and processed in a jurisdiction.
2. **Operational sovereignty**: who can operate/access the infrastructure (citizenship, local
   staff, provider access approval).
3. **Software/legal sovereignty**: protection from foreign legal access, ability to operate if
   the provider relationship ends, key control.

## Options by strictness
- **Standard regions + controls**: region restriction policies, customer-managed or external keys
  (EKM/XKS/HSM), access approval (Customer Lockbox, Access Transparency/Approval), data residency
  guarantees, confidential computing.
- **Sovereign landing zones** (policy packs: Microsoft Cloud for Sovereignty SLZ, Google Assured
  Workloads, AWS sovereignty controls).
- **Dedicated sovereign/government clouds**: AWS GovCloud, Azure Government, AWS European Sovereign
  Cloud, Google sovereign offerings with local partners (e.g. partner-operated in some EU countries).
- **Disconnected/air-gapped** options for classified workloads.

## Steps
1. Get the actual regulatory text/contract clauses; classify data and workloads.
2. Map each requirement to controls/offerings; prefer the least restrictive that satisfies it
   (dedicated clouds lag in services and cost more).
3. Enforce via policy (allowed regions, key requirements) and audit evidence.

## Verify
- [ ] Requirement → control matrix approved by legal/compliance.
- [ ] Allowed-region policy enforced on in-scope scopes.
