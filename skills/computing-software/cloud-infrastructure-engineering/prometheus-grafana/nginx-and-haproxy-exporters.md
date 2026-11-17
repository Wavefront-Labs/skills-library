---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.nginx-and-haproxy-exporters
name: nginx-and-haproxy-exporters
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [nginx-exporter, haproxy-exporter, exporters, stub-status, load-balancer-metrics, prometheus]
level: practitioner
status: docs-checked
description: "Get metrics from NGINX (stub_status exporter, NGINX Plus mode, log-based alternatives) and HAProxy (built-in Prometheus exporter) with the key queries for each."
sources: ["https://github.com/nginx/nginx-prometheus-exporter", "https://www.haproxy.com/documentation/haproxy-configuration-tutorials/alerts-and-monitoring/prometheus/", "https://nginx.org/en/docs/http/ngx_http_stub_status_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NGINX and HAProxy exporters

## NGINX (open source)
The stub_status module is not built by default (`--with-http_stub_status_module`). Enable it on a local-only location:
```nginx
server { listen 127.0.0.1:8080; location = /stub_status { stub_status; } }
```
Run the exporter (default listen `:9113`, path `/metrics`):
```bash
nginx-prometheus-exporter --nginx.scrape-uri=http://127.0.0.1:8080/stub_status
```
Metrics: `nginx_up`, `nginx_connections_active`, `nginx_connections_reading`, `nginx_connections_writing`,
`nginx_connections_waiting`, `nginx_connections_accepted`, `nginx_connections_handled`, `nginx_http_requests_total`.
stub_status gives connection and request counters only. NGINX Plus has a richer API: start the exporter with
`--nginx.plus` and the API URI as `--nginx.scrape-uri` (metrics are then `nginxplus_*`). For per-status-code and
latency (RED) metrics on open source NGINX, use an ingress controller's own metrics or parse access logs
(Loki recording rules / mtail).
```promql
rate(nginx_connections_accepted[5m]) - rate(nginx_connections_handled[5m])   # dropped connections (e.g. worker_connections limit)
```

## HAProxy (2.0+ built-in exporter)
Available since HAProxy 2.0. Add a frontend with the `prometheus-exporter` service:
```haproxy
frontend prometheus
  bind :8405
  mode http
  http-request use-service prometheus-exporter if { path /metrics }
  no log
```
Key metrics:
```promql
sum by (proxy) (rate(haproxy_backend_http_responses_total{code="5xx"}[5m]))
  / sum by (proxy) (rate(haproxy_backend_http_responses_total[5m]))
haproxy_backend_active_servers                    # active servers per backend
increase(haproxy_server_check_failures_total[5m]) > 0   # failing health checks
haproxy_backend_current_queue > 0                 # requests queued: saturation
haproxy_backend_response_time_average_seconds    # average of the last 1024 successful connections, not a histogram
```

## Gotchas
- Server-level metrics multiply by servers x backends; check the output size on large configs.
- NGINX stub_status must not be public.

## Verify
- [ ] 5xx ratio panel moves when a backend returns errors in a test.

## Checked
2026-10-31. Confirmed against the nginx-prometheus-exporter README (metric names, `--nginx.plus`, `--nginx.scrape-uri`,
port 9113 and /metrics), the nginx stub_status module page (build flag, handled vs accepted and worker_connections)
and the HAProxy Prometheus tutorial (2.0 availability, `use-service prometheus-exporter`, metric names and labels,
response-time average over 1024 connections). Removed: the claim that the standalone haproxy_exporter is deprecated,
the `?scope=` filter, and VTS / ingress-nginx mentions (not on the cited pages).
Method: documentation only; no commands were run.
