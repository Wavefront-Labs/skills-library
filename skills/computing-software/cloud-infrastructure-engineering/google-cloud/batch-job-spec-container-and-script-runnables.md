---
id: computing-software.cloud-infrastructure-engineering.google-cloud.batch-job-spec-container-and-script-runnables
name: batch-job-spec-container-and-script-runnables
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-batch, batch-job-spec, batch-json, batch-container-jobs, batch-script-jobs, array-jobs, spot-batch]
level: practitioner
status: docs-checked
description: "Write Cloud Batch job JSON: task groups, parallelism, container and script runnables, task index sharding, GCS volumes, retries by exit code, Spot allocation and logs."
sources: ["https://cloud.google.com/batch/docs/create-run-basic-job", "https://cloud.google.com/batch/docs/reference/rest/v1/projects.locations.jobs", "https://cloud.google.com/batch/docs/create-run-job-storage", "https://cloud.google.com/batch/docs/automate-task-retries"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Batch job spec: container and script runnables

## 1. A sharded container job on Spot
```json
{
  "taskGroups": [{
    "taskCount": 200,
    "parallelism": 40,
    "taskSpec": {
      "runnables": [
        {"script": {"text": "echo task ${BATCH_TASK_INDEX}/${BATCH_TASK_COUNT} on $(hostname)"}},
        {"container": {
          "imageUri": "europe-west2-docker.pkg.dev/<P>/batch/render:1.4.2",
          "entrypoint": "/bin/sh",
          "commands": ["-c", "render --in /mnt/in/shard-${BATCH_TASK_INDEX}.json --out /mnt/out/"]
        }}
      ],
      "volumes": [
        {"gcs": {"remotePath": "<BUCKET>/inputs"}, "mountPath": "/mnt/in"},
        {"gcs": {"remotePath": "<BUCKET>/outputs"}, "mountPath": "/mnt/out"}
      ],
      "computeResource": {"cpuMilli": 4000, "memoryMib": 8192},
      "maxRunDuration": "3600s",
      "maxRetryCount": 3,
      "lifecyclePolicies": [
        {"action": "FAIL_TASK", "actionCondition": {"exitCodes": [2]}}
      ]
    }
  }],
  "allocationPolicy": {
    "instances": [{"policy": {"machineType": "c3-standard-8", "provisioningModel": "SPOT"}}],
    "location": {"allowedLocations": ["regions/europe-west2"]}
  },
  "logsPolicy": {"destination": "CLOUD_LOGGING"},
  "labels": {"team": "media"}
}
```
`BATCH_TASK_INDEX` and `BATCH_TASK_COUNT` drive sharding. Runnables run in order; set
`"background": true` on a runnable that is not expected to exit, and add a `{"barrier": {}}` runnable to block later runnables until all tasks reach it. Spot preemption
surfaces as exit code `50001`; exit codes 50001-59999 are reserved by Batch.

**Retries:** `maxRetryCount` accepts 0-10 (default 0, never retry). Only one lifecycle policy is supported. Without a matching policy, a non-zero exit is retried up to `maxRetryCount` and exit 0 ends the task, so the policy above fails fast on exit code 2 while other failures (including 50001) are retried. A `RETRY_TASK` policy with `exitCodes: [50001]` is the other form.

## 2. Submit and watch
```bash
gcloud batch jobs submit render-20261016 --location=europe-west2 --config=job.json
gcloud batch jobs describe render-20261016 --location=europe-west2 --format='yaml(status)'
gcloud batch tasks list --job=render-20261016 --location=europe-west2 --filter='status.state=FAILED'
gcloud logging read 'labels.job_uid="<JOB_UID>"' --limit=50
```

## Gotchas
- Include a timestamp in job names so each submission is distinct.
- `computeResource` (`cpuMilli`, `memoryMib`) is per task; `taskCountPerNode` caps tasks per VM.
- `container.options` passes extra `docker run` options; `container.volumes` bind-mounts host paths into the container.
- `taskEnvironments` passes per-task variables; `taskCount` must then equal the array length (maximum 200 entries).

## Verify
- [ ] Job reaches `SUCCEEDED` with all 200 tasks; outputs bucket has 200 files.
- [ ] A task failing with exit code 2 fails without further retries; other failures are retried up to `maxRetryCount`.

## Checked
2026-10-27. Confirmed against the Batch REST reference and discovery document (v1 schemas for TaskGroup, TaskSpec, Runnable, Container, Barrier, Volume, GCS, ComputeResource, LifecyclePolicy, ActionCondition, AllocationPolicy, InstancePolicy, LogsPolicy; maxRetryCount range 0-10; only one lifecycle policy; default retry policy) and the Batch task-retry, basic-job and troubleshooting pages (exit codes 50001-59999 reserved, 50001 is Spot preemption, taskEnvironments limit). Removed: job-name uniqueness claim, agent headroom claim, GCS FUSE usage advice, network-host default claim. Corrected: the example listed two lifecycle policies but only one is supported, and the 50001 retry is covered by the default policy.
Method: documentation only; no commands were run.
