---
id: computing-software.cloud-infrastructure-engineering.gateway-api.httproute-spec-hostnames-rules-matches
name: httproute-spec-hostnames-rules-matches
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [httproute, hostnames, rules, matches, backendrefs, spec]
level: practitioner
status: docs-checked
description: "HTTPRoute spec anatomy: parentRefs, hostnames, rules with matches, filters, backendRefs, timeouts and name, including OR-between-matches and AND-within-match semantics."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/httproute.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/http-routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An HTTPRoute (`gateway.networking.k8s.io/v1`, Standard channel since v0.5.0) has:

- `parentRefs`: Gateways to attach to.
- `hostnames` (optional): matched against the Host header **before** any rule. IPs and ports are not allowed. With no hostnames, routing uses rules only.
- `rules`: each with `matches`, optional `filters`, `backendRefs`, `timeouts` and `name`.

Matching semantics: each entry in `matches` is independent (OR); within one match all conditions must hold (AND).

```yaml
rules:
- matches:
  - path:
      value: "/foo"
    headers:
    - name: "version"
      value: "2"
  - path:
      value: "/v2/foo"
```

This matches either (prefix `/foo` AND header `version: 2`) OR prefix `/v2/foo`. If `matches` is omitted the default is a prefix match on `/`, matching every request.

`backendRefs` omitted means no forwarding; with no response-producing filter either, the gateway returns a 500.

Worked example from the guide: host `foo.example.com` path prefix `/login` goes to `foo-svc`; host `bar.example.com` with header `env: canary` goes to `bar-svc-canary`, otherwise `bar-svc`. Separate hosts with different needs are deployed as separate HTTPRoutes (`foo-route`, `bar-route`) on one Gateway, and the most specific match takes precedence.

## Checked

2026-11-04. Confirmed on the Gateway API HTTPRoute reference and HTTP routing guide (httproute.md, http-routing.md): Standard channel since v0.5.0, spec fields, hostname rules, OR/AND match semantics, default match, 500 behaviour, worked example. Removed the "only one rule matches" sentence (not on the pages).

Method: documentation only; no commands were run.
