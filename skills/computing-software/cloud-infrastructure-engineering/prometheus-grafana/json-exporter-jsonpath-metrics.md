---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.json-exporter-jsonpath-metrics
name: json-exporter-jsonpath-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, json-exporter-config, jsonpath-metrics, json-exporter, rest-api-monitoring, multi-target-exporter]
level: practitioner
status: docs-checked
description: "Turn JSON APIs into Prometheus metrics with json_exporter: modules, JSONPath for values and labels, object type for arrays, per-module HTTP client config, and the /probe scrape."
sources: ["https://github.com/prometheus-community/json_exporter", "https://raw.githubusercontent.com/prometheus-community/json_exporter/master/examples/config.yml", "https://raw.githubusercontent.com/prometheus-community/json_exporter/master/config/config.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# json_exporter

json_exporter is a Prometheus exporter that scrapes remote JSON by JSONPath. A module in its config file describes one
kind of JSON document; Prometheus selects the module and target through the `/probe` endpoint.

## Config model (from config.go and examples/config.yml)
A `modules` map; each module has `metrics` (a list), and optionally `headers`, `http_client_config` (the Prometheus
common HTTPClientConfig, for example `tls_config` and `basic_auth`), `valid_status_codes` (default 2xx) and `body`.
Each metric has:
- `name`, `path` (JSONPath), `help` (defaults to the name), `labels` (map of label to static text or a path), and
  `valuetype` is `gauge`, `counter` or `untyped` (default `untyped`).
- `type`: `value` (default) or `object`. With `object`, `path` selects a set of objects and `values` maps value names
  to a path or a static number; the example config's `example_value` with value key `active` is exposed as
  `example_value_active`, with one series per selected object and labels such as `id`.
- `epochTimestamp` (a path to a unix timestamp). The README warns that custom timestamps disable staleness handling.
- `allow_missing_key: true` suppresses the error when the path is absent.

Example, adapted from the shipped `examples/config.yml`:
```yaml
modules:
  queues:
    headers:
      X-Dummy: my-test-header
    metrics:
    - name: queue
      type: object
      help: Queue stats
      path: '{ .queues[*] }'
      labels:
        queue: '{ .name }'
      values:
        depth: '{ .depth }'          # exposed as queue_depth
```
JSONPath here uses the braces form (`{ .values[?(@.state == "ACTIVE")] }`, `{ [*] }` for a top-level list), as in the
example config. The README links to a "Supported JSONPath Syntax" page for the details.

## Run and test
```bash
./json_exporter --config.file examples/config.yml
curl "http://localhost:7979/probe?module=default&target=http://localhost:8000/examples/data.json"
```
The README example uses port 7979 and the `module` and `target` query parameters. A Docker image is published at
`quay.io/prometheuscommunity/json-exporter`.

## Scrape from Prometheus
Use the multi-target pattern: `metrics_path: /probe`, `params: {module: [<name>]}`, targets are the JSON URLs, and
relabel `__address__` into `__param_target` and to the exporter's address. The README demonstrates this via
`examples/prometheus.yml`; check that file for the exact relabelling.

## Other features (README)
- POST bodies: if `modules.<module>.body` is set its `content` is sent and the method becomes POST. With
  `templatize: true` the content is a Go template with the Sprig functions, and the scrape query parameters are
  available as values (for example `{{ .myVal | first }}`).
- TLS for the exporter's own listener is configured via exporter-toolkit/web.

## Checked

Checked 2026-11-08 against the json_exporter README, `examples/config.yml` and `config/config.go` on the default branch.
Removed: `valueconverter` (not a field in the config struct or the examples, so the enum-mapping claim could not be
confirmed), the Bearer `authorization` snippet (use `http_client_config` per the examples), the claim that
non-numeric values are dropped silently, port 7979 in a relabel snippet (kept only where the README shows it), and the
"Kubernetes-style versus `$.a.b`" JSONPath assertion.
Method: docs-only read of cited pages, 2026-11-08
