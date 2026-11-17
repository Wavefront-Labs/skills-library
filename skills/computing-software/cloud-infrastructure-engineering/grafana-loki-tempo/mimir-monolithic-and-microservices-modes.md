---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.mimir-monolithic-and-microservices-modes
name: mimir-monolithic-and-microservices-modes
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [mimir-deployment-modes, mimir, monolithic-mode, microservices-mode, target-flag, components]
level: practitioner
status: docs-checked
description: "Choose Mimir monolithic or microservices deployment mode and run components with the -target flag."
sources: ["https://grafana.com/docs/mimir/latest/references/architecture/deployment-modes/", "https://grafana.com/docs/mimir/latest/references/http-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: right-size operational complexity for your scale. The documented modes are monolithic and microservices, selected with `-target` (CLI flag or YAML).

- Monolithic: `-target=all` runs all required components in one process. Suited to getting started and development. `./mimir -modules` lists the components that run. Scale horizontally by running more `-target=all` replicas for availability and scale without microservices configuration; not recommended for large-scale deployments because every component scales together.
- Microservices: each component is its own process with `-target=<component>` (for example `-target=ingester`, `-target=distributor`). You must deploy every required component. Recommended for production; it gives independent scaling and granular failure domains. Deploy it on Kubernetes with the `mimir-distributed` Helm chart.

```
mimir -config.file=/etc/mimir/mimir.yaml -target=all
mimir -config.file=/etc/mimir/mimir.yaml -target=ingester
```

Gotchas
- Even in microservices mode the read path (query-frontend, querier, store-gateway) depends on a healthy ring: queriers consult the hash ring to find ingesters, so unhealthy write components can make queries for recent data fail. True read/write isolation needs zone-aware replication and careful ring settings.
- Two architectures exist (classic and ingest storage); see the Mimir architecture page before choosing.

## Verify
`GET /ready` is the readiness probe and `GET /services` shows a page with the status of Mimir's internal services.

## Checked
2026-11-03. Confirmed against the Mimir deployment modes page and the HTTP API index (`/ready`, `/services`). Removed: the "read-write mode" with `-target=read|write|backend` (not in the docs), the single-node filesystem command line, the component data-flow paragraph, the "at least 3 ingesters" and "moving modes later" claims, and the memberlist-for-replicas remark.
Method: documentation only; no commands were run.
