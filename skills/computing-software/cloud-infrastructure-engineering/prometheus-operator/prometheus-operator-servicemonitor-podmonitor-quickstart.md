---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-servicemonitor-podmonitor-quickstart
name: prometheus-operator-servicemonitor-podmonitor-quickstart
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [servicemonitor-example, podmonitor-example, metrics-port-name, monitor-sample-app, team-label]
level: intro
status: docs-checked
description: "Monitor a sample application with a ServiceMonitor (via a Service) or a PodMonitor (via pod labels), and link them to Prometheus selectors."
sources:
  - https://prometheus-operator.dev/docs/developer/getting-started/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites: a running operator, a running Prometheus with RBAC, and an application exposing metrics on a port (the guide uses `quay.io/brancz/prometheus-example-app` on 8080).

## ServiceMonitor
1. Create a Service that selects the pods (label `app: example-app`) and **names** the metrics port (for example `web`).
2. Create a `ServiceMonitor` whose `spec.selector.matchLabels` is `app: example-app` and whose `spec.endpoints` lists `port: web`. Give it a label such as `team: frontend`.
3. The `Prometheus` object picks it up through `spec.serviceMonitorSelector.matchLabels: {team: frontend}`.

The ServiceMonitor references a Service by labels and by port **name**, never the Deployment or Pod.

## PodMonitor
A `PodMonitor` skips the Service and finds targets from pod labels in `spec.selector`, with `podMetricsEndpoints` naming the container port. The Prometheus object selects it with `spec.podMonitorSelector`.

## Choosing
A ServiceMonitor requires a Service; a PodMonitor bypasses the Service and finds targets from pod labels. Either is selected only if its labels match the Prometheus `serviceMonitorSelector` or `podMonitorSelector`.

## Checked

2026-11-08. Read the developer getting started guide in full. Manifests, selectors and the example app match. Removed unsourced remarks about when to choose each monitor and the Targets page.

Method: documentation only; no commands were run.
