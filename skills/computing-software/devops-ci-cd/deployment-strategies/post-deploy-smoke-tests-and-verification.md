---
id: computing-software.devops-ci-cd.deployment-strategies.post-deploy-smoke-tests-and-verification
name: post-deploy-smoke-tests-and-verification
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, post-deploy-verification, smoke-test, deployment-automation]
level: practitioner
status: docs-checked
description: "Verify a deployment actually worked: smoke tests against the new version, version endpoint checks, synthetic transactions, metric comparisons and automatic rollback triggers."
sources: ["https://sre.google/workbook/canarying-releases/", "https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Post-deploy smoke tests and verification

"kubectl apply succeeded" is not "the deploy worked". Verify in this order:

1. **Rollout completed**: `kubectl rollout status deploy/api`, ECS service stable
   (`aws ecs wait services-stable`), all instances on the new version.
2. **Right version serving**:
   ```bash
   for i in $(seq 1 20); do curl -fsS https://api.example.com/version | jq -r .git_sha; done | sort | uniq -c
   ```
   Expect only the new SHA (or the planned canary split).
3. **Smoke tests**: a handful of critical read-only paths and one safe write path with a test
   account, < 2 minutes, tagged `@smoke`.
4. **Metrics window**: error rate, p95 latency, saturation for 5-15 minutes compared with the
   pre-deploy period (Prometheus query or APM deployment markers).
   ```promql
   sum(rate(http_requests_total{job="api",code=~"5.."}[5m])) / sum(rate(http_requests_total{job="api"}[5m]))
   ```
5. **Logs**: new error signatures since deploy time.

## Automation
- Pipeline stage after deploy runs steps 1-4 and fails the deployment on breach (mark it failed in your CI/CD platform), triggering rollback.
- Annotate dashboards with the deploy for humans.

## Gotchas
- Smoke tests that hit caches or a single healthy pod pass while half the fleet is broken; spread requests.
- Writes in production smoke tests must be idempotent and cleanable.
- Background workers/cron are not covered by HTTP smoke tests; check queue lag and job success.

## Verify
- [ ] A deliberately broken release fails verification and is rolled back without human action.

## Checked

2026-10-28. Confirmed: `kubectl rollout status` on a Deployment (Kubernetes Deployment page), and `aws ecs wait services-stable` passed the command check; the Google SRE workbook canarying chapter supports comparing canary and baseline metrics over a window. Removed: the `--timeout` flag, GitHub deployment status and GitLab environment wording, and the Grafana annotation API reference.

Method: documentation only; no commands were run.
