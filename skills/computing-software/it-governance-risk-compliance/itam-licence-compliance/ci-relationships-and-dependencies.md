---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.ci-relationships-and-dependencies
name: ci-relationships-and-dependencies
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [ci-relationships-and-dependencies, configuration-management-cmdb, service mapping, dependency, ci relationship, topology, impact analysis, itam-licence-compliance]
level: advanced
status: draft
description: "Model CI relationships and map applications to infrastructure for impact analysis and licence metrics."
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

# CI relationships and service mapping

Goal: answer which services and licences break if a CI changes.

Method:
- Use typed relationships: runs on, depends on, hosted by, connects to, member of cluster.
- Populate from discovery (network flows, process-to-port maps) then curate business service tops.
- For licensing, relate software installations to host, host to cluster/host server (needed for Oracle and per-core metrics).
- Review relationship accuracy after each major release.

Gotchas:
- Auto-discovered maps include noise; filter to business-relevant ports.
- Cloud autoscaling creates churn; use tags/labels as stable service keys.

Verify: trace a sampled app to its host cluster and confirm in the hypervisor console.
