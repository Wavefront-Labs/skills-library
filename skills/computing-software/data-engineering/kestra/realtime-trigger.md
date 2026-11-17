---
id: computing-software.data-engineering.kestra.realtime-trigger
name: realtime-trigger
category: computing-software
field: data-engineering
product: kestra
tags: [realtime, event-driven, sqs, kafka, failover, termination-grace-period]
level: advanced
status: docs-checked
description: "Kestra realtime triggers: one execution per event with millisecond latency, how they differ from polling, supported sources, and worker failover timing."
sources:
  - https://kestra.io/docs/workflow-components/triggers/realtime-trigger
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A realtime trigger runs as a dedicated listener thread on a worker and starts exactly one execution per event, with millisecond latency. Each event is stored in its raw format (raw event payload and metadata).

Versus polling: a polling trigger micro-batches all events received within the poll interval into a file in internal storage (latency seconds or minutes, output is the file URI); a realtime trigger processes each event immediately as it arrives (latency milliseconds). Realtime triggers are stateless, so they suit orchestrating workflows and microservices in response to events, not continuous stateful stream processing.

Sources include Kafka, Pulsar, AMQP, MQTT, AWS SQS, Google Pub/Sub, Azure Event Hubs, NATS, Redis lists, and row changes in Postgres, MySQL or SQL Server.

```yaml
triggers:
  - id: realtime_trigger
    type: io.kestra.plugin.aws.sqs.RealtimeTrigger
    region: eu-north-1
    accessKeyId: "{{ secret('AWS_ACCESS_KEY_ID')}}"
    secretKeyId: "{{ secret('AWS_SECRET_ACCESS_KEY') }}"
    queueUrl: https://sqs.eu-north-1.amazonaws.com/123456789/MyQueue
```

Failover: each listener runs on one specific worker. If that worker stops, Kestra's liveness mechanism re-emits the trigger so another available worker can pick it up.

- Graceful shutdown (for example `docker stop`, rolling deploy): the Executor waits for `kestra.server.terminationGracePeriod` (default `PT5M`) before reassigning, to prevent duplicate processing when the worker is expected back shortly.
- Abrupt failure (no heartbeat): the Executor detects the missing heartbeat within `kestra.server.liveness.timeout` and reassigns without waiting for the grace period.

Events stay in the source system during failover and are consumed after the listener restarts.

## Checked

2026-11-04. Confirmed against "React Instantly to Kafka, SQS, and MQTT Events" (triggers/realtime-trigger): dedicated listener thread, one execution per event, supported sources, SQS example, failover timing and defaults, polling comparison table, stateless note. Reworded the raw-format line (the page does not say payload sits in a specific variable).
Method: documentation only; no commands were run.
