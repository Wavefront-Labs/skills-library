---
id: computing-software.cloud-infrastructure-engineering.kubernetes.blue-green-deploy-via-service-selector-swap
name: blue-green-deploy-via-service-selector-swap
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, blue-green, selector-swap, deployment-strategies, service, rollback, ckad]
level: practitioner
status: docs-checked
description: "Do blue/green on plain Kubernetes by running two Deployments and switching the Service selector, with preview testing, connection draining, instant rollback, and cleanup."
sources: ["https://kubernetes.io/docs/concepts/services-networking/service/", "https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/", "https://github.com/argoproj/argo-rollouts/blob/master/docs/features/bluegreen.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Blue/green via Service selector swap

## Setup
Two Deployments differing in a `slot` label; the Service selects one slot.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata: {name: web-green}
spec:
  replicas: 4
  selector: {matchLabels: {app: web, slot: green}}
  template:
    metadata: {labels: {app: web, slot: green}}
    spec:
      containers: [{name: web, image: "registry.example.com/web:2.0.0", readinessProbe: {httpGet: {path: /ready, port: 8080}}}]
---
apiVersion: v1
kind: Service
metadata: {name: web}
spec:
  selector: {app: web, slot: blue}      # live
  ports: [{port: 80, targetPort: 8080}]
---
apiVersion: v1
kind: Service
metadata: {name: web-preview}
spec:
  selector: {app: web, slot: green}     # candidate
  ports: [{port: 80, targetPort: 8080}]
```

## Cutover
```bash
kubectl rollout status deploy/web-green                       # all replicas Ready
kubectl patch svc web -p '{"spec":{"selector":{"app":"web","slot":"green"}}}'
kubectl get endpointslices -l kubernetes.io/service-name=web -o wide            # green pod IPs only
```
Smoke-test the candidate through `web-preview` before the patch. Rollback is the same patch back to
`blue`, while blue is still running.

## What happens to traffic
- After a selector change there is a propagation delay before all nodes update their rules to
  send traffic to the new pods (Argo Rollouts documents this delay for its own blue-green
  strategy, and uses `scaleDownDelaySeconds` to keep the old ReplicaSet around for it).
- Keep blue running through the bake period so rollback is instant.
- Stateful sessions need a shared store, because the two versions are separate pod sets.

## Rules
- Green must be at full capacity (same replicas, HPA minimum) before the swap.
- The database schema must work for both versions (expand/contract migrations).
- In GitOps the selector is a value in Git: the swap is a commit, and rollback is a revert.
- Cleanup: scale blue to 0 after the bake period; the next release deploys into blue.

## When to use a tool instead
Argo Rollouts `strategy.blueGreen` automates this with an active service and a `previewService`,
`autoPromotionEnabled`, `prePromotionAnalysis`, `postPromotionAnalysis` and
`scaleDownDelaySeconds`; use it when you do this more than occasionally.

## Verify
- [ ] The Service's EndpointSlices contain only the intended slot's pods; error rate and latency stay flat across the swap; blue stays Ready for the rollback window.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the Argo Rollouts blue-green documentation (previewService, autoPromotionEnabled, prePromotionAnalysis, postPromotionAnalysis, scaleDownDelaySeconds, selector-change propagation delay) and the Service concept page (selectors, EndpointSlices). Removed unconfirmed claims about keep-alive, HTTP/2 and gRPC connections staying on blue, the sub-second switch time, auto-rollback, the curl image and the acme registry image.

Method: documentation only; no commands were run.
