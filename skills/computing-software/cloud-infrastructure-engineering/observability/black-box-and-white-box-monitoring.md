---
id: computing-software.cloud-infrastructure-engineering.observability.black-box-and-white-box-monitoring
name: black-box-and-white-box-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [black-box-monitoring, white-box-monitoring, blackbox-exporter, synthetic-checks, golden-signals, sre]
level: practitioner
status: draft
description: "Split monitoring between black-box probes (user-visible symptoms) and white-box internals (causes, imminent failures), and decide which one pages."
sources: ["https://sre.google/sre-book/monitoring-distributed-systems/", "https://github.com/prometheus/blackbox_exporter", "https://sre.google/workbook/monitoring/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Black-box vs white-box monitoring

SRE Book definitions: black-box tests externally visible behaviour as a user sees it; white-box relies on internals (metrics, logs, profiling). Black-box is symptom-oriented and catches problems happening now; white-box catches imminent problems and masked failures (e.g. retries hiding errors).

## Split
| Use | Black-box | White-box |
|---|---|---|
| Page on it | yes, when the symptom is user-facing and sustained | yes if it is an SLO burn computed from request metrics |
| Detect | DNS, TLS, LB, total outage, region reachability | saturation, queue growth, dependency errors, disk filling |
| Debug | no (tells you what, not why) | yes |

## Black-box setup (blackbox_exporter)
```yaml
- job_name: probe-http
  metrics_path: /probe
  params: {module: [http_2xx]}
  static_configs: [{targets: [https://shop.example.com/healthz]}]
  relabel_configs:
    - {source_labels: [__address__], target_label: __param_target}
    - {source_labels: [__param_target], target_label: instance}
    - {target_label: __address__, replacement: blackbox-exporter:9115}
```
Alert: `probe_success == 0` for 2-5m from at least 2 probe locations (`min by (instance)` across locations or count failing locations >= 2).

## White-box essentials
Server-side request metrics per route, dependency client metrics, resource saturation, queue lag. Alert on SLO burn, not on every internal metric.

## Gotchas
- A single probe location makes network blips look like outages: probe from 2-3 places.
- Probing `/healthz` that returns 200 while the real path is broken: probe a real read-only user path.
- White-box from the server misses requests that never arrived (DNS, LB down): that is exactly what black-box covers.

## Verify
- [ ] Each user-facing endpoint has a black-box probe from more than one location.
- [ ] Killing the LB in staging fires the black-box alert while white-box metrics go silent.
