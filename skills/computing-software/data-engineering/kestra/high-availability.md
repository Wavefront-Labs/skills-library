---
id: computing-software.data-engineering.kestra.high-availability
name: high-availability
category: computing-software
field: data-engineering
product: kestra
tags: [high-availability, replicas, queue-backends, liveness, heartbeat, load-balancer]
level: advanced
status: docs-checked
description: "Run Kestra highly available: independent server roles, shared object storage, queue backend choice, replica counts, health checks and liveness settings."
sources:
  - https://kestra.io/docs/administrator-guide/high-availability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements:

- Run each role (Executor, Scheduler, Worker Controller, Worker, Webserver, Indexer) as its own scaled process, e.g. `kestra server executor`.
- Use shared object storage (GCS, S3, Azure Blob); local filesystem is unsuitable.
- Load balancer in front of the Webserver replicas; health checks at `/health` on port `8081` or `/ping` on port `8080`.
- Open the Worker Controller gRPC port (`50051` default) to Workers, which use one outbound connection and never touch the queue or database.
- With a database queue, run PostgreSQL in HA mode.

Queue backend affects throughput and latency, not fault tolerance: database (PostgreSQL or MySQL) is simplest; AMQP or Redis lower latency; Kafka highest throughput.

Replicas: Executor 2 to 3; Scheduler 2 to 3 (trigger evaluation splits across virtual nodes, 16 by default via `kestra.scheduler.vnodes`); Webserver at least 2; Workers are the main scaling target.

Liveness defaults: heartbeat every 3 seconds, Executor checks every 10 seconds, a Worker silent beyond 1 minute is marked failed. With `worker-task-restart-strategy: NEVER`, its in-flight jobs are not re-dispatched.

```yaml
kestra:
  server:
    liveness:
      enabled: true
      interval: 10s
      timeout: 1m
      heartbeat-interval: 3s
```

## Checked

2026-11-04. Confirmed against the Kestra high availability page: server roles and their kestra server commands, shared object storage requirement, load balancer health checks on /health port 8081 or /ping port 8080, gRPC port 50051, PostgreSQL HA for database queues, queue backend guidance, replica counts, 16 virtual nodes via kestra.scheduler.vnodes, liveness defaults of 3 seconds, 10 seconds and 1 minute, worker-task-restart-strategy NEVER. Nothing removed.

Method: documentation only; no commands were run.
