---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-opamp-bridge-overview
name: opentelemetry-operator-opamp-bridge-overview
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, opamp-bridge, opamp, opamp-server, remote-config, opamp-capabilities]
level: intro
status: docs-checked
description: "Understand the OpAMP Bridge that reports Collector state to an OpAMP server and applies remote config, and how to install it with the operator or the kube-stack chart."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/cmd/operator-opamp-bridge/README.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/opamp-bridge/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OpAMP Bridge overview and installation

The OpAMP Bridge is an optional operator component that implements the agent side of the OpAMP protocol so Collectors in Kubernetes can be reported on and managed by an OpAMP server. It can:
- Report status and effective configuration of `OpenTelemetryCollector` instances to the server.
- Receive Collector configurations from the server and perform the CRUD operations against the Kubernetes API to change the Collector resources.
- Emit its own telemetry to an OTLP/HTTP endpoint.

Example servers named in the docs: `jaronoff97/opamp-elixir` and `jaronoff97/opamp-operator-server`. A design document is linked from the README.

Installation: either as part of the operator, by creating an `OpAMPBridge` custom resource, or through the OpenTelemetry Kube Stack Helm chart, a quickstart that installs an operator and a suite of collectors including the bridge.

The `OpAMPBridge` spec core fields: `endpoint` (server address), `capabilities` (map such as `AcceptsRemoteConfig`, `ReportsEffectiveConfig`, `ReportsHealth`, `ReportsRemoteConfig`), `headers` (typically auth tokens), `tls`, `proxy`, `componentsAllowed` and `description`. `replicas` has a maximum of 1.

Note: `docs/opamp-bridge/README.md` is a placeholder saying documentation for the `OpAMPBridge` CRD is planned, pointing to the API reference, so the bridge README under `cmd/operator-opamp-bridge` is the working guide.

## Checked

2026-11-04. Confirmed against cmd/operator-opamp-bridge/README.md: the three capabilities of the bridge, the two named example servers, the design document link, and the two installation routes (OpAMPBridge custom resource, Kube Stack Helm chart quickstart). Confirmed against docs/api/opampbridges.md (raw Markdown): the spec fields endpoint, capabilities, headers, tls, proxy, componentsAllowed, description and replicas maximum 1. Confirmed that docs/opamp-bridge/README.md is a placeholder pointing to the API reference. Nothing removed.

Method: documentation only; no commands were run.
