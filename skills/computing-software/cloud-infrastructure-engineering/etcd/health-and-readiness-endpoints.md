---
id: computing-software.cloud-infrastructure-engineering.etcd.health-and-readiness-endpoints
name: health-and-readiness-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [health, livez, readyz, health-check, probes, load-balancer, kubernetes-probes]
level: practitioner
status: docs-checked
description: "Check etcd member health over HTTP: /health on metrics URLs, and /livez and /readyz with verbose and exclude parameters."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/monitoring/"
  - "https://etcd.io/docs/v3.5/faq/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Health endpoints, per the monitoring page:

- `/health`: since v3.3.0, any location given by `--listen-metrics-urls` also answers `/health`, in addition to `/metrics`. This helps when the standard endpoint requires mutual (client) TLS but a load balancer or monitoring service still needs the health check.
- `/livez` and `/readyz`, added in v3.5.12. `/livez` reflects whether the process is alive or needs a restart; `/readyz` reflects whether it is ready to serve traffic.
- Each of these endpoints runs several individual checks. Add the `verbose` parameter to print each check and its status; the example output lists `data_corruption`, `serializable_read` and `linearizable_read`. Exclude a check with `?exclude=data_corruption`.

```bash
curl -k "http://localhost:2379/readyz?verbose"
curl -k "http://localhost:2379/readyz?exclude=data_corruption"
```

Use `/livez` as a liveness probe and `/readyz` as a readiness probe or load-balancer check, matching the definitions above.

With `--log-level=debug` the server exports debugging information on its client port under `/debug` (including `/debug/pprof`); expect degraded performance and verbose logging.

## Checked

2026-11-08. Read in full: etcd v3.5 Monitoring etcd page and FAQ page. Confirmed /health on --listen-metrics-urls since v3.3.0, /livez and /readyz since v3.5.12, verbose and exclude parameters, the check names and the /debug note. Removed: the /health JSON body, the etcdctl endpoint health line, RBAC and client-certificate claims, the lack-of-quorum restart rationale and the --enable-pprof flag (not on the cited pages).
Method: documentation only; no commands were run.
