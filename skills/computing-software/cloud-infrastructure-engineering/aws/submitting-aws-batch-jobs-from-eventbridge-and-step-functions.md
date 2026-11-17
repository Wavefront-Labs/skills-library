---
id: computing-software.cloud-infrastructure-engineering.aws.submitting-aws-batch-jobs-from-eventbridge-and-step-functions
name: submitting-aws-batch-jobs-from-eventbridge-and-step-functions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-batch, batch-job-trigger, submit-job, eventbridge-scheduler, step-functions-sync, job-orchestration]
level: practitioner
status: docs-checked
description: "Trigger AWS Batch jobs from EventBridge rules, EventBridge Scheduler and Step Functions (.sync), pass parameters from events, and track job state changes."
sources: ["https://docs.aws.amazon.com/batch/latest/userguide/batch-cwe-target.html", "https://docs.aws.amazon.com/step-functions/latest/dg/connect-batch.html", "https://docs.aws.amazon.com/batch/latest/userguide/batch_cwe_events.html", "https://docs.aws.amazon.com/cli/latest/reference/batch/submit-job.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Submitting Batch jobs from EventBridge and Step Functions

## 1. Plain submit-job (what every integration does)
```bash
aws batch submit-job --job-name nightly-etl-$(date +%F) --job-queue etl-q \
  --job-definition etl:12 \
  --parameters inputPrefix=s3://raw/2026-10-18/ \
  --container-overrides 'environment=[{name=RUN_DATE,value=2026-10-18}],resourceRequirements=[{type=MEMORY,value=8192}]' \
  --retry-strategy attempts=3 --timeout attemptDurationSeconds=7200
```
`--parameters` substitute `Ref::inputPrefix` placeholders in the job definition command.

## 2. Scheduled with EventBridge Scheduler
```bash
aws scheduler create-schedule --name nightly-etl \
  --schedule-expression 'cron(0 2 * * ? *)' --schedule-expression-timezone Europe/London \
  --flexible-time-window Mode=OFF \
  --target '{"Arn":"arn:aws:scheduler:::aws-sdk:batch:submitJob",
    "RoleArn":"arn:aws:iam::<ACCOUNT_ID>:role/SchedulerBatch",
    "Input":"{\"JobName\":\"nightly-etl\",\"JobQueue\":\"etl-q\",\"JobDefinition\":\"etl\"}"}'
```
The role needs permission to submit jobs. The Batch documentation says scheduled EventBridge
rules are a legacy feature and recommends EventBridge Scheduler for new schedules.

## 3. Event-driven with an EventBridge rule
AWS Batch jobs can be EventBridge targets, for example a job submitted whenever an object is
uploaded to a bucket (via a CloudTrail-logged API call), with the EventBridge input
transformer passing the bucket and key to Batch parameters. In that scenario the S3 bucket,
EventBridge rule and CloudTrail logs must all be in the same Region. Input transformer shape:
```json
{"InputPathsMap": {"key": "$.detail.object.key"},
 "InputTemplate": "{\"Parameters\": {\"inputKey\": \"<key>\"}}"}
```
The EventBridge service needs an IAM role to run Batch jobs (the console can create it).
Array jobs: `ArrayProperties.Size` in the job submission.

## 4. Orchestrated with Step Functions
```json
"RunEtl": {
  "Type": "Task",
  "Resource": "arn:aws:states:::batch:submitJob.sync",
  "Arguments": {
    "JobName": "etl",
    "JobQueue": "arn:aws:batch:<REGION>:<ACCOUNT_ID>:job-queue/etl-q",
    "JobDefinition": "arn:aws:batch:<REGION>:<ACCOUNT_ID>:job-definition/etl:12",
    "Parameters": {"inputPrefix": "{% $states.input.prefix %}"}},
  "Next": "Publish"}
```
The Step Functions page shows an execution role with `batch:SubmitJob`, `batch:DescribeJobs`,
`batch:TerminateJob` and `events:PutTargets` (plus related events permissions) on the managed rule
`StepFunctionsGetEventsForBatchJobsRule`. With `batch:submitJob.sync`, jobs that use `ecsProperties`
or `eksProperties` need the matching override in the Task state, otherwise it fails with
`Batch.ClientException`. In the job definition, `Ref::TaskToken` references the task token for callbacks.

## 5. Tracking outcomes
AWS Batch sends job state change events to EventBridge when a job's status changes (for example
RUNNING to FAILED). Build an EventBridge rule on those events to route failures to SNS or chat.
Handle unknown event properties, as AWS may add fields.

## Gotchas
- A job definition without a revision uses the latest active revision; pin revisions in
  production.
- SUCCEEDED job state is kept in AWS Batch for at least 7 days.

## Verify
- [ ] Schedule fires at the right local time; job appears in the queue with the expected parameters.
- [ ] Uploading a test object starts a job with the object key.
- [ ] Step Functions execution waits for job completion.

## Checked

2026-10-28. Confirmed against AWS documentation: Batch as EventBridge target (same-Region rule for the CloudTrail scenario, IAM role requirement, legacy scheduled rules), Step Functions submitJob.sync permissions and managed rule, Ref::TaskToken, latest-active-revision default, job state change events, 7-day SUCCEEDED retention; submit-job flags via botocore.
Removed: S3 EventBridge-notification pattern, Retry/Catch and Map-state advice, detail-type string, at-least-once and idempotency gotcha, input-transformer validity claim, Scheduler time zone/retry claims; made account ids placeholders.
Method: documentation only; no commands were run.
