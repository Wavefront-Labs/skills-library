---
id: computing-software.devops-ci-cd.release-engineering.measuring-dora-four-keys
name: measuring-dora-four-keys
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, dora-metrics, four-keys, measuring-dora, deployment-frequency, lead-time-for-changes, change-failure-rate, time-to-restore, mttr, failed-deployment-recovery-time, reliability, accelerate, dora-report, elite-performers, metrics-definitions, deployment-events, incident-linking, four-keys-project, grafana-dora, gitlab-dora-metrics, github-deployments-api, goodhart, metric-gaming, value-stream]
level: practitioner
status: draft
description: "Measure the DORA four keys honestly: precise definitions and event sources, a minimal data model and SQL, benchmark tiers, GitLab/GitHub built-ins, and how teams game them."
sources: ["https://dora.dev/guides/dora-metrics-four-keys/", "Forsgren, Humble, Kim - Accelerate (2018), ch. 2 Measuring Performance", "https://dora.dev/research/2024/dora-report/", "https://github.com/dora-team/fourkeys", "https://docs.gitlab.com/ee/user/analytics/dora_metrics.html", "https://docs.github.com/en/rest/deployments/deployments"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Measuring the DORA four keys

**Goal:** four numbers per service/team that come from pipeline and incident events (not
surveys), are defined the same way everywhere, and are used to find bottlenecks — not to
rank people.

## 1. Definitions (be precise or the numbers are noise)
| metric | definition used here | event sources |
|---|---|---|
| **Deployment frequency** | count of *successful production deployments* per day (a deployment = one artifact version reaching production for a service) | deploy pipeline success events; GitHub Deployments API; GitLab environments; Argo CD sync-succeeded notifications |
| **Lead time for changes** | median time from **commit** (author timestamp of the first commit in the change, or PR open for squash workflows — pick one and document it) to that commit being **in production** | commits ↔ deployments (deployment carries the SHA; lead time = deploy time − commit time for every commit newly included since the previous deploy) |
| **Change failure rate** | % of production deployments that caused a **degradation needing remediation** (rollback, hotfix, patch, incident) | incidents/rollbacks linked to the deployment that introduced them |
| **Failed deployment recovery time** (ex-"time to restore") | median time from a failed deployment being detected to service restored (rollback complete or fix deployed) | incident open/close or rollback events linked to deployments |
2023+ DORA also tracks **reliability** (SLO attainment) as a fifth dimension; keep SLO
error budget burn alongside the four.
Document edge cases: config-only deploys count; feature-flag flips don't (they're not
deployments) unless you choose to; a canary that auto-rolled back is a failed deploy
(counts for CFR and recovery time).

## 2. Benchmarks (2024 report, rounded)
| tier | deploy freq | lead time | CFR | recovery |
|---|---|---|---|---|
| Elite | on demand (multiple/day) | < 1 day | ~5 % | < 1 h |
| High | daily–weekly | 1 day–1 week | ~10 % | < 1 day |
| Medium | weekly–monthly | 1 week–1 month | ~15 % | 1 day–1 week |
| Low | monthly+ | > 1 month | ~40 % | 1 week+ |
Tiers shift each year; use them for direction, not vanity. The useful comparison is your
own trend per team/service.

## 3. Minimal data model
Three tables (or one event stream):
```
deployments(id, service, env='prod', sha, version, started_at, finished_at, status, triggered_by)
changes(sha, service, authored_at, merged_at, pr_id)               -- from git log / PR API
incidents(id, service, caused_by_deployment_id NULL, opened_at, resolved_at, severity, remediation='rollback|hotfix|fix-forward')
```
Linking: deployments ↔ changes by `git log prev_sha..sha`; incidents ↔ deployment by
explicit field set during the post-mortem (or auto-link: incident opened within N hours
of a deploy on that service, confirmed by a human).
SQL sketches (Postgres):
```sql
-- deployment frequency per week
SELECT service, date_trunc('week', finished_at) wk, count(*) FROM deployments WHERE status='success' GROUP BY 1,2;
-- lead time: median over commits included in each deploy
WITH dc AS (SELECT d.id, d.service, d.finished_at, c.authored_at FROM deployments d JOIN changes c USING (service)
            WHERE c.merged_at <= d.finished_at AND c.merged_at > coalesce((SELECT max(finished_at) FROM deployments p WHERE p.service=d.service AND p.finished_at<d.finished_at AND p.status='success'), '1970-01-01'))
SELECT service, percentile_cont(0.5) WITHIN GROUP (ORDER BY finished_at-authored_at) FROM dc GROUP BY 1;
-- change failure rate
SELECT d.service, count(i.id)::float/count(d.id) FROM deployments d LEFT JOIN incidents i ON i.caused_by_deployment_id=d.id WHERE d.status='success' GROUP BY 1;
-- recovery time
SELECT service, percentile_cont(0.5) WITHIN GROUP (ORDER BY resolved_at-opened_at) FROM incidents WHERE caused_by_deployment_id IS NOT NULL GROUP BY 1;
```
Use medians (lead time, recovery) and rates over ≥ 30 deploys; small services need
monthly windows or the numbers jump around.

## 4. Getting the events
- **GitHub**: create a Deployment per prod deploy (`environment:` jobs do it); pull
  `/repos/{o}/{r}/deployments` + statuses; commits via `/compare/{base}...{head}`;
  incidents from PagerDuty/Opsgenie/Jira webhooks.
- **GitLab**: built-in DORA (Ultimate): CI/CD Analytics → DORA metrics, computed from
  environments with `deployment_tier: production` and incidents (issues with `incident`
  type linked by `related_to`); API `/projects/:id/dora/metrics?metric=deployment_frequency`.
- **Argo CD/Flux**: notification webhook on `on-deployed` → your events table with
  revision + app; map app → service.
- **Jenkins**: post-success `httpRequest` to the collector; or Prometheus `jenkins_job_*`.
- Google's open-source **Four Keys** project (BigQuery + Data Studio) ingests GitHub/
  GitLab/PagerDuty webhooks; Grafana dashboards exist for the same schema; Sleuth, LinearB,
  Jellyfish, Swarmia, Faros are commercial options. Build vs buy: build if you already
  have an events pipeline; otherwise the saved month is worth it.

## 5. Using them (and not abusing them)
- Look at the four **together**: speed without stability is just breaking things faster.
- Per *service/team*, trended; org averages hide everything.
- Pair with a **value-stream map**: lead time breaks down into coding, PR wait, review,
  CI, approval, deploy wait — fix the biggest segment (usually PR wait or approval).
- Never: individual developer metrics, targets without context ("CFR must be 5 %"),
  comparing teams with different risk profiles. Goodhart's law applies fast: deploy
  frequency inflates with no-op deploys, CFR deflates when incidents stop being linked.
  Mitigate by pairing with reliability (SLOs) and qualitative review in retros.
- Publish definitions and the query repo; people trust numbers they can reproduce.

## Verify
- [ ] For one service, the dashboard's deployment count for last month equals the count a human gets from the pipeline UI.
- [ ] Lead time definition (commit or PR open) is written down and the query implements it.
- [ ] Every incident from the last quarter has a `caused_by_deployment_id` or an explicit "not deploy-caused" mark.
- [ ] Metrics are shown per service with 90-day trends and discussed in retros, not in performance reviews.
