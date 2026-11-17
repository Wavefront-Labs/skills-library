---
id: computing-software.cloud-infrastructure-engineering.gateway-api.policy-attachment-direct-and-inherited
name: policy-attachment-direct-and-inherited
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [policy-attachment, direct-policy, inherited-policy, gep-713, targetrefs, status]
level: advanced
status: docs-checked
description: "Policy attachment pattern: policies target resources by targetRefs, Direct versus Inherited, how status ancestors report acceptance, and where the docs point for detail."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/policy-attachment.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/policy/backendtrafficpolicy.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/policy/backendtlspolicy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Policy Attachment is a Gateway API pattern that augments the behaviour of an object with settings that cannot be described in that object's spec. A Policy Attachment is a specific type of metaresource (ReferenceGrant is another metaresource). The pattern is EXPERIMENTAL and is described in GEP-713.

Two kinds:

- **Direct Policy Attachment**: affects settings on one object.
- **Inherited Policy Attachment**: affects objects in a hierarchy.

Examples in the reference pages:

- BackendTLSPolicy (Standard Channel since v1.4.0) is a Direct policy without defaults or overrides, applied to a Service. It must be in the same namespace as the Service, to avoid sharing trust across namespace boundaries. All Routes pointing to the Service should respect it.
- BackendTrafficPolicy (Experimental Channel since v1.3.0) is a Direct policy. Its `targetRefs` can name Service, ServiceImport or an implementation-specific backendRef, cannot be scoped to ports, and all Routes targeting the Backend should respect it.

Status: both policies report in `status.ancestors`, a list of `PolicyAncestorStatus` entries holding the ancestor parentReference, the controller name and conditions.

The policy attachment page is only a short pointer; for technical details, precedence and merge rules consult GEP-713, which this skill does not cover.

## Checked

2026-11-08. Read in full: the Policy Attachment page, the BackendTrafficPolicy page and the BackendTLSPolicy page (raw markdown on GitHub). The API overview page was dropped from sources and its claims removed. Confirmed: metaresource definition, Direct versus Inherited wording, EXPERIMENTAL status and GEP-713 pointer, the channel and Direct classification of both policies, same-namespace rule for BackendTLSPolicy, BackendTrafficPolicy target kinds and port limitation, and the status.ancestors shape. Removed: the claims about overrides and defaults for Inherited policies, allowed-namespace targeting, and policies declaring targetable kinds, none of which are on the pages.

Method: documentation only; no commands were run.
