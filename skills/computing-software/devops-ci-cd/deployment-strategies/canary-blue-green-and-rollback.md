---
id: computing-software.devops-ci-cd.deployment-strategies.canary-blue-green-and-rollback
name: canary-blue-green-and-rollback
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, deployment, deploy, rolling-update, rolling-deploy, canary, canary-release, blue-green, red-black, rollback, roll-forward, zero-downtime, expand-contract, parallel-change, database-migrations, schema-migration, readiness-probe, maxsurge, maxunavailable, connection-draining, kubernetes, argo-rollouts, flagger, slo, error-budget, progressive-delivery]
level: practitioner
status: draft
description: "Pick and run rolling, blue-green or canary deploys with real health gates, rollback plans and expand-contract database migrations that keep old and new versions working."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/deployment/", "https://martinfowler.com/bliki/BlueGreenDeployment.html", "https://martinfowler.com/bliki/ParallelChange.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deployment strategies — canary, blue-green, rolling and rollback

**Goal:** every production change is reversible within minutes, exposes a bad version
to as few users as possible, and never needs downtime for a schema change.

## 1. Choose the strategy
| Strategy | How | Pick when | Cost |
|---|---|---|---|
| Rolling | Replace instances a few at a time | Default for stateless services | Old + new serve traffic together during rollout |
| Blue-green | Full new stack, switch traffic at once, keep old warm | Need instant rollback; risky releases | 2× capacity during switch; the cutover hits everyone at once |
| Canary | Send 1% → 5% → 25% → 100% with checks between | High-traffic services with good metrics | Needs traffic splitting + automated analysis |
| Recreate | Stop all, start new | Can't run two versions at once (rare) | Downtime |
All but recreate mean **two versions run simultaneously** — APIs, message formats and
the database must tolerate that (section 4).

## 2. Rolling deploys done right (Kubernetes example)
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate: { maxSurge: 25%, maxUnavailable: 0 }   # never drop below capacity
  minReadySeconds: 10
  template:
    spec:
      terminationGracePeriodSeconds: 40
      containers:
        - name: app
          readinessProbe: { httpGet: { path: /ready, port: 8080 }, periodSeconds: 5 }
          lifecycle:
            preStop: { exec: { command: ["sleep", "10"] } }  # let the LB stop routing first
```
- The **readiness probe gates the rollout**: make `/ready` check what the instance truly
  needs (config loaded, DB pool connected) but not downstream services, or one flaky
  dependency stalls every deploy.
- The `preStop` sleep (needs `sleep` in the image) covers the gap between pod termination
  and load balancer deregistration; the app must also handle SIGTERM by finishing in-flight requests.
- Watch: `kubectl rollout status deploy/app --timeout=5m`; undo: `kubectl rollout undo deploy/app`.
  Set `progressDeadlineSeconds` so a stuck rollout is reported as failed.

## 3. Canary with automated analysis
- Split traffic at the load balancer, service mesh (Istio/Linkerd weights) or with
  **Argo Rollouts** / **Flagger**, e.g. steps `setWeight: 5 → pause 10m → 25 → pause 10m → 100`.
- Gate each step on **comparative** metrics: canary error rate and p99 latency vs. the
  stable version over the same window (Prometheus queries in an AnalysisTemplate). Absolute
  thresholds alone miss regressions on a quiet night.
- Canary needs enough traffic to be statistically meaningful; at low volume, extend the
  pause or use synthetic checks.
- Make the canary sticky per user if sessions/caches break when a user bounces between versions.

## 4. Database changes: expand → migrate → contract
Never ship a breaking schema change in the same deploy as the code that needs it.
1. **Expand:** add the new column/table, nullable or defaulted; deploy. Old code ignores it.
2. **Dual-write:** new code writes both old and new; backfill old rows in batches
   (small transactions, throttled) — not one giant `UPDATE`.
3. **Switch reads** to the new structure; deploy.
4. **Contract:** after the old version is fully gone *and* rollback past this point is no
   longer needed, drop the old column.
Gotchas: renaming a column is add + copy + drop, never `RENAME` in one step; adding
`NOT NULL` with a default or creating indexes can lock large tables — use online tools
(`CREATE INDEX CONCURRENTLY` in PostgreSQL; `gh-ost`/`pt-online-schema-change` for MySQL)
and set `lock_timeout`/`statement_timeout` on migration sessions.

## 5. Rollback planning
- Decide **before** deploying: the rollback command, the previous artifact digest, and
  who can trigger it. Rollback must be one action, not a rebuild.
- Code rollback is safe only if the schema is still compatible — another reason for
  expand/contract. Data written by the new version must be readable by the old.
- Prefer rollback over "roll forward with a quick fix" when users are impacted; fix
  forward only when the rollback itself is riskier (e.g. irreversible migration).
- Feature flags give a faster, narrower rollback than redeploying.

## Unconfirmed
YAML field values and the `preStop` duration are reasonable starting points, not universal;
tune to your load balancer's deregistration delay. Not hands-on verified.

## Verify
- [ ] A synthetic load test during a rolling deploy shows zero 5xx and no dropped connections.
- [ ] A deliberately broken canary (e.g. returns 500 on one route) is aborted automatically.
- [ ] Each migration in the release is labelled expand / migrate / contract and old code passes tests against the new schema.
- [ ] Rollback has been rehearsed and takes under ~5 minutes end to end.
