---
id: computing-software.cloud-infrastructure-engineering.linkerd.rate-limit-reference-fields
name: rate-limit-reference-fields
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, rate-limiting, reference, total-limit]
level: advanced
status: docs-checked
description: "Know the HTTPLocalRateLimitPolicy fields: targetRef, total, identity and overrides, and the constraints between them."
sources:
  - https://linkerd.io/2.19/reference/rate-limiting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`HTTPLocalRateLimitPolicy` must point at a `Server`, and a Server can be referred to by only one such policy. A Server's default `accessPolicy` is `deny`, so without AuthorizationPolicies it denies traffic. To add rate limits without writing authorization policies, set `accessPolicy` to a permissive value such as `all-unauthenticated`.

Spec fields:

- `targetRef`: the Server the policy applies to.
- `total.requestsPerSecond`: overall limit for all traffic to the target. If unset, no overall limit applies.
- `identity.requestsPerSecond`: fairness limit applied to each client, grouped by identity. When `total.requestsPerSecond` is also set, the identity value cannot be greater than the total.
- `overrides`: array of per-client exceptions. Each has `requestsPerSecond` (not greater than the total when one is set) and `clientRefs` with `kind` (only ServiceAccount is supported), `namespace` (empty means the policy's namespace) and `name`.

Example from the reference: total 100 RPS, 20 RPS per identity, and an override of 25 RPS for the `special-client` ServiceAccount in the emojivoto namespace:

```yaml
spec:
  targetRef:
    group: policy.linkerd.io
    kind: Server
    name: web-http
  total:
    requestsPerSecond: 100
  identity:
    requestsPerSecond: 20
  overrides:
    - requestsPerSecond: 25
      clientRefs:
        - kind: ServiceAccount
          namespace: emojivoto
          name: special-client
```

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/reference/rate-limiting/. Server targeting, one policy per Server, accessPolicy note, all spec and override fields with constraints, the example values.

Removed or reworded: The closing sizing advice.

Method: documentation only; no commands were run.
