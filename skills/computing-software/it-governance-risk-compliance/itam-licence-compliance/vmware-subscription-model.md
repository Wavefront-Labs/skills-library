---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.vmware-subscription-model
name: vmware-subscription-model
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [vmware-subscription-model, vmware-broadcom-licensing, vmware, broadcom, vcf, vsphere foundation, per core subscription, perpetual end, vcenter, itam-licence-compliance]
level: advanced
status: draft
description: "Understand the move to subscription bundles, per-core pricing with minimum cores and the end of perpetual sales."
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

# VMware subscription model after Broadcom

Goal: plan renewal and cost impact.

Key points (confirm with current Broadcom terms because they change):
- Perpetual licences stopped being sold in late 2023; products shifted to subscription bundles such as VMware Cloud Foundation and vSphere Foundation.
- Licensing is per physical CPU core with a minimum core count per CPU (16 cores per CPU at the time of the change; confirm).
- Support for perpetual licences ended or required renewal into subscription.
- Customers may have to count all cores on hosts, not VMs.

Method: inventory hosts, CPUs, core counts, clusters, features used (vSAN, NSX), then price bundles and alternatives.

Gotchas:
- Features split across bundles; do not buy larger bundles than needed.
- Cost uplift occurs when hosts have many low-core CPUs because of minimums.

Verify: renewal quote lines match the host inventory.
