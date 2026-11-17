---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-katib-metrics-collector
name: kubeflow-katib-metrics-collector
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [metrics-collector, stdout, tfevent, push-collector, report-metrics, metrics-format]
level: practitioner
status: docs-checked
description: "Configure how Katib collects Trial metrics: StdOut, File (TEXT or JSON), TensorFlowEvent, Custom and Push collectors, the namespace label and the metricsFormat regex."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/metrics-collector.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Katib metrics collector

Namespace prerequisite for pull-based collectors: label it `katib.kubeflow.org/metrics-collector-injection=enabled`, for example `kubectl label namespace <ns> katib.kubeflow.org/metrics-collector-injection=enabled`.

Set the collector in `metricsCollectorSpec`:

Pull-based (a sidecar reads output):
- `StdOut` (default): reads standard output.
- `File`: reads `.source.fileSystemPath.path` (default `/var/log/katib/metrics.log`), format `TEXT` (default) or `JSON`. JSON lines must carry `epoch` or `step` and a `timestamp` key.
- `TensorFlowEvent`: reads a tf.Event directory (default `/var/log/katib/tfevent/`). Since Katib 0.18, torch.utils.tensorboard or tensorboardX output also works.
- `Custom`: define your own container in `.collector.customCollector`.

Format: `.source.filter.metricsFormat` is a regex with two groups, name then value. The default matches `name=value` pairs, so printing `loss=3.0e-02` and `recall=0.5` each epoch works.

Push-based: training code calls `katib.report_metrics({"result": result})`, which sends a gRPC request with an automatic timestamp to the Katib DB Manager. The `kubeflow-katib` package must be installed in the training container. Select it with `.collector.kind: Push` in YAML, or `metrics_collector_config={"kind": "Push"}` in `tune()`.

## Checked

2026-11-08. Confirmed against the metrics collector guide: the namespace label and command, collector kinds and defaults, JSON format rule, tf.Event note, default metricsFormat behaviour and the push-based flow. Nothing needed removal.
Method: docs-only read of cited pages, 2026-11-08
