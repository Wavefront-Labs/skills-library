---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.windows-server-sql-licensing
name: windows-server-sql-licensing
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [windows-server-sql-licensing, microsoft-licensing, windows server, sql server, cal, core licence, datacenter, standard edition, hybrid benefit, itam-licence-compliance]
level: advanced
status: draft
description: "License Windows Server and SQL Server by cores with minimums, CALs, editions and virtualisation rights."
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

# Windows Server and SQL Server licensing

Goal: correct core counts and edition choice.

Windows Server (2016+): license all physical cores of the host, minimum 8 cores per processor and 16 per server; Standard grants two OSEs (VMs) per fully licensed host, Datacenter unlimited. Add Windows Server CALs for users or devices.
SQL Server: per core (minimum 4 cores per VM/processor; confirm), or Server + CAL for Standard. Enterprise licensed with Software Assurance allows unlimited VMs on a fully licensed host.
Azure Hybrid Benefit: use existing licences with Software Assurance for Azure VMs (conditions apply; confirm).

Method: inventory host cores, VM counts, edition and features used; choose Datacenter once VM density exceeds roughly 10-12 on a host (confirm by pricing).

Gotchas:
- Developer edition is for non-production only.
- Per-VM core licences require SA to move.

Verify: recompute for one cluster and compare.
