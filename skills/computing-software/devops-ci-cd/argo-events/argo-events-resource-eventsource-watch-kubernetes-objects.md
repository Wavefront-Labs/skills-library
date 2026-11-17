---
id: computing-software.devops-ci-cd.argo-events.argo-events-resource-eventsource-watch-kubernetes-objects
name: argo-events-resource-eventsource-watch-kubernetes-objects
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, resource-eventsource, watch, label-selector, field-selector, add-update-delete, rbac]
level: practitioner
status: docs-checked
description: "Trigger on Kubernetes object changes with the resource EventSource, using label and field selectors in filter and a service account with list and watch."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventsources/setup/resource.md", "https://github.com/argoproj/argo-events/blob/master/docs/service-accounts.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events resource eventsource watch kubernetes objects

The Resource EventSource watches change notifications for Kubernetes objects. The CloudEvent `data` has `type` (ADD, UPDATE or DELETE), `body` (the object as JSON), `group`, `version` and `resource`.

Example: the shipped `resource.yaml` watches Argo Workflows labelled `app: my-workflow`; creating a Workflow with that label makes the Sensor (`examples/sensors/resource.yaml`) trigger a workflow.

The `filter` block sets list options for the watch via Kubernetes selectors:

```yaml
filter:
  labels:
    - key: app
      operation: "=="      # ==, !=, etc.; defaults to ==
      value: my-workflow
  fields:
    - key: metadata.name
      operation: ==        # ==, !=, <=, >= etc.
      value: my-workflow
```

Add more key-operation-value items as needed. These selectors apply only when the watch is established. To filter on annotations or other fields, use Sensor Data filters instead. The EventSource needs a service account with `list` and `watch` on the watched resource, set with `spec.template.serviceAccountName` (Service Accounts page).

## Checked

2026-11-04. Confirmed against the Resource EventSource page (`data` fields, example manifests, the `app: my-workflow` label, `filter.labels` and `filter.fields` with `operation` defaulting to `==`, the watch-time-only note about selectors and Sensor Data filters) and the Service Accounts page (a `resource` EventSource needs a service account with `list` and `watch`). Nothing removed.
Method: documentation only; no commands were run.
