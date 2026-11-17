---
id: computing-software.devops-ci-cd.tekton.tekton-controller-metrics-config
name: tekton-controller-metrics-config
category: computing-software
field: devops-ci-cd
product: tekton
tags: [metrics, observability, config-observability, prometheus]
level: advanced
status: docs-checked
description: "Configure Tekton pipeline controller metric levels, duration types and labels in config-observability, and know the core metric names."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/metrics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Core metrics (all marked experimental in the docs) include `tekton_pipelines_controller_pipelinerun_duration_seconds`, `..._pipelinerun_taskrun_duration_seconds`, `..._taskrun_duration_seconds`, `..._pipelinerun_total`, `..._taskrun_total`, `..._running_pipelineruns`, `..._running_taskruns`, `..._running_taskruns_throttled_by_quota`, `..._running_taskruns_throttled_by_node`, resolution-wait gauges, and `..._taskruns_pod_latency_milliseconds` (unbounded cardinality). Infrastructure metrics are Knative workqueue (`kn_workqueue_depth`, `kn_workqueue_queue_duration_seconds`) and Go runtime metrics; all carry an `otel_scope_name` label after the OpenCensus-to-OpenTelemetry migration.

Defaults in the `config-observability` ConfigMap:

```yaml
metrics.taskrun.level: "task"
metrics.taskrun.duration-type: "histogram"
metrics.pipelinerun.level: "pipeline"
metrics.running-pipelinerun.level: ""
metrics.pipelinerun.duration-type: "histogram"
metrics.count.enable-reason: "false"
```

Levels trade detail for cardinality: taskrun metrics can be `taskrun`, `task` or `namespace`; pipelinerun metrics `pipelinerun`, `pipeline` or `namespace`. Choosing the per-run level forces `lastvalue` (gauge) instead of histogram, since a histogram of one run is useless. `metrics.count.enable-reason` adds a `reason` label to duration metrics only, never to `*_total` counters. `metrics.taskrun.throttle.enable-namespace` adds a namespace label to the quota-throttled metric.

## Checked

Checked 2026-11-08 against docs/metrics.md in tektoncd/pipeline (main), read in full. Confirmed the core and infrastructure metric names, the otel_scope_name label, the default config-observability values, the level options, the histogram-versus-lastvalue rule, metrics.count.enable-reason scope and metrics.taskrun.throttle.enable-namespace. Changed 'some experimental' to match the docs, where every core metric is marked experimental.

Method: documentation only; no commands were run.
