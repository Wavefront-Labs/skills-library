---
id: computing-software.cloud-infrastructure-engineering.observability.opentelemetry-kube-stack-chart
name: opentelemetry-kube-stack-chart
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [kube-stack-chart-install, opentelemetry-kube-stack, otel-kubernetes, otel-operator, helm]
level: practitioner
status: docs-checked
description: "Install the opentelemetry-kube-stack Helm chart: operator plus daemonset collectors, presets, webhook TLS options, CRD handling on uninstall and upgrade, 0.7 collector merge."
sources: ["https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# opentelemetry-kube-stack chart

A quickstart chart for OpenTelemetry on Kubernetes. It installs the OpenTelemetry Operator and a daemonset
collector pool covering Kubernetes infrastructure metrics, application logs, an OTLP trace receiver, Kubernetes
resource enrichment, Kubernetes events and cluster metrics. The README note says this setup requires the
leader election extension, with an alternative setup documented for cases where that is not possible.

## Prerequisites
- Kubernetes 1.24 or later for the operator, and Helm 4.0 or later (as stated in the README prerequisites).
- A TLS certificate for the operator's admission webhook. Options from the README:
  - Default: install cert-manager and set `opentelemetry-operator.admissionWebhooks.certManager.enabled` to
    true; cert-manager generates a self-signed certificate. Use `...certManager.issuerRef` (kind Issuer or
    ClusterIssuer, and name) for your own issuer.
  - Self-signed by Helm: set `...certManager.enabled` to false and `...autoGenerateCert.enabled` to true.
  - Your own certificate: set both to false and supply `cert_file`, `key_file` and `ca_file` under
    `opentelemetry-operator.admissionWebhooks`.
  - Sideload webhooks and certificate: disable `admissionWebhooks.create` and cert-manager, and set `secretName`.
  - Disable webhooks: turn off `admissionWebhooks.create` and set env var `ENABLE_WEBHOOKS` to "false".

## Install
```bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update
helm install opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack
```
Add `--namespace` if you use a custom namespace. For the Helm-generated certificate, pass
`--set opentelemetry-operator.admissionWebhooks.certManager.enabled=false` and the autoGenerateCert setting as
the README shows. The README points to its examples folder for a custom OTLP exporter, Instrumentation and OpAMP
Bridge resources.

## Presets (under defaultCRConfig.presets in the values table)
Each is off by default. logsCollection, hostMetrics, kubernetesAttributes and kubeletMetrics are best used with
mode daemonset. kubernetesEvents and clusterMetrics are best with mode deployment or statefulset and must run on
a collector with a single replica. The `presets.prometheus.*` family (nodeExporter, cadvisor, podAnnotations)
replaces the default `daemon_scrape_configs.yaml` scrape file; enabling any of them while `scrape_configs_file`
is non-empty fails chart rendering, and they require mode daemonset.

## Uninstall and upgrade
- `helm uninstall <release>` leaves the CRDs; delete them manually (opentelemetrycollectors, opampbridges and
  instrumentations under opentelemetry.io).
- CRDs are not updated by Helm on upgrade; update them manually.
- Upgrading 0.6.x to 0.7.x: the daemonset and deployment collectors were unified. Merge any custom `cluster`
  collector config into the `daemon` collector and remove the `collectors.cluster` section. GitOps tools may need
  pruning enabled to remove the old resources.

## Gotchas
- If node-exporter is installed through the subchart and a target allocator also picks up its ServiceMonitor
  while a nodeExporter preset or the scrape file is on, node-exporter metrics are scraped twice.
- The README states that the chart is not responsible for Prometheus rules, Alertmanager or a Prometheus instance.

## Checked
2026-11-09. Confirmed against the chart README on GitHub (features, prerequisites, certificate options, install,
uninstall CRD deletion, upgrade notes, preset descriptions and the values table). Removed the earlier values
example (the `collectors.cluster` layout predates 0.7), the cluster-name and Instrumentation annotation examples,
the `kubectl get` check and the port 8888 remark, none of which were confirmed. The opentelemetry.io companion
page was not read and was dropped.
Method: docs-checked 2026-11-09 against the opentelemetry-kube-stack chart README (raw.githubusercontent.com, main branch); documentation only, no commands run.
