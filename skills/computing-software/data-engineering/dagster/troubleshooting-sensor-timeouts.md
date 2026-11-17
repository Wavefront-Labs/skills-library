---
id: computing-software.data-engineering.dagster.troubleshooting-sensor-timeouts
name: troubleshooting-sensor-timeouts
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, sensor-timeout, dagster-sensor-grpc-timeout-seconds, default-sensor-timeout, dagster-grpc-max-workers, hybrid]
level: advanced
status: docs-checked
description: "Fix Dagster sensors that exceed the 60 second timeout: profile, split with cursors, move to schedules, then raise the timeout."
sources:
  - https://docs.dagster.io/deployment/troubleshooting/sensor-timeouts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting sensor timeouts

Default timeout is 60 seconds. Work down these steps; raising the timeout is the last resort.

1. Find the cause with `py-spy` (hanging external API calls are a correct timeout; consider shortening the timeout for resilience).
2. Break evaluation into steps with sensor cursors.
3. If evaluation needs more than about 3 minutes, use a schedule that sends run requests; sensors suit frequent evaluation of small data.
4. Increase the timeout.

## OSS
Env var `DAGSTER_SENSOR_GRPC_TIMEOUT_SECONDS`. Code server workers: `DAGSTER_GRPC_MAX_WORKERS`. Daemon workers in `dagster.yaml`:

```yaml
sensors:
  use_threads: true
  num_workers: 8
```

## Dagster+
Deployment setting `default_sensor_timeout` (seconds), affecting all sensors including future ones.

## Hybrid
Requests flow host cloud, agent, code server; bottlenecks are request concurrency, CPU, memory. Throughput logging needs dagster >= 1.6.4 on both agent and code server: Helm `agentMetrics.enabled: true` and `codeServerMetrics.enabled: true`; ECS `AgentMetricsEnabled` and `CodeServerMetricsEnabled`; Docker unsupported. Watch `num_running_requests`, `num_queued_requests`, `max_concurrent_requests`. Raise with `DAGSTER_CLOUD_AGENT_MAX_THREADPOOL_WORKERS` (agent) or `DAGSTER_GRPC_MAX_WORKERS` (code server). On ECS the CloudFormation template has `AgentMemory`, `AgentCpu`, `CodeServerMemory`, `CodeServerCPU`.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/deployment/troubleshooting/sensor-timeouts

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
