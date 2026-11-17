---
id: computing-software.cloud-infrastructure-engineering.calico.typha-scaling-and-configuration
name: typha-scaling-and-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [typha, scale, felix, datastore, configuration, tls, health]
level: practitioner
status: docs-checked
description: "Decide when Typha is needed, how it is configured (env vars or typha.cfg, not editable under the operator), its default ports, health probe quirk and Felix client TLS parameters."
sources:
  - https://docs.tigera.io/calico/latest/reference/typha/overview
  - https://docs.tigera.io/calico/latest/reference/typha/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Typha keeps one datastore connection on behalf of all clients (Felix, confd), caches state and fans deduplicated events out. One Typha can serve hundreds of Felix instances and filters updates irrelevant to Felix, cutting Felix CPU. With the Kubernetes API datastore it is recommended; with etcd it is redundant and not recommended because etcd v3 already handles many clients. Operator installs always install Typha.

**Where configuration lives.** With the operator, Typha configuration cannot be modified. For manifest installs it is read from, in order: environment variables prefixed `TYPHA_`, then the file `/etc/calico/typha.cfg` (override with `-c` or `--config-file`). The first location with a value wins.

Selected parameters and defaults:

| Parameter (env var) | Default / note |
|---|---|
| `DatastoreType` (`TYPHA_DATASTORETYPE`) | `etcdv3`; or `kubernetes` |
| `ServerPort` (`TYPHA_SERVERPORT`) | `5473`, the sync server |
| `HealthEnabled`, `HealthPort`, `HealthHost` | port `9098`, host `localhost` |
| `PrometheusMetricsEnabled` | `false`; port `9091` when on |
| `ShutdownTimeoutSecs` | Should match the pod `terminationGracePeriodSeconds` |

**Health probe trap.** The health endpoint binds to localhost, but kubelet probes the pod IP. The image provides `calico-typha check (readiness|liveness) --port=<port>`; if you change the health port, add `--port=<port>` to both probe commands.

**Felix to Typha TLS.** Typha uses `CAFile`, `ServerCertFile`, `ServerKeyFile`, and requires a value in `ClientCN` or `ClientURISAN` (a SPIFFE string is recommended) once TLS is on; either matching succeeds.

## Checked

2026-11-04. Behaviour, defaults, precedence and the probe note were confirmed on the Typha overview and Configuring Typha pages.

Method: documentation only; no commands were run.
