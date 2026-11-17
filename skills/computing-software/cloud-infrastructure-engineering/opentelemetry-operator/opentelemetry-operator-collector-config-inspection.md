---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-collector-config-inspection
name: opentelemetry-operator-collector-config-inspection
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, config-parsing, receiver-ports, headless-service, openshift-serving-cert, enablemetrics]
level: practitioner
status: docs-checked
description: "Know which parts of the Collector config the operator parses: receiver ports for Services, and the metrics port for ServiceMonitor creation, including env-var failure modes."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/getting-started/collector.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# How the operator inspects collector config

Although most of `spec.config` is passed through untouched, the operator reads it for two purposes.

1. Discover receivers and their ports. When receivers expose ports, the operator creates a pair of Kubernetes Services, one of them headless, exposing those ports inside the cluster. If a port uses environment variable expansion or cannot be parsed, reconciliation returns an error. The headless Service carries the annotation `service.beta.openshift.io/serving-cert-secret-name`, which makes OpenShift create a Secret holding a certificate and key. Mount that Secret as a volume and reference the files in the receivers' TLS settings.

2. Check whether Collector observability is enabled through `spec.observability.metrics.enableMetrics`. If it is, a Service and a ServiceMonitor (a PodMonitor in sidecar mode) are created for the instance. A metrics address with an invalid port, or one that uses environment variable expansion for the port, produces an error. The documented workaround is to set `enableMetrics` to `false` and create the Service and monitor yourself with the right port.

Practical consequences:
- Do not put `${env:PORT}` style expansion in receiver endpoints or in the Collector's own telemetry address if you rely on auto-created Services.
- When you need ports the operator cannot infer, `spec.ports` can list them explicitly (the API reference says the operator infers ports by parsing `.spec.config` and that `ports` can open additional ones it cannot infer, such as for custom receivers).

## Checked

2026-11-04. Confirmed against docs/getting-started/collector.md: `config` passed through as-is, the operator inspects config to discover receivers and ports (a pair of Services, one headless), the error on environment variable expansion or unparseable ports, the OpenShift `service.beta.openshift.io/serving-cert-secret-name` annotation on the headless Service, the `spec.observability.metrics.enableMetrics` check, the ServiceMonitor/PodMonitor creation, the invalid-port error and the enableMetrics false workaround. Confirmed in the generated OpenTelemetryCollector API reference (docs/api/opentelemetrycollectors.md, read as raw Markdown because the GitHub page view is a stub): `ports` and `enableMetrics` (ServiceMonitor, or PodMonitor in sidecar mode). Removed the unconfirmed claim that a Collector without receiver ports gets no Services.

Method: documentation only; no commands were run.
