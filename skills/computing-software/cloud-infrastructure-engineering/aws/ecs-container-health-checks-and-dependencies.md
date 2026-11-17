---
id: computing-software.cloud-infrastructure-engineering.aws.ecs-container-health-checks-and-dependencies
name: ecs-container-health-checks-and-dependencies
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecs, container-health-check, depends-on, start-period, sidecar-ordering, stop-timeout]
level: practitioner
status: docs-checked
description: "Configure ECS container health checks and startup/shutdown ordering: healthCheck command, startPeriod, dependsOn conditions for sidecars, stopTimeout, and ELB vs container health."
sources: ["https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/healthcheck.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECS container health checks and dependencies

## 1. Container health check
```json
"healthCheck": {
  "command": ["CMD-SHELL", "curl -fsS http://localhost:8080/health || exit 1"],
  "interval": 15, "timeout": 5, "retries": 3, "startPeriod": 60
}
```
- `command`: `CMD` (exec form, no shell) or `CMD-SHELL`. The binary must exist in the
  image: distroless/minimal images often lack `curl`/`wget`; ship a tiny health binary or
  use the app's own CLI (`["CMD", "/app/healthcheck"]`).
- `interval` 5-300 s (default 30), `timeout` 2-60 s (default 5), `retries` 1-10
  (default 3), `startPeriod` 0-300 s (disabled by default): failed checks during it do not count toward `retries`; a success during it makes the container healthy.
- Container health checks need ECS agent 1.17.0 or later, and on Fargate Linux platform version 1.1.0 or later. ECS ignores Docker `HEALTHCHECK` instructions baked into the image; define the check in the task definition.
- Status: `HEALTHY`, `UNHEALTHY`, `UNKNOWN`. Only **essential** containers that have a health check command count toward task health: any UNHEALTHY gives UNHEALTHY, else any UNKNOWN gives UNKNOWN, else HEALTHY.
- The check runs inside the container against localhost; an exit code of 0 is success.

## 2. Container health vs load balancer health
- ELB health checks decide whether the target receives traffic. For services behind a load balancer, `healthCheckGracePeriodSeconds` sets how long ECS ignores ELB failures after a task starts.
- Container health checks are internal (no network path needed) and catch hung processes
  that still accept TCP.
- Use both: ELB checks the user-facing path; container check verifies the process. Keep
  thresholds consistent so they do not fight (container check killing tasks the ALB
  considers fine, or the reverse).

## 3. Startup ordering with dependsOn
```json
"containerDefinitions": [
  {"name": "envoy", "essential": true, "healthCheck": {...}},
  {"name": "migrate", "essential": false, "command": ["./migrate"]},
  {"name": "app", "essential": true,
   "dependsOn": [
     {"containerName": "envoy", "condition": "HEALTHY"},
     {"containerName": "migrate", "condition": "SUCCESS"}]}]
```
Conditions:
- `START`: dependency has started.
- `COMPLETE`: dependency ran to completion (any exit code), for init containers; cannot be set on an essential container.
- `SUCCESS`: completed with exit code 0; cannot be set on an essential container.
- `HEALTHY`: dependency passed its health check (needs a healthCheck); evaluated only at task startup.
`startTimeout` (seconds, set on the container being waited for) bounds how long ECS waits to resolve its dependency; the maximum is 120. If a dependency is not met or times out, ECS does not progress the dependent containers.
`dependsOn` needs Fargate Linux platform version 1.3.0 or later.
Shutdown happens in reverse dependency order: app stops before envoy, so in-flight
requests can drain through the proxy.

## 4. Graceful shutdown
- ECS sends SIGTERM, waits `stopTimeout` (default 30 s, max 120 s; Linux platform 1.3.0 or later on Fargate; on EC2 the agent setting
  `ECS_CONTAINER_STOP_TIMEOUT` defaults to 30s), then SIGKILL.
- The app must handle SIGTERM: stop accepting, finish requests, exit. PID 1 issues: shell
  form `CMD` wraps the app in `sh` which does not forward signals; use exec form or
  `initProcessEnabled: true` (adds tini) in `linuxParameters`.
- Align `stopTimeout` with the target group's deregistration delay.

## Gotchas
- A health check that calls a downstream dependency makes every task unhealthy when the
  dependency blips, causing mass replacement. Check only local health.
- `essential: false` on the main app container means its crash does not stop the task.
- The container health status is visible in `describe-tasks` (`healthStatus`), not in logs unless
  your command logs.
- If the agent disconnects, container health is not changed to UNHEALTHY; the last reported status stands.

## Verify
- [ ] `describe-tasks` shows `healthStatus: HEALTHY` for tasks and containers after startPeriod.
- [ ] Killing the app process inside a task (ECS Exec) leads to UNHEALTHY and replacement.
- [ ] Deploys drain without 5xx: app handles SIGTERM within stopTimeout.

## Checked
Checked 2026-10-24 against the ECS developer guide (task definition parameters and container health checks pages).
Confirmed: interval/timeout/retries/startPeriod ranges and defaults, CMD vs CMD-SHELL, task health rules, dependsOn conditions and restrictions, startTimeout and stopTimeout maximum of 120 s, platform version gates, initProcessEnabled, EC2 agent stop timeout default.
Corrected: the old text gave startTimeout a Fargate default of 3 minutes and maximum of 10 minutes; the documented maximum is 120 seconds. Removed: unreferenced ALB deregistration default and the claim that an UNHEALTHY container always triggers replacement.

Method: documentation only; no commands were run.
