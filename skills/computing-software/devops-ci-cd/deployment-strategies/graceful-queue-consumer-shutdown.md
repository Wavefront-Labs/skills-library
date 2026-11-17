---
id: computing-software.devops-ci-cd.deployment-strategies.graceful-queue-consumer-shutdown
name: graceful-queue-consumer-shutdown
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, queue-consumer-shutdown, graceful-shutdown, zero-downtime]
level: advanced
status: docs-checked
description: "Deploy queue consumers and background workers without losing or duplicating work: stop fetching on SIGTERM, finish in-flight jobs, visibility timeouts and idempotency."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Graceful queue consumer shutdown

HTTP draining is handled by load balancers; workers need their own shutdown logic.

## On SIGTERM
1. **Stop fetching** new messages immediately.
2. Finish in-flight jobs within a budget shorter than `terminationGracePeriodSeconds`.
3. Ack/delete completed messages; for unfinished ones, **nack/requeue** (or let visibility timeout
   expire) so another worker picks them up.
4. Close connections, exit 0.

```python
stop = threading.Event()
signal.signal(signal.SIGTERM, lambda *_: stop.set())
while not stop.is_set():
    msgs = sqs.receive_message(QueueUrl=q, WaitTimeSeconds=10, MaxNumberOfMessages=5).get("Messages", [])
    for m in msgs:
        if stop.is_set():
            sqs.change_message_visibility(QueueUrl=q, ReceiptHandle=m["ReceiptHandle"], VisibilityTimeout=0)
            continue
        handle(m)
        sqs.delete_message(QueueUrl=q, ReceiptHandle=m["ReceiptHandle"])
```
Long polls (WaitTimeSeconds) delay noticing SIGTERM by up to that time: keep it below the grace period.

## Kubernetes settings
- `terminationGracePeriodSeconds` >= longest job budget + poll wait (e.g. 120).
- Long jobs (> minutes): checkpoint progress, or run them as Kubernetes Jobs rather than in rolling-updated workers.
- Check your framework's shutdown settings (worker shutdown timeout, acknowledge-after-processing) and align them with the grace period.

## Idempotency
At-least-once delivery means a job may run twice around deploys; make handlers idempotent
(dedupe keys, upserts).

## Verify
- [ ] Deploy during load: no messages in the DLQ, no duplicates beyond the idempotency guard, queue lag recovers.

## Checked

2026-10-28. Confirmed: Kubernetes pod termination (terminationGracePeriodSeconds, SIGTERM then force kill after the grace period) and SQS visibility timeout (ChangeMessageVisibility with VisibilityTimeout 0 immediately makes a message available to other consumers). Removed: Celery, Sidekiq and Kafka specifics (not in the sources).

Method: documentation only; no commands were run.
