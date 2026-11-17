---
id: computing-software.cloud-infrastructure-engineering.linkerd.route-retry-annotations
name: route-retry-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, retries, httproute, grpcroute, annotations]
level: practitioner
status: docs-checked
description: "Configure HTTP and gRPC retries with retry.linkerd.io annotations, including status code lists, limit and per-attempt timeout."
sources:
  - https://linkerd.io/2.19/reference/retries/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Retries run in the client's outbound proxy and are configured by annotations on a Service, HTTPRoute or GRPCRoute. Route annotations override all retry annotations on the parent Service. Requests with a body larger than 64KiB are not retried, and on a route with several backends each retry may go to a different backend.

HTTP: `retry.linkerd.io/http` on a Service or HTTPRoute (not valid on a GRPCRoute), a comma-separated list where each element is a single code (`"504"`, quoted because annotation values are strings), a range (`500-504`), `gateway-error` (502-504) or `5xx`.

gRPC: `retry.linkerd.io/grpc` on a Service or GRPCRoute (not valid on an HTTPRoute), a comma-separated list of `cancelled`, `deadline-exceeded`, `internal`, `resource-exhausted` and `unavailable`.

General, valid on all three resources:

- `retry.linkerd.io/limit`: maximum retries per request. Default 1.
- `retry.linkerd.io/timeout`: a timeout after which the request is cancelled and retried, if the retry limit has not been reached. If unspecified, no retry timeout is applied; a unit is required (`5s` and `200ms` are valid, `5` is not).

```yaml
kind: HTTPRoute
apiVersion: gateway.networking.k8s.io/v1beta1
metadata:
  name: schlep-default
  namespace: schlep
  annotations:
    retry.linkerd.io/http: 5xx
    retry.linkerd.io/limit: "2"
    retry.linkerd.io/timeout: 300ms
```

Retry annotations are incompatible with ServiceProfiles: if a ServiceProfile is defined for a Service, proxies use the ServiceProfile retry configuration and ignore the annotations.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Linkerd 2.19 Retries reference page (annotations, accepted values, limit default 1, timeout units, 64KiB body limit, route-over-Service override, ServiceProfile warning, example). The page is labelled as an older version at the time of reading, so check the current docs for newer behaviour.
