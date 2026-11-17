---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.synthetic-checks-private-probes-and-faro-setup
name: synthetic-checks-private-probes-and-faro-setup
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-synthetic-monitoring, ping-check, dns-check, tcp-check, traceroute-check, private-probes, probe-deployment, k6-scripted-check, browser-check, synthetic-monitoring-alerts, synthetic-monitoring-terraform, faro, faro-sdk-setup, faro-instrumentations, faro-tracing, otel-web-tracing, faro-receiver-config, source-map-upload, web-vitals-dashboards, frontend-slo]
level: practitioner
status: docs-checked
description: "Set up Grafana Synthetic Monitoring private probes and checks, and frontend RUM with the Faro Web SDK and Alloy faro.receiver, with documented defaults and warnings."
sources: ["https://grafana.com/docs/grafana-cloud/observe-and-act/testing/synthetic-monitoring/", "https://grafana.com/docs/grafana-cloud/observe-and-act/testing/synthetic-monitoring/set-up/set-up-private-probes/", "https://grafana.com/docs/grafana-cloud/observe-and-act/monitor-applications/frontend-observability/", "https://grafana.com/docs/alloy/latest/reference/components/faro/faro.receiver/", "https://github.com/grafana/faro-web-sdk"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Synthetic checks, private probes and Faro RUM

## Synthetic Monitoring
- Part of Grafana Cloud; black-box checks emulate user behaviour from probe locations. Each execution simulates one
  user from one probe; scripted and browser checks run one iteration of the script's test function.
- Docs sections: introduction, get started, set up, create checks (available check types), analyze results, configure
  alerts (check failure, TLS certificate about to expire, latency threshold), users and teams (basic roles and RBAC),
  REST API. Check type names and settings are on the "Choose a check type" and create-checks pages (not fetched
  here); look up exact types and Terraform fields there.
- MultiHTTP, scripted and browser checks run on k6; see `...prometheus-grafana.synthetic-monitoring-multihttp-checks`.

## Private probes
- A private probe is a probe you install in your environment or another location you choose; unlike public probes
  (operated by Grafana Labs) it is only accessible to you and only writes data to your Grafana Cloud account. It is an
  instance of the open source Grafana Synthetic Monitoring Agent.
- Docs cover: registering the probe, installing the agent with APT, YUM, Docker or Kubernetes and assigning checks;
  firewall access for service connections, script imports and monitored targets; CPU and memory requirements; feature
  flags, access to private IP addresses and browser check requirements; collecting Prometheus-style metrics from the
  agent with Prometheus or Alloy; troubleshooting (agent versions, authentication, API connectivity, logs).
- Run checks from more than one location so one location's failure alone does not page.

## Faro (frontend observability)
- The Grafana Faro Web SDK captures real user performance metrics, errors, logs and client-side traces from browser
  apps and sends them to Grafana Cloud Frontend Observability, to Alloy with the faro receiver, or to a custom
  receiver. Packages: `@grafana/faro-core`, `@grafana/faro-web-sdk`, `@grafana/faro-web-tracing`, `@grafana/faro-react`.
- Supported: browser apps and the client side of server-rendered apps. Not supported: server runtimes, browser
  extensions, web workers and service workers, Node.js and React Native. Faro v2 uses Web Vitals v5, which removes FID.
- Follow the quickstart for SDK initialisation options; this page does not reproduce option names because the fetched
  pages did not list them.

### Self-hosted receiver (Alloy `faro.receiver`)
- Does not work with Grafana Cloud Frontend Observability.
- Defaults: `listen_address` `127.0.0.1`, `listen_port` 12347, `cors_allowed_origins` `[]` (CORS off, `["*"]` allows
  all), `max_allowed_payload_size` `5MiB`, rate limiting on at 50 requests per second with burst 100 (HTTP 429 when
  exceeded). `api_key` makes clients send `X-API-Key` (HTTP 401 otherwise).
- `output` is required: `logs` to Loki receivers, `traces` to OpenTelemetry Collector components (for example
  `otelcol.exporter.otlphttp`).
- Source maps: `sourcemaps { download = true }` is the default with a `1s` timeout. By default Alloy fetches any URL
  a client reports, so an internet-facing receiver can be used to make Alloy request internal addresses. Set
  `download_from_origins` to your own origins, or set `download = false` and use `location` blocks (checked first;
  `path` may contain `{{ .Release }}`). A `location` needs `minified_path_prefix` and `path`.

## Verify
- [ ] Private probe appears as online in the Synthetics app and receives checks.
- [ ] Faro errors show original file and line once source maps are available to the receiver.
- [ ] The receiver is not reachable by untrusted networks without `download_from_origins` or download disabled.

## Checked
2026-11-08: confirmed against the Synthetic Monitoring overview and private-probes pages, the Frontend Observability
overview, the faro-web-sdk README and the Alloy faro.receiver reference. Removed: the k6 script example, container
variable names, per-check alert sensitivity levels, the Terraform resource, the SDK initialisation code and option
names, the list of check type names, and the LCP SLO example, because the fetched pages did not state them.
Method: documentation only; no commands were run.
