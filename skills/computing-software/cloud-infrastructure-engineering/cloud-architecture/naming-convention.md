---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.naming-convention
name: naming-convention
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, landing-zone, naming-convention, resource-naming, abbreviations, naming-standard]
level: practitioner
status: draft
description: "Define a cloud resource naming convention: components and order, abbreviations, length and character limits per service, uniqueness, and enforcement."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations", "https://learn.microsoft.com/azure/azure-resource-manager/management/resource-name-rules"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Naming convention

Names are for humans and are hard to change (many resources cannot be renamed). Put
metadata that changes (owner, cost centre) in tags, not names.

## Pattern
`<type-abbrev>-<workload>-<env>-<region>-<instance>` e.g. `rg-payments-prod-weu-001`,
`vnet-hub-prod-eus2-001`, `kv-payments-prd-weu-01`.
- Type abbreviations from a standard list (CAF abbreviations: `rg`, `vnet`, `snet`, `kv`, `st`, `func`, `aks`).
- Environment short codes: `prod`, `stg`, `dev`, `sbx`.
- Region short codes table (`weu`, `eus2`, `use1`).

## Steps
1. **Collect constraints per service**: Azure storage accounts 3-24 lowercase letters and
   digits, no hyphens, globally unique; Key Vault 3-24, globally unique; S3 buckets 3-63,
   lowercase, globally unique, no underscores; GCP project IDs 6-30, immutable.
2. **Define variants** for constrained services (drop hyphens, shorter codes).
3. **Uniqueness** for global names: add a short hash or org prefix, not random words.
4. **Enforce**: IaC naming module that generates names (e.g. Azure naming Terraform module);
   policy to audit or deny non-conforming names where feasible.
5. **Publish** the abbreviation and region tables in the repository.

## Gotchas
- Putting team names in resource names; teams reorganise, resources stay.
- Ignoring length limits until a 25-character name fails in production deploy.

## Verify
- [ ] Naming module used by all landing-zone and workload IaC.
- [ ] Policy compliance report shows conforming names.
