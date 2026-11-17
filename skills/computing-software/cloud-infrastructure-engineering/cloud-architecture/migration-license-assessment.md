---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.migration-license-assessment
name: migration-license-assessment
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-assessment, migration-license-assessment, licence-mobility, byol-eligibility, software-assurance, licence-included]
level: practitioner
status: draft
description: "Assess software licences before migration: mobility rights, BYOL eligibility, licence-included pricing, dedicated host needs and true-up exposure per product."
sources: ["https://www.microsoft.com/licensing/docs/view/Licensing-Use-Rights", "https://aws.amazon.com/windows/resources/licensing/", "https://cloud.google.com/compute/docs/instances/bring-your-own-license"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Licence assessment before migration

## Steps
1. Inventory installed software from discovery (product, edition, version, core count).
2. Match to entitlements from the licensing team (contracts, Software Assurance, subscriptions).
3. For each product decide the cloud licensing path:
   - **Licence-included** pay-as-you-go (simple, often most expensive for SQL Server Enterprise).
   - **BYOL with mobility** (e.g. Microsoft Licence Mobility through SA for server apps, Azure
     Hybrid Benefit on Azure).
   - **BYOL requiring dedicated hosts** (licences without mobility rights, e.g. Windows Server
     perpetual without SA on AWS/GCP outside Azure).
   - **Switch** to open source or managed equivalent.
4. Calculate cost of each path per workload (vCPU-based licensing changes counts vs physical cores).
5. Check third-party vendor terms (Oracle, IBM, SAP) for authorised cloud environments and
   vCPU-to-licence conversion rules.
6. Feed into TCO and 7 R decisions; involve SAM team for true-up risk.

## Gotchas
- Licensing per vCPU on cloud can multiply cost vs a dense on-prem host.
- Outsourcing rule changes (Microsoft "Listed Providers") affect BYOL to some clouds.
- Unused on-prem licences after migration can be retired or reused - capture the saving.

## Verify
- [ ] Each workload has a licensing path and cost.
- [ ] SAM team sign-off on compliance position.
