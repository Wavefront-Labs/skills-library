---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.web-queue-worker
name: web-queue-worker
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-styles, web-queue-worker, background-jobs, worker-service, job-queue, paas, keda]
level: practitioner
status: docs-checked
description: "Split a web front end from background workers via a queue: what goes async, idempotent jobs, scaling each side on its own signal, job status, and avoiding monolithic workers."
sources: ["https://learn.microsoft.com/azure/architecture/guide/architecture-styles/web-queue-worker", "https://learn.microsoft.com/azure/architecture/best-practices/background-jobs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web-queue-worker

A web front end handles client requests; a worker does resource-intensive tasks, long-running workflows or batch
jobs. The two communicate through a message queue. Both components are stateless (session state can live in a
distributed cache). The worker is optional if the application has no long-running operations.

## Steps
1. **Classify work**: simple reads and writes can be handled by the web front end directly; reserve workers for
   resource-intensive tasks or long-running workflows.
2. **Make every job idempotent.** Queues deliver at least once, schedulers can overlap, and restarts can replay
   partially completed work, so the same input must give the same outcome when a job runs more than once.
3. **Queue**: the Microsoft reference architecture uses Azure Queue Storage or Azure Service Bus, depending on
   messaging requirements.
4. **Scale workers on queue depth, not CPU alone.** Background work scales on different signals from the UI, so host
   it separately (for example in separate App Service plans) and let each side scale independently. Container Apps
   and AKS use KEDA for queue-length scaling. More workers do not help if the queue, database or downstream API is
   the bottleneck: scale those too.
5. **Status**: if a caller waits for a result, return a status endpoint URL on submit and let the caller poll
   (Asynchronous Request-Reply), or use a reply queue, or write progress to shared storage the caller monitors.
6. **Scheduling**: use the platform scheduler or timer triggers. Several scheduler instances can start several
   copies of a task, so make scheduled tasks idempotent; for single-instance tasks, Functions timer triggers use a
   distributed lock, and Kubernetes CronJob has `concurrencyPolicy: Forbid`.

## Gotchas
- Without careful design, front end and worker grow into large monolithic components that are hard to maintain.
- Shared data schemas or code modules between front end and worker create hidden dependencies.
- The front end can fail after writing to the database but before sending the queue message, so the worker never
  runs. Use the Transactional Outbox pattern.
- Dead-lettered messages are work that did not complete: alert on dead-letter queue depth and message age.
- Missed schedules raise no error because nothing ran: compare actual run times with the expected schedule.

## Verify
- [ ] Worker crash mid-job: job retried, no duplicate side effects.
- [ ] Web latency unaffected by a burst of queued jobs.

## Checked
2026-11-08. Confirmed against the Azure Architecture Center pages Web-Queue-Worker architecture style and Background
jobs best practices: component roles, stateless front end and worker, optional worker, Queue Storage or Service Bus,
separate App Service plans, queue-depth scaling and KEDA, idempotency, status endpoint/reply queue/shared storage,
timer-trigger distributed lock, CronJob concurrencyPolicy Forbid, outbox, monolithic-component and hidden-dependency
challenges, dead-letter and missed-schedule alerts. Removed as not stated on those pages: job message shape guidance,
named job frameworks (Celery, Sidekiq, BullMQ, Hangfire) and the Redis durability remark, ECS target tracking, the
shared-database long-transaction and message-versioning gotchas, and the "simpler than microservices" claim.
Method: documentation only; no commands were run.
