---
id: computing-software.cloud-infrastructure-engineering.contour.contour-ip-allow-deny-filtering
name: contour-ip-allow-deny-filtering
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [ipallowpolicy, ipdenypolicy, cidr, rbac-filter, source-peer, source-remote, numtrustedhops, 403]
level: practitioner
status: docs-checked
description: "HTTPProxy IP filtering with ipAllowPolicy and ipDenyPolicy: CIDR syntax, Peer vs Remote source, vhost versus route precedence, numTrustedHops for X-Forwarded-For."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/ip-filtering.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy IP filtering

Contour uses Envoy's RBAC filter. Allowed requests are proxied to the upstream; denied requests receive HTTP 403 (Forbidden). Rules sit on `virtualhost` and/or individual routes.

```yaml
spec:
  virtualhost:
    fqdn: foo-basic.bar.com
    ipAllowPolicy:
    - cidr: 127.0.0.1/32
      source: Peer
  routes:
  - conditions: [{prefix: /}]
    services: [{name: s1, port: 80}]
    ipAllowPolicy:
    - cidr: 127.0.0.1/32
      source: Peer
    - cidr: 99.99.0.0/16
      source: Remote
```

- CIDRs may be IPv4 or IPv6; a bare IP means the range containing that one address only (`127.0.0.1`, `2001:db8::68`).
- `ipAllowPolicy` only allows requests that match the filters. The page describes `ipDenyPolicy` as denying all requests unless they match the filters; its wording is ambiguous, so confirm the deny semantics with a test request. You cannot specify both on the same virtualhost or route.
- `source: Peer` uses Envoy `direct_remote_ip`, which is always the physical peer.
- `source: Remote` uses Envoy `remote_ip`, which may be inferred from the `X-Forwarded-For` header or proxy protocol. With `X-Forwarded-For` it may be necessary to configure Contour's `numTrustedHops` in the Network Parameters.
- Precedence: vhost rules apply to all routes of the virtual host unless a route has its own; route rules override vhost rules and are not additive.

## Checked

2026-11-08. Read the Contour main-branch config page ip-filtering.md in full. Confirmed: RBAC filter, 403 on deny, ipAllowPolicy and ipDenyPolicy on virtualhost and route, CIDR forms, mutual exclusion, Peer versus Remote sources, numTrustedHops, and override precedence. Removed the load balancer remark and the `network.num-trusted-hops` config key spelling, which the page does not give. The deny wording is quoted from the page as ambiguous rather than restated.

Method: documentation only; no commands were run.
