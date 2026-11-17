---
id: computing-software.cloud-infrastructure-engineering.etcd.upgrade-3-4-to-3-5
name: upgrade-3-4-to-3-5
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [upgrade, rolling-upgrade, v3-5, downgrade, upgrade-checklist, version-skew, migration]
level: advanced
status: docs-checked
description: "Upgrade etcd from 3.4 to 3.5: rolling procedure, backup first, auth caveat and notable changes."
sources:
  - "https://etcd.io/docs/v3.5/upgrades/upgrade_3_5/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Upgrade one minor version at a time. The 3.5 guide's checklist:

1. Requirements: the running cluster must be 3.4 or greater (earlier clusters upgrade to 3.4 first) and healthy. Check with `etcdctl endpoint health`.
2. Test the services that rely on etcd in staging first.
3. Download a snapshot backup from the leader with `etcdctl snapshot save`; it backs up only v3 data. The backup is the downgrade path.
4. Rolling upgrade: one by one, stop a 3.4 member, start the 3.5 binary with the same configuration, and confirm each member and then the cluster is healthy before the next.
5. Mixed versions are supported during the upgrade and the cluster uses the protocol of the lowest common version; it is only considered upgraded once all members run 3.5.

Notable points from the guide:

- A cluster with auth enabled cannot be rolling-upgraded from 3.4 or older, because 3.5 changes the format of WAL entries related to auth.
- With a v2 data set over 50MB, a newly upgraded member may take up to two minutes to catch up, so wait two minutes between members.
- `etcd_debugging_mvcc_*` metrics (db_total_size_in_bytes, put_total, delete_total, txn_total, range_total) were promoted to `etcd_mvcc_*` names and the old names deprecated, which can break dashboards.
- `--logger=capnslog` is deprecated and `--logger=zap` is the default; `--log-output` is deprecated in favour of `--log-outputs`; `--debug` is replaced by `--log-level debug`; `--log-package-levels` and the `/config/local/log` endpoint are deprecated.
- The `/v3beta` gRPC gateway endpoints are removed; use `/v3`.

Downgrade: once all members run 3.5 the cluster is upgraded and downgrade from that state is not possible; while any member is still 3.4 the cluster stays at 3.4 and you can go back to 3.4 binaries. The snapshot backup makes a downgrade possible even after a complete upgrade.

## Checked
2026-11-08: confirmed against the etcd v3.5 upgrade guide, read in full (requirements, preparation, mixed versions, limitations, downgrade, deprecations and the five-step procedure). Removed: the --cluster flag on endpoint health, leader-last advice, the auth workaround, the experimental corrupt-check and watch flags with their defaults, and the etcdutl claim.
Method: documentation only; no commands were run.
