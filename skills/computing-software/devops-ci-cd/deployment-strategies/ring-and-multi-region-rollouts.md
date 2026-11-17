---
id: computing-software.devops-ci-cd.deployment-strategies.ring-and-multi-region-rollouts
name: ring-and-multi-region-rollouts
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, ring-deployment, ring-based-deployment, rings, wave-deployment, staged-rollout, multi-region-rollout, bake-time, bake-period, soak-time, blast-radius, safe-deployment-practices, azure-sdp, one-box, pilot-region, canary-region, cell-based-architecture, cells, availability-zones, regional-isolation, global-rollout, rollout-orchestration, automatic-halt, health-gates, change-velocity, concurrency-of-regions, rollback-across-regions, time-zone-aware-rollouts]
level: advanced
status: draft
description: "Roll a change across regions, clusters or cells safely: ring/wave design (dev, pilot, one region, paired regions, all), bake times and health gates per ring, automatic halt, orchestration, rollback."
sources: ["https://learn.microsoft.com/en-us/devops/operate/safe-deployment-practices", "https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/", "https://sre.google/workbook/canarying-releases/", "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_tracking_changes_automated_changemgmt.html", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Progressive-Syncs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ring and multi-region rollouts

**Goal:** a bad change is caught while it affects one small ring, never reaches a second
region before the first has soaked, and halting or rolling back is one action — not a
Slack scramble across time zones.

## 1. Design the rings
Order by blast radius and signal quality, not by convenience:
```
ring 0  dev/integration            — automated tests only
ring 1  internal / dogfood tenant  — employees, synthetic users; hours of bake
ring 2  one-box / 1 cell in pilot region — real traffic, tiny share
ring 3  pilot region (smallest prod region, or lowest-revenue)
ring 4  one region per geography (one AMER, one EMEA, one APAC) in sequence
ring 5  remaining regions in waves of N, never two paired/DR regions in the same wave
```
Rules: a ring holds ≤ ~10–25 % of traffic until the last wave; **paired regions**
(active/standby, DR pairs, AZ pairs within a region for AZ-level deploys) are never in
the same wave; follow the sun so each ring deploys in that region's low-traffic window
and the team that can respond is awake; cell-based architectures ring by **cell**
(1 cell → 10 % of cells → 50 % → all), which gives better isolation than by region.

## 2. Bake time and health gates
Each ring has an explicit **bake** (soak) before the next starts — long enough for the
failure modes you care about to show: request-level bugs (minutes), memory leaks and
slow degradation (hours), daily batch jobs (24 h), weekly reports (7 days for the final
ring if those exist). Typical: ring 1 = 1–4 h, ring 2–3 = 2–24 h, waves = 1 h each with
the last at 24 h. Gates evaluated continuously during bake, not just at the end:
- SLO burn rate (fast 1 h/5 min windows) for the ring's traffic ≤ baseline.
- Error rate, p95/p99 latency, saturation vs the *same ring before the change* and vs
  the *other rings now* (A/A comparison beats absolute thresholds).
- Business KPIs (orders/min, login success) within a band of the previous week.
- Crash/restart counts, log error-rate, dependency error rates.
- No new alerts attributed to the service; no incident open.
Gates are per ring and per service; define them in code (the rollout tool's config),
not in a wiki.

## 3. Automatic halt (and when to roll back)
Any gate failure **halts** the rollout (no new rings) immediately and pages the owning
team; rollback of the affected ring is automatic when the failure is unambiguous
(error-rate/SLO breach) and manual-with-default-rollback when it's business-KPI only.
Halting is cheap and reversible; design for *halt first, decide in minutes*. A halted
rollout older than N hours auto-rolls-back the deployed rings (a half-rolled fleet is a
mixed-version fleet — see §6).
Manual overrides (skip bake, force next ring) require a second person and a reason, and
leave an audit record; "we're confident" is how global outages start.

## 4. Orchestration tooling
- **Argo CD ApplicationSet Progressive Syncs** (`RollingSync` steps by label, `maxUpdate`)
  — ring = step; gates = Application health only (add an external controller or
  Argo Rollouts analysis per app for metric gates).
- **Argo Rollouts / Flagger** per cluster for the inside-ring canary; an outer orchestrator
  (pipeline with environments per ring + wait timers, Spinnaker pipelines with
  wait/judgment stages, Harness/Octopus/Keptn, AWS CodePipeline with cross-region stages,
  Azure DevOps environments with checks) sequences rings.
- **GitHub Actions**: one job per ring with `environment: ring-3-pilot` (wait-timer =
  bake, required reviewers for later rings), `needs:` chain, `concurrency` to serialise
  rollouts of the same service; a gate step that queries Prometheus/Datadog and fails
  on breach.
- **GitLab**: stages per ring, `resource_group` per service, `when: delayed` +
  `start_in: 2 hours` for bake, protected environments per ring.
- **AWS**: CodeDeploy/CodePipeline with wave stages; AWS Systems Manager Change Manager
  for governed sequences; the "hands-off deployments" model (pre-prod → one-box → single
  region waves → all) is the reference.
- **Feature flags** as the ring mechanism for *behaviour* changes: deploy everywhere
  dark, enable per ring/tenant/region with the same bake/gate discipline — cheaper and
  reversible in seconds when the change is flag-able.
Whatever the tool: the rollout **state** (which rings have which version, when, gate
results) must be visible on one page.

## 5. Config, data and infra changes
Infra (IaC) and config changes are rolled by rings too — a Terraform apply to all
regions at once is a global change. Schema migrations: expand everywhere first (safe
with both versions), then ring the code, then contract after the final bake. Global
singletons (DNS, CDN config, identity provider, global tables) have no rings — treat
them as emergency-grade changes with rehearsal and instant revert.

## 6. Mixed versions are the normal state
During a multi-day rollout, ring 5 runs v1 while ring 2 runs v2: APIs, events and data
formats must be compatible in both directions (expand/contract, versioned events,
tolerant readers). Cross-region replication of data written by v2 and read by v1 is the
classic failure — test v1-reads-v2-data in ring 1. Clients that pin to a region see
only one version; global load balancers must not route a user across versions
mid-session unless sessions are version-agnostic.

## 7. Rollback across rings
Rollback is *also* ringed — but faster: revert the newest ring first (smallest soak,
most suspect), confirm, then the rest in reverse order or in parallel if the failure is
clear. Keep the previous artifact warm (images cached, Lambda versions retained, AMIs
not deregistered) in every region for at least one rollout cycle. Practise a full
multi-region rollback quarterly; measure time-to-last-region.

## 8. Velocity vs safety
Total rollout time = Σ(bake) + Σ(deploy); a 5-ring plan with 24 h final bake means ~2–3
days from ring 0 to global. That's fine for most services; for urgent fixes define an
**expedited** profile (shorter bakes, still ringed) that still forbids skipping ring 2.
Track: rollouts per week, % halted, time-to-halt, mean rollout duration, and incidents
that reached > 1 ring — the last should trend to zero.

## Verify
- [ ] Ring plan per service is in code with bake times and gate queries; the rollout dashboard shows per-ring version and gate status.
- [ ] A synthetic failure injected in ring 2 halts the rollout automatically and pages; ring 3 never receives the version.
- [ ] Paired/DR regions are never in the same wave (checked by a test on the plan file).
- [ ] Previous artifact remains deployable in every region; quarterly rollback drill timed.
