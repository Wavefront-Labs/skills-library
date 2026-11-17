---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.ibm-pvu-metric
name: ibm-pvu-metric
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [ibm-pvu-metric, ibm-licensing, ibm pvu, processor value unit, pvu table, full capacity, sub-capacity, passport advantage, itam-licence-compliance]
level: advanced
status: draft
description: "Calculate Processor Value Units from cores times the PVU table value per processor type and apply sub-capacity rules."
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

# IBM PVU metric and processor values

Goal: right PVU demand for IBM middleware.

Method:
- PVU = number of cores x PVUs per core from IBM's Processor Value Unit table for the processor model (table changes; fetch the current one).
- Full capacity: all cores in the physical server (or all server cores in the cluster for some metrics).
- Sub-capacity: allowed only for eligible virtualisation technologies, licensing the virtual cores available to the product (maximum equals physical cores) and requires ILMT reporting.
- Retain ILMT reports for at least 2 years as the terms require (confirm).

Gotchas:
- Without ILMT on time, you fall back to full capacity.
- Unsupported hypervisors lose sub-capacity eligibility.

Verify: ILMT reports covering every quarter exist and ILMT agent coverage is complete.
