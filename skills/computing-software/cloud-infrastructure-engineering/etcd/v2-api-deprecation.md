---
id: computing-software.cloud-infrastructure-engineering.etcd.v2-api-deprecation
name: v2-api-deprecation
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [v2, enable-v2, v2-deprecation, v2-store, migration, deprecated, proxy-mode]
level: intro
status: docs-checked
description: "The deprecated etcd v2 API: --enable-v2 default false, --v2-deprecation phases and moving to v3."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
  - "https://etcd.io/docs/v3.5/upgrades/upgrade_3_4/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The v2 API (the HTTP directory tree store) is deprecated. Facts from the docs:

- `--enable-v2` defaults to false since 3.4. When false, the member does not serve the v2 API.
- `--v2-deprecation` selects the phase of v2store deprecation; `not-yet` (default in 3.5) issues a warning if the v2store has meaningful content; `write-only` disallows custom v2 state (default in v3.6 and v3.7); `write-only-skip-check` ignores custom v2 state if present (available in v3.5.32+, v3.6.13+, v3.7.0+, use at your own risk); `write-only-drop-data` deletes custom v2 state (planned default in v3.8). `--enable-v2` is deprecated and to be decommissioned in v3.6.
- The `etcdctl` default in 3.4 and later is `ETCDCTL_API=3`.
- `etcdctl snapshot` only backs up v3 data; v2 data needs its own backup.
- `--experimental-enable-v2v3` (serve v2 requests through the v3 backend under a prefix) is also deprecated and to be decommissioned in v3.6.

Migration approach: stop writing through v2, export your v2 data, write it into v3 keys with a script (mapping directories to key prefixes), verify, then keep `--enable-v2` off and pick a `--v2-deprecation` phase.

v2 commands such as `etcdctl set` need `ETCDCTL_API=2` (the 3.4 upgrade guide shows `ETCDCTL_API=2 etcdctl set foo bar`).

Do not enable v2 in new deployments.

## Checked

2026-11-03. Confirmed on the v3.5 op-guide configuration page: --enable-v2 default false and deprecation for v3.6, --v2-deprecation phases and their defaults, --experimental-enable-v2v3. Confirmed on the upgrade_3_4 guide: enable-v2 false default, ETCDCTL_API=3 default, ETCDCTL_API=2 etcdctl set example, snapshot backs up only v3 data. Removed: the v2-migration source (404), the separate-keyspace, snap-file storage, Kubernetes and v2-auth-open claims, the nonexistent gone phase and the unverified ls --recursive command.

Method: documentation only; no commands were run.
