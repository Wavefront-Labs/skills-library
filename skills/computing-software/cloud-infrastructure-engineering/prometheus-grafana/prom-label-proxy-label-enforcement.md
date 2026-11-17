---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prom-label-proxy-label-enforcement
name: prom-label-proxy-label-enforcement
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prom-label-proxy, label-enforcement-proxy, multi-tenancy, prometheus-security, query-isolation]
level: advanced
status: docs-checked
description: "Enforce per-tenant label matchers on PromQL queries, series, rules and Alertmanager APIs with prom-label-proxy for read multi-tenancy on a shared Prometheus or Thanos."
sources: ["https://github.com/prometheus-community/prom-label-proxy", "https://prometheus.io/docs/operating/security/", "https://thanos.io/tip/components/query.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# prom-label-proxy

prom-label-proxy enforces a given label in a PromQL query, in Prometheus API responses or in Alertmanager API requests.
That gives read multi-tenancy for Prometheus, Alertmanager or Thanos. It does no authentication or authorization: those
must happen before the request reaches it (the README names kube-rbac-proxy as an example building block).

## Where the tenant value comes from
```bash
# 1. From a query/form parameter
prom-label-proxy -query-param tenant -label tenant -upstream http://prometheus:9090 -insecure-listen-address 127.0.0.1:8080
# 2. From a header
prom-label-proxy -header-name X-Tenant -label tenant -upstream http://prometheus:9090 -insecure-listen-address 127.0.0.1:8080
# 3. A static value (repeat -label-value for several; they become tenant=~"a|b")
prom-label-proxy -label tenant -label-value prometheus -upstream http://prometheus:9090 -insecure-listen-address 127.0.0.1:8080
```
- With the parameter mode, a request without the parameter gets an error from the proxy; several `tenant` parameters (or
  several headers) supply several values; POST bodies work too.
- `-query-param-only` stops the proxy merging a POST-form value of the parameter into the matcher (such requests get
  HTTP 400); it is effective only with `-query-param`. Use it when an upstream authorizer checks only URL values.
- `-regex-match` matches the label value by regular expression; the README marks it experimental and warns that a too
  permissive expression can expose sensitive metrics.
- `-error-on-replace` errors when the query already holds a conflicting matcher for the label.
- `-enable-label-apis` enables `/api/v1/labels` and `/api/v1/label/<name>/values`; they are off by default because they
  need `match[]` support upstream (Prometheus 2.24.0 or later; Thanos v0.18.0 at least, 0.23.0 or later recommended).
- `-rules-with-active-alerts` also returns alerting rules that have active alerts matching the label;
  `-enable-label-matchers-for-rules-api` filters at the source if the upstream supports it (Prometheus v2.54.0 or later,
  Thanos v0.25.0 or later).

## How requests are rewritten
- `/api/v1/query` and `query_range`: all selectors in the parsed PromQL are modified, whether or not the query already
  had a matcher for the label (`http_requests_total{namespace=~"a.*"}` enforced to `b` becomes
  `http_requests_total{namespace=~"b"}`).
- `/api/v1/series` (and the label endpoints when enabled): the label is injected into every `match[]` selector.
- `/federate`: every selector must contain the exact label match; other matchers for the label are discarded.
- `/api/v1/rules` and `/api/v1/alerts`: rules or alerts without an exact match on the label are dropped from the
  response.
- Alertmanager silences: GET gets a filter for the label, POST and DELETE can only affect silences matching the label.
  Multiple label values are not supported for the silences endpoints.
- Also proxied: `/api/v1/query_exemplars`, `/api/v2/alerts/groups` and `/api/v2/alerts`.

## Limits stated by the project
- Not a goal: write tenant isolation. A tenant that controls its scrape relabelling can set arbitrary labels, and a
  target with `honor_labels` can pollute other tenants' metrics; the README points to Prometheus Operator label
  enforcement, Thanos soft/hard tenancy or Cortex for that.
- OpenShift's setup pairs the proxy (label key `namespace`) with kube-rbac-proxy and its URL rewrite: first ServiceAccount
  token authentication, then authorization against the same RBAC role as the Kubernetes Resource Metrics API.

## Verify
- [ ] A request for `up` with one tenant value never returns series from another tenant, including with regex selectors.
- [ ] Direct access to the upstream is blocked (network policy), since the proxy is not a security boundary on its own.

## Checked

Checked 2026-11-08 against the prom-label-proxy README (flags, endpoints, version requirements and stated limits).
Corrected the flag `-value` to `-label-value` and added the real parameter flag `-query-param`. Removed because the
README does not state them: "series without the label are invisible", recording-rule advice, and the specific
adversarial test queries. The Prometheus security and Thanos Query pages were not needed for the remaining claims.
Method: docs-only read of cited pages, 2026-11-08
