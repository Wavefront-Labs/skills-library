---
id: computing-software.devops-ci-cd.argo-cd.progressive-delivery-with-argo-rollouts
name: progressive-delivery-with-argo-rollouts
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, argo-rollouts, rollout, progressive-delivery, canary, blue-green, analysistemplate, analysisrun, prometheus, traffic-routing, istio, nginx-ingress, aws-alb, gateway-api, setweight, pause, promote, abort, workloadref, kubectl-argo-rollouts, ignoredifferences, gitops, kubernetes, k8s, flagger]
level: advanced
status: gated
description: "Canary and blue-green in GitOps with Argo Rollouts under Argo CD: Rollout CR, traffic routing, AnalysisTemplates on Prometheus, promote/abort, and the Git-vs-abort interaction."
sources: ["https://argo-rollouts.readthedocs.io/en/stable/", "https://argo-rollouts.readthedocs.io/en/stable/features/analysis/", "https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Progressive delivery with Argo Rollouts under Argo CD

**Goal:** a new image committed to Git rolls out as a stepped canary (or blue-green),
gated by metrics, aborts automatically on regression, and Argo CD shows the truth the
whole time.

Strategy-level theory (what to measure, how to pick steps) is in
`computing-software.devops-ci-cd.deployment-strategies.canary-deployment-and-automated-rollback`;
this skill is the Argo Rollouts + Argo CD mechanics.

## 1. Adopt Rollouts without rewriting the Deployment
Install the controller and the `kubectl argo rollouts` plugin. Instead of converting the
Deployment, reference it:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata: { name: payments }
spec:
  workloadRef: { apiVersion: apps/v1, kind: Deployment, name: payments, scaleDown: progressively }
  strategy:
    canary:
      canaryService: payments-canary
      stableService: payments-stable
      trafficRouting:
        nginx: { stableIngress: payments }       # or istio / alb / plugins (Gateway API)
      analysis:
        templates: [{ templateName: error-rate }]
        startingStep: 1                           # background analysis from step 1
        args: [{ name: service, value: payments }]
      steps:
        - setWeight: 5
        - pause: { duration: 10m }
        - setWeight: 25
        - pause: { duration: 10m }
        - setWeight: 50
        - pause: {}                               # indefinite: needs manual promote
```
The `workloadRef` fields, scaleDown behaviour and the nginx `trafficRouting` block above were not checked against the Rollouts docs (gated: unconfirmed, source is paywalled or blocked). **Without `trafficRouting`**, weights are approximated by pod counts (gated: unconfirmed, source is paywalled or blocked); use a mesh/ingress for real percentages.

## 2. AnalysisTemplate
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata: { name: error-rate }
spec:
  args: [{ name: service }]
  metrics:
    - name: error-rate
      interval: 1m
      failureLimit: 2            # tolerate 2 bad samples, abort on the 3rd
      successCondition: len(result) == 0 || result[0] < 0.01
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            sum(rate(http_requests_total{service="{{args.service}}",role="canary",code=~"5.."}[2m]))
            / sum(rate(http_requests_total{service="{{args.service}}",role="canary"}[2m]))
```
- Handle **no data**: an empty result at 5% weight at night is common; decide explicitly
  whether that is pass (`len(result) == 0 ||`) or inconclusive.
- An AnalysisRun completes as Successful, Failed or Inconclusive; the Rollouts analysis docs describe how Inconclusive pauses the rollout.
- Providers beyond Prometheus listed in the docs: Wavefront, Kayenta, Web, Kubernetes Jobs, Datadog, New Relic, Graphite, InfluxDB.

## 3. Operating it
```
kubectl argo rollouts get rollout payments --watch
kubectl argo rollouts promote payments          # skip current pause (gated: unconfirmed, source is paywalled or blocked)
```
The kubectl plugin page documents `kubectl argo rollouts get rollout NAME --watch`; the promote, abort and retry subcommands, `--full`, and Argo CD resource actions for Rollouts were not checked (gated: unconfirmed, source is paywalled or blocked).

## 4. The Argo CD interaction you must understand
- **Abort ≠ rollback in Git.** After an abort the Rollout returns traffic to stable but
  Git still holds the new image; the Rollout sits `Degraded`, the app shows Degraded.
  Finish with `git revert` of the image bump. Running "retry" without fixing Git just
  re-runs the bad canary.
- `selfHeal` doesn't fight Rollouts: weights live on mesh/ingress objects that the
  controller mutates. Add `ignoreDifferences` for those fields (e.g. VirtualService
  `/spec/http/0/route`, or the canary Ingress the controller creates), or Argo CD will
  flip weights back mid-canary.
- An indefinite pause (`pause: {}`) keeps the rollout waiting; do not wire PostSync hooks that expect completion (PostSync runs only once resources are Healthy, per the hooks docs).

## 5. Blue-green variant
`strategy.blueGreen` with `activeService`, `previewService`, `autoPromotionEnabled: false`,
`prePromotionAnalysis` (run against preview before switch), `postPromotionAnalysis`,
and `scaleDownDelaySeconds` (default 30 seconds per the BlueGreen docs) to keep the old ReplicaSet for fast rollback.

## Verify
- [ ] A build returning 500s on one endpoint is aborted by analysis without a human.
- [ ] Traffic split measured at the ingress matches `setWeight` (not pod-count approximation).
- [ ] After abort, team knows to revert in Git; rehearsed once.
- [ ] Argo CD does not report OutOfSync on mesh weights during a canary.
- [ ] Empty-metric behaviour at low traffic is a deliberate choice, documented in the template.

## Checked

2026-11-02. Confirmed against the Argo Rollouts analysis, BlueGreen and kubectl plugin pages: startingStep, failureLimit semantics, AnalysisRun outcomes, supported metric providers, kubectl argo rollouts get rollout --watch, scaleDownDelaySeconds default 30 seconds, post-promotion analysis failure aborts the rollout. Removed: CloudWatch as a provider (not listed), inconclusiveLimit claim, the Argo CD health-check Paused/Suspended claim. Gated: workloadRef scaleDown, nginx trafficRouting block, pod-count weight approximation, promote/abort/retry/--full subcommands and Argo CD resource actions.

Method: documentation only; no commands were run.
