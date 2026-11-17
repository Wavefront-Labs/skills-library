---
id: computing-software.database-administration.cloudnative-pg.pooler-monitoring-pause-and-limitations
name: pooler-monitoring-pause-and-limitations
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [pooler, pgbouncer, podmonitor, metrics, pause, resume, enablepodmonitor, limitations]
level: advanced
status: docs-checked
description: "Monitor a PgBouncer Pooler with the port 9127 exporter and a manual PodMonitor, enable metrics TLS, pause and resume connections around switchover, and know its limits."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/connection_pooling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The pooler exporter listens on port `9127` of each pod and exposes `cnpg_pgbouncer_` metrics from `SHOW LISTS`, `SHOW POOLS` and `SHOW STATS` plus `go_*` runtime metrics. Useful signal: `cnpg_pgbouncer_pools_maxwait` growing means the server pool is too small or the server is overloaded. PgBouncer's own `log_stats` is off by default for this reason.

`.spec.monitoring.enablePodMonitor` is **deprecated**. Set it to `false` and create your own:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: <POOLER_NAME>
spec:
  selector:
    matchLabels:
      cnpg.io/poolerName: <POOLER_NAME>
  podMetricsEndpoints:
  - port: metrics
```

Serve metrics over HTTPS with `.spec.monitoring.tls.enabled: true`; the cluster server certificate is used, or `.spec.pgbouncer.clientTLSSecret` if set, reloaded on each handshake. The generated PodMonitor scrapes with `insecureSkipVerify=true` because pod IPs are usually not in the SANs and it is overwritten on every reconcile, so for strict verification manage the PodMonitor yourself.

**Pausing.** `spec.pgbouncer.paused: true` runs PgBouncer `PAUSE`: active queries complete, server connections close, new client connections wait. Setting it back to `false` runs `RESUME`. Until switchover integrates this natively, set `paused: true`, run the switchover with the `cnpg` plugin, then set `false`.

**Limitations.** A pooler serves one cluster only. The operator manages TLS, authentication, `databases` and `users` sections, and only listed options are configurable; values are passed to PgBouncer unvalidated, so a bad value can crash-loop every pod.

## Checked

2026-11-04. Exporter port and prefixes, PodMonitor example, TLS options, paused behaviour and limitations confirmed on the Connection pooling page.

Method: documentation only; no commands were run.
