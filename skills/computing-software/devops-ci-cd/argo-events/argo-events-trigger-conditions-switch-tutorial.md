---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-conditions-switch-tutorial
name: argo-events-trigger-conditions-switch-tutorial
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, conditions, switch, webhook, minio, group-1, multiple-dependencies]
level: practitioner
status: docs-checked
description: "Run different triggers for different EventSources in one Sensor with conditions, and restore the default wait-for-all behavior."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/tutorials/06-trigger-conditions.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger conditions switch tutorial

Whenever a Sensor defines multiple dependencies, it applies AND by default: it waits for every dependency before running triggers. `conditions` change that.

Scenario: a Webhook EventSource (port 12000) and a Minio EventSource (events `PUT` and `DELETE` on bucket `test`, Minio at `minio-service.argo-events:9000`). One workflow should run for the webhook event and another for the Minio event.

1. Apply the two EventSources from `examples/tutorials/06-trigger-conditions/` and confirm no errors.
2. Apply `sensor-01.yaml`. Each trigger template has a `conditions` boolean expression of dependency names; the matching trigger runs as soon as its expression resolves true.
3. POST `{"message":"this is my first webhook"}` to `/example`: a workflow `group-1-xxxx` prints that message.
4. Drop a file into the `test` bucket: workflow `group-2-xxxx` prints `test`.
5. Apply `sensor-02.yaml`, a trigger that waits for both dependencies (the behavior when `conditions` is undefined). Do both actions and the output is `this is my first webhook test`.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/tutorials/06-trigger-conditions.md. Confirmed: default AND behaviour, scenario, Minio PUT/DELETE on bucket test, sensor-01 and sensor-02 outputs. Removed or changed: the closing sentences about a FAQ answer and conditionsReset, which this page does not state. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
