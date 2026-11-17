---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.launch-rollout-plan-and-phasing
name: launch-rollout-plan-and-phasing
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [launch, rollout, staged-rollout, feature-flags, canary]
level: practitioner
status: docs-checked
description: "Plan a staged launch with the Google SRE Book techniques: gradual rollouts and canaries, feature flag frameworks, abusive-client safeguards, load tests, contingency planning."
sources: ["https://sre.google/sre-book/reliable-product-launches/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Launch rollout plan and phasing

Techniques from the SRE Book chapter "Reliable Product Launches at Scale".

## Gradual and staged rollouts
- Very few Google launches are push-button; almost all updates proceed gradually with verification steps. Example from the book: install a new server on a few machines in one datacenter and observe for a defined period; if fine, all machines in that datacenter; then globally. The first stages are "canaries".
- Tools that install software observe the new server for a while and automatically roll back if it does not pass the validation period.
- Mobile apps can roll out gradually, raising the percentage of upgraded installs over time until 100%; useful when the new version adds backend traffic.
- Invite systems and rate-limited signups are another form of gradual rollout.

## Feature flag frameworks
The book lists typical requirements: roll out many changes in parallel, each to a few servers, users, entities or datacenters; gradually increase to a larger but limited group, "usually between 1 and 10 percent"; route traffic by user, session, object or location; handle failure of new code paths without affecting users; revert each change independently and immediately; measure the effect on user experience. Stateless UI changes can use an HTTP payload rewriter keyed on a cookie hash; stateful services tend to key on logged-in user ID or entity ID and proxy or reroute requests.

## Client safeguards
- Exponential backoff and jitter on retries; do not retry on 4xx errors that indicate a client fault.
- Randomise the time of periodic client actions (the book's example: a 2 a.m. update download creates a nightly thundering herd).
- Server-controlled client configuration lets you switch a feature off without shipping a new app version; dormant code shipped in advance makes abort easier.

## Overload and load tests
Services rarely scale linearly into overload; the book recommends load tests, says they are required for most launches, and notes launch traffic mix can differ from steady state.

## Rollout planning items from the checklist
- A launch plan naming actions and the person responsible for each; identify risk in individual steps and add contingency measures.
- Configuration changes can take hours; a working test configuration does not guarantee the same on live; some launches need ordered steps.
- External requirements (a keynote date) need contingency, for example a backup slide.
- The 2005 checklist's schedule section asks about hard deadlines, external events and "Mondays or Fridays".

## Phase table (your own design)
Define per phase: exposure, duration, numeric success criteria and a rollback trigger agreed in advance. The book does not prescribe phase names, durations or thresholds.

## Verify
- [ ] Every phase has success criteria and a rollback trigger.
- [ ] Rollback or flag-off has been exercised before real user exposure.

## Checked
Confirmed against the SRE Book "Reliable Product Launches at Scale" (Gradual and Staged Rollouts, Feature Flag Frameworks, Dealing with Abusive Client Behavior, Overload Behavior and Load Tests, Rollout Planning) and the "Launch Coordination Checklist" appendix. Removed: the dark-launch definition and Envoy/Istio mirroring YAML (not in the book), the sample phase table with durations and thresholds, and the launch-time and regional-ordering advice.
Method: docs-only read of cited pages, 2026-11-08
