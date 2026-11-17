---
id: computing-software.devops-ci-cd.release-engineering.feature-flags-and-safe-rollback
name: feature-flags-and-safe-rollback
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, feature-flags, feature-toggles, kill-switch, ops-flags, release-toggles, experiment-flags, percentage-rollout, targeting, sticky-bucketing, openfeature, launchdarkly, unleash, flagsmith, growthbook, flipt, flag-defaults, flag-debt, flag-cleanup, piranha, dark-launch, decouple-deploy-from-release, rollback, roll-forward, audit-log]
level: practitioner
status: draft
description: "Use feature flags as a rollback mechanism: flag types, safe defaults when the flag service fails, sticky percentage rollouts, what a flag cannot undo, change control and flag-debt cleanup."
sources: ["https://martinfowler.com/articles/feature-toggles.html", "https://openfeature.dev/docs/reference/intro", "https://docs.getunleash.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Feature flags and safe rollback

**Goal:** turning a feature off is faster and narrower than redeploying, works even when
the flag service is down, and doesn't leave the codebase full of dead branches.

## 1. Know which kind of flag you are adding
| Type | Lifetime | Who flips it | Example |
|---|---|---|---|
| Release toggle | days–weeks | engineers | new checkout flow, rolled 1% → 100% |
| Ops toggle / kill switch | permanent | on-call | disable recommendations under load |
| Experiment | weeks | product/data | A/B test variant |
| Permission | permanent | product/sales | beta access, plan entitlements |
Mixing these in one undifferentiated list is how kill switches get "cleaned up" and
release toggles live for years. Encode the type in naming or metadata (`release.checkout-v2`,
`ops.disable-recs`) and give release toggles an **expiry date** at creation.

## 2. Evaluation design
- Prefer **server-side evaluation with a local cache**: SDKs (LaunchDarkly, Unleash,
  Flagsmith, GrowthBook, Flipt) stream rules and evaluate in-process — no network call per
  check. Use **OpenFeature** as the API in code so the vendor is swappable.
- **Code default = the safe value.** If the SDK can't initialise or loses the stream,
  `getBooleanValue("release.checkout-v2", false)` falls back to the default — make that the
  old, known-good behaviour. For a kill switch, the default is "feature on" (normal
  operation) only if killing it when the flag store is down would be worse; decide per flag.
- Evaluate **once per request** and pass the result down; evaluating repeatedly can give a
  user both code paths mid-request if rules change.
- Client-side flags (browser/mobile) are visible to users — never gate security on them,
  and don't leak unreleased feature names in flag keys.

## 3. Percentage rollouts that behave
- Bucketing must be **sticky**: hash of (flag key + stable user/account id), not random
  per request, or users flicker between versions.
- Choose the unit deliberately: per-user for UI, per-account/tenant for B2B (one company
  shouldn't see two behaviours), per-request only for stateless backend paths.
- Ramp with checks between steps (1% → 5% → 25% → 50% → 100%) watching the same error/
  latency metrics you'd use for a canary, sliced by flag variation.

## 4. What a flag can and cannot roll back
A flag rollback is instant only if the "off" path still works with today's data.
It **cannot** undo:
- Data written in a new format the old path can't read → write in a backward-compatible
  format until the flag is at 100% and removed (expand/contract, see
  `computing-software.devops-ci-cd.deployment-strategies.canary-blue-green-and-rollback`).
- Schema migrations — they ride deploys, not flags.
- External side effects already happened: emails sent, payments captured, webhooks fired.
- Caches populated by the new path with incompatible entries → version cache keys by flag variation.
So: **test both paths in CI** (parametrise tests over flag values), and before ramping
write down "if we flip this off at 50%, what breaks?".
Roll back with the flag when the problem is inside the flagged path; redeploy/revert when
the problem is outside it (a bad dependency, a startup crash) — the flag won't help.

## 5. Flag changes are production changes
- Require approvals for production flag changes on critical flags; keep the audit log
  (who, when, old → new) and stream it into the same timeline as deploys, so incident
  responders see "flag flipped 14:02" next to the error spike.
- Manage long-lived flag config as code where the vendor allows (Terraform providers,
  GitOps for Unleash/Flipt) — *support varies by vendor*.

## 6. Flag debt
- Release toggle at 100% for > 2 weeks → ticket to delete the flag **and** the old code
  path. Track count of stale flags as a team metric.
- Automated help: vendor "stale flag" reports, code-reference scanners (e.g.
  `ld-find-code-refs`), Uber's Piranha for automated removal in some languages.
- Never reuse a flag key for a different feature; old SDK caches and analytics will
  confuse the two.

## Verify
- [ ] With the flag SDK blocked from the network, the app starts and serves the safe default.
- [ ] CI runs the affected tests with the flag both on and off.
- [ ] The same user gets the same variation across 100 requests at a 50% rollout.
- [ ] A rollback drill: flipping the flag off at 50% restores baseline error rate within minutes.
- [ ] Every release toggle has an owner and expiry; none older than the agreed limit.
