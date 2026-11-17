---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-opamp-bridge-crd-labels
name: opentelemetry-operator-opamp-bridge-crd-labels
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, opamp-managed, opamp-reporting, componentsallowed, opampbridge-crd, collector-labels]
level: practitioner
status: docs-checked
description: "Create an OpAMPBridge with allowed components and opt Collectors in with the opentelemetry.io/opamp-reporting or opamp-managed labels, optionally naming a bridge."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/cmd/operator-opamp-bridge/README.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/api/opampbridges.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OpAMPBridge resource and collector labels

Create the bridge:

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: OpAMPBridge
metadata:
  name: opamp-bridge
spec:
  endpoint: "<OPAMP_SERVER_ENDPOINT>"
  capabilities:
    AcceptsRemoteConfig: true
    ReportsEffectiveConfig: true
    ReportsHealth: true
    ReportsRemoteConfig: true
  componentsAllowed:
    receivers: [otlp]
    processors: [memory_limiter, batch]
    exporters: [otlphttp]
```

`componentsAllowed` is a list of allowed OpenTelemetry components for each pipeline type, so the bridge works with a specific set of components.

A Collector is operated by the bridge only if its `OpenTelemetryCollector` carries a label:
- `opentelemetry.io/opamp-reporting: "true"`: reporting only.
- `opentelemetry.io/opamp-managed: "true"`: reporting and management (remote config can be applied).
- `opentelemetry.io/opamp-managed: opamp-bridge`: the label value can name a specific bridge instance that should manage it.

Other spec fields from the API reference: `headers` for authorization, `tls` for the server connection, `proxy` for the backend connection only, `serviceAccount`, `upgradeStrategy`, scheduling fields, and `replicas` limited to a maximum of 1.

## Checked

2026-11-04. Confirmed against cmd/operator-opamp-bridge/README.md: the OpAMPBridge example, the label requirement, `opamp-reporting` for reporting only, `opamp-managed` for reporting and management, and a bridge name as the `opamp-managed` value. Confirmed against docs/api/opampbridges.md (raw Markdown): `capabilities`, `componentsAllowed`, `headers` for access tokens, `proxy` used only for the backend connection, `serviceAccount`, `upgradeStrategy` (automatic or none), `nodeSelector` and `replicas` with maximum 1. Reworded the componentsAllowed explanation and removed the unconfirmed selection advice.

Method: documentation only; no commands were run.
