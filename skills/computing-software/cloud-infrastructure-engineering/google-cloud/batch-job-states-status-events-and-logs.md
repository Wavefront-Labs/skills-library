---
id: computing-software.cloud-infrastructure-engineering.google-cloud.batch-job-states-status-events-and-logs
name: batch-job-states-status-events-and-logs
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-batch, batch-job-status-events, batch-job-monitoring, batch-notifications, batch-task-logs]
level: practitioner
status: docs-checked
description: "Monitor Cloud Batch jobs: job and task states, status events explaining stuck QUEUED or SCHEDULED jobs, per-task logs, Pub/Sub notifications, and common failure exit codes."
sources: ["https://cloud.google.com/batch/docs/view-jobs-tasks", "https://cloud.google.com/batch/docs/analyze-job-using-logs", "https://cloud.google.com/batch/docs/enable-notifications"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch job states, status events and logs

## States
Job: `QUEUED` -> `SCHEDULED` -> `RUNNING` -> `SUCCEEDED` / `FAILED`, plus `DELETION_IN_PROGRESS`, `CANCELLATION_IN_PROGRESS` and `CANCELLED`.
Task: `PENDING`, `ASSIGNED`, `RUNNING`, `SUCCEEDED`, `FAILED`, `UNEXECUTED` (not executed when the job finished).

```bash
gcloud batch jobs describe <JOB> --location=<R> --format="yaml(status)"
gcloud batch tasks list --job=<JOB> --location=<R> --format="table(name.basename(),status.state)"
gcloud batch tasks describe <TASK_INDEX> --job=<JOB> --task_group=group0 --location=<R>
```
`status.statusEvents[]` explain problems in QUEUED, SCHEDULED or FAILED jobs, for example
"Quota checking process decides to delay scheduling ... due to inadequate quotas",
"Quota QUOTA_NAME exceeded. Limit: ... in region REGION", "No VM has agent reporting correctly within time window ...",
and "Constraint constraints/compute.vmExternalIpAccess violated".

## Stuck jobs
| Stuck at | Usual cause |
|---|---|
| QUEUED / SCHEDULED with quota text in `statusEvents` | quota delaying scheduling |
| "No VM has agent reporting correctly" | job service account lacks `roles/batch.agentReporter`, VM network problems, or an outdated Batch VM image |
| FAILED with `compute.vmExternalIpAccess` violated | org policy forbids external IPs: block external access for all VMs in the job |
| RUNNING but no progress | task hanging; check `maxRunDuration` |

## Logs
With `logsPolicy.destination: CLOUD_LOGGING`:
```
logName=("projects/<P>/logs/batch_task_logs" OR "projects/<P>/logs/batch_agent_logs")
labels.job_uid="<JOB_UID>"
```
`batch_agent_logs` record activity of the Batch service agent; `batch_task_logs` hold what runnables write to stdout and stderr. If a job produced no logs, check that the Cloud Logging API is enabled, the job service account has `roles/logging.logWriter`, and `logsPolicy` is set.

## Exit codes
Exit codes 50001-59999 are reserved by Batch:
- 50001: VM preemption (Spot).
- 50002: Batch no longer receives VM updates (VM reporting timeout).
- 50003: VM rebooted during task execution. 50004: VM and task unresponsive (task cannot be cancelled).
- 50005: task ran over the maximum runtime. 50006: VM recreated during task execution.
- Your process's exit codes pass through; use `lifecyclePolicies` (one policy is supported) and `maxRetryCount` (0-10) to control retries.

## Notifications
```json
"notifications": [{"pubsubTopic": "projects/<P>/topics/batch-events",
  "message": {"type": "JOB_STATE_CHANGED"}}, {"pubsubTopic": "projects/<P>/topics/batch-events",
  "message": {"type": "TASK_STATE_CHANGED", "newTaskState": "FAILED"}}]
```
The job's service account (not your user account) needs `roles/pubsub.publisher` on the topic.

## Verify
- [ ] A failed test task produces a FAILED notification and its stderr in batch_task_logs.

## Checked
2026-10-27. Confirmed against the Batch troubleshooting page (statusEvents messages, quota delay text, no-agent-reporting causes, vmExternalIpAccess message, exit codes 50001-50006 and their meanings), analyze-job-using-logs page (batch_task_logs and batch_agent_logs, labels.job_uid), enable-notifications page (Pub/Sub Publisher on the job's service account) and the Batch discovery document (job and task state enums, Message type values, JobNotification fields). Removed: ZONE_RESOURCE_POOL_EXHAUSTED and QUOTA_EXCEEDED names, the QUEUED-to-SCHEDULED event text, the task_id label format, the hedge about checking the troubleshooting table. Corrected: Pub/Sub publisher role goes to the job's service account, not the Batch service agent; job and task state lists were incomplete.
Method: documentation only; no commands were run.
