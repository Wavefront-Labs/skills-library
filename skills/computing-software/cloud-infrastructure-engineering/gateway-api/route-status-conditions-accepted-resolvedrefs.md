---
id: computing-software.cloud-infrastructure-engineering.gateway-api.route-status-conditions-accepted-resolvedrefs
name: route-status-conditions-accepted-resolvedrefs
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [status, conditions, accepted, resolvedrefs, troubleshooting, observedgeneration]
level: practitioner
status: docs-checked
description: "Read Gateway API status conditions: Accepted, Programmed, ResolvedRefs and observedGeneration, status scope rules, and why status is the first thing to check when traffic fails."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/troubleshooting.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/api-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When troubleshooting Gateway API objects, check `status.conditions` first. Each condition has a type, a boolean-like status, a reason and a human-readable message.

Common conditions:

- `Accepted`: True when the object is semantically and syntactically valid, will produce configuration in the data plane, and has been accepted by a controller.
- `Programmed`: True when the object's config has been fully parsed and successfully sent to a data plane; it will be ready "soon", defined per implementation.
- `ResolvedRefs`: True when all references to other objects are valid: the objects exist and each is valid for the field where it is used.
- `observedGeneration` (required by Gateway API, optional field) is the `metadata.generation` at the time status was written. If a condition's value does not match `metadata.generation`, the status is out of date: a controller fault, or the object fell out of the implementation's scope.

The Gateway object also has a conditions array per listener.

Scope: an implementation must not update status of an object it cannot trace to a GatewayClass it owns. So a Route whose `parentRef` does not point to a valid parent gets no status at all. For any in-scope object expect a status update on every change, even if only `observedGeneration`.

Ways to read status: `kubectl get -o yaml`, `kubectl describe` (readable, but can struggle with CustomResourceDefinitions and lists), or `gwctl` from the Gateway API subproject.

## Checked

2026-11-04. Confirmed on the Gateway API troubleshooting and status page (troubleshooting.md): condition fields, Accepted, Programmed, ResolvedRefs, observedGeneration, per-listener conditions, scope rule, tools. Removed the per-parent `status.parents[]` detail, ReferenceGrant and attachedRoutes remarks, the numbered debug order and the example reason strings (not on the pages).

Method: documentation only; no commands were run.
