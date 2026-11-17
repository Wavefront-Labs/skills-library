---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.synthetic-monitoring-and-frontend-rum
name: synthetic-monitoring-and-frontend-rum
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, grafana-synthetic-monitoring, synthetic-monitoring, synthetic-checks, uptime-checks, blackbox-exporter, probes, multihttp-checks, scripted-checks, k6-browser, real-user-monitoring, rum, faro, grafana-faro, faro-web-sdk, browser-telemetry, web-vitals, core-web-vitals, lcp, inp, cls, frontend-observability, session-tracking, javascript-errors, source-maps, otel-js-browser, alloy-faro-receiver]
level: practitioner
status: docs-checked
description: "Outside-in view: synthetic checks (Grafana Synthetic Monitoring or blackbox_exporter) for uptime and latency from many probes, plus Faro RUM for web vitals and JS errors."
sources: ["https://grafana.com/docs/grafana-cloud/observe-and-act/testing/synthetic-monitoring/", "https://github.com/prometheus/blackbox_exporter", "https://grafana.com/docs/grafana-cloud/observe-and-act/monitor-applications/frontend-observability/", "https://github.com/grafana/faro-web-sdk", "https://grafana.com/docs/alloy/latest/reference/components/faro/faro.receiver/", "https://web.dev/articles/vitals", "https://grafana.com/docs/grafana-cloud/observe-and-act/testing/synthetic-monitoring/set-up/set-up-private-probes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synthetic monitoring and frontend real user monitoring

**Goal:** know the service is reachable and fast *from where users are* even with no traffic
(synthetics), and know what real users actually experienced in the browser (RUM).

## 1. Synthetic checks: what to run
Black-box checks test externally visible behaviour the way a user reaches it, with no instrumentation
in your code. Useful journeys:
- HTTP(S) readiness request from several regions: catches DNS, TLS, load balancer and edge outages.
- TLS certificate expiry: catches failing renewals.
- DNS answers, TCP or ICMP to VPN and database endpoints: network path.
- Multi-step flows (login, add to cart, checkout): business-flow regressions.
- Browser checks: front-end regressions.

Pick frequencies per journey; keep synthetics to a small set of critical journeys. They do not replace SLIs from real
traffic.

### Grafana Synthetic Monitoring (Cloud)
- Part of Grafana Cloud. Each execution of a check simulates a single user from one probe location; for scripted and
  browser checks the execution runs one iteration of the script's test function.
- Probes: public probes are operated by Grafana Labs. A **private probe** is a probe you install in your environment or
  another location you choose; it is an instance of the open source Grafana Synthetic Monitoring Agent, is only
  accessible to you and only writes data to your Grafana Cloud account.
- The private-probe docs cover installing the agent using APT, YUM, Docker or Kubernetes, firewall and resource
  requirements, feature flags, access to private IP addresses, and collecting Prometheus-style metrics from the agent.
- Docs sections exist for alerts (check failure, TLS certificate about to expire, latency threshold), users and teams
  (basic roles and RBAC) and a REST API to manage checks programmatically. Look up exact metric names, check settings
  and Terraform arguments in those pages before relying on them.
- Alert on a majority of probes failing rather than one probe, so a single bad probe or network blip does not page.

### Self-hosted: blackbox_exporter
- `/probe?target=...&module=...` returns metrics for one probe (the README example is `module=http_2xx`);
  `probe_success` says whether the probe succeeded, and `debug=true` returns debug information.
- Multi-target pattern: Prometheus scrape job with `params: module`, targets as `__param_target`, and a relabel rule
  that replaces `__address__` with the exporter's real host:port (see the README's scrape config example).
- Run exporters in at least two regions and alert on `probe_success`. See
  `computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-exporters-and-custom-exporter`.

## 2. Real user monitoring with Faro
- The Grafana Faro Web SDK instruments browser frontend applications and can send telemetry to Grafana Alloy (with the
  faro receiver), to a Grafana Cloud instance, or to a custom receiver. Alloy can then send the data to Loki or Tempo.
- Packages: `@grafana/faro-core`, `@grafana/faro-web-sdk` (instrumentations, metas, transports), `@grafana/faro-web-tracing`
  (tracing), `@grafana/faro-react` (React integration).
