---
id: computing-software.messaging-and-integration.dapr.configuration-apply-to-sidecar
name: configuration-apply-to-sidecar
category: computing-software
field: messaging-and-integration
product: dapr
tags: [configuration, dapr-config, annotations, dapr-run, kubernetes, daprsystem, self-hosted]
level: practitioner
status: docs-checked
description: "Apply a Dapr Configuration to a sidecar: self-hosted file and --config, Kubernetes resource plus dapr.io/config annotation, dapr configurations -k, and daprsystem mTLS."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/configuration/configuration-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Dapr Configuration changes the behaviour of one app sidecar (or, for `daprsystem`, the control plane).

Self-hosted: the configuration is a file such as `config.yaml`. The sidecar looks for it in the default Dapr folder under the user home (`config.yaml`), or you pass a path: `dapr run --config <file>`.

Kubernetes: it is a Configuration resource.

```bash
kubectl apply -f myappconfig.yaml
dapr configurations -k
```

Reference it from the pod template (it is read by the sidecar injector):

```yml
  annotations:
    dapr.io/enabled: "true"
    dapr.io/app-id: "nodeapp"
    dapr.io/app-port: "3000"
    dapr.io/config: "myappconfig"
```

Settings sections available per app: tracing, metrics, logging, `httpPipeline` / `appHttpPipeline` middleware, name resolution, secret store scopes, access control allow lists for building block APIs and for service invocation, `components.deny`, and preview features.

Control plane: a single Configuration called `daprsystem` is installed by Kubernetes deployments and holds global settings, currently only `mtls`. Properties: `enabled`, `allowedClockSkew` (Go duration, default `15m`), `workloadCertTTL` (default `24h`), `sentryAddress`, `controlPlaneTrustDomain`, `tokenValidators`.

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: daprsystem
  namespace: default
spec:
  mtls:
    enabled: true
    allowedClockSkew: 15m
    workloadCertTTL: 24h
```

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; all claims matched the page and none were changed.

Method: documentation only; no commands were run.
