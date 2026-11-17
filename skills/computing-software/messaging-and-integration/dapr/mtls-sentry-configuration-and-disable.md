---
id: computing-software.messaging-and-integration.dapr.mtls-sentry-configuration-and-disable
name: mtls-sentry-configuration-and-disable
category: computing-software
field: messaging-and-integration
product: dapr
tags: [mtls, sentry, configuration, daprsystem, workloadcertttl, allowedclockskew, kubernetes]
level: practitioner
status: docs-checked
description: "Control Dapr mTLS via the daprsystem Configuration: enabled, workloadCertTTL, allowedClockSkew, restarts after edits, disabling with Helm or CLI, and Sentry logs."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/security/mtls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sentry is the control plane Certificate Authority. Without your own certs Dapr creates and persists self-signed root and issuer certs valid for one year; on Kubernetes they sit in a secret in the Dapr system namespace, in self-hosted mode on disk. The mTLS settings live in the control plane Configuration, which Dapr creates on Kubernetes with these defaults:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: daprsystem
  namespace: default
spec:
  mtls:
    enabled: true
    workloadCertTTL: "24h"
    allowedClockSkew: "15m"
```

View it with `kubectl get configurations/daprsystem --namespace <DAPR_NAMESPACE> -o yaml` and edit with `kubectl edit configurations/daprsystem --namespace <DAPR_NAMESPACE>`. After saving, roll the control plane (the sidecar injector does not need it):

```
kubectl rollout restart deploy/dapr-sentry -n <DAPR_NAMESPACE>
kubectl rollout restart deploy/dapr-operator -n <DAPR_NAMESPACE>
kubectl rollout restart statefulsets/dapr-placement-server -n <DAPR_NAMESPACE>
```

Disable mTLS for workloads (the control plane keeps using mTLS):

```bash
helm install --set global.mtls.enabled=false --namespace dapr-system dapr dapr/dapr
dapr init --kubernetes --enable-mtls=false
```

Sentry logs: `kubectl logs --selector=app=dapr-sentry --namespace <DAPR_NAMESPACE>`.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; all claims matched the page and none were changed.

Method: documentation only; no commands were run.
