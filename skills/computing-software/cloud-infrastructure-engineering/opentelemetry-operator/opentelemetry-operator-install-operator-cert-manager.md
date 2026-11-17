---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-install-operator-cert-manager
name: opentelemetry-operator-install-operator-cert-manager
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, install, cert-manager, helm-chart, kubectl-apply, operator-deployment]
level: intro
status: docs-checked
description: "Install the OpenTelemetry Operator on an existing cluster with cert-manager and the release manifest, or through the Helm chart, and know what it manages."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/README.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/getting-started/collector.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/getting-started/compatibility.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/reference/configuration.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/cmd/operator-opamp-bridge/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install the OpenTelemetry Operator

The OpenTelemetry Operator is a Kubernetes Operator that manages two things: OpenTelemetry Collector instances and auto-instrumentation of workloads using OpenTelemetry instrumentation libraries.

Prerequisite: `cert-manager` must already be installed in the cluster; the README says to make sure it is installed before applying the manifest, and the compatibility page says the operator uses cert-manager for some features. Then apply the latest release manifest:

```bash
kubectl apply -f https://github.com/open-telemetry/opentelemetry-operator/releases/latest/download/opentelemetry-operator.yaml
```

Wait for the `opentelemetry-operator` deployment to become ready before creating any custom resources. The README also points to a Helm chart in the `opentelemetry-helm-charts` repository, and the OpAMP Bridge README says the bridge is available as a component of the OpenTelemetry Kube Stack Helm chart, which installs an operator plus a suite of collectors.

Private GKE clusters need one extra step: the control-plane (master) nodes must be allowed to reach port `9443/tcp` on worker nodes, either with a new firewall rule or by widening the existing rule that allows ports 80, 443 and 10254, because 9443 is the default `webhook-port` of the manager.

The README lists the user documentation under `docs/` by section: getting started, concepts, collector (`OpenTelemetryCollector`), auto-instrumentation (`Instrumentation`), Target Allocator, OpAMP Bridge (`OpAMPBridge`), use cases, troubleshooting, reference (API docs, CRD changelog, feature gates) and design RFCs. The next step after installing is to create a first Collector resource.

## Checked

2026-11-04. Confirmed against README.md: the two things the operator manages, the cert-manager prerequisite, the `kubectl apply` of the latest release manifest, waiting for the deployment before creating a Collector, the Helm chart pointer and the docs sections. Confirmed against docs/getting-started/collector.md: the private GKE firewall step for port 9443/tcp (and the 80, 443 and 10254 rule). Confirmed against docs/reference/configuration.md: `webhook-port` default 9443. Confirmed against cmd/operator-opamp-bridge/README.md: the Kube Stack Helm chart bundles the OpAMP Bridge. Removed the claims that webhooks use cert-manager certificates and the exact chart names, which these pages do not state.

Method: documentation only; no commands were run.
