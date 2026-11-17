---
id: computing-software.cloud-infrastructure-engineering.etcd.configuration-flags-and-precedence
name: configuration-flags-and-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [configuration, flags, environment-variables, config-file, precedence, data-dir, name, listen-client-urls, advertise-client-urls]
level: practitioner
status: docs-checked
description: "Configure etcd with flags, ETCD_ environment variables or a YAML config file, with precedence rules and the core member flags."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

etcd can be configured three ways:

- Command-line flags, for example `--name infra0`.
- Environment variables: the flag name in upper case with underscores and an `ETCD_` prefix, for example `ETCD_NAME`. A flag overrides its environment variable.
- A YAML config file via `--config-file`. If you use it, other flags and environment variables are ignored.

Core member flags:

- `--name`: human-readable member name (default `default`).
- `--data-dir`: data directory (default `${name}.etcd`).
- `--listen-client-urls` (default `http://localhost:2379`) and `--advertise-client-urls`: what clients connect to and what the member tells them.
- `--listen-peer-urls` (default `http://localhost:2380`) and `--initial-advertise-peer-urls`: Raft traffic between members.
- `--initial-cluster`, `--initial-cluster-state` (`new` or `existing`), `--initial-cluster-token`: bootstrap settings.
- `--wal-dir`, `--snapshot-count`, `--max-snapshots`, `--max-wals`.
- `--quota-backend-bytes`, `--max-request-bytes`.
- `--heartbeat-interval`, `--election-timeout`.
- `--auto-compaction-mode`, `--auto-compaction-retention`.
- `--logger`, `--log-level`, `--log-outputs`.

Advertise URLs must be reachable by the intended clients: a common mistake is leaving `--advertise-client-urls` at its default (`http://localhost:2379`) or setting it to localhost when remote clients must reach etcd. The page's flag list may be out of date; run `etcd --help` for the current flags.

Because a config file overrides everything else, mixing sources is risky; pick one per deployment.

## Checked

2026-11-03. Confirmed on the v3.5 configuration options page: three configuration methods, ETCD_ prefix with upper-case snake case, flags take precedence over environment variables, a configuration file causes all flags and environment variables to be ignored, and the listed defaults and flag names (--name default, --data-dir ${name}.etcd, listen client/peer URLs, --initial-cluster-state new or existing, --quota-backend-bytes, --max-request-bytes, --heartbeat-interval, --election-timeout, auto-compaction and logger flags). Removed: the 0.0.0.0 advertise rule and the systemd/container recommendation, which the page does not state.

Method: documentation only; no commands were run.
