---
id: computing-software.devops-ci-cd.flagger.flagger-datadog-and-external-metrics
name: flagger-datadog-and-external-metrics
category: computing-software
field: devops-ci-cd
product: flagger
tags: [datadog, external-metrics, rate-limits, metrictemplate]
level: advanced
status: docs-checked
description: "Use the Datadog provider in Flagger, avoid Datadog API rate limits through the cluster agent, and query the Kubernetes External Metrics API."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/metrics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Datadog: store `datadog_api_key` and `datadog_application_key` in a Secret, then set `provider.type: datadog`, `address: https://api.datadoghq.com` and `secretRef`. The query uses Datadog syntax, for example `sum:istio.mesh.request.count{reporter:destination,destination_workload:{{ target }},!response_code:404}.as_count()`.

Rate limits: large setups can hit the Datadog API limit. Instead use the Datadog Cluster Agent, which retrieves metrics in batches and exposes them as an external metrics server. After enabling the external metrics endpoint and the `DatadogMetric` CRD (registerAPIService is not required), use Flagger's external metrics provider. The server is usually `datadog-cluster-agent-metrics-server` on port 8443, and metrics are named `datadogmetric@<namespace>:<metricname>`.

External Metrics provider: `type: externalmetrics`, an `address` of the metrics server, and a `query` such as `webapp-frontend/job-success-rate?labelSelector=env%3Dproduction`. By default Flagger authenticates with its own service account; optionally supply a bearer `token` in a Secret via `secretRef`.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/metrics.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
