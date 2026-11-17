---
id: computing-software.ai-ml-engineering.ray.dashboard-and-metrics
name: dashboard-and-metrics
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-metrics, ray-dashboard, prometheus-ray, metrics-export-port]
level: practitioner
status: docs-checked
description: "Use the Ray dashboard and export Prometheus metrics (metrics-export-port, ray metrics launch-prometheus, Grafana dashboards)."
sources:
  - https://docs.ray.io/en/latest/ray-observability/getting-started.html
  - https://docs.ray.io/en/latest/cluster/metrics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dashboard and metrics

```bash
pip install -U "ray[default]"                       # dashboard and metrics need the default install
ray start --head --dashboard-host=0.0.0.0 --metrics-export-port=8080
ray metrics launch-prometheus                       # downloads and starts a local Prometheus (default URL http://localhost:9090)
ray metrics shutdown-prometheus                     # Ray > 2.40; otherwise kill the Prometheus process
```
The dashboard is on port 8265 by default; Ray prints its URL at startup and `ray.init()` returns it as `context.dashboard_url`. Inside a docker container `--dashboard-host` is required (for example `0.0.0.0`). On a cluster started by the VM cluster launcher, KubeRay or by hand, the dashboard port may not be publicly exposed.

Prometheus config: Ray generates one at `/tmp/ray/session_latest/metrics/prometheus/prometheus.yml` (under the `--temp-dir` instead if you set one). It scrapes `/tmp/ray/prom_metrics_service_discovery.json`, a service discovery file on the head node that Ray periodically updates with the address of every node's metrics agent. For a static list of nodes, set a fixed `--metrics-export-port` on all nodes (on KubeRay, `rayStartParams.metrics-export-port`).

Grafana: run Grafana with the built-in config in `/tmp/ray/session_latest/metrics/grafana` (`grafana.ini`), then open dashboards, manage, Ray, Default Dashboard. Ray's dashboard JSON files are in `/tmp/ray/session_latest/metrics/grafana/dashboards`. If Grafana reports the datasource is missing, add a datasource variable whose name equals the `RAY_PROMETHEUS_NAME` environment variable (default `Prometheus`).

## Gotchas
- Plain `ray` without the dashboard component does not export metrics; install `ray[default]`.
- Ray runs a metrics agent per node; each exposes its own Prometheus endpoint, so scrape every node.
- Ray does not provide storage for metrics or start a Prometheus server for you; you manage metric lifecycle yourself.
- The Jobs view shows up to 10K tasks per job; tasks beyond that are not accounted for.
- With docker, symbolic links such as `/tmp/ray/session_latest/metrics` cannot be mounted on shared volumes, so Prometheus and Grafana configs may fail to load.

## Verify
After `ray start --head --metrics-export-port=8080` with Prometheus running, the query `ray_dashboard_api_requests_count_requests_total` returns a series in the Prometheus UI.

## Checked

Method: docs-checked 2026-11-09 against docs.ray.io cluster/metrics and ray-observability/getting-started (downloaded and read); removed custom metrics code, ray list commands, RAY_GRAFANA_HOST and RAY_PROMETHEUS_HOST, the ray_ prefix claim, the state retention figure and the authentication remark, which these pages do not confirm
