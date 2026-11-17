---
id: computing-software.devops-ci-cd.github-actions.monitoring-runner-fleets-and-queue-time
name: monitoring-runner-fleets-and-queue-time
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, runner-monitoring, runner-queue-metrics, arc-metrics, workflow-job-webhook, runner-utilisation]
level: advanced
status: docs-checked
description: "Monitor self-hosted runners: ARC Prometheus metrics, queue time from workflow_job webhooks, runner status via the API, and alerts for starved or offline pools."
sources: ["https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/deploying-runner-scale-sets-with-actions-runner-controller#enabling-metrics", "https://docs.github.com/en/webhooks/webhook-events-and-payloads#workflow_job", "https://docs.github.com/en/rest/actions/self-hosted-runners"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring the runner fleet

The two numbers that matter: **queue time** (job created → started) and **capacity headroom**.

## 1. ARC metrics
Controller values:
```yaml
metrics:
  controllerManagerAddr: ":8080"
  listenerAddr: ":8080"
  listenerEndpoint: "/metrics"
```
The controller-manager and listener pods then serve metrics on the configured port and path; scrape them.
Listener gauges: `gha_assigned_jobs`, `gha_running_jobs` (running or queued to run), `gha_registered_runners`,
`gha_busy_runners`, `gha_idle_runners`, `gha_min_runners`, `gha_max_runners`, `gha_desired_runners`;
counters `gha_started_jobs_total`, `gha_completed_jobs_total`; histograms `gha_job_startup_duration_seconds`
(time waiting for a job to start on a scale-set runner) and `gha_job_execution_duration_seconds`.
Controller-manager gauges: `gha_controller_pending_ephemeral_runners`, `gha_controller_running_ephemeral_runners`,
`gha_controller_failed_ephemeral_runners`, `gha_controller_running_listeners`.
Alert ideas: `gha_desired_runners` pinned at `gha_max_runners` while `gha_assigned_jobs` stays high, and a high
percentile of `gha_job_startup_duration_seconds` (check the exact label names on your scrape).

## 2. Queue time anywhere (incl. non-ARC runners)
Subscribe an org webhook to the `workflow_job` event and derive queue time from the job's creation and
start timestamps in the payload (see the `workflow_job` payload docs for exact field names), grouped by
runner labels. A job queued with labels no runner has stays queued until the 24-hour timeout, so alert on
long-queued jobs well before that.

## 3. Runner status via API
`GET /orgs/{org}/actions/runners` lists the org's self-hosted runners with `name`, `status` (`online` or
`offline`), `busy` and `labels`. A long-lived runner showing `offline` usually means a crashed service or lost
registration. Page through results for large fleets.

## Verify
- [ ] Dashboard shows queue time p50/p95 per label.
- [ ] Alert fires when a scale set sits at maxRunners with jobs pending.

## Checked
2026-10-31. Confirmed in GitHub's ARC "enabling metrics" section (values keys, endpoint, metric names and types) and the REST self-hosted runners page (org runners endpoint, `status`, `busy`, `labels`); the 24-hour queued-job timeout is from the self-hosted runners reference.
Removed (not confirmed in fetched pages): PromQL alert expressions, `workflow_job` field list, the Waiting-for-a-runner message, the 14-day removal rule, the Insights menu description, the `gh api` one-liner.
Method: documentation only; no commands were run.
