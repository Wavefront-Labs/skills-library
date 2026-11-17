---
id: computing-software.devops-ci-cd.deployment-strategies.rings-via-feature-flags-vs-infrastructure
name: rings-via-feature-flags-vs-infrastructure
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, flag-rings, ring-deployment, feature-flags, targeting-rules, progressive-delivery, deployment-rings]
level: practitioner
status: draft
description: "Choose between ring deployments done with feature flag targeting and rings built from separate infrastructure: trade-offs, ring definitions, flag rules and combining both."
sources:
  - https://learn.microsoft.com/en-us/azure/devops/migrate/phase-rollout-with-rings
  - https://docs.getunleash.io/reference/activation-strategies
  - https://openfeature.dev/docs/reference/intro
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Rings via feature flags vs infrastructure

Rings expose a change to progressively larger audiences: ring 0 (team), ring 1 (internal/dogfood), ring 2 (early adopters/small region), ring 3 (everyone).

## Two ways to build rings
| | Infrastructure rings | Flag rings |
|---|---|---|
| Mechanism | separate deployments/clusters/regions/scale units; users routed to a ring | one deployment; flag targeting decides who sees the new code path |
| Ships | the whole build (binaries, config, dependencies) | only flagged features; everything else ships to all at once |
| Catches | crashes, perf regressions, dependency/runtime/config issues, infra changes | functional and UX issues in the flagged feature |
| Rollback | redeploy/reroute the ring | flip the flag (seconds) |
| Cost | extra environments, routing, per-ring pipelines | flag service, code paths, flag debt |
Infrastructure rings protect against *the build*; flag rings protect against *the feature*. Mature setups use both: infra rings for every release, flags for risky features within it.

## Flag rings
Define rings as segments, not hard-coded user lists:
```yaml
segments:
  ring0: { rule: "email endsWith '@example.com' and team in ['payments']" }
  ring1: { rule: "email endsWith '@example.com'" }
  ring2: { rule: "account.plan == 'beta' or percentage(user.id) < 5" }
flag: new-checkout
  rules:
    - { segment: ring0, serve: on }    # day 0
    - { segment: ring1, serve: on }    # day 2
    - { segment: ring2, serve: on }    # day 5
  default: off
```
- Percentage rollouts hash a stable key (user or account ID) so users don't flip between variants.
- Target accounts/tenants, not users, for B2B (whole company sees the same UI).
- Track metrics by flag variant (flag evaluation events to analytics/APM).
- Every flag gets an owner and removal date; stale flags are tech debt and test-matrix explosion.

## Infrastructure rings
- Map rings to scale units: canary cluster, one small region, half the regions, all regions (Azure's safe deployment practice).
- Pipeline stages per ring with bake time and health gates; promotion requires the previous ring healthy.
- Route internal users to ring 1 via DNS, tenant mapping, or header-based routing.

## Pitfalls
- Using flags for changes they can't cover (DB migrations, library upgrades, runtime changes) gives a false sense of safety.
- Flag service outage: SDKs must fall back to safe defaults and cache last values.
- Too many concurrent flagged features in the same ring confound metrics.

## Verify
- [ ] Each release passes infrastructure rings; risky features additionally gated by flag segments with owners and expiry.
- [ ] Turning a flag off removes the feature for its ring within seconds.
