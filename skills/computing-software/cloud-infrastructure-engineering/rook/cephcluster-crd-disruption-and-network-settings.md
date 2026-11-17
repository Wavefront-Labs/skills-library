---
id: computing-software.cloud-infrastructure-engineering.rook.cephcluster-crd-disruption-and-network-settings
name: cephcluster-crd-disruption-and-network-settings
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [disruptionmanagement, managepodbudgets, osdmaintenancetimeout, network, multus, addressranges, ipfamily]
level: advanced
status: docs-checked
description: "PodDisruptionBudget management, drain timeout and the network provider, selectors, address ranges and IP family fields of the CephCluster CR."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/ceph-cluster-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Disruption management, under `spec.disruptionManagement`:
- `managePodBudgets`: when true the operator creates and manages PodDisruptionBudgets for OSD, Mon, RGW and MDS daemons. By default it blocks eviction of OSDs and unblocks them safely when drains are detected.
- `osdMaintenanceTimeout`: minutes that a whole failure domain (region, zone or host) is held in `noout` while draining, in addition to the default DOWN/OUT interval. Default 30.
- `pgHealthyRegex`: regular expression deciding which PG states count as healthy.

Network settings, under `spec.network`; if unspecified the default SDN is used:
- `provider`: `host` or `multus`.
- `selectors` (multus only): choose the NetworkAttachmentDefinitions for the `public` and `cluster` networks.
- `addressRanges` (host or multus): override the CIDR lists Ceph listens on, `public` and `cluster`.
- `ipFamily`: the network stack Ceph daemons listen on.
- `dualStack`: listen on both IPv4 and IPv6.
- `connections`: connection-level settings such as encryption and compression.

Related fields in the same spec: `cleanupPolicy`, `security` for key management, `cephConfig` and `cephConfigFromSecret` to set Ceph options through the mon config store, and `csi` for CSI driver options.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-cluster-crd) against this skill: 21 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 1 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
