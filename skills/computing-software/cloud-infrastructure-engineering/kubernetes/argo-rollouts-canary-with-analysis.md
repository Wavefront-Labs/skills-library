---
id: computing-software.cloud-infrastructure-engineering.kubernetes.argo-rollouts-canary-with-analysis
name: argo-rollouts-canary-with-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, argo-rollouts, analysistemplate, analysis-template, canary-traffic-routing, nginx-canary-annotations, kubectl-argo-rollouts, rollout-promote, progressive-delivery]
level: advanced
status: docs-checked
description: "Run Argo Rollouts canaries end to end: traffic routing via ingress-nginx or Istio, AnalysisTemplates on Prometheus metrics, and promote/abort/undo with the kubectl plugin."
sources: ["https://argo-rollouts.readthedocs.io/en/stable/features/canary/", "https://argo-rollouts.readthedocs.io/en/stable/features/analysis/", "https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/nginx/", "https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo Rollouts canary with traffic routing and analysis

## Rollout with ingress-nginx traffic routing
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata: {name: web}
spec:
  replicas: 10
  selector: {matchLabels: {app: web}}
  template: {...}                       # same as a Deployment template
  strategy:
    canary:
      stableService: web-stable
      canaryService: web-canary
      trafficRouting:
        nginx: {stableIngress: web}     # controller creates web-canary ingress with canary annotations
        # istio: {virtualService: {name: web, routes: [primary]}}
      analysis:                         # background analysis for the whole rollout
        templates: [{templateName: success-rate}]
        startingStep: 1
        args: [{name: service-name, value: web-canary.default.svc.cluster.local}]
      steps:
      - setWeight: 5
      - pause: {duration: 5m}
      - setWeight: 25
      - pause: {duration: 10m}
      - setWeight: 50
      - pause: {}                       # manual gate
```
Without traffic management the controller makes a best-effort attempt to approximate the weights
with replica counts. With nginx, the controller
sets the `canary: "true"` and `canary-weight` annotations (default `nginx.ingress.kubernetes.io`
prefix) on a generated canary Ingress; add extra annotations through
`additionalIngressAnnotations` or `canaryIngressAnnotations` rather than hand-editing it. Both Services must exist; the controller patches their selectors
with `rollouts-pod-template-hash`.

## AnalysisTemplate
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata: {name: success-rate}
spec:
  args: [{name: service-name}]
  metrics:
  - name: success-rate
    interval: 1m
    count: 10
    failureLimit: 2
    successCondition: result[0] >= 0.99
    provider:
      prometheus:
        address: http://prometheus-operated.monitoring:9090
        query: |
          sum(irate(
            istio_requests_total{reporter="source",destination_service=~"{{args.service-name}}",response_code!~"5.*"}[5m]
          )) /
          sum(irate(
            istio_requests_total{reporter="source",destination_service=~"{{args.service-name}}"}[5m]
          ))
```
The query above is the Istio success-rate query from the Argo Rollouts docs (Prometheus returns a
vector, hence `result[0]`); swap in your ingress controller's request metrics if you use nginx.
Too many failures (`failureLimit`) abort the rollout: traffic goes back to the stable Service.
Guard against "no data": Prometheus can return an empty array, so decide the outcome explicitly,
for example `successCondition: len(result) == 0 || result[0] >= 0.99` treats no data as success
(the docs show both the success and failure variants). Providers include Prometheus, Datadog,
New Relic, CloudWatch, Wavefront, Graphite, InfluxDB, Kayenta, SkyWalking, Web (HTTP) and Job.

## Operating with the kubectl plugin
```bash
kubectl argo rollouts get rollout web --watch
kubectl argo rollouts promote web             # skip current pause
kubectl argo rollouts promote web --full      # skip analysis, pauses and steps
kubectl argo rollouts abort web               # back to stable; spec.template still holds the new version
kubectl argo rollouts retry rollout web       # after abort, re-run
kubectl argo rollouts undo web                # roll spec back to previous revision
kubectl argo rollouts set image web web=myapp:1.9.1
kubectl argo rollouts dashboard               # local UI
```
After `abort`, `spec.template` still describes the new version and the Rollout will try to reach it
if it leaves the aborted state, so fix forward (new image), `retry rollout`, or `undo`; in GitOps,
revert the commit instead of `undo` to avoid drift.

## Verify
- [ ] A deliberately failing canary (inject 5xx) aborts automatically within the analysis window.
- [ ] `kubectl argo rollouts get rollout web` shows Healthy, stable = new revision after success.

## Checked

Documentation release: Argo Rollouts docs (argo-rollouts repo docs/, latest release v1.10.1, repo commit 2026-10-20).
Confirmed: `stableService`, `canaryService`, `trafficRouting.nginx.stableIngress`, Istio `virtualService` with `routes`; nginx canary annotations and `additionalIngressAnnotations`/`canaryIngressAnnotations`; background `analysis` with `templates`, `startingStep`, `args`; AnalysisTemplate `interval`, `count`, `failureLimit`, `successCondition: result[0] >= ...` and the Prometheus empty-array handling; the provider list; CLI `get rollout`, `promote --full`, `abort`, `retry rollout`, `undo`, `set image ROLLOUT CONTAINER=IMAGE`, `dashboard`.
Replaced: the nginx Prometheus query (its `canary` label is not documented) with the documented Istio query; removed the unconfirmed Degraded status claim, the `inconclusiveLimit` claim and the `or vector(1)` suggestion.

Method: documentation only; no commands were run.
