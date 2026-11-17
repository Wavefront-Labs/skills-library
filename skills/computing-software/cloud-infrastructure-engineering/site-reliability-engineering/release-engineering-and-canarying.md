---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.release-engineering-and-canarying
name: release-engineering-and-canarying
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, release-engineering, canarying, canary-release, canary-analysis, progressive-delivery, progressive-rollout, hermetic-builds, reproducible-builds, release-process, release-cadence, rollback, feature-flags, blue-green, argo-rollouts, flagger, kayenta, automated-canary-analysis, deploy-annotations, change-failure-rate, release-branching, artifact-promotion, deployment-safety]
level: advanced
status: draft
description: "Ship changes safely: hermetic reproducible builds and artifact promotion, a canary process with population, duration and metric selection."
sources: ["https://sre.google/sre-book/release-engineering/", "https://sre.google/workbook/canarying-releases/", "https://argoproj.github.io/argo-rollouts/features/analysis/", "https://docs.flagger.app/", "https://sre.google/workbook/configuration-specifics/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Release engineering and canarying

**Goal:** every change reaches a small, representative slice of production first, is judged
by metrics against a control, and is rolled back automatically if it is worse — so a bad
release costs minutes of a sliver of users, not an incident.

## 1. Release engineering principles (SRE Book)
- **Self-service**: teams release without SRE hands; the pipeline is the product.
- **High velocity, small deltas**: frequent small releases are safer than big-bang ones;
  release cadence by time (daily/weekly) not by "when it's ready".
- **Hermetic builds**: same source + same toolchain ⇒ same artifact, independent of the
  build host: pinned compilers/base images, vendored or lock-filed dependencies, no network
  at build (or a proxy with pinned hashes), build in containers. Verify with two builds and
  a checksum compare; SLSA provenance/`cosign` attestations make it auditable.
- **Policy as code**: who can promote what where lives in the pipeline (branch protection,
  signed artifacts, environment gates), not in a wiki.
- **Build once, promote the same artifact** through dev → staging → canary → prod; never
  rebuild per environment. Configuration (not code) changes per environment, and config is
  released with the same canary discipline (`...site-reliability-engineering.configuration-design-and-safety`).

## 2. Canary design (SRE Workbook)
A canary is an experiment: a **treatment** (new version) vs a **control** (old version)
under live traffic, judged on metrics, with a predetermined decision rule.
- **Population**: small enough that failure fits the error budget, large enough to see
  signal. Rule: a canary that is 100% broken for the canary duration must spend < ~25% of
  the window's remaining error budget. e.g. SLO 99.9%/30d (43 min full outage), 5% canary
  for 30 min ⇒ 1.5 min-equivalent ⇒ fine. For rare paths, pick the population by traffic
  share of that path, not by instance count.
- **Representative**: same hardware class, same region/traffic mix, same time of day as
  the control; otherwise you compare apples with oranges. Use a dedicated control cohort
  of the *old* version with the same size, not "the rest of the fleet".
- **Duration**: long enough to cover the signal's latency (caches warming, hourly jobs,
  GC cycles, memory leaks); typically 30–60 min per step, longer for low traffic. Stage
  durations grow as exposure grows.
- **Metrics**: a few SLI-aligned ones — error ratio, latency p50/p99, saturation (CPU,
  memory, GC), crash/restart count, and 1–2 business signals (checkout rate). Avoid
  dozens: multiple comparisons generate false alarms. Compare **ratios/rates**, not counts.
- **Decision rule, in advance**: e.g. "fail if error ratio of treatment − control > 0.5
  percentage points for 5 consecutive minutes, or p99 latency > control × 1.2". Mann-Whitney
  / confidence intervals for automated analysis (Kayenta); for simple pipelines a threshold
  on the difference with a minimum sample size.
- **Stages**: 1 pod → 5% → 25% → 50% → 100%, each with its own analysis and bake time;
  region-by-region for multi-region; last stage is a decision, not a formality.

## 3. Implementation on Kubernetes
```yaml
# Argo Rollouts canary with analysis against Prometheus
apiVersion: argoproj.io/v1alpha1
kind: Rollout
spec:
  strategy:
    canary:
      canaryService: api-canary
      stableService: api-stable
      trafficRouting: { istio: { virtualService: { name: api } } }   # or nginx/alb/smi; without routing it is pod-count based
      steps:
        - setWeight: 5
        - pause: { duration: 15m }
        - analysis: { templates: [{ templateName: error-ratio }, { templateName: latency }], args: [{ name: canary, value: api-canary }, { name: stable, value: api-stable }] }
        - setWeight: 25
        - pause: { duration: 30m }
        - analysis: { templates: [{ templateName: error-ratio }] }
        - setWeight: 50
        - pause: { duration: 30m }
      abortScaleDownDelaySeconds: 30
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata: { name: error-ratio }
spec:
  args: [{ name: canary }, { name: stable }]
  metrics:
    - name: error-ratio-delta
      interval: 1m
      count: 5
      failureLimit: 1
      provider:
        prometheus:
          address: http://mimir-query-frontend/prometheus
          query: |
            ( sum(rate(http_requests_total{service="{{args.canary}}",code=~"5.."}[5m])) / sum(rate(http_requests_total{service="{{args.canary}}"}[5m])) )
            - ( sum(rate(http_requests_total{service="{{args.stable}}",code=~"5.."}[5m])) / sum(rate(http_requests_total{service="{{args.stable}}"}[5m])) )
      successCondition: result[0] < 0.005
```
Flagger does the same declaratively (`Canary` CR with `analysis.metrics` and `webhooks`
for load tests). Kayenta/Spinnaker provides statistical ACA for VM fleets. Feature flags
(LaunchDarkly/OpenFeature) canary *behaviour* independent of binary rollout: use for
risky logic, keep the flag lifetime short.

## 4. Rollback is the primary mitigation
- Rollback must be one command/button, tested weekly by the pipeline itself, and faster
  than diagnosis (minutes). Keep the previous artifact warm (blue/green) for the highest tiers.
- Not everything rolls back: schema migrations (expand/contract pattern; never destructive
  in the same release), data format changes, external side effects. Mark releases
  "irreversible" and gate them with longer canaries.
- Automatic rollback on analysis failure; human approval only to **proceed**, never to stop.

## 5. Observability for releases
- Emit a `version` label (`build_info{version}`) and deploy annotations into Grafana
  (`...prometheus-grafana.grafana-dashboard-design`); every incident review starts with "what changed".
- Track DORA: deployment frequency, lead time, **change failure rate**, time to restore.
  Change failure rate > 15% ⇒ invest in canary quality, not more approvals.
- Keep a changelog of config and flag changes in the same timeline as deploys.

## Gotchas
- Canary on one pod with pod-count routing: 1 of 20 pods = 5%, but sticky sessions/LB
  warmup may send it 0% or 30%; verify actual share from metrics before judging.
- Comparing canary against the whole fleet that includes the canary dilutes the signal.
- Latency improvement in canary because it has fewer connections (cold cache in your
  favour) — compare like with like, or warm up before the analysis window.
- Rolling back the binary but not the config/flag/schema reintroduces the fault differently.
- Weekend/holiday canaries see different traffic; schedule canaries during representative hours.

## Verify
- [ ] Two independent builds of the same commit produce byte-identical artifacts (or identical content hashes after normalisation).
- [ ] A deliberately broken canary (returns 500 on 5% of requests) is aborted automatically within one analysis interval and traffic returns to stable with no manual step.
- [ ] Canary population × duration fits the error-budget rule above, written next to the Rollout.
- [ ] Deploy annotations appear on the SLO dashboard with the version label.
