---
id: computing-software.devops-ci-cd.flagger.flagger-keda-scaledobject-canary
name: flagger-keda-scaledobject-canary
category: computing-software
field: devops-ci-cd
product: flagger
tags: [keda, scaledobject, autoscaling, blue-green]
level: advanced
status: docs-checked
description: "Autoscale a workload with a KEDA ScaledObject during a Flagger canary analysis, using the Kubernetes provider and blue/green."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/tutorials/keda-scaledobject.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements: Kubernetes v1.16 or newer and KEDA 2.7.1 or newer. The tutorial uses blue/green with the Kubernetes provider, installed with `--set prometheus.install=true --set meshProvider=kubernetes`, but any strategy and provider can be combined with this.

Flagger takes a Deployment and a KEDA ScaledObject that targets it, then creates the primary and canary Deployments, ClusterIP Services and a second ScaledObject targeting the generated Deployment.

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: podinfo-so
  namespace: test
spec:
  scaleTargetRef:
    name: podinfo
  pollingInterval: 10
  cooldownPeriod: 20
  minReplicaCount: 1
  maxReplicaCount: 3
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://flagger-prometheus.flagger:9090
      query: sum(rate(http_requests_total{ app="podinfo" }[30s]))
      threshold: '5'
```

The Canary then references the ScaledObject as its autoscaler. A load tester (`kubectl apply -k https://github.com/fluxcd/flagger//kustomize/tester?ref=main`) generates the traffic that drives scaling during analysis.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/tutorials/keda-scaledobject.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
