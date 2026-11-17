---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.virtual-machine-sprawl
name: virtual-machine-sprawl
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [virtual-machine-sprawl, cloud-and-virtual-asset-management, vm sprawl, orphaned resources, rightsizing, idle instances, snapshots, scheduling, itam-licence-compliance]
level: practitioner
status: draft
description: "Find idle VMs, orphaned disks and snapshots, and rightsize or schedule them to cut spend and licence exposure."
sources:
  - https://www.iso.org/standard/68291.html
  - https://spdx.github.io/spdx-spec/
  - https://cyclonedx.org/specification/overview/
  - https://www.ntia.gov/page/software-bill-materials
  - https://openchainproject.org/
  - https://reuse.software/spec/
  - https://opensource.org/licenses
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VM sprawl, orphaned resources and rightsizing

Goal: reduce waste and licence consumption from forgotten resources.

Method:
- Query for VMs with CPU under 5% over 14 days, unattached disks, old snapshots, unused IPs and load balancers.
- Use cloud tools (AWS Compute Optimizer, Azure Advisor, GCP Recommender) for rightsizing suggestions.
- Apply start/stop schedules to non-production; set expiry tags.
- For licensed workloads (SQL Server, Oracle, Windows), each idle VM still consumes licence or costs licence-included price.

Gotchas:
- Rightsizing must respect licensing core minimums (confirm vendor rules).
- Delete with a hold period and backup for safety.

Verify: monthly waste report with trend and savings realised.
