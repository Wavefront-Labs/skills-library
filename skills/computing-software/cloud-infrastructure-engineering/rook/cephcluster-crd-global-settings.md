---
id: computing-software.cloud-infrastructure-engineering.rook.cephcluster-crd-global-settings
name: cephcluster-crd-global-settings
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [cephcluster, cephversion, datadirhostpath, skipupgradechecks, allowunsupported]
level: practitioner
status: docs-checked
description: "Core CephCluster spec settings: cephVersion image pinning, allowUnsupported, dataDirHostPath rules and the upgrade-check flags."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/ceph-cluster-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The CephCluster CR has four modes: host storage, PVC storage, stretched, and external. The `name` is usually the same as the namespace because multiple clusters cannot share a namespace; clusters in one Kubernetes cluster must not have conflicting devices or host paths.

Key fields:
- `cephVersion.image`: the Ceph daemon image, for example `quay.io/ceph/ceph:v20.2.4`. Pin a specific version in production. A general tag such as `v19` moves with each Squid build and can leave different nodes on different versions.
- `cephVersion.allowUnsupported`: allows an unsupported major release. Squid and Tentacle are supported; keep this false in production.
- `cephVersion.imagePullPolicy`: Always, IfNotPresent or Never; default IfNotPresent.
- `dataDirHostPath`: host path for config and data. It must be unique per cluster, is created if missing, and persists after pods are deleted. Never use `/etc/ceph`, `/rook` or `/var/log/ceph` or their subpaths. If empty, pods use ephemeral directories. After deleting a test cluster, wipe this path before starting a new one or the new mons fail on stale keys.
- `skipUpgradeChecks`: skip upgrade checks at your own risk.
- `continueUpgradeAfterChecksEvenIfNotHealthy`: continue OSD or MDS upgrade even when PGs are not clean.
- `upgradeOSDRequiresHealthyPGs`: hold OSD upgrade until PGs are healthy.

Image tags: `vRELNUM`, `vRELNUM.Y`, `vRELNUM.Y.Z` and `vRELNUM.Y.Z-YYYYMMDD` for a specific build.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-cluster-crd) against this skill: 18 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 2 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
