---
id: computing-software.cloud-infrastructure-engineering.external-dns.gateway-api-route-sources
name: gateway-api-route-sources
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, gateway-api, gateway-httproute, listenerset, gateway-listener-sets, gateway-hostname-source]
level: advanced
status: docs-checked
description: "Configure ExternalDNS Gateway API sources: route kinds and versions, hostnames, annotation placement (Gateway target vs Route), ListenerSets, RBAC and filters."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/sources/gateway-api.md
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/annotations/annotations.md
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/operational-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gateway API sources

Sources: `gateway-httproute`, `gateway-grpcroute`, `gateway-tlsroute`, `gateway-tcproute`, `gateway-udproute`. ExternalDNS uses the `v1` API for all routes, making Gateway API v1.6.0 the minimum (ListenerSet v1.5.0, TLSRoute v1.5.0 standard).

**Hostnames:** HTTPRoute and TLSRoute specs and Gateway listeners supply them. TCPRoute and UDPRoute have none, so use the `hostname` annotation. For HTTPRoute/TLSRoute prefer the spec, because the Gateway will not recognise extra annotation hosts.

**Annotation placement**
- Gateway: only `external-dns.kubernetes.io/target`.
- ListenerSet: also `target`, which takes precedence over the parent Gateway; requires `--gateway-listener-sets`.
- Routes: everything else (`hostname`, `ttl`, `controller`, `set-identifier`, `cloudflare-*`, `aws-*`, `scw-*`).

Putting `cloudflare-proxied` or `ttl` on a Gateway, or `target` on a Route, is ignored.

**Conflicting hostnames.** To keep a CNAME such as `company.public.example.com` from being overwritten by an A record, set on the Route:
```yaml
external-dns.kubernetes.io/gateway-hostname-source: annotation-only
external-dns.kubernetes.io/hostname: company.private.example.com
```

**Scoping flags:** `--namespace`, `--label-filter`, `--gateway-name`, `--gateway-namespace`, `--gateway-label-filter`, `--gateway-listener-sets`.

**RBAC:** get/watch/list on `namespaces`, and on gateways, httproutes, grpcroutes, tlsroutes, tcproutes, udproutes, listenersets in `gateway.networking.k8s.io`.

Install the Gateway API CRDs before enabling these sources: a missing CRD can make the informer block and time out at startup.

## Checked

2026-11-04. Confirmed against the ExternalDNS Gateway API Route Sources page (versions table, hostnames, annotation placement, common mistakes, gateway-hostname-source example, RBAC and flags) and the Operational Best Practices page (missing CRD timeout). Removed the word "silently".
Method: documentation only; no commands were run.
