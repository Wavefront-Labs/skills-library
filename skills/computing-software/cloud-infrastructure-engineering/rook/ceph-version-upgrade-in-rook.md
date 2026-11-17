---
id: computing-software.cloud-infrastructure-engineering.rook.ceph-version-upgrade-in-rook
name: ceph-version-upgrade-in-rook
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [ceph-upgrade, cephversion-image, rolling-upgrade, tentacle, squid, health-err]
level: advanced
status: docs-checked
description: "Upgrade Ceph through the CephCluster image: the daemon-by-daemon checks, supported versions, HEALTH_ERR refusal and image tagging advice."
sources:
  - https://rook.io/docs/rook/latest-release/Upgrade/ceph-upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rook performs Ceph upgrades in a rolling fashion so application pods are not disrupted. When the Ceph image in the CR changes, Rook goes through the daemons one by one: it checks a daemon can be stopped, updates its deployment, then waits for things to settle (mons in quorum, PGs clean for OSDs, MDSes up) before the next. Storage may still be unavailable for short periods, and the page warns of risk including data loss, so read it fully.

Supported in the documented release:
- Ceph Squid v19.2.0 or newer.
- Ceph Tentacle v20.2.1 or newer. Disabling the rook mgr module before upgrading to Tentacle is recommended.
- Squid v19.2.6 and Tentacle v20.2.4 multisite deployments need RGW settings applied before upgrading because of SigV4 hardening; see the multisite documentation.
- Tentacle v20.2.0 is not recommended: a data-corruption issue exists when read affinity (`csi.readAffinity.enabled: true`, disabled by default) is on. Upgrade to v20.2.2 or newer if it is enabled; Rook disables it internally with v20.2.0, and existing applications must be restarted afterward.

If Ceph is in `HEALTH_ERR`, the operator refuses to proceed. The overrides are `skipUpgradeChecks: true` or `continueUpgradeAfterChecksEvenIfNotHealthy: true`, which are unsafe.

Image tags: full version-and-build tags such as `v20.2.2-20260616` are recommended for production because the cluster cannot become heterogeneous. Major tags such as `v20` suit development and test clusters.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-upgrade) against this skill: 12 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
