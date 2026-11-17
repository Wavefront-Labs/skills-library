---
id: computing-software.systems-network-administration.immich.monitoring-prometheus-grafana
name: monitoring-prometheus-grafana
category: computing-software
field: systems-network-administration
product: immich
tags: [prometheus, grafana, telemetry, metrics, immich-telemetry-include]
level: practitioner
status: docs-checked
description: "Expose Immich Prometheus metrics with IMMICH_TELEMETRY_INCLUDE, scrape them with a Prometheus container, and add Grafana in Docker Compose."
sources:
  - https://docs.immich.app/features/monitoring
  - https://docs.immich.app/install/environment-variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: collect Immich performance metrics locally. The feature is opt-in and sends nothing beyond what you configure.

Metric groups: API (endpoint calls and response times), host (memory and CPU), IO (database queries, image processing) and `repo`/`job`. Each group can be switched on or off independently.

Enable the endpoint in `.env`:

```
IMMICH_TELEMETRY_INCLUDE=all
```

Or list groups, for example `IMMICH_TELEMETRY_INCLUDE=repo,api`. `IMMICH_TELEMETRY_EXCLUDE` does the reverse. The valid groups are `host`, `api`, `io`, `repo` and `job`, and only the server container reads these.

Add Prometheus to the compose file:

```yaml
immich-prometheus:
  container_name: immich_prometheus
  ports:
    - 9090:9090
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
    - prometheus-data:/prometheus
```

Declare `prometheus-data` under `volumes:`, and download the `prometheus.yml` linked from the docs page into the compose folder. Run `docker compose down` then `docker compose up -d`.

To inspect raw metrics, publish ports `8081:8081` (API) and `8082:8082` (microservices) on `immich_server` and visit `/metrics`. Change them with `IMMICH_API_METRICS_PORT` and `IMMICH_MICROSERVICES_METRICS_PORT`.

For dashboards, add a Grafana service (`image: grafana/grafana`, port 3000, `command: ['./run.sh', '-disable-reporting']`, volume `grafana-data:/var/lib/grafana`). First login is `admin` / `admin`; change the password, then add a data source pointing at `http://immich-prometheus:9090`.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading features/monitoring in full (Prometheus, Grafana) and the Prometheus and General tables in install/environment-variables.
Reworded: the prometheus.yml source and the Grafana data source URL, to match the page.
Method: documentation only; no commands were run.
