---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.oracle-cloud-licensing
name: oracle-cloud-licensing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, licensing-and-saas, oracle-cloud-licensing, authorized-cloud-environment, oracle-vcpu-licensing, byol-oracle, rds-oracle-licence]
level: advanced
status: draft
description: "Navigate Oracle licensing in public cloud: Authorized Cloud Environment vCPU rules, BYOL vs licence-included, editions, and options like Oracle Database@Azure/AWS/Google."
sources: ["https://www.oracle.com/assets/cloud-licensing-070579.pdf", "https://aws.amazon.com/rds/oracle/pricing/", "https://www.oracle.com/cloud/azure/oracle-database-at-azure/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oracle licensing in cloud

## Authorized Cloud Environment policy (Oracle, check current document)
- Applies to AWS, Azure, Google Cloud and Oracle Cloud listed environments.
- **Processor licences**: on AWS/Azure/Google, 2 vCPUs = 1 processor licence when hyper-threading
  is enabled (1 vCPU = 1 licence if not). The Oracle core factor table is **not** applied.
- **Standard Edition / SE2**: instances up to 8 vCPUs count as limited sockets (SE2 limited to
  instances with <= 8 vCPUs; every 4 vCPUs = 1 socket).
- Named User Plus minimums per processor still apply.

## Options
1. **Licence-included** (RDS for Oracle SE2 LI): simplest; limited editions.
2. **BYOL** on IaaS or RDS: count vCPUs per policy; Enterprise Edition options (RAC, partitioning,
   diagnostics packs) licensed separately - disable unused options/packs.
3. **Oracle Database@Azure / @AWS / @Google Cloud**: Oracle-managed Exadata in hyperscaler data
   centres with Oracle licensing (including BYOL and Support Rewards) - often favourable for EE.
4. **Migrate off** to PostgreSQL where feasible (biggest saving, biggest effort).

## Steps
1. Inventory DB instances, editions, options in use (DBA_FEATURE_USAGE_STATISTICS).
2. Model each option's licence + infrastructure cost; reduce vCPUs (constrained vCPU instance types:
   e.g. RDS/EC2 optimize CPUs to lower vCPU count while keeping memory).
3. Engage licensing specialists; document positions for audits.

## Gotchas
- Oracle VM or "soft partitioning" rules on-prem don't translate; cloud vCPU rules apply.
- Feature usage of packs triggered by tooling (e.g. AWR) without licences.

## Verify
- [ ] Licence position per instance documented and reconciled with entitlements.
