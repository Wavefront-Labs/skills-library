---
id: computing-software.cloud-infrastructure-engineering.aws.ecs-task-definition-sizing-and-essential-containers
name: ecs-task-definition-sizing-and-essential-containers
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecs, container-definition, essential-container, task-definition, fargate]
level: practitioner
status: docs-checked
description: "Write ECS task definitions with valid task CPU/memory, container memory limits and reservations, essential flags, dependsOn ordering and stop timeouts."
sources: ["https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task size, container definitions and essential containers

## 1. Task-level size (required on Fargate)
Valid Fargate pairs: 256 CPU with 512 MiB, 1 GB or 2 GB; 512 with 1-4 GB; 1024 with 2-8 GB;
2048 with 4-16 GB; 4096 with 8-30 GB; 8192 with 16-60 GB (4 GB steps); 16384 with 32-120 GB (8 GB steps); 32768 with 60, 120 or 244 GB. The 8192 and larger sizes need Linux platform version 1.4.0 or later. Invalid pairs fail registration.

## 2. Container-level settings
```json
{"family":"api","requiresCompatibilities":["FARGATE"],"networkMode":"awsvpc","cpu":"1024","memory":"2048",
 "containerDefinitions":[
  {"name":"app","image":"<ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/api:1.4.2","essential":true,
   "cpu":768,"memoryReservation":1024,"memory":1792,
   "portMappings":[{"name":"http","containerPort":8080}],
   "dependsOn":[{"containerName":"migrate","condition":"SUCCESS"},{"containerName":"envoy","condition":"HEALTHY"}],
   "stopTimeout":60,"linuxParameters":{"initProcessEnabled":true},
   "logConfiguration":{"logDriver":"awslogs","options":{"awslogs-group":"/ecs/api","awslogs-region":"<REGION>","awslogs-stream-prefix":"app"}}},
  {"name":"migrate","image":"...","essential":false,"command":["./migrate"]},
  {"name":"envoy","image":"...","essential":true,
   "healthCheck":{"command":["CMD-SHELL","curl -sf localhost:9901/ready"],"interval":10,"retries":3,"startPeriod":20}}]}
```
| Field | Meaning |
|---|---|
| `memory` | hard limit: container is OOM-killed above it |
| `memoryReservation` | soft limit in MiB; the container can use more, up to `memory` (if set) or available memory. On EC2 the reservation is what is subtracted from the instance's free memory |
| `cpu` | CPU units share (1024 = 1 vCPU) |
| `essential` | if this container stops, the whole task stops |
| `dependsOn` | `START`, `COMPLETE`, `SUCCESS` (exit 0), `HEALTHY` |
| `stopTimeout` | seconds before the container is forcibly killed (default 30, max 120; Linux platform 1.3.0+) |

## 3. Patterns
- Init/migration container: `essential: false` + app `dependsOn ... SUCCESS`.
- Sidecars (log router, proxy) usually `essential: true` so a dead proxy fails the task visibly.
- `initProcessEnabled` runs an init process in the container that forwards signals and reaps processes.

## Verify
- [ ] `aws ecs register-task-definition --cli-input-json file://td.json` succeeds.
- [ ] Stopped tasks show the expected `stoppedReason` when a non-essential container exits (task keeps running).

## Checked
Checked 2026-10-24 against the ECS developer guide (Fargate task CPU and memory table, task definition parameters).
Confirmed: full CPU/memory table to 32 vCPU, platform 1.4.0 requirement for 8 vCPU and above, memory vs memoryReservation semantics, dependsOn conditions, stopTimeout default 30 and maximum 120, initProcessEnabled.
Corrected: the earlier text capped Fargate at 16 vCPU / 120 GB; the documented maximum is 32 vCPU. Removed the unreferenced claim that at least one container must be essential.

Method: documentation only; no commands were run.
