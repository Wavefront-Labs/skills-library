---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.pre-migration-baseline
name: pre-migration-baseline
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, onboarding-workloads, workload-onboarding, pre-migration-baseline, migration-business-case, on-premises-cost]
level: practitioner
status: draft
description: "Build a pre-migration cost baseline: on-prem cost per workload (hardware, licences, facilities, labour), utilisation data, and a target cloud estimate."
sources: ["https://www.finops.org/framework/capabilities/onboarding-workloads/", "https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-portfolio-discovery/welcome.html", "https://learn.microsoft.com/en-us/azure/migrate/concepts-business-case-calculation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pre-migration cost baseline

Without a baseline, nobody can say whether migration saved money, and the business case gets
judged on cloud spend alone.

## Baseline components per workload (annualised)
- **Hardware**: server and storage depreciation (or lease), allocated by VM/host share; network
  gear share.
- **Software licences**: OS, hypervisor (VMware), database (SQL Server, Oracle), middleware;
  support and maintenance contracts.
- **Facilities**: data center rack/power/cooling or colocation fees per kW.
- **Labour**: infrastructure operations FTE share (hardware, patching, backups).
- **Other**: backup and DR infrastructure, WAN circuits, security tooling.
Mark each item as avoidable (stops after migration and decommission) or sunk.

## Utilisation data (drives cloud sizing)
Collect 2-4 weeks minimum (30+ days preferred) of CPU, memory, disk IOPS and throughput, network
per VM with discovery tools (AWS Application Discovery Service / Migration Evaluator, Azure Migrate
appliance, Google Migration Center). Size to observed P95, not allocated specs.

## Steps
1. Get finance data for the fixed asset register, contracts and facility costs.
2. Allocate shared costs to workloads with clear keys (vCPU share, storage TB, rack units).
3. Produce the target cloud estimate (rightsized, with expected commitment discounts and licence
   choices such as BYOL vs licence-included).
4. Document assumptions and freeze the baseline (version, date) before migration starts.
5. Plan double-running cost during the migration window and decommission dates.

## Gotchas
- Comparing fully loaded cloud cost with on-prem hardware only flatters on-prem.
- Savings that only happen when hardware is decommissioned or contracts end; track those dates.
- Sizing from allocated VM specs overestimates cloud cost by 30-50% in typical estates.

## Verify
- [ ] Baseline per workload signed off by finance with avoidable vs sunk split.
- [ ] Cloud estimate uses measured utilisation.
