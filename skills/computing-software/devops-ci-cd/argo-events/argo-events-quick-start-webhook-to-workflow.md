---
id: computing-software.devops-ci-cd.argo-events.argo-events-quick-start-webhook-to-workflow
name: argo-events-quick-start-webhook-to-workflow
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, getting-started, webhook, argo-workflows, install, sensor-rbac, port-forward]
level: intro
status: docs-checked
description: "Walk the official quick start: install Argo Workflows and Events, create the EventBus, a webhook EventSource, RBAC and a Sensor that triggers a Workflow."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/quick_start.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events quick start webhook to workflow

Goal: an HTTP POST triggers an Argo Workflow. Argo Workflows must be installed and its controller must watch Workflow objects in the `argo-events` namespace (cluster scope, or `--managed-namespace` set accordingly).

1. Install Workflows (example `ARGO_WORKFLOWS_VERSION=3.5.4`): create namespace `argo` and apply its `install.yaml`.
2. Install Events: `kubectl create namespace argo-events`, then apply `manifests/install.yaml` (or `install-validating-webhook.yaml` for the validating admission controller).
3. Create the EventBus: `kubectl apply -n argo-events -f .../examples/eventbus/native.yaml`.
4. Optionally lint copies of the example resources with `argo-events lint`.
5. Create the webhook EventSource: it runs an HTTP server on port 12000 with endpoint `example`; the controller creates a pod and a Service.
6. Create RBAC: `examples/rbac/sensor-rbac.yaml` (lets the Sensor trigger workflows) and `workflow-rbac.yaml` (lets workflows function).
7. Create the webhook Sensor from `examples/sensors/webhook.yaml`; the controller creates its pod.
8. Expose the EventSource: `kubectl -n argo-events port-forward svc/webhook-eventsource-svc 12000:12000` (or Ingress or an OpenShift Route).
9. `curl -d '{"message":"this is my first webhook"}' -H "Content-Type: application/json" -X POST http://localhost:12000/example`.
10. Verify: `kubectl -n argo-events get workflows | grep "webhook"`.

## Checked

2026-11-04. Confirmed against the Getting Started page: the Argo Workflows prerequisite and controller scope, the example `ARGO_WORKFLOWS_VERSION=3.5.4`, install commands and manifests, EventBus `native.yaml`, optional `argo-events lint`, webhook port 12000 and endpoint `example`, sensor and workflow RBAC files, the port-forward, curl and verification commands. Nothing removed.
Method: documentation only; no commands were run.
