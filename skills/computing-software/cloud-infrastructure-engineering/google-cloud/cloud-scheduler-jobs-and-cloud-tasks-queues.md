---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-scheduler-jobs-and-cloud-tasks-queues
name: cloud-scheduler-jobs-and-cloud-tasks-queues
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-scheduler-cron, scheduler-http-target, cloud-tasks-queues, task-rate-limits, task-deduplication, oidc]
level: practitioner
status: docs-checked
description: "Run cron jobs with Cloud Scheduler (HTTP with OIDC, Pub/Sub, time zones, retries) and buffer work with Cloud Tasks queues: rate limits, retries and named-task deduplication."
sources: ["https://cloud.google.com/scheduler/docs/creating", "https://cloud.google.com/scheduler/docs/http-target-auth", "https://cloud.google.com/tasks/docs/configuring-queues", "https://cloud.google.com/tasks/docs/creating-http-target-tasks", "https://cloud.google.com/tasks/docs/dual-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Scheduler jobs and Cloud Tasks queues

## 1. Scheduler: authenticated HTTP cron
```bash
gcloud scheduler jobs create http nightly-report --location=europe-west2 \
  --schedule="30 2 * * *" --time-zone="Europe/London" \
  --uri=https://reports-<hash>.a.run.app/run --http-method=POST \
  --message-body='{"kind":"nightly"}' --headers=Content-Type=application/json \
  --oidc-service-account-email=sched-reports@<P>.iam.gserviceaccount.com \
  --oidc-token-audience=https://reports-<hash>.a.run.app \
  --attempt-deadline=900s --max-retry-attempts=3 --min-backoff=60s
gcloud scheduler jobs run nightly-report --location=europe-west2      # test now
gcloud scheduler jobs pause|resume nightly-report --location=europe-west2
```
- OIDC token is generally used, except for Google APIs on `*.googleapis.com`, which expect an OAuth token (`--oauth-service-account-email`).
- Pub/Sub target: `gcloud scheduler jobs create pubsub ... --topic=<T> --message-body=...`.
- `--schedule` accepts any unix-cron compatible string; `--time-zone` takes a time zone database name.
- HTTP target attempt deadline (`--attempt-deadline`): default 3 minutes, allowed 15 seconds to 30 minutes; ignored for Pub/Sub targets. Longer work: trigger a Workflow or Cloud Run job.
- Duplicates: rarely a job request may be delivered more than once; dedupe with the job name plus the `X-CloudScheduler-ScheduleTime` header, which stays constant across retries.

## 2. Tasks: queue with rate limits
```bash
gcloud tasks queues create email-send --location=europe-west2 \
  --max-dispatches-per-second=20 --max-concurrent-dispatches=50 \
  --max-attempts=8 --min-backoff=2s --max-backoff=600s --max-doublings=5 --max-retry-duration=86400s
gcloud tasks create-http-task welcome-u123 --queue=email-send --location=europe-west2 \
  --url=https://mailer-<hash>.a.run.app/send --method=POST \
  --header=Content-Type:application/json --body-content='{"user":"u123"}' \
  --oidc-service-account-email=tasks-mailer@<P>.iam.gserviceaccount.com --schedule-time=2026-10-16T18:00:00Z
```
- **Named tasks** (`welcome-u123`) dedupe: creating a task whose name already exists in the queue fails, and Cloud Tasks remembers names for up to 24 hours after the task is deleted. Unnamed tasks get a generated name, so there is nothing to dedupe. Naming can add latency. Task IDs allow letters, numbers, hyphens and underscores, up to 500 characters.
- HTTP task dispatch deadline: default 10 minutes, allowed 15 seconds to 30 minutes; a missed deadline is a `DEADLINE_EXCEEDED` attempt that is retried per the retry config.
- `gcloud tasks queues pause|resume|purge email-send` for incidents.

## Gotchas
- Scheduler and Cloud Tasks may deliver more than once; the target must be idempotent.
- For Cloud Run and current Cloud Run functions the job's service account needs `roles/run.invoker` on the target (1st gen functions: `roles/cloudfunctions.invoker`); whoever attaches the service account needs `roles/iam.serviceAccountUser` on it. Do not revoke `roles/cloudscheduler.serviceAgent` from the Scheduler service agent (authenticated targets then return 403).
- Queue rate limits (`--max-dispatches-per-second`, `--max-concurrent-dispatches`) are per queue; size them from downstream capacity.

## Verify
- [ ] `gcloud scheduler jobs describe nightly-report --location=<R>` shows `state: ENABLED` and a recent successful attempt.
- [ ] Creating the same named task twice fails the second time; queue metrics show dispatch rate at the cap during a burst.

## Checked
Date: 2026-10-28. Confirmed against the Cloud Scheduler and Cloud Tasks docs pages (creating jobs, HTTP target auth, configuring queues, HTTP target tasks, overview) and the cloudscheduler v1 and cloudtasks v2 discovery documents: unix-cron schedules, OIDC versus OAuth token rule, attempt deadline (default 3 minutes, 15 seconds to 30 minutes), task dispatch deadline (default 10 minutes, 15 seconds to 30 minutes), 24-hour name memory, 500-character task ID limit, IAM roles, idempotency advice; gcloud flags checked against the CLI reference. Removed: the 100 KB payload limit, the 1M-task example, the older-projects `serviceAccountTokenCreator` remark, and the old "period after" dedupe wording (the page gives 24 hours). Hostnames and IDs are placeholders.
Method: documentation only; no commands were run.
