---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.federate-endpoint-scrape-config
name: federate-endpoint-scrape-config
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, federation, federate-match-params, federation-scrape-config, honor-labels, external-labels]
level: practitioner
status: verified
description: "Write the scrape job that pulls /federate: match[] params, honor_labels, external labels, interval/timeout, and testing the selector with curl first."
sources: ["https://prometheus.io/docs/prometheus/latest/federation/#configuring-federation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuring the /federate scrape

## 1. Test the selector
```bash
curl -sG http://dc1-prom:9090/federate \
  --data-urlencode 'match[]={__name__=~"job:.*"}' \
  --data-urlencode 'match[]=up{job="kubernetes-apiservers"}' | head
curl -sG http://dc1-prom:9090/federate --data-urlencode 'match[]={__name__=~"job:.*"}' | grep -vc '^#'   # series count
```
Each `match[]` is an instant-vector selector; multiple are ORed. Response is text exposition with
timestamps, plus the source server's **external labels** added to every series.

## 2. Scrape job
```yaml
scrape_configs:
  - job_name: federate-dc1
    scrape_interval: 30s
    scrape_timeout: 25s
    honor_labels: true            # keep source job/instance instead of renaming to exported_*
    metrics_path: /federate
    params:
      'match[]':
        - '{__name__=~"job:.*"}'
        - '{__name__="up"}'
    static_configs:
      - targets: [dc1-prom:9090]
        labels: {federated_from: dc1}
```
- `honor_labels: true` is required, otherwise `job` and `instance` from the source are overwritten (tested on 3.15.1: with `false` they arrived as `exported_job` and `exported_instance`; the static `federated_from` label was added either way).
- Source servers must have distinct `global.external_labels` (e.g. `dc: dc1`) so series don't collide.
- Auth/TLS: same `basic_auth`/`tls_config` options as any scrape if the source is protected.

## 3. Operator form
Prometheus Operator: a `ScrapeConfig` CR (or `additionalScrapeConfigs`) with `metricsPath: /federate`,
`honorLabels: true`, `params: {"match[]": [...]}`.

## Gotchas
- The scrape fails entirely (not partially) if the body exceeds `body_size_limit` or `sample_limit`.
- Federating the `ALERTS` series is useful for a global alert overview, but don't re-alert on it blindly.
- `/federate` reads only the head/most recent sample per series (lookback 5 min); it is not for history.

## Verify
- [ ] `up{job="federate-dc1"} == 1` and `scrape_samples_scraped` matches the curl count.
- [ ] Federated series carry `dc="dc1"` and original `job`/`instance`.
