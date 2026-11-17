---
id: computing-software.devops-ci-cd.tekton.tekton-events-and-cloudevents
name: tekton-events-and-cloudevents
category: computing-software
field: devops-ci-cd
product: tekton
tags: [events, cloudevents, taskrun, pipelinerun]
level: practitioner
status: docs-checked
description: "Understand Kubernetes events and CloudEvents emitted by Tekton TaskRuns, PipelineRuns and CustomRuns and how delivery and ordering behave."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kubernetes events: TaskRuns emit `Started` (first pickup by the reconciler after webhook validation; not proof a step is running), `Succeeded` (all steps incl. injected post-steps ran) and `Failed` (a step failed, timeout, cancellation or failed validation). PipelineRuns add `Running` (validation passed, execution begins) and `Succeeded` once all DAG-reachable tasks succeed.

CloudEvents are sent by the dedicated `tekton-events-controller`, which must be running, once a sink is configured (see the CloudEvents notification config). Event types follow `dev.tekton.event.<taskrun|pipelinerun|customrun>.<queued|started|running|unknown|successful|failed>.v1` (the docs table lists only started, running, successful and failed for customrun). `Queued` fires when the resource is created but not yet picked up. `unknown` is a condition change while running.

Config in `config-events`:

```yaml
data:
  formats: tektonv1
  sink: https://my-sink-url
```

Behaviour: events go out in a parallel routine with exponential back-off retries, so order is not guaranteed; an in-memory cache deduplicates, so a controller restart can send a few duplicates. Each attempt is recorded as a Kubernetes Event `CloudEventSent` or `CloudEventFailed`, visible with `kubectl describe taskrun NAME`. `status.cloudEvents` is deprecated and no longer populated.

## Checked

Checked 2026-11-08 against docs/events.md in tektoncd/pipeline (main), read in full. Confirmed TaskRun and PipelineRun reasons, the tekton-events-controller, event type table, Queued semantics, config-events format, retry and dedup behaviour, CloudEventSent and CloudEventFailed, and the status.cloudEvents deprecation. Corrected the customrun event list (the table has no queued or unknown for customrun).

Method: documentation only; no commands were run.