- Grafana Cloud Frontend Observability: the Faro Web SDK captures real user performance metrics, errors, logs and
  client-side traces and sends them to Frontend Observability. Docs sections cover instrumenting, sampling and
  filtering, alerts, RBAC and data privacy.
- Supported: browser web applications and the client side of server-rendered apps (Next.js, React SSR). Not supported:
  the server runtime of server-rendered apps, browser extensions, web workers and service workers, Node.js and React
  Native.
- Faro v2 upgraded to Web Vitals v5, which removes the FID metric.

### Self-hosted receiver: Alloy `faro.receiver`
- It does not work with Grafana Cloud Frontend Observability (use one or the other).
- `output { logs = [...Loki receivers]  traces = [...otelcol components] }` is required: logs go to Loki components and
  traces go to OpenTelemetry Collector components (for example `otelcol.exporter.otlphttp`), not directly to Tempo.
- `server` block defaults: `listen_address` `127.0.0.1`, `listen_port` 12347, `cors_allowed_origins` `[]` (CORS
  disabled; `["*"]` allows all), `max_allowed_payload_size` `5MiB`. Set `listen_address` to a reachable interface for
  browsers. Optional `api_key` makes clients send an `X-API-Key` header; wrong or missing gives HTTP 401.
- Allowed cross-origin request headers include `Traceparent`, `X-Faro-Session-Id`, `X-API-Key`, `X-Scope-OrgID`,
  `Content-Type`, `Content-Encoding` and `Idempotency-Key`. Gzip request bodies are accepted.
- `rate_limiting` block: enabled by default, `rate` 50 per second, `burst_size` 100, `strategy` `global` or `per_app`;
  excess requests get HTTP 429.
- `sourcemaps` block: `download` defaults to true with `download_timeout` `1s`. By default Alloy requests any URL a
  client puts in its telemetry, so an internet-facing receiver lets clients make Alloy fetch internal addresses. Set
  `download_from_origins` to your own origins, or set `download = false` and use `location` blocks (local paths are
  checked before remote ones; `path` may contain `{{ .Release }}`).
- The component exposes metrics such as `faro_receiver_logs_total`, `faro_receiver_exceptions_total`,
  `faro_receiver_request_duration_seconds` and `faro_receiver_sourcemap_downloads_total`.

## 3. Reading RUM
- Core Web Vitals thresholds (web.dev): LCP within 2.5 seconds, INP 200 milliseconds or less, CLS 0.1 or less, measured
  at the 75th percentile of page loads, segmented across mobile and desktop. A page passes when all three meet the
  target at p75.
- Lab tools such as Lighthouse cannot measure INP because there is no user input; Total Blocking Time is a lab proxy.
- Compute per route and device class; one bad route hides in a global p75.
- Alert on new error signatures and on error rate per session rather than raw counts.
- Privacy: keep PII out of attributes and URLs, and allow-list the collector origin with `cors_allowed_origins`.

## Gotchas
- A probe from one region pages on that region's network blips; use several probes and a majority rule.
- Bot and WAF rules can block probes and RUM collectors; allow-list probe addresses and the collector origin.
- For frontend spans to link to backend traces, the browser must send `traceparent` to your API and the API's CORS
  config must allow that header (the receiver lists `Traceparent` among its allowed headers).

## Verify
- [ ] The synthetic dashboard shows several probes per critical check and a deliberate bad route fails on all of them.
- [ ] A forced JS error in staging appears de-minified once source maps are available to the receiver or Cloud.
- [ ] A slow API call from the browser shows a trace spanning frontend and API in Tempo.
- [ ] The collector rejects an unknown origin.

## Checked
2026-11-08: confirmed against the Synthetic Monitoring overview and private-probes pages, the Frontend Observability
overview, the faro-web-sdk README, the Alloy faro.receiver reference (defaults, headers, rate limiting, sourcemaps,
metrics), the blackbox_exporter README (probe endpoint, probe_success, scrape config) and web.dev Core Web Vitals
(thresholds, p75, INP lab limitation). Removed: check frequencies, the private-probe docker command, probe_all_success
and sm_check_info metrics, the Terraform check resource, the SDK code sample and its option names, source-map upload
tooling names, the OpenTelemetry JS alternative detail, Loki query example and session-sampling cost claim, because the
fetched pages did not state them.
Method: documentation only; no commands were run.
