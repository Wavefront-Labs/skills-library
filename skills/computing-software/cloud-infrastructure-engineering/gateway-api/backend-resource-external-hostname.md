---
id: computing-software.cloud-infrastructure-engineering.gateway-api.backend-resource-external-hostname
name: backend-resource-external-hostname
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [backend, externalhostname, endpointselector, experimental, external-services]
level: advanced
status: docs-checked
description: "Use the experimental Backend resource for an external hostname or selected in-cluster Pods, and how it differs from ExternalName Services."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/backend.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Backend` is part of the Experimental channel. It defines a backend destination and backend-specific connection behaviour for a Gateway acting as a client. Uses: external destinations without synthetic `ExternalName` Services, in-cluster destinations without configuring a Service directly, protocol expectations, and backend TLS settings on the destination.

Spec fields: `type` (`EndpointSelector` for internal or `ExternalHostname` for external destinations), `port`, `endpointSelector`, `externalHostname`, `sessionPersistence` (for `EndpointSelector`), `protocol` (the protocol the implementation should use to connect) and `tls`.

- `EndpointSelector`: set `spec.type` to `EndpointSelector` and give Pod labels in `spec.endpointSelector.matchLabels`; `matchLabels` is the only selection mechanism today. It decorates internal endpoints with Gateway-specific configuration such as TLS and session persistence, and is an additional way to represent an internal destination, not a replacement for Service; Routes can still target Services. The feature is still being developed, and until then a controller may use a Service behind the scenes.
- `ExternalHostname`: an external FQDN destination. Validation does not allow hostnames ending in `.cluster.local`, to stop references that look like in-cluster Service names.

Versus `ExternalName`: both depend on DNS, but `ExternalHostname` gives a clearer and safer model for egress. `ExternalName` has a history of DNS rebinding concerns (for example CVE-2021-25740). DNS trust is still required, so the page advises implementations to add guardrails such as egress domain allow-lists, together with admission and network-level controls.

Status is reported per ancestor in `status.ancestors`: `Accepted` shows whether the controller accepted the Backend and `ResolvedRefs` whether all references resolved.

Because it is Experimental, confirm that your implementation and CRD channel include it, and expect changes between releases. The example manifests are Hugo includes and were not visible, so the `backendRef` syntax for pointing a Route at a Backend is not given here; take it from the implementation docs.

## Checked

2026-11-08. Read in full (GitHub markdown): the Backend reference page. Confirmed: Experimental channel, purposes, spec field list, EndpointSelector and ExternalHostname rules, ExternalName comparison including the CVE and guardrail advice, status fields. Removed: the claim that the Gateway resolves the name so DNS changes need no Route edits, that `protocol` works like Service `appProtocol` for h2c or WebSocket, that the Kubernetes documentation warns about ExternalName misuse, and the instruction for the `backendRef` kind and group (not on the page).

Method: documentation only; no commands were run.
