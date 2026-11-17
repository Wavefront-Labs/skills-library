---
id: computing-software.cloud-infrastructure-engineering.gateway-api.status-scope-and-missing-parentref-status
name: status-scope-and-missing-parentref-status
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [status, parentrefs, troubleshooting, controller, routes, no-status]
level: practitioner
status: docs-checked
description: "Why a Route may show no status at all: status is written only by a controller that owns the parent, so a wrong parentRef gives no status."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/troubleshooting.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/api-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A common surprise: a Route has an empty `status.parents` even though it is applied. The docs explain the scope.

- Several implementations can run in one cluster, so an implementation may update status only for objects in its scope. If it cannot establish a chain of ownership from an object to a GatewayClass it owns, the object is out of scope and MUST NOT have its status updated by it.
- A Route whose `parentRef` does not point to a valid parent therefore gets no status at all: the implementation cannot tell you that you pointed at the wrong Gateway because it cannot know whether that parentRef is its responsibility.
- Absence of status is thus a hint of a bad or foreign parentRef rather than of success. For an in-scope object you should always see a status update on any change, even if only `observedGeneration` changes.

Checks:

1. Read the full status: `kubectl get -o yaml` (conditions do not summarise in plain `kubectl get`), `kubectl describe`, or `gwctl` from the Gateway API subproject. Always check `status.conditions` first.
2. Compare the Gateway namespace and name to `parentRefs`; `namespace` may be omitted only if the Route and Gateway share a namespace.
3. If `sectionName` is set, it must equal the `name` of a real listener; otherwise the set of relevant listeners is empty and that parentRef is ignored.
4. Compare `observedGeneration` on each condition with `metadata.generation`; a mismatch means stale status (a controller fault, or the object fell out of the implementation's scope).

The shared condition types are `Accepted` (valid and accepted by a controller), `Programmed` (configuration sent to the data plane) and `ResolvedRefs` (all references valid). A Route attached to several Gateways has one entry per parent in `status.parents`, written by the controller that owns that Gateway. Do not read a populated status from one controller as proof another parent works.

## Checked

2026-11-08. Read in full (GitHub markdown): the Troubleshooting and Status page and the API overview; the traffic matching page was read for the sectionName rule. Confirmed: scope and ownership rule, no status for an invalid parentRef, observedGeneration staleness check, the three shared condition types, kubectl and gwctl options, namespace default for parentRefs. Removed: the claim that a sectionName or port mismatch usually yields Accepted False (the docs say a non-matching sectionName leaves no relevant listener and the parentRef is ignored) and the `controllerName` field name (not on these pages).

Method: documentation only; no commands were run.
