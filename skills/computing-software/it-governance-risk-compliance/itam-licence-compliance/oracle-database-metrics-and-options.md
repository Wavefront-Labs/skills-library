---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.oracle-database-metrics-and-options
name: oracle-database-metrics-and-options
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [oracle-database-metrics-and-options, oracle-licensing, oracle database, processor licence, named user plus, core factor, diagnostics pack, tuning pack, options, itam-licence-compliance]
level: advanced
status: draft
description: "Count Oracle Database by Processor with the core factor or Named User Plus and detect options and management packs in use."
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

# Oracle Database metrics, editions and options

Goal: accurate Oracle position.

- Processor metric: number of cores x core factor (Oracle core factor table; x86 usually 0.5) rounded up.
- Named User Plus: minimum per processor (25 for Enterprise Edition, 10 for Standard Edition; confirm current rules).
- Edition limits: Standard Edition 2 has socket limits (confirm current).
- Options and packs (Partitioning, Advanced Compression, Diagnostics, Tuning, RAC): each is separately licensed; use of the features even by accident may be counted.

Method: run Oracle's feature usage (DBA_FEATURE_USAGE_STATISTICS) and LMS scripts under legal review; compare options enabled versus purchased; disable unused options and document.

Gotchas:
- Packs are enabled by default in some Enterprise installations.
- Usage statistics reflect history even if feature is disabled now.

Verify: option usage report signed by the DBA owner.
