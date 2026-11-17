---
id: computing-software.ai-ml-engineering.mlops.scheduled-and-event-triggered-pipeline-runs
name: scheduled-and-event-triggered-pipeline-runs
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, pipeline-schedules, event-triggers, continuous-training, cron, eventbridge]
level: practitioner
status: draft
description: "Trigger ML pipelines on schedules and events: Vertex, SageMaker, Kubeflow and Azure ML schedules, data-arrival triggers, concurrency limits, catchup and data-readiness checks."
sources:
  - https://cloud.google.com/vertex-ai/docs/pipelines/schedule-pipeline-run
  - https://docs.aws.amazon.com/sagemaker/latest/dg/pipeline-eventbridge.html
  - https://www.kubeflow.org/docs/components/pipelines/user-guides/core-functions/run-a-pipeline/
  - https://learn.microsoft.com/en-us/azure/machine-learning/how-to-schedule-pipeline-job
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Scheduled and event-triggered pipeline runs

**Goal:** training and batch pipelines run when they should (time or new data), never twice concurrently, and never on incomplete data.

## Pick the trigger
| Trigger | Use for |
|---|---|
| Cron schedule | batch scoring, periodic retraining |
| Data arrival (object created, partition landed) | retrain or score when inputs exist |
| Monitoring alert (drift, metric drop) | conditional retraining |
| Code/config merge | CI/CD (separate from CT) |

## Platform schedules
- **Vertex AI:** `job = aiplatform.PipelineJob(template_path="pipeline.json", pipeline_root=ROOT, parameter_values={...}); job.create_schedule(display_name="nightly", cron="TZ=Etc/UTC 0 2 * * *", max_concurrent_run_count=1)`.
- **SageMaker Pipelines:** `PipelineSchedule(name="nightly", cron="0 2 * * ? *")` with `pipeline.put_triggers(triggers=[...], role_arn=...)`, or an EventBridge rule targeting the pipeline (schedule expression or event pattern, with parameters passed in the target).
- **Kubeflow Pipelines:** `client.create_recurring_run(experiment_id=..., job_name="nightly", cron_expression="0 0 2 * * *", pipeline_package_path="pipeline.yaml", max_concurrency=1)` - note the 6-field cron with seconds.
- **Azure ML:** `JobSchedule(name="nightly", trigger=CronTrigger(expression="0 2 * * *", time_zone="UTC"), create_job=pipeline_job)` then `ml_client.schedules.begin_create_or_update(schedule)`.
- **Airflow:** schedule on time or on data assets (datasets) produced by upstream DAGs.

## Event triggers
GCS object finalize -> Eventarc/Cloud Run function -> submit `PipelineJob`; S3 `Object Created` -> EventBridge -> SageMaker pipeline target. Trigger on a completion marker (`_SUCCESS` file, or a table partition commit), not on every file, or you start one run per shard.

## Run hygiene
- **Concurrency 1** for retraining pipelines; overlapping runs race on registry aliases.
- **Data readiness:** first step asserts row counts, freshness and partition completeness; fail fast with a clear message.
- **Logical date as a parameter:** pass the data interval explicitly (`run_date=2026-10-17`) so reruns and backfills are idempotent.
- **Catchup:** decide whether missed intervals run (Airflow `catchup`) - usually yes for scoring, no for retraining.
- **Time zones:** schedule in UTC; DST shifts double-run or skip local-time schedules.
- **Alerting:** a scheduled pipeline that silently stops is the common failure; alert on "no successful run in N hours", not just on failures.

## Verify
- [ ] Two triggers in quick succession produce one active run.
- [ ] A run on incomplete data fails at the readiness step.
- [ ] Missing-run alert fires when the schedule is paused in a test.
