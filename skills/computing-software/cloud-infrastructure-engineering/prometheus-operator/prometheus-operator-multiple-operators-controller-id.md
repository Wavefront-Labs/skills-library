---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-multiple-operators-controller-id
name: prometheus-operator-multiple-operators-controller-id
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [controller-id-annotation, multiple-operators, terminating-loop, reconcile-conflict, operator-prometheus-io]
level: advanced
status: docs-checked
description: "Stop Prometheus or Alertmanager pods flapping in a terminating loop caused by two operators, and run several operators safely with --controller-id."
sources: ["https://prometheus-operator.dev/docs/platform/troubleshooting/", "https://prometheus-operator.dev/docs/platform/operator/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## Symptom
Prometheus or Alertmanager pods enter a terminating loop although start-up logs look healthy. This usually means more than one operator wants to manage the same resource.

## Diagnose
`kubectl get pods --all-namespaces | grep 'prom.*operator'`, then compare the logs of each operator for the same resources.

## Fix: controller-id
Give each operator a different `--controller-id`. Each reconciles only resources carrying the annotation `operator.prometheus.io/controller-id` with the same value. The resource owner must set the annotation; the operator never adds it.

| Operator has `--controller-id` | Resource has the annotation | Result |
|---|---|---|
| yes | yes | reconciled only if values match |
| yes | no | not reconciled |
| no | yes | not reconciled |
| no | no | reconciled |

If `--controller-id` is unset, the operator reconciles everything except annotated resources, which is how conflicts arise. Apply to Alertmanager, Prometheus, PrometheusAgent and ThanosRuler objects.

## Checked

2026-11-08. Read the troubleshooting page and the CLI reference in full. Added the CLI reference as a source, which confirms the object kinds controller-id filters.

Method: documentation only; no commands were run.
