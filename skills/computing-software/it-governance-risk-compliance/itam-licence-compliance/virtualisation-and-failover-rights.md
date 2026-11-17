---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.virtualisation-and-failover-rights
name: virtualisation-and-failover-rights
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [virtualisation-and-failover-rights, licence-metrics-and-rights, virtualisation licensing, license mobility, dr rights, cold standby, vmotion, cluster licensing, itam-licence-compliance]
level: advanced
status: draft
description: "Interpret licence mobility, cold standby and DR rights when software runs on virtualised or clustered hosts."
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

# Virtualisation, failover and disaster recovery rights

Goal: avoid licensing every host in a cluster by mistake or underlicensing movers.

Check the vendor terms:
- Is licensing by virtual machine, by host, or by cluster?
- Is movement of a VM between hosts permitted, and at what frequency (Microsoft licence mobility rules for server apps with Software Assurance; confirm current terms)?
- Are passive/failover and disaster-recovery copies free (typically cold standby only; confirm ratio and conditions)?
- Does a hypervisor boundary (soft partitioning) count for the vendor (Oracle: not accepted for VMware as partitioning, so the whole cluster may count; confirm in current policy)?

Method: keep a host-to-VM mapping history to show time-bound licence use.

Gotchas:
- vMotion enabled across hosts can drag the whole cluster into scope.
- DR test periods may need limits.

Verify: written vendor confirmation for non-standard readings.
