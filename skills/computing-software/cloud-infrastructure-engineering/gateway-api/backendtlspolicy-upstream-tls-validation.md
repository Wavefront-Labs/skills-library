---
id: computing-software.cloud-infrastructure-engineering.gateway-api.backendtlspolicy-upstream-tls-validation
name: backendtlspolicy-upstream-tls-validation
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [backendtlspolicy, tls, upstream, validation, cacertificaterefs, subjectaltnames]
level: advanced
status: docs-checked
description: "Make the Gateway verify upstream TLS with BackendTLSPolicy: targetRefs Services, validation hostname, CA bundle or System trust, SANs, options, and same-namespace rules."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/policy/backendtlspolicy.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/tls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`BackendTLSPolicy` describes how a Gateway should establish TLS to a backend Service and how to verify it.

Fields:

- `targetRefs`: the Services the policy applies to. The policy must live in the same namespace as the targeted Service.
- `validation.hostname`: the server name to verify in the backend certificate. Wildcards are not allowed.
- `validation.caCertificateRefs` **or** `validation.wellKnownCACertificates: System`: exactly one of the two. The first references objects holding PEM-encoded CA certificates (cross-namespace references are not allowed); the second, `System`, tells the Gateway to use trusted system CA certificates, which vary by implementation.
- `validation.subjectAltNames`: optional (Extended feature `BackendTLSPolicySANValidation`); the backend certificate must match at least one entry. Maximum 5; each is a Hostname or URI (for example a SPIFFE ID), with a `type`; IPs and wildcards are not allowed.
- `options`: implementation-specific TLS options (check the implementation's docs).

Behaviour notes:

- Standard channel since v1.4.0. It is a Direct PolicyAttachment without defaults or overrides.
- `validation.hostname` is the SNI the Gateway uses and must match the backend certificate; IP addresses are not allowed.
- It is a union feature: all Routes that point to the referenced Service should respect it, including GRPCRoute and TLSRoute (Terminate mode).
- Status uses `PolicyAncestorStatus`, so `status.ancestors` shows which parent each status belongs to.

## Checked

2026-11-04. Confirmed on the Gateway API BackendTLSPolicy reference (backendtlspolicy.md): channel, fields, same-namespace rule, either/or CA settings, SAN limits and types, union feature, ancestor status. Removed the request-mirroring example, the ConfigMap claim, the client-certificate pointer and the closing usage tips (not on the page).

Method: documentation only; no commands were run.
