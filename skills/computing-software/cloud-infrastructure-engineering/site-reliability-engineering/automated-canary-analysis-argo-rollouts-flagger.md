---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.automated-canary-analysis-argo-rollouts-flagger
name: automated-canary-analysis-argo-rollouts-flagger
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, release-canarying, argo-rollouts-analysis, flagger-canary, progressive-delivery, kubernetes]
level: advanced
status: docs-checked
description: "Automate canary analysis on Kubernetes with Argo Rollouts AnalysisTemplates or Flagger metric checks against Prometheus, with automatic promotion and rollback."
sources: ["https://argo-rollouts.readthedocs.io/en/stable/features/analysis/", "https://argo-rollouts.readthedocs.io/en/stable/features/canary/", "https://docs.flagger.app/usage/how-it-works", "https://docs.flagger.app/usage/metrics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automated canary analysis: Argo Rollouts and Flagger

**Goal:** canaries judged by metrics and rolled back by machines, not by someone watching a dashboard.

## Argo Rollouts
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata: { name: checkout }
spec:
  strategy:
    canary:
      canaryService: checkout-canary
      stableService: checkout-stable
      trafficRouting: { nginx: { stableIngress: checkout } }     # one traffic router; see Argo canary docs for others
      analysis:
        templates: [ { templateName: success-rate } ]
        startingStep: 1
        args: [ { name: service, value: checkout-canary } ]
      steps:
      - setWeight: 5
      - pause: { duration: 10m }
      - setWeight: 25
      - pause: { duration: 10m }
      - setWeight: 50
      - pause: { duration: 10m }
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata: { name: success-rate }
spec:
  args: [ { name: service } ]
  metrics:
  - name: success-rate
    interval: 2m
    count: 5
    failureLimit: 1
    successCondition: result[0] >= 0.99
    provider:
      prometheus:
        address: http://prometheus.monitoring:9090
        query: |
          sum(rate(http_requests_total{service="{{args.service}}",code!~"5.."}[2m]))
          / sum(rate(http_requests_total{service="{{args.service}}"}[2m]))
```
Background analysis runs during steps; a failed measurement beyond `failureLimit` aborts and shifts traffic back to stable.

## Flagger
```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata: { name: checkout }
spec:
  targetRef: { apiVersion: apps/v1, kind: Deployment, name: checkout }
  service: { port: 8080 }
  analysis:
    interval: 1m
    threshold: 5            # failed checks before rollback
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate     # built-in metric; see Flagger metrics docs
      thresholdRange: { min: 99 }
      interval: 1m
    - name: request-duration
      thresholdRange: { max: 500 }
      interval: 1m
    webhooks:
    - name: load-test
      url: http://<LOADTESTER_HOST>/
      metadata: { cmd: "<load generator command against the canary service>" }
```
Custom metrics via `MetricTemplate` CRs (the metrics page documents providers such as Prometheus and Datadog).

## Design notes
- Compare canary vs stable (ratio or difference), not canary vs a fixed number, when baseline varies by time of day.
- Low traffic: add a load-test webhook or longer intervals so there is enough signal.
- Analysis must include the SLIs users feel (errors, latency) plus saturation.

## Verify
- [ ] Deploy a deliberately failing build in staging: rollout aborts automatically and traffic returns to stable.

## Checked
2026-11-01. Field names checked by phrase search against the Argo Rollouts analysis and canary pages and the Flagger how-it-works and metrics pages (`canaryService`, `stableService`, `trafficRouting`, `analysis`, `startingStep`, `failureLimit`, `successCondition`, `interval`, `count`, `thresholdRange`, `stepWeight`, `maxWeight`, `threshold`, `MetricTemplate`, Datadog provider). Removed: the kubectl plugin command, the load-test command, the built-in-for-mesh claim and the CloudWatch and New Relic provider claims. Example URLs and the PromQL are illustrative.
Method: documentation only; no commands were run.
