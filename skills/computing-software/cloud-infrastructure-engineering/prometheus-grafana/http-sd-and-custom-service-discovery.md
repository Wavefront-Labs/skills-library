---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.http-sd-and-custom-service-discovery
name: http-sd-and-custom-service-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, service-discovery, http-sd-configs, custom-service-discovery, http-sd, file-sd-generator, sd-endpoint, target-groups-json, cmdb-integration, netbox, inventory-to-targets, refresh-interval, pca]
level: practitioner
status: verified
description: "Feed Prometheus from any inventory (CMDB, NetBox, a database) by serving the http_sd JSON format or generating file_sd files: the schema, error semantics, caching, and a minimal endpoint."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#http_sd_config", "https://prometheus.io/docs/prometheus/latest/http_sd/", "https://prometheus.io/docs/guides/file-sd/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http_sd and custom service discovery

**Goal:** turn a system of record you already have into Prometheus targets without a
bespoke SD plugin: either an HTTP endpoint returning target groups, or a script writing
file_sd files.

## 1. The target-group format (shared by http_sd and file_sd)
```json
[
  {"targets": ["10.0.0.5:9100", "10.0.0.6:9100"],
   "labels": {"job": "node", "env": "prod", "__meta_cmdb_owner": "payments"}},
  {"targets": ["db1:9187"], "labels": {"job": "postgres", "__metrics_path__": "/metrics"}}
]
```
- Labels may include `__address__`-affecting magic labels (`__metrics_path__`, `__scheme__`,
  `__param_x`) and your own `__meta_*` labels (dropped after relabeling, usable in
  `relabel_configs`). Non-`__` labels are attached to every series.
- `targets` entries are `host:port`. A target without a port is not rejected: `localhost` was scraped as `http://localhost/metrics`
  (default port 80) with `instance="localhost"`.

## 2. http_sd
```yaml
  - job_name: cmdb
    http_sd_configs:
      - url: https://sd.internal/prometheus/targets?env=prod
        refresh_interval: 60s
        authorization: {credentials_file: /etc/prometheus/secrets/sd.token}
        tls_config: {ca_file: /etc/prometheus/secrets/ca.crt}
    relabel_configs:
      - source_labels: [__meta_cmdb_owner]
        target_label: team
```
Contract the endpoint must honour:
- `GET`, respond `200` with `Content-Type: application/json`, body = the array above (an empty array `[]` is valid and
  yields zero targets). `text/plain` is refused: `unsupported content type "text/plain"`.
- A non-200 response → Prometheus **keeps the last good target list** (tested: three good refreshes, then HTTP 500: the
  target stayed `up`) and increments `prometheus_sd_http_failures_total`. Alert on it.
- Prometheus sends `Accept: application/json` and `X-Prometheus-Refresh-Interval-Seconds: <seconds>`; use the latter for cache TTL.
- The whole list is replaced on every refresh (no deltas).

Minimal endpoint (Python/Flask) over a SQL inventory:
```python
@app.get("/prometheus/targets")
def targets():
    rows = db.execute("select ip, port, job, env, owner from hosts where monitored").fetchall()
    groups = {}
    for ip, port, job, env, owner in rows:
        groups.setdefault((job, env, owner), []).append(f"{ip}:{port}")
    return jsonify([{"targets": t, "labels": {"job": j, "env": e, "__meta_cmdb_owner": o}}
                    for (j, e, o), t in groups.items()])
```
Group targets by identical label sets: one group per host with its own labels works but
makes the `/service-discovery` page and the JSON huge.

## 3. file_sd as the alternative
```yaml
    file_sd_configs:
      - files: ["/etc/prometheus/targets/*.json", "/etc/prometheus/targets/*.yml"]
        refresh_interval: 5m       # backstop; the file watcher picked up an edit within seconds (tested on Windows)
```
A cron/CI job writes the file **atomically** (write to temp, `mv`): a half-written file is
logged as `Error reading file ... unexpected end of JSON input` and the previous targets are kept. YAML is accepted
(`- targets: […]` / `labels:`). This is the right choice when the inventory tool can't
host an endpoint but can push to a ConfigMap or volume.

## 4. When to use which
- http_sd: inventory already has an API, several Prometheus instances consume it, or the
  list changes often. One endpoint can serve many jobs by query parameter.
- file_sd: single instance, air-gapped, or you want the target list in git for review.
- Neither: if the source is Kubernetes, Consul, a cloud API or DNS, the built-in SD is
  cheaper and health-aware.

## Gotchas
- An endpoint that returns `200` with `{}` (object, not array) is not a valid target list: from a cold start the job had zero
  targets and the failure counter kept rising. Alert on `prometheus_sd_http_failures_total` and on
  `prometheus_sd_discovered_targets` dropping.
- Label names follow the validation scheme: with the 3.15 default (`utf8`) a label named `team-name` was accepted and attached to
  the target, so a typo in a label name is not caught by Prometheus.

## Verify
- [ ] `curl -s <url> | jq 'map(.targets|length)|add'` equals the active target count on `/targets`.
- [ ] Stopping the endpoint keeps targets scraping and raises `prometheus_sd_http_failures_total`.
- [ ] A new host appears within one `refresh_interval` after being added to the inventory.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), Prometheus Operator API reference (main), jq 1.8.2, Flask 3.
- A local server returned: the target-group array, `{}`, HTTP 500, a target without a port, a `team-name` label, `[]`, `text/plain`, and (via a counter) three good answers followed by HTTP 500. Prometheus 3.15.1 results: the good job `up`; `{}`, 500 and `[]` jobs had 0 discovered targets; the 500-after-good job stayed `up`; `prometheus_sd_http_failures_total` rose; `text/plain` gave the logged error above; the portless target was scraped on port 80; `team-name` was attached as a label. Request headers logged by the server: `Accept: application/json`, `X-Prometheus-Refresh-Interval-Seconds: 5`.
- `http_sd_configs` YAML (url, refresh_interval, authorization.credentials_file, tls_config.ca_file, relabel_configs) and the `file_sd_configs` block pass `promtool check config` (with the referenced files present).
- file_sd: a `.json` and a `.yml` file were both loaded; overwriting the JSON with a truncated document logged `Error reading file` and kept the old targets; a corrected file was applied within seconds with `refresh_interval: 5m`.
- The Flask endpoint from the skill, run through Flask's test client over an in-memory SQLite `hosts` table, returned `200 application/json` with two groups; the `jq 'map(.targets|length)|add'` check returned 3 on a sample array.
