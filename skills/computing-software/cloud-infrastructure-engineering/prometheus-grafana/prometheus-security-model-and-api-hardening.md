---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-security-model-and-api-hardening
name: prometheus-security-model-and-api-hardening
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, security-model, admin-api-hardening, lifecycle-api, threat-model]
level: advanced
status: docs-checked
description: "Apply the Prometheus security model: who is trusted, which endpoints are dangerous (admin, lifecycle, remote-write and OTLP receivers), and how to lock them down."
sources: ["https://prometheus.io/docs/operating/security/", "https://prometheus.io/docs/prometheus/latest/command-line/prometheus/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus security model and API hardening

## The model (from prometheus.io/docs/operating/security)
- Untrusted users are presumed to have access to the Prometheus HTTP endpoint and logs, and so to all time series in the database plus operational and debugging information.
- Only trusted users are presumed able to change the command line, configuration file, rule files and the runtime environment.
- Scraped targets may be run by untrusted users. By default a target should not be able to expose data that impersonates a different target; the `honor_labels` option removes this protection, as can certain relabelling setups.
- Prometheus HTTP endpoints should not be exposed to publicly accessible networks (unless you know what you are doing), and it is easy to overload servers with requests.
- Secret-marked fields in configuration files are not exposed in logs or via the HTTP API; put secrets only in such fields, and protect files on disk yourself.
- For authentication, Prometheus supports TLS (including client certificates) and basic auth through the web config file (`--web.config.file`); see the HTTPS page. Basic auth without TLS sends passwords in cleartext.

## Dangerous switches (off by default)
| Flag | Exposes | Default |
|---|---|---|
| `--web.enable-admin-api` | administrative and mutating endpoints under `/api/*/admin/`, such as deleting time series | false |
| `--web.enable-lifecycle` | HTTP reload and shutdown, under `/-/reload` and `/-/quit` | false |
| `--web.enable-remote-write-receiver` | an endpoint accepting remote write requests | false |
| `--web.enable-otlp-receiver` | an endpoint accepting OTLP write requests | false |

Enable only what you use. Instead of the lifecycle API, `--config.auto-reload` (default false, interval `--config.auto-reload-interval`, default 30s) reloads the configuration file when it changes.
There is no built-in CSRF protection on administrative and mutating endpoints; with a reverse proxy you may wish to block those paths. For non-mutating endpoints, set CORS headers such as `Access-Control-Allow-Origin` in the proxy if another origin must read responses. The `--web.cors.origin` flag is a fully anchored regex for the CORS origin (default `.*`).

## Other components
- Remote read lets anyone with HTTP access send queries to the endpoint.
- Grafana dashboard permissions are not data source permissions, so they do not limit a user's ability to run arbitrary queries in proxy mode.
- If PromQL queries include untrusted user input, escape it to prevent injection.
- SNMP and Blackbox exporters take targets from URL parameters, so anyone with HTTP access can make them send requests to arbitrary endpoints, which could leak client-side secrets such as basic auth passwords or SNMP community strings. Most exporters support TLS.
- Alertmanager serves `/api/v2` with `Access-Control-Allow-Origin: *`, so unauthenticated Alertmanagers are reachable by any website a browser can reach it from.

## Checked
Date: 2026-11-07.
Read in full: the Security model page (trust assumptions, `honor_labels`, admin API and lifecycle flags, remote read, Alertmanager CORS, exporters, authentication and TLS, API security, secrets) and the Prometheus command-line page (flag names and defaults for `--web.enable-admin-api`, `--web.enable-lifecycle`, `--web.enable-remote-write-receiver`, `--web.enable-otlp-receiver`, `--web.cors.origin`, `--config.auto-reload`, `--config.auto-reload-interval`, `--web.config.file`).
Removed because neither page confirms them: the specific admin endpoint names, `POST` methods and receiver paths, the `/api/v1/status/config` and `<secret>` claims, label-limit advice, the SIGHUP advice, the Kubernetes NetworkPolicy, oauth2-proxy and non-root advice (Kubernetes is not covered by the cited sources), the mysqld_exporter and node_exporter examples, and the invented Verify checklist.
Method: documentation only; no commands were run.
