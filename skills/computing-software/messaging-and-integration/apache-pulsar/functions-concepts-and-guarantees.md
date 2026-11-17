---
id: computing-software.messaging-and-integration.apache-pulsar.functions-concepts-and-guarantees
name: functions-concepts-and-guarantees
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [pulsar-functions, function-instance, function-worker, runtime, processing-guarantees, fqfn]
level: practitioner
status: docs-checked
description: "Understand Pulsar Functions: FQFN, instances, workers, thread/process/Kubernetes runtimes, processing guarantees and subscription type limits."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/functions-concepts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right runtime and delivery guarantee for a Pulsar Function.

Naming: each function has a Fully Qualified Function Name `tenant/namespace/name`, so the same function name can exist in different namespaces.

Function instance: a set of consumers on the input topics, an executor that invokes the function, and a producer for the output topic. A function may run several instances (number set in the configuration). Consumers use the FQFN as subscription name so instances load-balance according to the subscription type. Each function has a separate state store (keyed by FQFN) persisted in BookKeeper and queryable.

Function worker: monitors, orchestrates and runs functions in cluster mode. Request flow: REST server, function metadata manager (writes to the function metadata topic), schedule manager (writes the assignment topic), function runtime manager (reads assignments), and membership manager (a coordination topic with a failover subscription elects the leader worker that performs assignment).

Runtimes:
- Thread: each instance a thread in the worker JVM; Java functions only.
- Process: each instance a process on the worker machine.
- Kubernetes: workers submit a StatefulSet; each instance is a pod; labels can be added to StatefulSets and services.

Processing guarantees (set at create or `update`): at-most-once (needs `autoAck` true), at-least-once (the default when `--processing-guarantees` is omitted), effectively-once (at-least-once plus duplicate suppression), manual (the function acks with `context.getCurrentRecord().ack()`).
```bash
bin/pulsar-admin functions create --name my-effectively-once-function --processing-guarantees EFFECTIVELY_ONCE
bin/pulsar-admin functions update --processing-guarantees ATMOST_ONCE
```

Subscription types: Exclusive is not available to functions. To move from shared to key_shared use `--retain-key-ordering`. For Python and Go runtimes, output batching is set via `producerConfig` (for example `batchingConfig` with `batchingMaxPublishDelayMs`); without it batching stays on with a 10 ms maximum delay.

## Checked

2026-11-03. Confirmed against the pulsar-site page functions-concepts: FQFN, instance parts, worker request flow, the three runtimes, the guarantees table and default, Exclusive note, `--retain-key-ordering`, create/update commands and the Python and Go batching text. Removed the invented Verify step.

Method: documentation only; no commands were run.
