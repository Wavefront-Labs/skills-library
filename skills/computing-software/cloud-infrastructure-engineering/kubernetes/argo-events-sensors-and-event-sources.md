---
id: computing-software.cloud-infrastructure-engineering.kubernetes.argo-events-sensors-and-event-sources
name: argo-events-sensors-and-event-sources
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, platform-engineering, argo-events, event-driven, argo-workflows, automation]
level: practitioner
status: docs-checked
description: "Wire external events (webhooks, Git pushes, queues, schedules) to Kubernetes actions with Argo Events EventBus, EventSources and Sensors with triggers and RBAC."
sources: ["https://argoproj.github.io/argo-events/", "https://argoproj.github.io/argo-events/eventbus/jetstream/", "https://argoproj.github.io/argo-events/eventsources/webhook-authentication/", "https://argoproj.github.io/argo-events/sensors/more-about-sensors-and-triggers/", "https://argoproj.github.io/argo-events/service-accounts/", "https://argoproj.github.io/argo-events/sensors/triggers/argo-workflow/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo Events

Components: an **EventBus** (NATS JetStream) transports events; **EventSources** receive them
(webhook, GitHub, GitLab, Kafka, SQS, SNS, calendar, resource watches); **Sensors** filter events
and fire **triggers** (create a Workflow or any Kubernetes object, HTTP call, Kafka message).

## Minimal webhook to Workflow
```yaml
apiVersion: argoproj.io/v1alpha1
kind: EventBus
metadata: {name: default, namespace: argo-events}
spec:
  jetstream: {version: latest}   # example only: pin a version listed in argo-events-controller-config
---
apiVersion: argoproj.io/v1alpha1
kind: EventSource
metadata: {name: webhook, namespace: argo-events}
spec:
  service: {ports: [{port: 12000, targetPort: 12000}]}
  webhook:
    deploy: {port: "12000", endpoint: /deploy, method: POST}
---
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata: {name: deploy, namespace: argo-events}
spec:
  template: {serviceAccountName: argo-events-sensor}
  dependencies:
  - name: dep
    eventSourceName: webhook
    eventName: deploy
    filters:
      data: [{path: body.env, type: string, value: [staging]}]
  triggers:
  - template:
      name: run-workflow
      argoWorkflow:
        operation: submit
        source:
          resource:
            apiVersion: argoproj.io/v1alpha1
            kind: Workflow
            metadata: {generateName: deploy-}
            spec: {workflowTemplateRef: {name: deploy-pipeline}}
        parameters:
        - {src: {dependencyName: dep, dataKey: body.version}, dest: spec.arguments.parameters.0.value}
```
## Operations
- Expose webhook EventSources through an Ingress, and set `authSecret` (a secret key selector
  holding a bearer token) on the webhook EventSource, or serve it over TLS with
  `serverCertSecret` and `serverKeySecret`.
- Triggers are not retried by default. Add `retryStrategy` (`steps`, optionally `duration`
  and `factor`) to a trigger, and a `dlqTrigger` (with `atLeastOnce: true` on both triggers)
  to act after the retries are exhausted.
- A Sensor needs `spec.template.serviceAccountName` only for `k8s` and `argoWorkflow`
  triggers; submitting a Workflow needs `create` and `list` on `workflows.argoproj.io`.
- Watch sensor and eventsource pod logs for filter mismatches.

## Verify
```bash
curl -X POST -d '{"env":"staging","version":"1.4.2"}' https://events.example.com/deploy
kubectl get workflows -n argo-events
```
A new Workflow appears with the version parameter.

## Checked

Documentation release: Argo Events docs on the project site and repo (argo-events repo docs/, commit 2026-10-24).
Confirmed: EventBus JetStream spec (and the warning not to use `version: latest` in a real deployment; `jetstreamExotic` exists for an external cluster); webhook EventSource fields (`service.ports`, per-name `port`, `endpoint`, `method`) and `authSecret`; data filter `path`/`type`/`value` applied under `data` (so `body.env`); `argoWorkflow` trigger `operation: submit` with `workflowTemplateRef`; Sensor `spec.template.serviceAccountName` and the `create`/`list` permission; trigger retry defaults and `retryStrategy`, `dlqTrigger`, `atLeastOnce`; supported event sources and trigger types.
Removed: the unsourced "shared secret header / GitHub webhook secret" advice, replaced by the documented `authSecret`.

Method: documentation only; no commands were run.
