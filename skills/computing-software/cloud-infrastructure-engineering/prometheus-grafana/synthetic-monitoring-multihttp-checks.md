---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.synthetic-monitoring-multihttp-checks
name: synthetic-monitoring-multihttp-checks
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [synthetic-monitoring, multihttp-check, api-testing, variables, assertions]
level: advanced
status: docs-checked
description: "Build Grafana Synthetic Monitoring MultiHTTP checks that chain requests, capture variables from responses, and assert on body, headers, status and JSONPath per request."
sources: ["https://grafana.com/docs/grafana-cloud/observe-and-act/testing/synthetic-monitoring/create-checks/checks/multihttp/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MultiHTTP checks

**Goal:** test a multi-step API journey (for example login, create, read) as one synthetic check.

## What it is
- A MultiHTTP check tests multiple URLs in a single check, measuring uptime and latency like other check types, lets
  you use the result of one request in a later one, and supports several assertions per request.
- In the Synthetics app, create it with the **Multi Step** option. Its check type identifier is `multihttp`, used by
  the REST API, Terraform, check metrics and the Checks list.
- **Requests are not validated against a 200 status automatically.** Define assertions for each request (the Uptime
  step of the check form) or failed requests will not affect uptime and reachability.
- Executions make outbound connections to `jslib.k6.io`; on private probes behind a firewall, allow it.

## Common options
- Frequency: 10 to 3600 seconds. Timeout: 1 to 60 seconds. Only `sm_check_info` carries the frequency label.
- Job name becomes the `job` label, target the `instance` label, probe location the `probe` label; custom labels are
  optional.
- Per request: request target (URL), method, headers, query parameters, assertions, variables.

## Assertions (four types)
- **Text**: match a string against body, headers or status code using contains, does not contain, equals, starts with
  or ends with. Headers are matched as lower-cased name, a colon and space, then the value; one matching header
  suffices.
- **JSON path value**: response body must be JSON; compare a JSONPath result using contains, does not contain, equals,
  starts with, ends with.
- **JSON path**: the JSONPath expression must evaluate to a non-empty result.
- **Regex**: against body, headers or status code.

## Variables
Capture a value from a response and reuse it in later requests with `${name}` anywhere a string is expected (headers,
assertion values). The name must be unique across all requests. Sources: a JSONPath, a regular expression, or a CSS
selector (optionally with an attribute name).

## Metrics
Common: `probe_success`, `probe_duration_seconds`, `probe_all_success`, `probe_all_duration_seconds`, `sm_check_info`.
MultiHTTP adds, for example: `probe_checks_total` (labels include `check`, `result` pass or fail), `probe_check_success_rate`,
`probe_http_status_code`, `probe_http_duration_seconds` (by `phase`), `probe_http_requests_failed_total`,
`probe_data_received_bytes`, `probe_data_sent_bytes`, `probe_iteration_duration_seconds` and
`probe_script_duration_seconds`. If k6 startup fails (module download or syntax error), `probe_script_duration_seconds`
is not reported and `probe_duration_seconds` reports the full time up to the timeout.

## Practices
- Use a dedicated synthetic user with minimal permissions; do not put secrets in plain headers in code.
- Clean up data the flow creates (a delete step) or use idempotent test resources.
- Keep heavy flows at a lower frequency and a simple HTTP check at a higher one for availability.
- For real browser journeys use browser checks instead.
- The Terraform resource for checks is documented in the Grafana Terraform provider docs; confirm field names there
  for your provider version (not verified here).

## Verify
- [ ] Every request has at least one assertion, including a status code check.
- [ ] Breaking the first step makes the check fail with the assertion visible in `probe_checks_total{result="fail"}`.

## Checked
2026-11-08: confirmed against the Grafana Synthetic Monitoring MultiHTTP check page (options and ranges, assertion
types, variables, metrics, jslib.k6.io note, no automatic 200 validation). Removed: the Terraform example and its
field names, a request-count limit, secret-store advice, and per-step timing claims, because the Terraform registry
page returned no readable text and the MultiHTTP page did not state the others.
Method: documentation only; no commands were run.
