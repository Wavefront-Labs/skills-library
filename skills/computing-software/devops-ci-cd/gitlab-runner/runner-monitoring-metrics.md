---
id: computing-software.devops-ci-cd.gitlab-runner.runner-monitoring-metrics
name: runner-monitoring-metrics
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [monitoring, prometheus, metrics, listen-address, pprof]
level: practitioner
status: docs-checked
description: "Expose Prometheus metrics and pprof from the runner."
sources: ["https://docs.gitlab.com/runner/monitoring/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Monitoring the runner

Set `listen_address` in the global section of `config.toml` (the docs example port is `9252`) and the runner serves Prometheus metrics at `/metrics`.

Metrics are prefixed `gitlab_runner_`. Scrape them with a Prometheus job targeting the runner host.

The same server exposes pprof at `/debug/pprof/` for profiling.

The docs warn that the metrics server exposes information about the runner and must not be publicly available. Bind to a private address or restrict access with firewall rules.

In the Helm chart, the metrics port setting (`9252` in the example values) can be paired with a prometheus-operator `serviceMonitor` for automatic discovery.

## Checked

2026-11-03. Confirmed against listen_address, port 9252, metrics, pprof and serviceMonitor on the Monitoring page.

Method: documentation only; no commands were run.
