---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.user-device-core-metrics
name: user-device-core-metrics
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [user-device-core-metrics, licence-metrics-and-rights, named user, concurrent user, per device, per core, per socket, core factor, metric, itam-licence-compliance]
level: practitioner
status: draft
description: "Count licences by named user, concurrent user, device, processor core and socket and apply core factors correctly."
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

# User, device, core and processor metrics

Goal: pick and count the right metric.

Common metrics:
- Named user: a person, regardless of devices; reuse reassignment rules matter.
- Concurrent: peak simultaneous use; needs usage metering.
- Device: each installed or accessing endpoint.
- Processor/core: physical or virtual cores, often times a core factor (Oracle core factor table, per processor type) with minimum counts per processor (e.g. 2 or 4 cores for Windows Server/SQL Server per CPU; confirm current terms).
- Socket: per physical CPU (VMware historically; terms changed with Broadcom, confirm).

Method: record metric per product in the entitlement and compute demand from discovery.

Gotchas:
- Multiplexing (pooling users via a front end) can still require licences per end user.
- Hyperthreading may or may not count.

Verify: recompute a sample server by hand.
