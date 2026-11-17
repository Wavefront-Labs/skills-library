---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-architecture-and-pull-model
name: prometheus-architecture-and-pull-model
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, prometheus-architecture, prometheus-components, push-vs-pull, pull-model, pushgateway, scrape, tsdb, alertmanager, service-discovery, exporters, client-libraries, up-metric, staleness, batch-jobs, honor-labels, pca]
level: practitioner
status: docs-checked
description: "Explain the Prometheus architecture: what each component does, why scraping (pull) beats push, when the Pushgateway is legitimate, and the failure modes each choice creates."
sources: ["https://prometheus.io/docs/introduction/overview/", "https://prometheus.io/docs/practices/pushing/", "https://prometheus.io/docs/instrumenting/pushing/", "https://training.linuxfoundation.org/certification/prometheus-certified-associate/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus architecture and the pull model

**Goal:** know what each box does and why, so design choices (pull vs push, where a
Pushgateway belongs, what `up` means) are made deliberately rather than copied.

## 1. The components
| Component | Job | Lives where |
|---|---|---|
| Prometheus server | discovers targets, **scrapes** `/metrics` over HTTP on an interval, stores samples in its local TSDB, evaluates recording/alerting rules, serves PromQL | one or more per failure domain |
| Client libraries | expose in-process metrics on an HTTP endpoint | inside your app |
| Exporters | translate a third-party system's state into the exposition format (node_exporter, blackbox, mysqld, kube-state-metrics) | sidecar/daemon next to the thing |
| Pushgateway | accepts pushed metrics from short-lived jobs and holds them for scraping | one per environment, rarely more |
| Alertmanager | dedupes, groups, routes and silences alerts sent by Prometheus | clustered for HA |
| Service discovery | Kubernetes, Consul, EC2, file_sd, DNS, HTTP SD... feeds target lists | config |
| Remote storage | long-term/HA via remote_write (Thanos, Mimir, Cortex, VictoriaMetrics) | optional |

Prometheus is **single-node by design**: each server is independent, has no clustering,
and keeps data on local disk. HA is "run two identical servers"; global view and long
retention come from Thanos/Mimir, not from Prometheus itself.

## 2. Why pull
- **Health comes free**: every scrape yields `up{job,instance}` = 1/0. A dead target is
  observable; with push, silence is ambiguous (crashed? network? forgot to push?).
- The server controls load (`scrape_interval`, `scrape_timeout`, `sample_limit`), so a
  misbehaving app cannot flood it.
- Targets are inspectable by humans: `curl http://host:9100/metrics`.
- Config lives in one place (service discovery), not in every app's push URL.
- Scraping across NAT/firewalls is the real cost; solve it with an agent-mode Prometheus
  per network doing `remote_write` outward, not by pushing from apps.

## 3. When push is legitimate (Pushgateway)
Only for **service-level batch jobs** with no persistent process to scrape (a nightly
export, a cron job). Rules that matter:
- Pushgateway is **not** an aggregator or an event bus. Metrics pushed stay forever until
  deleted; a job that stops pushing still shows its last value, so `up` tells you nothing.
  Push your own last-success timestamp metric and alert on its age instead.
- Push with a stable grouping key and delete series you no longer need through the Pushgateway API.
- Scrape it with `honor_labels: true` so the pushed `job`/`instance` labels win.
- One Pushgateway per environment; it is a SPOF for those metrics, so keep it out of
  critical alerting paths.
- Machine-level batch jobs (security-update cron, config-management runs) should use the
  **Node Exporter textfile collector** instead of the Pushgateway.

## 4. Data flow and timing facts
- Samples are timestamped by the **server** at scrape time (unless the exposition carries
  its own timestamp, which is discouraged).
- An instant query returns a series only while its most recent sample is within the
  lookback period; `absent()` and `up == 0` are the two ways to notice a vanished target.
- Rule evaluation (`evaluation_interval`) is separate from scraping; alerts become
  `pending` then `firing` after `for:`.
- Alerts are sent to **every** configured Alertmanager; the Alertmanager cluster dedupes.

## 5. Sizing anchors
- Memory is roughly proportional to active series, plus query headroom.
- Disk grows with samples per second times retention; beyond one server's capacity, shard by
  job/team and federate or remote_write into Mimir/Thanos.

## Gotchas
- Two Prometheus servers scraping the same target produce slightly different sample
  timestamps; that is expected, not a bug.
- Pushing counters to the Pushgateway from several instances with the same grouping key
  overwrites each other. Use distinct `instance` or rethink.
- `up` is produced by the scraper, not by the target: 1 if the instance is reachable, 0 if the scrape failed.

## Checked
2026-10-31. Confirmed on the Prometheus overview, Pushgateway best-practice and jobs/instances pages: component roles, Pushgateway for short-lived service-level batch jobs, it is a single point of failure and never forgets series until deleted, machine-level batch jobs use the Node Exporter textfile collector, `up` and `scrape_samples_scraped` definitions. Removed: sizing figures, client-library list, PUT/POST advice, example push command and the 5-minute staleness wording (not in the fetched docs).
Method: documentation only; no commands were run.

## Verify
- [ ] Every job in `/targets` shows `UP`, and `up == 0` alerts exist with ownership.
- [ ] Any Pushgateway job has a `*_last_success_seconds` freshness alert.
- [ ] You can point at each component on the diagram and say what breaks if it dies.
