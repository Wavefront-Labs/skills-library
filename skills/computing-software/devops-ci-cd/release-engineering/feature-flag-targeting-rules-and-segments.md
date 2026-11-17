---
id: computing-software.devops-ci-cd.release-engineering.feature-flag-targeting-rules-and-segments
name: feature-flag-targeting-rules-and-segments
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, targeting-rules, user-segments, feature-flags]
level: practitioner
status: docs-checked
description: "Design feature flag targeting: evaluation context attributes, segments, rule ordering, percentage rollouts within segments and keeping PII out of flag providers."
sources: ["https://openfeature.dev/docs/reference/concepts/evaluation-context", "https://docs.getunleash.io/reference/activation-strategies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Feature flag targeting rules and segments

## Evaluation context
Every evaluation passes a context: a stable **targeting key** plus attributes.
```ts
const client = OpenFeature.getClient();
const enabled = await client.getBooleanValue('new-checkout', false, {
  targetingKey: user.id,                 // stable, not email
  plan: user.plan, country: user.country, org: user.orgId, appVersion: '5.2.0',
});
```

## Rules, evaluated top to bottom
1. Individual overrides (QA accounts, a customer under incident).
2. Segment rules: `internal-staff`, `beta-orgs`, `eu-customers`.
3. Attribute rules: `appVersion >= 5.2.0`, `plan in [enterprise]`.
4. Default rule with percentage rollout: 10% on, bucketed by `targetingKey` (or `org` to keep whole
   organisations consistent).
Rule combination semantics differ by provider (in Unleash a strategy applies when its constraints and segments match); read your provider's documentation before relying on order.

## Segments
Reusable named audiences maintained once (staff list, beta programme). Keep membership in the flag
system or sync from your CRM; very large lists should be attribute-based instead.

## Privacy
- Send only attributes needed for targeting; hash or omit emails and names.
- Prefer server-side evaluation for sensitive attributes.

## Gotchas
- Bucketing by a different key per call (session id vs user id) flips users between variants.
- Mobile: old app versions cannot handle new variants; target by `appVersion`.

## Verify
- [ ] Flag debugger/evaluation log shows the expected rule matched for a staff user, a beta org and a regular user.

## Checked

2026-10-28. Confirmed: OpenFeature evaluation context with targetingKey; Unleash activation strategies (rollout percentage by normalised MurmurHash of the user ID with stickiness, constraints, reusable segments). Removed: first-match-wins ordering (provider-specific, not in the sources), the semver comparison claim, the list-size figure and the client-side exposure claim.

Method: documentation only; no commands were run.
