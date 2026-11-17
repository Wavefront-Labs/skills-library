---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.feature-flag-rollouts-decoupling-deploy-from-release
name: feature-flag-rollouts-decoupling-deploy-from-release
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, release-canarying, feature-flag-rollout, progressive-delivery, kill-switch, openfeature]
level: practitioner
status: docs-checked
description: "Use feature flags to separate deploy from release: toggle types, gradual rollouts, kill switches, flag inventory and cleanup, and the OpenFeature API."
sources: ["https://sre.google/workbook/canarying-releases/", "https://martinfowler.com/articles/feature-toggles.html", "https://openfeature.dev/docs/reference/intro"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Feature flag rollouts

**Goal:** ship code dark, turn features on gradually, and turn them off quickly without a deploy.

## Toggle types (Martin Fowler, Feature Toggles)
| Type | Lifetime and dynamism | Use |
|---|---|---|
| Release toggle | Transitionary: generally no more than a week or two, though product-centric ones may stay longer; decision is static per release | Ship incomplete or untested code paths as latent code that may never be turned on |
| Experiment toggle | Hours to weeks, long enough for statistically significant results; highly dynamic, per request | A/B or multivariate testing with users placed in cohorts |
| Ops toggle | Mostly short-lived; a few long-lived "kill switches" | Let operators disable or degrade a feature quickly, for example under heavy load; can be seen as a manually managed circuit breaker; must be reconfigurable extremely quickly |
| Permissioning toggle | Can be very long-lived; decision always per request | Gate features by user characteristics |

## Rollout idea
1. Deploy code with the flag off (deployment no longer means release).
2. Enable for a small group, then widen. OpenFeature lists canary-style rollout of a new feature to an initially
   small subset of users as a core use, which needs context-aware flagging decisions (which user is making the
   request) and configuration that changes without redeploying or restarting.
3. Watch your health metrics during each step; roll back by changing the flag, then fix forward.
4. The SRE Workbook (Canarying Releases) notes that service components change at different rates (binaries,
   runtimes, libraries, service config or flags, feature or experiment config, user config) and that the
   principles of feature flags and experiments apply to any type of change, not just software releases.
5. Remove the flag after full rollout.

## OpenFeature
OpenFeature is an open specification giving a vendor-agnostic flag-evaluation API; an SDK plugs into third-party
flag providers, whether open source or commercial, self-hosted or cloud. Parts: the evaluation API, evaluation
context (data such as the user or client IP used for dynamic evaluation), providers (the translation layer to a
flag management system), hooks (validation, logging, telemetry at points in the evaluation life cycle) and events
(provider readiness, errors, flag configuration changes).

## Managing flags as inventory
Fowler: treat flags as inventory with a carrying cost and keep it low. Common practices: add a removal task to the
backlog when a release toggle is introduced; set expiration dates; "time bombs" that fail a test, or refuse to
start the application, once a flag is past its expiration date; or cap the number of flags a system may have.

## Verify
- [ ] Every flag has an owner, type and expiry; the kill switch is tested in a non-production environment.
- [ ] Flag changes are logged so they can be correlated with incidents.

## Checked

Checked 2026-11-09. Confirmed against Martin Fowler's Feature Toggles article (toggle categories, lifetimes, kill switches, inventory practices), the OpenFeature introduction page (use cases and components) and the SRE Workbook Canarying Releases page (components changing at different rates, flags and experiments for any change). Removed: the 1/5/25/50/100 percent ladder, OpenTelemetry attribute names, the named flag vendors, the TypeScript SDK snippet, the "evaluate server-side" and "fail closed" advice, and the Grafana annotation claim, none of which appeared on a page read. The SRE Book release-engineering source was dropped from the source list as it supported none of the remaining claims.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
