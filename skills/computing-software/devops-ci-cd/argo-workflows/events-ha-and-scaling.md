---
id: computing-software.devops-ci-cd.argo-workflows.events-ha-and-scaling
name: events-ha-and-scaling
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [event-worker-count, event-operation-queue-size, events-high-availability, argo-server-replicas, events-503]
level: advanced
status: docs-checked
description: "Scale Argo Server event handling with --event-async-dispatch, queue size, worker count and replicas, and avoid losing events."
sources: ["https://argo-workflows.readthedocs.io/en/latest/events/", "https://argo-workflows.readthedocs.io/en/latest/webhooks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Events endpoint capacity and HA
By default the events endpoint processes each event before it returns and can report failures to the caller. With `--event-async-dispatch` it instead queues the event and returns without waiting, so failures are not reported synchronously, and it returns 503 when the queue is full.

Loss and ordering: run at least two Argo Server replicas, otherwise events can be lost. Events are not always processed in the order received.

Capacity: with `--event-async-dispatch`, one Argo Server queues 16 events by default before the endpoint starts returning 503 errors. Tune it:
- Vertically, raise `--event-operation-queue-size` to absorb temporary bursts.
- Vertically, raise `--event-worker-count` for sustained event rates.
- Horizontally, run more Argo Server replicas; this helps sustained load and also gives high availability.

Clients should treat 503 as a signal to back off and retry. With async dispatch a success reply does not prove a Workflow was created. A malformed selector expression is logged by the Argo Server and recorded as a `WorkflowEventBindingError` Kubernetes Event on the WorkflowEventBinding.

Request bodies for signature-based webhooks are limited to 2MB.

## Checked
2026-11-08. Confirmed against the Argo Workflows Events page and Webhooks page: `--event-async-dispatch` behaviour, the default queue of 16 events, 503 when the queue is full, `--event-operation-queue-size`, `--event-worker-count`, the two-replica warning, no ordering guarantee, `WorkflowEventBindingError` and the 2MB webhook body limit. Corrected the default (was 64 and implied async by default) and the malformed-expression advice.
Method: documentation only; no commands were run.
