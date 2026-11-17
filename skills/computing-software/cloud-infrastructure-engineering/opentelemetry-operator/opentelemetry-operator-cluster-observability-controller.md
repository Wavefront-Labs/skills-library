---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-cluster-observability-controller
name: opentelemetry-operator-cluster-observability-controller
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, clusterobservability, controller-of-controllers, agent-collector, cluster-collector, feature-gate]
level: advanced
status: docs-checked
description: "Deploy cluster-wide observability with one ClusterObservability resource that creates an agent DaemonSet, a cluster StatefulSet and an Instrumentation resource."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/collector/cluster-observability.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ClusterObservability controller

`ClusterObservability` (apiVersion `opentelemetry.io/v1alpha1`) deploys observability for a whole cluster from one resource. It follows a controller-of-controllers pattern, creating ordinary `OpenTelemetryCollector` and `Instrumentation` resources that their own controllers then reconcile:
- Agent Collector: a DaemonSet for node-level metrics, logs and a host OTLP receiver (kubeletstats and filelog receivers; OTLP on 4317 and 4318 over the host network).
- Cluster Collector: a StatefulSet for cluster-level metrics (k8s_cluster receiver).
- One Instrumentation resource, pointing at the local agent.

It is gated behind `operator.clusterobservability`: start the manager with `--feature-gates=+operator.clusterobservability`.

The spec has a single main field, `exporter`, an OTLP HTTP exporter (`endpoint`, optional `traces_endpoint`, `metrics_endpoint`, `logs_endpoint`, `headers`, `compression`, `timeout`). All signals are enabled by default. TLS file mounting (`ca_file`, `cert_file`, `key_file`) is not supported yet.

Pod Security: the agent needs `hostNetwork` and hostPath volumes, so label its namespace `pod-security.kubernetes.io/enforce=privileged` before creating the resource. OpenShift is detected automatically and gets a scoped SecurityContextConstraints, plus kubelet CA verification; on other platforms the base config skips kubelet certificate verification.

Applications opt in by annotating pods with `instrumentation.opentelemetry.io/inject-java: "namespace/name"` referencing the single Instrumentation resource in the ClusterObservability namespace (pattern `namespace/instrumentation-name`). Only one ClusterObservability resource is active per cluster: the oldest stays active and later ones are marked Conflicted.

## Checked

2026-11-04. Confirmed against docs/collector/cluster-observability.md: the controller-of-controllers pattern, agent DaemonSet and cluster StatefulSet, the single Instrumentation resource, the `operator.clusterobservability` feature gate, the single `exporter` field and its sub-fields, TLS file mounting not supported yet, the privileged Pod Security label, OpenShift SCC and kubelet CA handling, and the inject annotation pattern (the page example uses `inject-java`). Added the documented singleton and Conflicted behaviour. Nothing else removed.

Method: documentation only; no commands were run.
