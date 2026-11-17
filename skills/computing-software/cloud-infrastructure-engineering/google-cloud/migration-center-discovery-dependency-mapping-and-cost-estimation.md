---
id: computing-software.cloud-infrastructure-engineering.google-cloud.migration-center-discovery-dependency-mapping-and-cost-estimation
name: migration-center-discovery-dependency-mapping-and-cost-estimation
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, migration-center, workload-assessment, application-dependency-mapping, migration-cost-estimation, tco-calculator, database-migration-planning, migration-waves]
level: practitioner
status: draft
description: "Plan a migration with Migration Center: discover servers and databases, map dependencies into move groups, produce cost and TCO estimates, and plan database migrations by engine and downtime."
sources: ["https://cloud.google.com/migration-center/docs/migration-center-overview", "https://cloud.google.com/migration-center/docs/discovery-client-overview", "https://cloud.google.com/migration-center/docs/create-pricing-report", "https://cloud.google.com/migration-center/docs/database-assessment", "https://cloud.google.com/architecture/migration-to-gcp-assessing-and-discovering-your-workloads"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration Center: discovery, dependency mapping and cost

## 1. Discover
- **Discovery client** (`mcdc`, runs on a Windows/Linux host on-prem): scans vCenter, Windows/Linux guests (WMI/SSH) for specs, utilisation and **network connections**.
- Or import CMDB/RVTools/CSV exports for a quick first pass (no dependencies).
- Collect at least 2–4 weeks of performance data so sizing reflects peaks, not averages.

## 2. Map dependencies into move groups
Use collected connections (process ↔ port ↔ remote host) to build groups that must move together
(app + its DB + its batch servers). Rules of thumb:
- Chatty, low-latency pairs move in the same wave.
- Shared services (AD, DNS, file shares, monitoring) move first or get hybrid connectivity early.
- Record owners and business windows per group; that's your wave plan.

## 3. Cost and TCO
In Migration Center create **asset groups** and **preference sets** (target region, machine series,
commitment term, OS licensing, sole-tenancy for BYOL), then a **pricing report** and a **TCO report**
comparing current on-prem costs (hardware, power, licences, staff) against Google Cloud. Validate a
few line items in the Google Cloud Pricing Calculator. Include egress, hybrid connectivity,
migration tooling, dual-running months and training.

## 4. Database migration planning
Database assessment (SQL Server, MySQL, PostgreSQL, Oracle collectors) reports sizes, features in
use and compatibility per target (Cloud SQL, AlloyDB, Spanner, Bare Metal for Oracle). For each DB decide:
| Question | Drives |
|---|---|
| Allowed downtime | offline dump/restore vs DMS continuous replication |
| Engine change? | heterogeneous (schema conversion, app changes) vs homogeneous |
| Size and change rate | network bandwidth, initial load duration |
| Features (CLR, linked servers, PL/SQL packages) | target choice or refactor |

## Gotchas
- Sizing from allocated (not used) resources overspends; use the utilisation-based recommendation.
- Discovery traffic and credentials need security approval early — it's often the longest lead time.
- Licence-included vs BYOL changes TCO dramatically for Windows/SQL Server.

## Verify
- [ ] Every in-scope server is in exactly one move group with an owner and wave.
- [ ] TCO report reviewed with finance; assumptions documented.
