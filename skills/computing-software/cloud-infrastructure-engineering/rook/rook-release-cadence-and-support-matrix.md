---
id: computing-software.cloud-infrastructure-engineering.rook.rook-release-cadence-and-support-matrix
name: rook-release-cadence-and-support-matrix
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [maintenance, support-matrix, release-cadence, ceph-versions, tentacle]
level: intro
status: docs-checked
description: "Rook release cadence, which minor versions are maintained, and the Kubernetes and Ceph versions each Rook series supports."
sources:
  - https://rook.io/docs/rook/latest-release/Getting-Started/maintenance-and-support/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cadence stated on the Maintenance and Support page:
- A new minor version is planned three times a year, roughly every four months.
- The two most recent minor releases are actively maintained.
- Patch releases for the latest minor are typically bi-weekly, and urgent patches may come sooner.
- Patches for the previous minor are commonly monthly, varying with urgency.

Maintenance means relevant fixes merged to the main branch are eligible for back-porting to a maintained release branch. It carries no SLA on response time.

Supported versions at release time (the table notes patch releases can extend support):
- Rook 1.21: Kubernetes v1.32 to v1.37; Ceph Squid v19.2.0+ and Tentacle v20.2.1+
- Rook 1.20: Kubernetes v1.31 to v1.37; Squid v19.2.0+, Tentacle v20.2.1+
- Rook 1.19: Kubernetes v1.30 to v1.35; Squid v19.2.0+, Tentacle v20.2.1+
- Rook 1.18: Kubernetes v1.29 to v1.34; Reef v18.2.0+, Squid, Tentacle v20.2.0+

For the current release the authoritative sources are the Prerequisites page for Kubernetes and the Ceph Upgrade guide for Ceph.

Rook expects to support the most recent six Kubernetes versions. Ceph Tentacle v20.2.0 is not recommended because of a known data-corruption issue when the read affinity feature is enabled; use v20.2.1 or newer.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (maintenance-and-support) against this skill: 11 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
