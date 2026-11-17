---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-agent-mode-operations
name: prometheus-agent-mode-operations
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, agent-mode, agent-mode-ops, agent-wal, prometheus-agent, remote-write, edge-collection]
level: practitioner
status: docs-checked
description: "Run Prometheus in agent mode: flags, WAL truncation and retention bounds, what is disabled (queries, rules, alerts), sizing, and monitoring the forwarder."
sources: ["https://prometheus.io/docs/prometheus/latest/feature_flags/", "https://prometheus.io/blog/2021/11/16/agent/", "https://prometheus.io/docs/prometheus/latest/command-line/prometheus/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operating Prometheus agent mode

Agent mode = scrape + WAL + remote_write only. No local TSDB blocks, no PromQL query API, no rule
evaluation, no alerting. Use it at the edge or per cluster when a central Mimir/Thanos/vendor does the rest.

## Start it
```bash
# --agent runs Prometheus in agent mode; v2.32 introduced it as experimental --enable-feature=agent
prometheus --agent \
  --config.file=/etc/prometheus/agent.yml \
  --storage.agent.path=/data/agent \
  --storage.agent.retention.min-time=5m \
  --storage.agent.retention.max-time=4h \
  --storage.agent.wal-compression
```
Scraping, service discovery and their configuration work as in server mode; querying, alerting and local
storage are disabled, and flags marked "server mode only" do not apply.

## WAL behaviour
- `--storage.agent.retention.min-time` (default 5m): minimum age samples must reach before they are considered
  for deletion when the WAL is truncated.
- `--storage.agent.retention.max-time` (default 4h): maximum age before samples are forcibly deleted at truncation, which
  bounds disk use during an outage at the cost of losing unsent data.
- Size the volume for your ingest rate times the longest outage you want to survive, up to `max-time`.

## Monitoring the agent
Same metrics as server mode for scraping and remote write:
```promql
up{job="prometheus-agent"}
prometheus_agent_active_series
rate(prometheus_remote_storage_samples_failed_total[5m])
prometheus_remote_storage_queue_highest_timestamp_seconds - prometheus_remote_storage_queue_highest_sent_timestamp_seconds
```
There is no query API, so the agent can't alert on itself: scrape it from the central side (or have it
remote-write its own metrics) and alert there, including on absence.

## Kubernetes
- Prometheus Operator (v0.64.0 or newer): `PrometheusAgent` CRD (`monitoring.coreos.com/v1alpha1`). Its spec
  resembles the Prometheus CRD, without alerting, retention or Thanos fields.
- Use persistent storage if you want buffered data to survive restarts; emptyDir loses it.

## Gotchas
- The web UI shows build info, configuration, targets and service discovery, but query capabilities are disabled;
  Grafana data sources pointing at an agent get errors.
- External labels are still applied; set `cluster`/`replica` so central dedup works.
- Do not run two collectors scraping the same targets in one cluster.

## Checked
2026-10-28. Confirmed: command-line page (`--agent`, `--storage.agent.path`, `--storage.agent.wal-compression`,
`--storage.agent.retention.min-time` default 5m and `max-time` default 4h and their meaning), agent mode blog (v2.32,
`--enable-feature=agent`, disabled features, UI behaviour), Prometheus Operator agent page (v0.64.0, `PrometheusAgent`,
`monitoring.coreos.com/v1alpha1`, unavailable fields), HTTP API page (`/api/v1/features`, v3.8), source (`prometheus_agent_active_series`,
queue metrics). Removed: config-rejection claim, WAL truncation-after-send claim, outage sizing figure, DaemonSet mode,
collector advice.
Method: documentation only; no commands were run.

## Verify
- [ ] `/api/v1/status/flags` shows the `--agent` flag you started with (or `/api/v1/features` reports `prometheus.agent_mode` on v3.8+).
- [ ] Central backend has fresh `up` series with this agent's external labels.
- [ ] WAL directory size stays bounded across a simulated backend outage.
