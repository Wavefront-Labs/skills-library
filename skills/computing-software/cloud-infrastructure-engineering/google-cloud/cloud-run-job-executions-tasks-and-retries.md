---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-run-job-executions-tasks-and-retries
name: cloud-run-job-executions-tasks-and-retries
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-run, cloud-run-jobs-execution, cloud-run-job-tasks, cloud-run-task-index, batch-jobs, max-retries]
level: practitioner
status: docs-checked
description: "Run Cloud Run jobs: create and execute with overrides, split work across tasks with CLOUD_RUN_TASK_INDEX, parallelism, per-task retries and timeouts, and schedule them."
sources: ["https://docs.cloud.google.com/run/docs/create-jobs", "https://docs.cloud.google.com/run/docs/execute/jobs", "https://docs.cloud.google.com/run/docs/configuring/task-timeout", "https://docs.cloud.google.com/run/docs/execute/jobs-on-schedule"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Run job executions, tasks and retries

## Create and run
```bash
gcloud run jobs create etl --region=<R> --image=<AR>/etl:1.4 \
  --tasks=50 --parallelism=10 --max-retries=3 --task-timeout=2h \
  --cpu=2 --memory=4Gi --service-account=etl@<P>.iam.gserviceaccount.com \
  --set-env-vars=BUCKET=raw-data
gcloud run jobs execute etl --region=<R> --wait
gcloud run jobs execute etl --region=<R> --args="--date=2026-10-17" --tasks=5 --update-env-vars=MODE=backfill   # per-execution overrides
```

## Splitting work
Each task gets `CLOUD_RUN_TASK_INDEX` (0..N-1) and `CLOUD_RUN_TASK_COUNT`:
```python
import os
i, n = int(os.environ["CLOUD_RUN_TASK_INDEX"]), int(os.environ["CLOUD_RUN_TASK_COUNT"])
for f in sorted(files)[i::n]:
    process(f)
```
Make tasks idempotent, because a failed task is retried.

## Limits and behaviour
- `--tasks` is 1 to 10,000 (default 1).
- Task timeout up to 168 h (7 days), default 10 min; for GPU tasks the maximum is 1 hour.
- `--max-retries` accepts 0 to 10 (default 3 retries); a retry count of 1 means two attempts in total.
- `--parallelism` is the maximum number of tasks running at once; by default tasks start as quickly as possible.

## Scheduling
```bash
gcloud scheduler jobs create http etl-nightly --location=<R> --schedule="0 2 * * *" \
  --uri="https://run.googleapis.com/v2/projects/<P>/locations/<R>/jobs/etl:run" --http-method=POST \
  --oauth-service-account-email=scheduler@<P>.iam.gserviceaccount.com
```
The scheduler service account must have permission to invoke the job (`roles/run.invoker` is the documented role for executing jobs from the CLI).

## Gotchas
- A job does not listen for or serve requests.
- Cancelling: `gcloud run jobs executions cancel <EXEC>`.

## Verify
- [ ] `gcloud run jobs execute etl --region=<R> --wait` returns after all tasks finish and reports failure if any task fails after its retries.

## Checked

2026-10-24, Cloud Run create-jobs, execute-jobs, task-timeout and jobs-on-schedule pages on docs.cloud.google.com. Confirmed: `--tasks` range, `--max-retries` range and default, `--task-timeout` default, maximum and GPU limit, `CLOUD_RUN_TASK_INDEX` and `CLOUD_RUN_TASK_COUNT`, execute-time overrides, `--wait`, `executions cancel`, the Cloud Scheduler URI and flags. Removed unconfirmed claims (`executions list/describe` formats, `CLOUD_RUN_TASK_ATTEMPT`, parallelism 0, `run.jobs.run`, task log label).

Method: documentation only; no commands were run.
