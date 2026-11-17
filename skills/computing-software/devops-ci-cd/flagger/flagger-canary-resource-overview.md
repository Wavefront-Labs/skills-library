---
id: computing-software.devops-ci-cd.flagger.flagger-canary-resource-overview
name: flagger-canary-resource-overview
category: computing-software
field: devops-ci-cd
product: flagger
tags: [canary, crd, progressive-delivery, targetref]
level: intro
status: docs-checked
description: "Read and write the Flagger Canary custom resource: targetRef, service port and the analysis block with metrics and webhooks."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/how-it-works.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `Canary` custom resource (`flagger.app/v1beta1`) defines the release process of one workload and is portable across clusters, meshes and ingress providers.

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: podinfo
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: podinfo
  service:
    port: 9898
  analysis:
    interval: 1m
    threshold: 10
    maxWeight: 50
    stepWeight: 5
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: 500
        interval: 1m
    webhooks:
      - name: load-test
        url: http://flagger-loadtester.test/
        metadata:
          cmd: "hey -z 1m -q 10 -c 2 http://podinfo-canary.test:9898/"
```

When a new version is deployed Flagger shifts traffic gradually while measuring success rate and average response duration. Extend the analysis with custom metrics, acceptance tests and load tests. If several meshes or ingress controllers share a cluster, override the global provider per canary with `spec.provider`.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/how-it-works.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
