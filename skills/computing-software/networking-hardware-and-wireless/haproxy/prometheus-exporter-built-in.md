---
id: computing-software.networking-hardware-and-wireless.haproxy.prometheus-exporter-built-in
name: prometheus-exporter-built-in
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, prometheus-exporter, haproxy-metrics, use-service, scrape-config]
level: practitioner
status: docs-checked
description: "Enable HAProxy's built-in Prometheus endpoint with http-request use-service prometheus-exporter and scrape the main metric families."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
  - https://raw.githubusercontent.com/haproxy/haproxy/v3.0.0/addons/promex/README
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# prometheus exporter built in
PROMEX is a Prometheus exporter served by HAProxy itself, as a service like the stats applet. It is an optional build component (Makefile `USE_PROMEX=1`), so check your binary: `haproxy -vv` reports `Built with the Prometheus exporter as a service` when it is present. If it is absent, the Prometheus project's separate Go `haproxy_exporter` is the alternative.

Enable it with an `http-request` rule in an HTTP-mode frontend (the README requires HTX support on that proxy):
```
frontend fe_prom
    bind 10.0.0.5:8405
    mode http
    http-request use-service prometheus-exporter if { path /metrics }
```
`use-service` is a final action: no further rules in the set are evaluated. Add that endpoint as a normal static target in a Prometheus scrape job.

Query-string filters reduce the output:
- `scope`: repeat it with `global`, `frontend`, `backend`, `server` or `*`; e.g. `/metrics?scope=frontend&scope=backend`. An empty `scope=` resets earlier scopes (so `?scope=*&scope=` exports nothing). Default is everything.
- `metrics`: comma-separated names to include, or `-name` to exclude, e.g. `/metrics?metrics=-haproxy_server_check_status`. Naming at least one inclusion turns off the default of dumping all.
- `no-maint`: drops servers in maintenance mode (helps with server-template setups). There is no consistency check on server state during a dump.
- `extra-counters`: adds counters registered by modules (frontend, backend, server, listener only).

Key series confirmed in the exporter's metric tables: `haproxy_frontend_http_responses_total`, `haproxy_frontend_connections_total`, `haproxy_backend_current_queue`, `haproxy_backend_active_servers`, `haproxy_backend_http_responses_total`, `haproxy_backend_response_time_average_seconds`, `haproxy_server_check_failures_total`, `haproxy_process_current_connections`. Look at your own `/metrics` output for label names before writing alerts on response classes.

Gotchas:
- All lines of one metric are emitted as one group, so large configurations cost more: the README benchmark found a PROMEX dump about 5x slower and 20x more verbose than the CSV export of the stats page. Scope the scrape.
- The listener exposes your topology; bind it to an internal address and firewall it.

Verify: `haproxy -vv` shows the exporter line, and fetching `/metrics` from the bound address returns lines starting with `haproxy_`.

## Checked
2026-11-09. Confirmed against the HAProxy 3.0 configuration manual (`use-service` action, prometheus-exporter example, final-rule behaviour) and the PROMEX README (build flag, `-vv` text, HTX requirement, scope/metrics/no-maint/extra-counters filters, benchmark, metric names). Removed: "compiled in since 2.0 on most packages", `?exclude=server`, the exporter scrape-uri flag, counter-reset-on-reload remark, the 5xx ratio expression with a `code` label, `no log`, scrape_timeout advice, Prometheus config snippet.
Method: documentation only; no commands were run.
