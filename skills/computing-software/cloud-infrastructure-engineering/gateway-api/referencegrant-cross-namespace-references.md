---
id: computing-software.cloud-infrastructure-engineering.gateway-api.referencegrant-cross-namespace-references
name: referencegrant-cross-namespace-references
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [referencegrant, cross-namespace, security, secret, backendref, from-to]
level: practitioner
status: docs-checked
description: "Allow references across namespaces with ReferenceGrant: from and to entries, one namespace per from, additive grants, and no existence leakage."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/referencegrant.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/security.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default a Gateway API resource may only reference objects in its own namespace. A `ReferenceGrant` created in the **target** namespace lets resources in another namespace refer to specific objects there.

Structure:

- `spec.from`: list of entries, each with `group`, `kind` and a **single** `namespace` of the referring resource.
- `spec.to`: list of entries, each with `group` and `kind` (and optionally `name`). No namespace is needed, because a grant only allows references to resources in its own namespace. The security page says to specify `group`, `kind` and `name`, and not to leave the optional `name` unspecified without a very good reason, since that grants a blanket.

Example use cases: a Route forwarding traffic to a backend (usually a Service) in another namespace, as in the reference example (HTTPRoute in `foo`, ReferenceGrant and Service in `bar`); a Gateway referring to a Secret in another namespace.

Rules to remember:

- Each ReferenceGrant has a single `from` and `to` section; more trust relationships need more grants. Grants are purely additive and stack, so they cannot conflict; there is no deny.
- The owner of the referenced object creates the grant, which is the security model: the referenced namespace opts in.
- `from` has no resource names, because they give little protection, and allows a single namespace per entry (a selector would encourage insecure configuration).
- Implementations must not reveal whether a target object exists when a reference is not permitted, so the status does not leak information across namespaces.
- ReferenceGrant is a Core conformance requirement for cross-namespace references from Gateway, GRPCRoute, HTTPRoute, TLSRoute, TCPRoute and UDPRoute. Cross-namespace Route to Gateway binding is separate and uses `allowedRoutes` on the listener.

Without a ReferenceGrant a cross-namespace reference is invalid. Implementations must watch grants and recalculate validity after each change or deletion, so deleting the grant revokes access.

The reference page recommends using ReferenceGrants with caution, with admins applying validations and limits (the security page shows ValidatingAdmissionPolicy examples). Its API group may change in future.

## Checked

2026-11-08. Read in full: the ReferenceGrant reference and the Security concept page (raw markdown on GitHub). Confirmed: from and to structure, same-namespace to, single namespace per from, additive effect, no existence leakage, runtime recalculation on change or deletion, Core conformance for the listed kinds, and the guidance on name in to entries. Removed: the BackendTLSPolicy CA ConfigMap example and the RefNotPermitted reason, neither of which appears on the pages. Example namespace names were replaced with those on the page.

Method: documentation only; no commands were run.
