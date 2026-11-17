---
id: computing-software.messaging-and-integration.dapr.preview-features-opt-in
name: preview-features-opt-in
category: computing-software
field: messaging-and-integration
product: dapr
tags: [preview-features, configuration, features, opt-in, dapr-run, kubernetes, experimental]
level: practitioner
status: docs-checked
description: "Opt in to Dapr preview features per app via the Configuration features list: name and enabled fields, self-hosted config or dapr run --config, Kubernetes dapr.io/config."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/configuration/preview-features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Preview features ship as experimental and are off until you opt in, per application, through the `features` section of a Configuration. Each entry has `name` (the feature) and `enabled` (bool).

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: featureconfig
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin.default.svc.cluster.local:9411/api/v2/spans"
  features:
    - name: Feature1
      enabled: true
    - name: Feature2
      enabled: true
```

(`Feature1` and `Feature2` are the page placeholders; use the real feature name from the preview features list for your release.)

Self-hosted: either edit the default config created by `dapr init` (`config.yaml` in the user Dapr folder, on Windows under the user profile and on Linux/macOS under the home directory), or keep a separate file and run:

```bash
dapr run --app-id myApp --config ./previewConfig.yaml ./app
```

Kubernetes: apply the Configuration and reference it from each app that needs it.

```bash
kubectl apply -f previewConfig.yaml
```

```yaml
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "nodeapp"
        dapr.io/app-port: "3000"
        dapr.io/config: "featureconfig"
```

The page states that enablement is per application instance and that preview features are considered experimental when first released.

## Checked

2026-11-08. features properties, the example Configuration, default config file locations, the dapr run --config command and the Kubernetes apply plus dapr.io/config steps confirmed on the Enable preview features page. Changed: replaced advice about publishers, consumers and production use with what the page states.

Method: documentation only; every cited page read in full; no commands were run.
