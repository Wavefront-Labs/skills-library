---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.database-licensing
name: database-licensing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, licensing-and-saas, database-licensing, sql-server-licensing, oracle-licensing, os-licensing, windows-sql-licensing]
level: advanced
status: draft
description: "Manage commercial database and OS licensing in cloud: SQL Server and Oracle core counting, licence-included vs BYOL, optimise-CPUs, and audit risk."
sources: ["https://www.finops.org/framework/capabilities/licensing-saas/", "https://aws.amazon.com/ec2/instance-types/optimize-cpu/", "https://www.oracle.com/assets/cloud-licensing-070579.pdf", "https://www.microsoft.com/licensing/docs/view/SQL-Server"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Commercial database and OS licensing in cloud

Licences frequently cost more than the infrastructure for SQL Server Enterprise and Oracle.

## Rules of thumb (verify against current terms)
- **SQL Server**: licensed per core with a 4-core minimum per VM when licensing by virtual
  machine; Standard vs Enterprise price gap is large; passive DR replicas get free rights
  with Software Assurance (and with AHB on Azure).
- **Oracle** on authorised clouds (AWS, Azure, GCP): count vCPUs - 2 vCPUs = 1 processor
  licence when hyperthreading is enabled; Standard Edition 2 limited to instances up to 8 vCPUs.
- **Windows Server**: licence-included on shared tenancy, or BYOL on dedicated hosts.
- **RHEL/SUSE**: pay-as-you-go images or BYOS via Red Hat Cloud Access.

## Steps
1. **Inventory** engines, editions, vCPUs and licence model per instance.
2. **Reduce core count**: rightsizing; AWS Optimize CPUs (fewer cores, hyperthreading off)
   and Azure constrained vCPU sizes keep memory and IO while cutting licensed cores.
3. **Edition downgrade**: many Enterprise installs use no Enterprise features; check feature
   usage (`sys.dm_db_persisted_sku_features` for SQL Server; Oracle DBA_FEATURE_USAGE_STATISTICS).
4. **Engine change** where viable (PostgreSQL, Aurora, Babelfish) for large licence savings.
5. **Model** licence-included vs BYOL per instance and track in licence management tooling.
6. **Audit readiness**: evidence of core counts over time; Oracle audit risk on VMware-style
   counting does not apply on authorised clouds but configuration must match policy.

## Gotchas
- Scaling up an instance for a short event can create a licence liability under BYOL.
- Oracle options and packs (Diagnostics, Tuning, Partitioning) are separate licences and easy to enable by accident.

## Verify
- [ ] Licence position reconciled monthly with deployed cores.
- [ ] Feature-usage reports reviewed before edition decisions.
