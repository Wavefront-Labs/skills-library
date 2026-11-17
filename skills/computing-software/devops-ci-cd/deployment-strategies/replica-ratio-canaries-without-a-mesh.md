---
id: computing-software.devops-ci-cd.deployment-strategies.replica-ratio-canaries-without-a-mesh
name: replica-ratio-canaries-without-a-mesh
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, replica-ratio-canary, canary, kubernetes-canary, label-selector, stable-and-canary-deployments, traffic-split]
level: practitioner
status: draft
description: "Run canaries on plain Kubernetes or VM pools by replica ratio: two Deployments behind one Service, sizing the split, sticky-session caveats, metrics by track label and rollback."
sources:
  - https://kubernetes.io/docs/concepts/workloads/management/#canary-deployments
  - https://argoproj.github.io/argo-rollouts/features/canary/
  - https://kubernetes.io/docs/concepts/services-networking/service/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Replica-ratio canaries without a mesh

Without Istio/Linkerd/a smart ingress, you can still canary by running a few pods of the new version behind the same Service. Traffic share is roughly `canary replicas / total replicas`.

## Two Deployments, one Service
```yaml
apiVersion: v1
kind: Service
metadata: { name: web }
spec:
  selector: { app: web }            # no 'track' label: selects both
  ports: [{ port: 80, targetPort: 8080 }]
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: web-stable }
spec:
  replicas: 9
  selector: { matchLabels: { app: web, track: stable } }
  template:
    metadata: { labels: { app: web, track: stable, version: "1.4.0" } }
    spec: { containers: [{ name: web, image: "registry/web@sha256:aaa..." }] }
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: web-canary }
spec:
  replicas: 1                       # ~10%
  selector: { matchLabels: { app: web, track: canary } }
  template:
    metadata: { labels: { app: web, track: canary, version: "1.5.0" } }
    spec: { containers: [{ name: web, image: "registry/web@sha256:bbb..." }] }
```

## Limits of the approach
- Granularity: with 10 pods the smallest step is 10%; 1% needs 100 pods. Scale stable up temporarily for finer splits.
- kube-proxy balances per **connection**, not per request; long-lived HTTP/2/gRPC connections or keep-alive clients can pin to one version. Uneven traffic is common.
- No header-based routing (no "send internal users to canary").
- Session affinity (`sessionAffinity: ClientIP`) skews the ratio and keeps users on one version - fine for consistency, bad for measuring.
- HPA on both Deployments changes the ratio as they scale independently; disable HPA on the canary or keep min=max.

## Measure by track
Expose the version label in metrics (pod label via Prometheus relabelling) and compare:
```promql
sum(rate(http_requests_total{app="web",track="canary",code=~"5.."}[5m])) / sum(rate(http_requests_total{app="web",track="canary"}[5m]))
```
Compare against stable over the same window; also latency p95/p99.

## Promote / roll back
- Promote: update `web-stable` image to the canary digest (rolling update), then scale canary to 0.
- Roll back: `kubectl scale deploy/web-canary --replicas=0` - instant.
- Argo Rollouts without a traffic router does exactly this (`setWeight` approximated by replica count) and adds automated analysis.

## On VMs
Same idea with a load balancer pool: add one new-version instance to a 10-instance target group; weight it lower if the LB supports weights.

## Verify
- [ ] Canary pods receive roughly the expected share (requests by track) over 15 minutes.
- [ ] Scaling canary to zero restores 100% stable with no errors.
