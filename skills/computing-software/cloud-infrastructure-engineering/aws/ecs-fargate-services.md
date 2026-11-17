---
id: computing-software.cloud-infrastructure-engineering.aws.ecs-fargate-services
name: ecs-fargate-services
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecs, fargate, task-definition, ecs-service, ecs-cluster, containers, awsvpc, task-role, execution-role, capacity-provider, fargate-spot, ecs-exec, service-auto-scaling, deployment-circuit-breaker, rolling-deployment, blue-green, alb-target-group, awslogs, firelens, graviton, arm64, ecs-anywhere]
level: practitioner
status: docs-checked
description: "Run containers on ECS Fargate: task definitions (roles, sizing, logging, secrets), services behind an ALB, capacity providers with Fargate Spot, circuit-breaker deployments and ECS Exec debugging."
sources: ["https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-capacity-providers.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-storage.html", "https://docs.aws.amazon.com/autoscaling/application/APIReference/API_PredefinedMetricSpecification.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECS on Fargate — task definitions and services that deploy safely

**Goal:** a stateless web/worker service on Fargate with correct IAM separation,
right-sized CPU/memory, logs and secrets wired in, a load balancer in front, Spot where
tolerable, and a deployment that rolls back on its own when the new task is unhealthy.

## 1. Task definition essentials
```json
{
  "family": "api",
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "512", "memory": "1024",
  "runtimePlatform": {"cpuArchitecture": "ARM64", "operatingSystemFamily": "LINUX"},
  "executionRoleArn": "arn:aws:iam::<ACCOUNT_ID>:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::<ACCOUNT_ID>:role/api-task-role",
  "containerDefinitions": [{
    "name": "api",
    "image": "<ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/api@sha256:...",
    "portMappings": [{"containerPort": 8080, "protocol": "tcp"}],
    "essential": true,
    "readonlyRootFilesystem": true,
    "secrets": [{"name": "DB_PASSWORD",
                 "valueFrom": "arn:aws:secretsmanager:<REGION>:<ACCOUNT_ID>:secret:db-creds:password::"}],
    "environment": [{"name": "PORT", "value": "8080"}],
    "logConfiguration": {"logDriver": "awslogs",
      "options": {"awslogs-group": "/ecs/api", "awslogs-region": "<REGION>",
                  "awslogs-stream-prefix": "api", "awslogs-create-group": "true"}},
    "healthCheck": {"command": ["CMD-SHELL", "curl -sf http://localhost:8080/health || exit 1"],
                    "interval": 15, "timeout": 5, "retries": 3, "startPeriod": 30},
    "ulimits": [{"name": "nofile", "softLimit": 65536, "hardLimit": 65536}]
  }]
}
```
- **Two roles, never one.** *Execution role* = what the ECS agent needs to start the
  task (pull from ECR, write logs, read the secret ARNs listed in `secrets`). *Task
  role* = what your code calls (S3, DynamoDB…). Code never needs ECR permissions.
- Fargate CPU/memory come in fixed pairs (0.25 vCPU with 512 MiB-2 GB up to 32 vCPU with 60, 120 or 244 GB; 8 vCPU and above need Linux platform 1.4.0+);
  an invalid pair fails registration. Task-level values are the bill; container-level
  `memoryReservation` is only for sharing within a task.
- Pin images by digest in production; `:latest` makes rollbacks meaningless.
- `ARM64` (Graviton) is supported for Linux tasks; the image architecture must match `cpuArchitecture`, so build multi-arch or arm64 images.
- Ephemeral storage is 20 GiB by default on platform 1.4.0+, expandable up to 200 GiB via `ephemeralStorage.sizeInGiB`; the pulled and unpacked image counts against it.
- `secrets` resolves at task start only; rotating a secret requires a new deployment
  (or the app re-reads from Secrets Manager itself).

## 2. Service
```bash
aws ecs create-service --cluster prod --service-name api --task-definition api:12 \
  --desired-count 3 --launch-type FARGATE --platform-version LATEST \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-a,subnet-b],securityGroups=[sg-api],assignPublicIp=DISABLED}" \
  --load-balancers targetGroupArn=arn:...:targetgroup/api/...,containerName=api,containerPort=8080 \
  --health-check-grace-period-seconds 60 \
  --deployment-configuration "minimumHealthyPercent=100,maximumPercent=200,deploymentCircuitBreaker={enable=true,rollback=true}" \
  --enable-execute-command
```
- Private subnets + `assignPublicIp=DISABLED` need NAT or VPC endpoints for
  `ecr.api`, `ecr.dkr`, `s3` (gateway, for image layers), `logs`, `secretsmanager`/`ssm`.
  The classic "CannotPullContainerError … i/o timeout" is a missing endpoint/NAT route.
- Target group must be `ip` target type (awsvpc tasks are IPs, not instances).
- **Deployment circuit breaker** marks the deployment failed after repeated task
  launch/health-check failures and (with `rollback=true`) redeploys the previous task
  definition — turn it on everywhere. Pair with CloudWatch alarms on the deployment
  (the CloudWatch alarm option) for metric-based rollback.
- Blue/green via CodeDeploy (`deploymentController=CODE_DEPLOY`) when you need traffic
  shifting and test listeners, or the native ECS blue/green deployment that the ECS guide now recommends; otherwise rolling is simpler. The circuit breaker only applies to the rolling (`ECS`) controller.

## 3. Capacity providers and Fargate Spot
```bash
aws ecs put-cluster-capacity-providers --cluster prod \
  --capacity-providers FARGATE FARGATE_SPOT \
  --default-capacity-provider-strategy capacityProvider=FARGATE,base=2,weight=1 capacityProvider=FARGATE_SPOT,weight=3
```
`base` is the minimum number of tasks on that provider (only one provider in a strategy may set it); `weight` splits the rest, and at least one provider needs a weight above zero (CLI/API default weight is 0). A Fargate Spot interruption sends a two-minute warning as an EventBridge task state change and a `SIGTERM` to the task (stop code `SpotInterruption`; `stopTimeout` up to 120 s applies). Fargate does not replace Spot capacity with On-Demand. A service created with
`--launch-type` can move to a capacity-provider strategy by forcing a new deployment
(`update-service --capacity-provider-strategy ... --force-new-deployment`).

## 4. Scaling
Application Auto Scaling target tracking on `ECSServiceAverageCPUUtilization`,
`ECSServiceAverageMemoryUtilization`, or `ALBRequestCountPerTarget`:
```bash
aws application-autoscaling register-scalable-target --service-namespace ecs \
  --resource-id service/prod/api --scalable-dimension ecs:service:DesiredCount --min-capacity 2 --max-capacity 20
aws application-autoscaling put-scaling-policy --service-namespace ecs --resource-id service/prod/api \
  --scalable-dimension ecs:service:DesiredCount --policy-name cpu60 --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration '{"TargetValue":60,"PredefinedMetricSpecification":{"PredefinedMetricType":"ECSServiceAverageCPUUtilization"},"ScaleOutCooldown":60,"ScaleInCooldown":300}'
```

## 5. Debugging with ECS Exec
Requires `--enable-execute-command` on the service (new tasks only; existing tasks cannot be enabled), the Session Manager plugin
locally, a task role with the SSM Session Manager permissions listed in the ECS Exec guide, and an `ssmmessages` VPC endpoint if tasks have no internet path.
```bash
aws ecs execute-command --cluster prod --task <TASK_ID> --container api --interactive --command "/bin/sh"
```
When it fails, check `describe-tasks` for `enableExecuteCommand: true` and the `ExecuteCommandAgent` managed agent with `lastStatus: RUNNING`. The usual causes are a missing `ssmmessages` endpoint, a task role without the SSM permissions, `readonlyRootFilesystem: true` (not supported with ECS Exec, because the SSM agent must write to the container file system), or a task that started before the flag was set.

## Gotchas
- `stopTimeout` default 30 s; graceful shutdown of a busy worker needs more (max 120 s).
- `STOPPED` task with `Essential container in task exited` — read `stoppedReason` and
  the container `exitCode`; `137` = OOM-killed, raise memory or fix the leak.
- Platform version `LATEST` resolves at deploy; ephemeral storage above the default and 8+ vCPU sizes need Linux platform 1.4.0 or later.
- Health check grace period only suppresses ALB-driven replacement; container
  `healthCheck` failures still stop the task — make `startPeriod` cover warm-up.
- The `awslogs` driver has a `mode` option: `blocking` can make the application unresponsive when CloudWatch is unreachable, `non-blocking` buffers in memory (`max-buffer-size`, default 10m) and drops logs when the buffer fills. Since 25 June 2025 the ECS default is `non-blocking`; set `mode: blocking` or the `defaultLogDriverMode` account setting to keep the old behaviour. Fargate supports the `awslogs`, `splunk` and `awsfirelens` log drivers.

## Verify
- [ ] `describe-services` shows `runningCount == desiredCount` and the latest deployment `COMPLETED`.
- [ ] Target group healthy-host count equals running tasks; ALB 5xx near zero during a deploy.
- [ ] Pushing a deliberately broken image triggers circuit-breaker rollback with no user-facing errors.
- [ ] `execute-command` opens a shell; task role has no ECR permissions; execution role has no app permissions (ECS Exec idle sessions time out after 20 minutes).
- [ ] Spot interruption (observe `SpotInterruption` stop reason) does not reduce healthy count below `base`.

## Checked
Checked 2026-10-24 against the ECS developer guide (Fargate task definition differences, task definition parameters, ephemeral storage, capacity providers, circuit breaker, ECS Exec) and the Application Auto Scaling API reference.
Confirmed: Fargate CPU/memory table up to 32 vCPU, ephemeral storage 20 GiB default and 200 GiB maximum, awsvpc requires ip target type, Spot two-minute warning/SIGTERM/stopTimeout up to 120, base and weight rules, force-new-deployment when moving to a capacity provider strategy, circuit breaker applies to the ECS rolling controller, ECS Exec requirements, awslogs default mode change on 25 June 2025, target tracking metric names ECSServiceAverageCPUUtilization, ECSServiceAverageMemoryUtilization and ALBRequestCountPerTarget (the latter needs a resource label).
Corrected: ECS Exec does not support a read-only root file system and Fargate does not support tmpfs, so the earlier tmpfs workaround was wrong; the awslogs default is now non-blocking; the maximum task size is 32 vCPU. Removed as unconfirmed: Graviton price difference, SSM permission wildcard.

Method: documentation only; no commands were run.
