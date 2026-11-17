---
id: computing-software.devops-ci-cd.release-engineering.release-train-vs-trunk-based-release
name: release-train-vs-trunk-based-release
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, release-train, release-cadence, trunk-based-development, continuous-deployment, continuous-delivery, release-branches, branch-cut, code-freeze, stabilisation, cherry-pick, backport, hotfix, release-captain, release-manager, gitflow, mobile-releases, app-store, phased-rollout, lts, supported-versions, dora-metrics, lead-time, branching-strategy]
level: practitioner
status: draft
description: "Choose and run a release model: continuous deploy from trunk vs scheduled release trains with branch cuts, plus cherry-pick/backport policy, release captains and the anti-patterns of each."
sources: ["https://trunkbaseddevelopment.com/", "https://martinfowler.com/articles/branching-patterns.html", "https://dora.dev/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Release trains vs trunk-based release

**Goal:** pick the release model your *delivery constraints* demand (not the one in
fashion), and run it so releases are boring and on time.

Both models assume trunk-based *development* — short-lived branches merged to `main`
daily. They differ in how code gets from `main` to users.

## 1. Choose by constraint
| Constraint | Points toward |
|---|---|
| You own the servers; deploy is cheap and reversible | **Continuous deploy from trunk** |
| Mobile apps (store review, users update slowly), desktop, firmware | **Release train** |
| Customers run your software on-prem and need supported versions | **Train + maintained release branches** |
| Regulated sign-off per release (medical, finance) | **Train**, with sign-off as a train stage |
| Many teams, one binary, coordination costs | **Train** (fixed cadence replaces coordination) |
| Small team, one service, good tests and flags | **Trunk**; a train adds only delay |
Hybrids are normal: backend deploys continuously, the mobile client rides a 1-2-week train.
Avoid GitFlow-style long-lived `develop` branches for anything you deploy yourself; it
adds a merge step and a second source of truth without reducing risk.

## 2. Running continuous deploy from trunk
- Every merge to `main` builds once and deploys automatically through staging → prod
  with automated gates (see
  `computing-software.devops-ci-cd.deployment-strategies.canary-deployment-and-automated-rollback`).
- Unfinished work ships dark behind flags
  (`computing-software.devops-ci-cd.release-engineering.feature-flags-and-safe-rollback`).
- Batch size is the safety mechanism: many small deploys per day. If deploys get
  queued up into "one big deploy on Thursday", you have drifted into an informal train
  without its safeguards.
- Rollback = redeploy previous artifact or `git revert`; no release branches exist.

## 3. Running a release train
**Calendar** (example two-week train, adjust):
- Day 0: **branch cut** — automation creates `release/2026.42` (or `release/4.12`) from
  `main` at a fixed time. No negotiation; late features catch the next train.
- Days 0-5: **stabilisation** on the branch — QA, beta channel / internal dogfood,
  only bug fixes enter.
- Day 5: ship (mobile: submit for review, then **phased rollout** e.g. 1% → 10% → 50% → 100%
  with crash-rate gates; pause the rollout rather than pulling the release).
- Overlap: train N+1 is cut while N is rolling out — so at most two release branches
  are live.
**Roles:** a rotating **release captain** owns the branch: approves cherry-picks,
watches crash/error dashboards, makes the ship/hold call. Write the runbook; the captain
changes every train.
**Branch cut, not code freeze:** freezing `main` blocks everyone for the stabilisation
period; cutting a branch lets `main` keep moving.

## 4. Cherry-pick and backport policy
- **Fix on `main` first**, then `git cherry-pick -x` to the release branch. A fix that
  exists only on the branch reappears as a regression next train.
- Automate: a `backport release/4.12` label triggers a bot (e.g. the `backport` GitHub
  Action, or GitLab's cherry-pick button) to open the pick PR; conflicts go back to the author.
- **Entry bar for picks** (written down): crash/data-loss/security fixes, regressions
  from this train. Not "small features". Every exception trains people to sneak in.
- Never merge a release branch back into `main` — it drags release-only commits (version
  bumps, reverts) into trunk. Everything already came from `main`.

## 5. Supported versions
If you maintain old releases, publish the support window (e.g. last two minors, LTS for
12 months). Each supported branch needs CI running on it; un-tested backports are how
"patch" releases break things.

## 6. Anti-patterns
- Holding the train for one feature → the next train is bigger and riskier. Ship without it.
- Release branch living for months collecting fixes → it's a fork; nobody can reason about it.
- Trunk-based but main is red for hours → you can't release from it; revert first.
- Train without an owner → nobody says "no" to cherry-picks.

## Verify
- [ ] The chosen model is justified against the constraint table, in writing.
- [ ] Trunk model: median merge-to-production time is hours, not days (DORA lead time).
- [ ] Train model: last 5 branch cuts happened on schedule, untouched by feature requests.
- [ ] Every commit on a release branch has a `(cherry picked from commit ...)` trailer pointing at `main`.
- [ ] A release-captain runbook exists and was used by at least two different people.
