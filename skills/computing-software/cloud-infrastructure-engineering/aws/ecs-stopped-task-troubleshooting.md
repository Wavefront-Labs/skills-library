---
id: computing-software.cloud-infrastructure-engineering.aws.ecs-stopped-task-troubleshooting
name: ecs-stopped-task-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecs, stopped-task-reason, cannotpullcontainer, resourceinitializationerror, essential-container-exited, fargate]
level: practitioner
status: docs-checked
description: "Find why ECS tasks stop or never start: stoppedReason and exit codes, CannotPullContainerError, ResourceInitializationError for secrets/logs, OOM kills and health-check churn."
sources: ["https://docs.aws.amazon.com/AmazonECS/latest/developerguide/stopped-task-errors.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/stopped-task-error-codes.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_cannot_pull_image.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/resource-initialization-error.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECS stopped task troubleshooting

## 1. Get the reason
```bash
aws ecs list-tasks --cluster prod --service-name api --desired-status STOPPED
aws ecs describe-tasks --cluster prod --tasks <task-arn> \
  --query 'tasks[].{stopCode:stopCode,reason:stoppedReason,containers:containers[].{n:name,exit:exitCode,r:reason}}'
aws ecs describe-services --cluster prod --services api --query 'services[].events[:10]'
```
Stopped tasks appear in the console for 1 hour; capture them with an EventBridge rule on
`ECS Task State Change` where `lastStatus = STOPPED` into CloudWatch Logs for history.
Service events show placement failures ("unable to place a task") that never create tasks.

## 2. Reasons and fixes
| stoppedReason / container reason | Cause | Fix |
|---|---|---|
| `CannotPullContainerError: ... i/o timeout` | No route to ECR/registry | Private subnet needs NAT or VPC endpoints `ecr.api`, `ecr.dkr` + S3 gateway endpoint; Fargate public subnet needs `assignPublicIp=ENABLED` |
| `CannotPullContainerError: pull image manifest has been retried 5 time(s): failed to resolve ref` | Image tag no longer matches the repository (ECS keeps image versions stable per deployment, so a changed or deleted `:latest` fails) | Pin a specific tag or digest; protect deployed tags from lifecycle rules |
| `CannotPullContainerError: ... pull access denied` or role-permission message | Role lacks permission to pull (task execution role on Fargate, container instance role on EC2), or private registry credentials are wrong | Fix the role's ECR permissions; fix the registry credentials |
| `ResourceInitializationError: ... unable to pull secrets or registry auth` | No network path from the task to ECR, Secrets Manager or Systems Manager, or the execution role lacks Secrets Manager/SSM permissions, or the secret ARN does not exist in the Region | Fix NAT or VPC endpoints; add the secrets permissions to the execution role; check the ARN |
| `ResourceInitializationError: failed to initialize logging driver` | The `awslogs-group` in the task definition does not exist (or is wrong), or the task cannot reach CloudWatch Logs | Create the group (or set `awslogs-create-group` with permission to create it) or fix the network path |
| `Essential container in task exited` with exit code 1 | App crashed | Read the container's logs |
| stop code or container reason `OutOfMemoryError` (exit code 137) | Exceeded the container hard `memory` limit | Raise memory/task size; fix leak |
| exit code 139 | Segfault | App/runtime bug, architecture mismatch |
| exit code 143 | Process ended on SIGTERM (normal stop) | Ensure graceful shutdown within `stopTimeout` |
| Stopped for failing Elastic Load Balancing health checks (service event) | Target group health check failing or grace period too short | `healthCheckGracePeriodSeconds`, correct port/path, SG from ALB |
| Essential container UNHEALTHY | Container `healthCheck` command failing | Fix command (the binary must exist in the image) and `startPeriod` |
| Task stuck or failing while attaching its network interface | awsvpc ENI limit on EC2 or subnet IP exhaustion | Bigger subnets; ENI trunking on EC2 |
| `CannotStartContainerError` | Bad entrypoint/command, missing binary, permission | Run the image locally with the same command |
| stop code `SpotInterruption` (Fargate Spot) | Capacity reclaimed after a two-minute warning | Expected; mix FARGATE capacity |

## 3. Placement failures (service events)
A service event saying ECS was unable to place a task lists the reasons that followed: insufficient CPU/memory/ports on EC2 instances, placement
constraints unmatched (the task stays `PENDING`), no instances registered (agent disconnected), or ENI limit.
Fargate capacity can be briefly unavailable; give the service subnets in several AZs.

## 4. Debugging tools
- ECS Exec into a running task (`aws ecs execute-command --interactive --command /bin/sh`).
- Run the task once manually with a debug command override (`run-task --overrides`).
- Container Insights / CloudWatch Logs for app output; on EC2, the agent and container runtime logs on the host.
- Deployment circuit breaker stops endless failing deployments and rolls back.

## Verify
- [ ] Task state-change events archived to logs; dashboard of stoppedReason counts.
- [ ] New deployment reaches steady state ("has reached a steady state" service event).
- [ ] Circuit breaker with rollback enabled on services.

## Checked
Checked 2026-10-24 against the ECS developer guide (viewing stopped task errors, stopped task error codes, CannotPullContainer and ResourceInitializationError pages).
Confirmed: stopCode/stoppedReason/container reason fields, stopped tasks visible 1 hour in the console, the stop code categories (ResourceInitializationError, OutOfMemoryError, CannotStartContainerError, SpotInterruption, and others), image-pull causes (no route/NAT, S3 route for layers, role permissions, failed to resolve ref after tag change), secrets/registry-auth network and permission causes, missing log group cause, Fargate Spot two-minute warning.
Removed as unconfirmed: quoted messages for stop reasons that the docs do not list (scaling activity, ELB and container health check texts, network interface timeout, placement phrases) and the exact ECR action list.

Method: documentation only; no commands were run.
