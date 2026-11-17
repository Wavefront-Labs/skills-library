---
id: computing-software.cloud-infrastructure-engineering.rook.cephcluster-crd-mon-settings
name: cephcluster-crd-mon-settings
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [mon, count, allowmultiplepernode, volumeclaimtemplate, failuredomainlabel, quorum]
level: advanced
status: docs-checked
description: "Configure the Ceph mon count, quorum maths, PVC-backed mons, zones and the mon health check interval in the CephCluster CR."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/ceph-cluster-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`mon.count` sets how many mons start, from 1 to 9, and 3 is the common recommendation. An odd count gives the highest availability. An even count can add durability against mon loss, but availability may be lower. A majority must be up: two of three, three of four, both of two. If quorum is lost, follow the disaster recovery guide to restore it from a single mon.

Other fields:
- `allowMultiplePerNode`: default false; only true in test environments.
- `volumeClaimTemplate`: creates PVCs for mon storage instead of hostPath mounts. Only the `storageClassName` and the storage request and limit are used. The default request is 10Gi, and the storage class should use `volumeBindingMode: WaitForFirstConsumer`. It only affects new mons created when the count grows or a mon is recreated after failure.
- `failureDomainLabel`: the topology label expected on nodes; an alternative to a topologySpreadConstraints rule in placement.
- `externalMonIDs`: IDs of mons outside Rook that Rook must not remove from quorum. Local clusters in normal mode only.
- `zones`: at least three failure-domain names, each with its own optional `volumeClaimTemplate`. When used, zone settings take precedence over mon placement.

When these settings change, the operator updates the mon count during its periodic mon health check, by default every 45 seconds. Health intervals should be short enough to protect quorum yet long enough to ignore network blips.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-cluster-crd) against this skill: 9 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
