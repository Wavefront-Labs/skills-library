---
id: computing-software.cloud-infrastructure-engineering.linkerd.route-timeout-annotations
name: route-timeout-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, timeouts, httproute, annotations]
level: practitioner
status: docs-checked
description: "Configure request, response and idle timeouts with annotations on a Service, HTTPRoute or GRPCRoute."
sources:
  - https://linkerd.io/2.19/reference/timeouts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Timeouts are enforced by the outbound side of the client proxy. They are set with annotations on a Kubernetes Service, or on an HTTPRoute or GRPCRoute that has a Service as its parent:

- `timeout.linkerd.io/request`: the maximum time a full request-response stream is in flight.
- `timeout.linkerd.io/response`: the maximum time a backend response may be in flight.
- `timeout.linkerd.io/idle`: the maximum time a stream may be idle, regardless of state.

Annotations on a route override all timeout annotations on the parent Service. If the request timeout field is set on an HTTPRoute, it is used as the request timeout, but the annotation wins when both are present.

```yaml
kind: HTTPRoute
apiVersion: gateway.networking.k8s.io/v1beta1
metadata:
  name: schlep-default
  namespace: schlep
  annotations:
    timeout.linkerd.io/request: 2s
    timeout.linkerd.io/response: 1s
spec:
  parentRefs:
    - name: schlep
      kind: Service
      group: core
      port: 80
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: "/"
```

Two cautions. Timeouts configured this way are not retryable: when one fires, the request is not retried. Retryable timeouts are configured as part of retry configuration. And these annotations are incompatible with ServiceProfiles: if a ServiceProfile exists for the Service, its timeout configuration is used and the annotations are ignored.

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/reference/timeouts/. Three annotations and definitions, client-side outbound enforcement, route-over-Service override, HTTPRoute field priority, non-retryable note, ServiceProfile incompatibility, example.

Removed or reworded: The explicit `timeouts.request` field path and the retry annotation name.

Method: documentation only; no commands were run.
