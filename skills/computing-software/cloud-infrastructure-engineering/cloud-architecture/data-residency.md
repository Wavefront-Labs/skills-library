---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.data-residency
name: data-residency
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, information-systems-architecture, togaf, data-residency, data-sovereignty, gdpr-transfers, region-restriction]
level: advanced
status: draft
description: "Design for data residency and sovereignty: map legal requirements, constrain regions with policy, handle backups, logs, support access and cross-border transfers."
sources: ["https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection_en", "https://learn.microsoft.com/azure/governance/policy/samples/built-in-policies", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_examples_general.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data residency and sovereignty design

Residency = where data is stored and processed. Sovereignty = whose laws can reach it
(including foreign-government access to a provider). Different requirements, different controls.

## Steps
1. **Map obligations per dataset**: GDPR (transfers outside the EEA need adequacy, SCCs plus
   a transfer impact assessment), sector rules (banking, health, public sector), contracts.
2. **Choose regions** that satisfy residency, including paired/DR regions - an in-country
   pair may not exist.
3. **Enforce region restriction**: AWS SCP with `aws:RequestedRegion`, Azure Policy
   "Allowed locations", GCP organisation policy `gcp.resourceLocations`. Exempt global
   services carefully (IAM, CDN, DNS).
4. **Follow the data's shadows**: backups, snapshots and replicas; logs and telemetry
   (SaaS observability vendors often store in the US by default); support case attachments;
   AI/ML services that process prompts in another geography.
5. **Sovereignty controls** where needed: customer-managed keys in an in-country HSM or
   external key manager, provider sovereign offerings, access transparency and approval for
   provider support access.
6. **Document** a data-flow diagram showing every location, for the DPIA and auditors.

## Gotchas
- Global services and CDNs cache data at edges outside the region.
- Encryption with provider-held keys does not address sovereignty concerns about compelled access.

## Verify
- [ ] Region policy denies resource creation outside approved regions (tested).
- [ ] Data-flow diagram covers backups, logs and support paths.
