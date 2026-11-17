---
id: computing-software.systems-network-administration.patch-management.canary-releases-and-feature-flags
name: canary-releases-and-feature-flags
category: computing-software
field: systems-network-administration
product: patch-management
tags: [canary-release, feature-flags, progressive-delivery, release-deployment-mgmt, patch-management]
level: practitioner
status: docs-checked
description: "Release changes progressively with canary deployments and feature flags: weighted steps, flag-gated rollout, kill switches, flag removal and how this applies to patches."
sources:
  - https://martinfowler.com/articles/feature-toggles.html
  - https://argo-rollouts.readthedocs.io/en/stable/features/canary/
  - https://openfeature.dev/docs/reference/intro
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Canary releases and feature flags

Two complementary ways to limit blast radius:
- **Canary release**: release the new version to a small percentage of production traffic,
  then widen.
- **Feature flag**: an if/else controlled at runtime, so behaviour changes without deploying
  new code. Flags can also be used to canary a feature to an initially small subset of users.

## Canary mechanics (Argo Rollouts)
Steps are listed under `strategy.canary.steps`:
```yaml
strategy:
  canary:
    steps:
    - setWeight: 10
    - pause:
        duration: 1h
    - setWeight: 20
    - pause: {}
```
- `pause` accepts a duration with suffix `s`, `m` or `h` (seconds if no suffix). With no
  duration the rollout pauses indefinitely until promoted (`promote` in the argo kubectl
  plugin).
- By default the controller scales the canary to match the current traffic weight (25% of
  four replicas gives one canary pod). With a traffic router, `setCanaryScale` can decouple
  scale from weight; combining it badly with `setWeight` can send most traffic to few pods.
- An `analysis` entry runs background analysis during the rollout and aborts the rollout if
  the analysis is unsuccessful.
- The same idea applies to patches on fleets: patch a small slice first, check, then widen.

## Feature flags
- Fowler's categories: Release Toggles (latent code; usually a week or two), Experiment
  Toggles (hours to weeks), Ops Toggles (let operators disable or degrade a feature quickly)
  and Permissioning Toggles (can last years).
- A few long-lived Ops Toggles act as **kill switches**: operators can gracefully degrade
  non-vital functionality, for example under heavy load. An Ops Toggle must be
  reconfigurable very quickly, not by shipping a new release.
- OpenFeature is a vendor-neutral flag API (evaluation API, evaluation context, providers,
  hooks, events) that plugs into a flag management system.

## Flag hygiene
- Flags carry a cost (extra conditional logic and a testing burden); treat them as inventory
  to keep low, and remove flags that are no longer needed.
- Practices Fowler lists: add a removal task to the backlog when a Release Toggle is
  created, put expiration dates on toggles (some teams fail a test or refuse to start when a
  flag outlives its date), or cap the number of flags.

## Verify
Rollout history shows each step with analysis results; flags past their removal date are
reported.

## Checked
2026-11-08. Confirmed against the Argo Rollouts canary page (`setWeight`, `pause` units and
default, indefinite pause, scale matching, `setCanaryScale` with a traffic router,
`analysis` abort), Martin Fowler's Feature Toggles article (toggle categories, lifetimes,
kill switches, carrying cost, removal practices) and the OpenFeature introduction. Removed
claims not on those pages: specific load balancer and flag products, the 5/25/100 step
example and its durations, the VM 10% rule, safe-default advice, and the sticky-session and
schema-migration gotchas.
Method: documentation only; no commands were run.
