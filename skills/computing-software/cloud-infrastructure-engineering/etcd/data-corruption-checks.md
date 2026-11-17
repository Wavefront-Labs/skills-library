---
id: computing-software.cloud-infrastructure-engineering.etcd.data-corruption-checks
name: data-corruption-checks
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [corruption, corrupt-check, initial-corrupt-check, hashkv, corrupt-alarm, data-integrity, experimental]
level: advanced
status: docs-checked
description: "Detect divergence between members with the experimental initial-corrupt-check and corrupt-check-time flags."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
  - "https://etcd.io/docs/v3.5/op-guide/runtime-configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The v3.5 configuration page lists two experimental flags for detecting data corruption:

- `--experimental-initial-corrupt-check` (default `false`): enable to check data corruption before serving any client or peer traffic.
- `--experimental-corrupt-check-time` (default `0s`): duration of time between cluster corruption check passes.

The flag names carry the `experimental-` prefix, so check `etcd --help` and the changelog of your version before relying on them. For replacing a failed or corrupted member, the runtime configuration guide says to remove the member and add a new one in its place, and to migrate its data directory if the cluster holds more than 50MB and the directory is still accessible. Snapshot restore is covered in the disaster recovery guide.

## Checked

2026-11-03. Confirmed on the v3.5 configuration page: --experimental-initial-corrupt-check default false and description, --experimental-corrupt-check-time default 0s and description. Confirmed on the runtime reconfiguration guide: replace a failed member by removing it and adding a new one, and the 50MB data directory migration advice. Removed: the hashkv commands, CORRUPT alarm behaviour and recovery procedure, and the periodic-check leader/follower description, none of which appear on the fetched pages. The upgrade_3_5 source was replaced because it does not mention these flags.

Method: documentation only; no commands were run.
