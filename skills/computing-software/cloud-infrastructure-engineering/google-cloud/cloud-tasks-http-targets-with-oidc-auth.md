---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-tasks-http-targets-with-oidc-auth
name: cloud-tasks-http-targets-with-oidc-auth
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-tasks, cloud-tasks-oidc, http-target-tasks, oidc-token, cloud-run, task-dispatch, queue-level-routing]
level: practitioner
status: docs-checked
description: "Create Cloud Tasks HTTP target tasks that call Cloud Run or private endpoints with OIDC or OAuth tokens, queue-level HTTP target overrides, dispatch deadlines and task dedup."
sources: ["https://cloud.google.com/tasks/docs/creating-http-target-tasks", "https://cloud.google.com/tasks/docs/configuring-queues#configuring_http_target", "https://cloud.google.com/tasks/docs/dual-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Tasks HTTP targets with OIDC auth

## Create a task (Python)
```python
from google.cloud import tasks_v2
import json, datetime
c = tasks_v2.CloudTasksClient()
parent = c.queue_path("<P>", "europe-west2", "emails")
task = {
  "name": c.task_path("<P>", "europe-west2", "emails", "order-8812-receipt"),   # dedup key
  "http_request": {
    "http_method": tasks_v2.HttpMethod.POST,
    "url": "https://mailer-abc123-nw.a.run.app/send",
    "headers": {"Content-Type": "application/json"},
    "body": json.dumps({"order": 8812}).encode(),
    "oidc_token": {"service_account_email": "tasks-invoker@<P>.iam.gserviceaccount.com",
                    "audience": "https://mailer-abc123-nw.a.run.app"},
  },
  "dispatch_deadline": {"seconds": 300},
}
c.create_task(parent=parent, task=task)
```
- OIDC (ID) tokens are used in Google's examples; use the OAuth token variant for Google APIs on `*.googleapis.com`.
- Named tasks dedupe: creating a task whose name exists in the queue fails, and names are remembered for up to 24 hours after the task is deleted. The processing for this can add latency.
- Queue-level `httpTarget` auth overrides task-level auth: a queue with an OIDC override dispatches OAuth tasks with the OIDC token.

## IAM
- Service account that creates tasks: the Cloud Tasks Enqueuer role.
- Cloud Tasks primary service agent: `roles/iam.serviceAccountUser` on the token service account, so it can mint tokens (the agent's `roles/cloudtasks.serviceAgent` role can be added manually if missing).
- Token service account: `roles/run.invoker` on a Cloud Run target.

## Queue-level HTTP target
Set URI override and auth on the queue so producers only send bodies:
```bash
gcloud tasks queues update emails --location=europe-west2 \
  --http-uri-override=host:mailer-abc123-nw.a.run.app,path:/send \
  --http-oidc-service-account-email-override=tasks-invoker@<P>.iam.gserviceaccount.com \
  --http-oidc-token-audience-override=https://mailer-abc123-nw.a.run.app
```

## Retries and deadlines
Target must respond within `dispatch_deadline` (15 seconds to 30 minutes for HTTP tasks, default 10 minutes); otherwise
the attempt is cancelled as `DEADLINE_EXCEEDED` and retried per the queue retry config (`--max-attempts`, `--min-backoff`, `--max-doublings`).
Delivery is at least once, so handlers must be idempotent; header `X-CloudTasks-TaskRetryCount` is the retry count (0 on the first attempt).

## Verify
- [ ] Target logs show requests with a valid ID token; a 500 from the handler causes retries with backoff.

## Checked
Date: 2026-10-28. Confirmed against the Cloud Tasks pages (Create HTTP target tasks, Configuring queues, overview) and the cloudtasks v2 discovery document: `dispatchDeadline` range and default, 24-hour name memory, queue-level auth override precedence, `X-CloudTasks-TaskRetryCount`, at-least-once delivery, service agent roles; queue `--http-*-override` flags checked against the CLI reference. Corrected: the dedupe window was given as about 1 hour (page says 24 hours). Removed: the IAP use, the `cloud-platform` scope note, hashed-name advice, and the role id for the enqueuer. Hostnames and IDs are placeholders.
Method: documentation only; no commands were run.
