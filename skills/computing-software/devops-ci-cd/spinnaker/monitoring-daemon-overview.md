---
id: computing-software.devops-ci-cd.spinnaker.monitoring-daemon-overview
name: monitoring-daemon-overview
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [monitoring, metrics, spinnaker-monitoring, prometheus, datadog, stackdriver, metric-filters, spectator]
level: practitioner
status: draft
description: "Understand how Spinnaker exports metrics: the spinnaker-monitoring daemon, supported systems, the /spectator/metrics endpoint, Halyard setup, and the experimental metric filter files."
sources:
  - https://spinnaker.io/docs/setup/other_config/monitoring/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Every Spinnaker microservice exposes metrics on a built-in endpoint, and the **spinnaker-monitoring daemon** collects them from each service instance and forwards them to a third-party system for dashboards and alerts. Metrics use a multi-dimensional, tag-based model. You may also scrape a microservice's HTTP endpoint `/spectator/metrics` directly; it returns a JSON document described in the Monitoring reference.

**Supported systems:** Prometheus, Datadog and Stackdriver. All three are implemented through the daemon's extension mechanism; none is native, so adding others should be straightforward.

**Halyard** ensures the daemon is installed on every host running a monitorable service and supplies the credentials or endpoints for your chosen system (`hal config metric-stores`). After deploying you can optionally install the `spinnaker-monitoring-third-party` package to get pre-configured dashboards.

**Metric filters (experimental, added in 1.10).** The daemon has a `metric_filter_dir` property, defaulting to `/opt/spinnaker-monitoring/filters`. Put `default.yml` for all services and `<service>.yml` overrides there, or place YAML files in the `monitoring-daemon/filters` folder of the Halyard profiles directory and Halyard configures it. A filter holds regular expressions in a `meters` section; by default all metrics are forwarded. Precedence: `byLiteralName` entries first, then exclusion by `excludeNameRegex`, then inclusion by `byNameRegex`. Filtering reduces cost and load on the metric store. The page says a different long-term mechanism will likely replace it.

## Checked

2026-11-04. Daemon role, tag model, scrape endpoint, supported systems, Halyard behaviour and the filter directory and precedence comment were confirmed on the Monitoring overview page.

Method: documentation only; no commands were run.
