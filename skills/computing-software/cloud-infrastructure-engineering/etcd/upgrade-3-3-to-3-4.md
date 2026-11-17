---
id: computing-software.cloud-infrastructure-engineering.etcd.upgrade-3-3-to-3-4
name: upgrade-3-3-to-3-4
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [upgrade, v3-4, enable-v2, log-outputs, ca-file, deprecated-flags, rolling-upgrade]
level: advanced
status: docs-checked
description: "Notable 3.3 to 3.4 upgrade changes: v2 API off by default, --ca-file deprecated, --log-output renamed and the learner member."
sources:
  - "https://etcd.io/docs/v3.5/upgrades/upgrade_3_4/"
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The 3.4 guide lists changes to review before a rolling upgrade from 3.3.

Defaults and flags:

- `--enable-v2` now defaults to false. Enable it explicitly only if you still use the v2 store (a deprecated API), and plan to migrate data. `--v2-deprecation` (default `not-yet` in 3.5) sets the phase of v2store deprecation.
- `--ca-file` and `--peer-ca-file` are deprecated; use `--trusted-ca-file` and `--peer-trusted-ca-file`.
- `--log-output` is replaced by `--log-outputs`.
- `--logger` selects `zap` (structured) over the legacy `capnslog`.
- `ETCDCTL_API=3` is now the `etcdctl` default.

Procedure: check cluster health with `etcdctl endpoint health`, download a snapshot backup from the leader, then one by one stop each 3.3 process and replace it with a 3.4 process. If all members are 3.4 the cluster is 3.4 and downgrade from that state is not possible; with any member still on 3.3 you can return to 3.3 binaries. With a v2 data set over 50MB, wait about 2 minutes between members.

Clients: the new Go client balancer uses an asynchronous resolver, so a v3.4 client requires the `grpc.WithBlock` dial option to wait until the connection is up. Some metrics were promoted out of the experimental `etcd_debugging_*` namespace (for example `etcd_debugging_mvcc_put_total` to `etcd_mvcc_put_total`); the old names are still served in 3.4 and fully deprecated in 3.5, so check dashboards and alerts.

The snapshot command only backs up v3 data; v2 data needs its own backup.

## Checked

2026-11-03. Confirmed on the v3.5 upgrade_3_4 guide: --enable-v2 false default, ETCDCTL_API=3 default, --ca-file and --peer-ca-file deprecated in favour of --trusted-ca-file and --peer-trusted-ca-file, --log-output renamed --log-outputs with zap supporting multiple outputs and capnslog deprecated in 3.5, grpc.WithBlock requirement, etcd_debugging_* metric promotion, rolling-upgrade procedure, health check, snapshot backup, 50MB v2 and 2 minute wait, no downgrade once all members are 3.4. --v2-deprecation default not-yet confirmed on the op-guide configuration page. Removed: learner/pre-vote/etcdutl feature list, CommonName claim and endpoint status step (not on the page).

Method: documentation only; no commands were run.
