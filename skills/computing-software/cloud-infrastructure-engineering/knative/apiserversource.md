---
id: computing-software.cloud-infrastructure-engineering.knative.apiserversource
name: apiserversource
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [apiserversource, kubernetes-events, resources-parameter, namespaceselector, serviceaccountname]
level: practitioner
status: docs-checked
description: "Turn Kubernetes API lifecycle events into CloudEvents with resources, mode, owner and namespace selectors."
sources:
  - https://knative.dev/docs/eventing/sources/apiserversource/
  - https://knative.dev/docs/eventing/sources/apiserversource/reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: forward changes to Kubernetes objects to a sink as CloudEvents.

The ApiServerSource listens for events emitted by the Kubernetes API server, such as pod creation and deployment updates, and forwards them as CloudEvents. It ships with Knative Eventing, and you may create multiple instances.

Spec fields:
- `spec.resources` (required): list of `apiVersion` and `kind` pairs to watch, each with an optional `selector` using `matchLabels` or `matchExpressions` (operators `In`, `NotIn`, `Exists`, `DoesNotExist`; requirements are ANDed).
- `spec.mode`: `Reference` (default) sends a `dataref` event carrying only a reference to the object; `Resource` puts the full resource in the payload.
- `spec.owner`: only track resources owned by a given type.
- `spec.serviceAccountName`: account the source runs as; defaults to `default`.
- `spec.namespaceSelector`: label selector to track several namespaces; if unset, only the source's own namespace is tracked.
- `spec.sink` (required) and `spec.ceOverrides`.

```yaml
spec:
  mode: Resource
  serviceAccountName: events-sa
  resources:
    - apiVersion: v1
      kind: Pod
    - apiVersion: apps/v1
      kind: Deployment
  sink:
    ref:
      apiVersion: eventing.knative.dev/v1
      kind: Broker
      name: default
```

This example receives events for all Pods and Deployments in the namespace.

## Checked

2026-11-04. Confirmed against the ApiServerSource overview and reference pages (knative/docs source): spec fields and their required/optional status, `mode` values and the `Reference` default, `serviceAccountName` default `default`, `namespaceSelector` default behaviour, selector operators (`In`, `NotIn`, `Exists`, `DoesNotExist`), ANDed requirements, and the Pod/Deployment example. Added the reference page to sources. Nothing removed.

Method: documentation only; no commands were run.
