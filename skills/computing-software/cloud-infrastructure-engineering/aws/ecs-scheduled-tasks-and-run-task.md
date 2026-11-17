---
id: computing-software.cloud-infrastructure-engineering.aws.ecs-scheduled-tasks-and-run-task
name: ecs-scheduled-tasks-and-run-task
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecs, scheduled-tasks, run-task, batch-jobs, eventbridge-scheduler]
level: practitioner
status: docs-checked
description: "Run one-off and scheduled ECS tasks: run-task with network config and overrides, EventBridge Scheduler targets, roles and PassRole, placement failures and exit codes."
sources: ["https://docs.aws.amazon.com/AmazonECS/latest/developerguide/scheduled_tasks.html", "https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-templated.html", "https://docs.aws.amazon.com/scheduler/latest/APIReference/API_EcsParameters.html", "https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled tasks and standalone run-task

## 1. One-off task
```bash
aws ecs run-task --cluster prod --task-definition reports:12 --count 1 \
  --capacity-provider-strategy capacityProvider=FARGATE_SPOT,weight=1 \
  --network-configuration 'awsvpcConfiguration={subnets=[subnet-a,subnet-b],securityGroups=[sg-jobs],assignPublicIp=DISABLED}' \
  --overrides '{"containerOverrides":[{"name":"app","command":["python","report.py","--date","2026-10-17"]}]}' \
  --started-by manual-backfill --query '{tasks:tasks[].taskArn,failures:failures}'
```
Always check `failures`: a successful response can contain zero tasks.

## 2. Wait and get the result
```bash
aws ecs wait tasks-stopped --cluster prod --tasks <TASK_ARN>
aws ecs describe-tasks --cluster prod --tasks <TASK_ARN> --query 'tasks[].{reason:stoppedReason,exit:containers[].exitCode}'
```
Fail the pipeline on non-zero exit code; `stoppedReason` explains infrastructure stops.

## 3. Scheduled
```bash
aws scheduler create-schedule --name nightly-reports --schedule-expression "cron(30 1 * * ? *)" \
  --flexible-time-window Mode=OFF --target '{
   "Arn":"arn:aws:ecs:<REGION>:<ACCOUNT_ID>:cluster/prod",
   "RoleArn":"arn:aws:iam::<ACCOUNT_ID>:role/scheduler-ecs",
   "EcsParameters":{"TaskDefinitionArn":"arn:aws:ecs:<REGION>:<ACCOUNT_ID>:task-definition/reports",
     "LaunchType":"FARGATE","TaskCount":1,
     "NetworkConfiguration":{"awsvpcConfiguration":{"Subnets":["subnet-a"],"SecurityGroups":["sg-jobs"],"AssignPublicIp":"DISABLED"}}}}'
```
The target is the ECS `RunTask` templated target: `EcsParameters.LaunchType` accepts `EC2`, `FARGATE` or `EXTERNAL` and must match the task definition's compatibilities; `TaskCount` is 1-10 (default 1). The schedule's execution role must allow `ecs:RunTask`; because RunTask hands the task and execution roles to ECS, it also needs `iam:PassRole` for them. Cron expressions have six fields (minutes hours day-of-month month day-of-week year); use `?` in day-of-month or day-of-week.

## 4. Gotchas
- Overlapping runs: each invocation calls RunTask independently, so guard against a still-running previous task with a lock inside the job.
- Jobs with retries, dependencies or fan-out: AWS Batch or Step Functions `ecs:runTask.sync`.

## Verify
- [ ] Scheduled run creates a task that stops with exit code 0.

## Checked
Checked 2026-10-24 against the EventBridge Scheduler API reference (Target, EcsParameters), templated targets guide, schedule types (cron format) and the ECS developer guide.
Confirmed: ECS RunTask is a templated target with EcsParameters (TaskDefinitionArn required, LaunchType EC2/FARGATE/EXTERNAL, NetworkConfiguration, CapacityProviderStrategy, TaskCount 1-10), six-field cron format, role-based execution.
Removed as unconfirmed: failure reason strings, unversioned task definition ARN behaviour, retry policy fragment, startedBy value.

Method: documentation only; no commands were run.
