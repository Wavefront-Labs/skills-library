---
id: computing-software.cloud-infrastructure-engineering.contour.contour-header-rewrite-policies
name: contour-header-rewrite-policies
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [requestheaderspolicy, responseheaderspolicy, header-rewrite, set, remove, host-header, dynamic-headers]
level: practitioner
status: docs-checked
description: "HTTPProxy request and response header policies per route or service: set/remove, dynamic Envoy variables, CONTOUR_* variables, and Host header rewrite."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/request-rewriting.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy header rewriting

`requestHeadersPolicy` and `responseHeadersPolicy` take `set` (name/value list; creates or overwrites) and `remove` (names). They go on a route or on a specific service entry.

```yaml
routes:
- services:
  - name: s1
    port: 80
    requestHeadersPolicy:
      set:
      - name: l5d-dst-override
        value: "%CONTOUR_SERVICE_NAME%.%CONTOUR_NAMESPACE%.svc.cluster.local:%CONTOUR_SERVICE_PORT%"
  responseHeadersPolicy:
    set:
    - name: X-Envoy-Response-Flags
      value: "%RESPONSE_FLAGS%"
    remove: [X-Internal-Secret]
```

Dynamic values: Envoy variables such as `%HOSTNAME%`, `%PROTOCOL%`, `%REQ(header)%`, `%DOWNSTREAM_REMOTE_ADDRESS%`, `%DOWNSTREAM_PEER_SUBJECT%`, `%DOWNSTREAM_TLS_VERSION%`, `%TLS_JA3_FINGERPRINT%`, `%RESPONSE_CODE_DETAILS%`. Unexpandable ones pass through or are skipped: `%UPSTREAM_REMOTE_ADDRESS%` stays literal on requests (upstream not yet chosen), `%REQ(Missing)%` is skipped. Contour already sets `X-Request-Start: t=%START_TIME(%s.%3f)%`.

Contour variables `%CONTOUR_NAMESPACE%`, `%CONTOUR_SERVICE_NAME%`, `%CONTOUR_SERVICE_PORT%` resolve per service; on a route-level policy only the namespace is set and the other two come out literal.

Host header: set `name: host` with a static value (route or service level), or a dynamic `"%REQ(x-rewrite-header)%"` (route level only; empty header ignored). Only one of static or dynamic. The header must come from a trusted source, and the rewrite affects forwarding only, not routing.

## Checked

2026-11-04. Confirmed against the Contour request rewriting page (config/request-rewriting.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
