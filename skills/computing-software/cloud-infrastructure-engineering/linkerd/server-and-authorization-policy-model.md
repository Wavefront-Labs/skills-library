---
id: computing-software.cloud-infrastructure-engineering.linkerd.server-and-authorization-policy-model
name: server-and-authorization-policy-model
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, authorization-policy, server, meshtlsauthentication]
level: advanced
status: docs-checked
description: "Combine Server, HTTPRoute, MeshTLSAuthentication and AuthorizationPolicy resources to authorize traffic, and avoid overlapping Servers."
sources:
  - https://linkerd.io/2.19/reference/authorization-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fine-grained policy follows one pattern:

- A `Server` selects a port on a set of pods in its namespace.
- Optionally an `HTTPRoute` references the Server and describes a subset of HTTP traffic.
- A `MeshTLSAuthentication` or `NetworkAuthentication` says who may access.
- An `AuthorizationPolicy` references the Server or HTTPRoute and the authentication resource.

Server spec fields: `podSelector` (exactly one of `matchLabels` or `matchExpressions`), `port` (name or number, from the pod spec's ports), `proxyProtocol` (one of `unknown`, `HTTP/1`, `HTTP/2`, `gRPC`, `opaque`, `TLS`; supersedes the `config.linkerd.io/opaque-ports` annotation) and `accessPolicy`, the policy for traffic matching no authorization policy. It defaults to `deny` and accepts the same values as default policies, including `audit`. `proxyProtocol` defaults to `unknown` if not set.

Once a Server exists, all traffic to that port is denied unless authorized or in audit mode. Servers must not overlap, meaning no two select the same pod and port pair, and an admission controller rejects overlapping ones.

Use `accessPolicy: audit` to test policies before enforcing them; audit mode flags requests in logs and metrics.

The legacy `ServerAuthorization` still exists but only works with Servers, not routes.

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/reference/authorization-policy/. The Server, HTTPRoute, authentication and AuthorizationPolicy pattern, Server spec fields and their rules, deny-by-default note, the no-overlap rule and admission controller, ServerAuthorization limits.

Removed or reworded: The step-by-step audit-to-deny workflow wording (reworded to what the page states).

Method: documentation only; no commands were run.
