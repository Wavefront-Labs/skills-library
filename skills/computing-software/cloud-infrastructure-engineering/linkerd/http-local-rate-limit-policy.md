---
id: computing-software.cloud-infrastructure-engineering.linkerd.http-local-rate-limit-policy
name: http-local-rate-limit-policy
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, rate-limiting, httplocalratelimitpolicy, server]
level: practitioner
status: docs-checked
description: "Protect a service with an HTTPLocalRateLimitPolicy that targets a Server, with a per-identity limit and a per-ServiceAccount override."
sources:
  - https://linkerd.io/2.19/tasks/configuring-rate-limiting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rate limiting uses an `HTTPLocalRateLimitPolicy` that points at a `Server`. Create the Server first, with a permissive `accessPolicy` so that you do not also need authorization policies:

```yaml
apiVersion: policy.linkerd.io/v1beta3
kind: Server
metadata:
  namespace: emojivoto
  name: web-http
spec:
  accessPolicy: all-unauthenticated
  podSelector:
    matchLabels:
      app: web-svc
  port: http
  proxyProtocol: HTTP/1
```

Then the policy, here 4 requests per second per client identity:

```yaml
apiVersion: policy.linkerd.io/v1alpha1
kind: HTTPLocalRateLimitPolicy
metadata:
  namespace: emojivoto
  name: web-http
spec:
  targetRef:
    group: policy.linkerd.io
    kind: Server
    name: web-http
  identity:
    requestsPerSecond: 4
```

Ten concurrent requests from an unmeshed client allowed only 4; the rest received HTTP 429.

To give one client a higher allowance, add an override that references its ServiceAccount:

```yaml
  overrides:
  - requestsPerSecond: 6
    clientRefs:
    - kind: ServiceAccount
      namespace: emojivoto
      name: default
```

In the guide, a client in the injected emojivoto namespace used the `default` ServiceAccount and got 6 requests through, while the earlier unmeshed client remained at 4.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/tasks/configuring-rate-limiting/.

Removed or reworded: Unmeshed-clients-as-a-group claim.

Method: documentation only; no commands were run.
