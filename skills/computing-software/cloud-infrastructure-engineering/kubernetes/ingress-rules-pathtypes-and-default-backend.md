---
id: computing-software.cloud-infrastructure-engineering.kubernetes.ingress-rules-pathtypes-and-default-backend
name: ingress-rules-pathtypes-and-default-backend
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, ingress, pathtype, default-backend, ingressclass, host-rules, wildcard-hosts, ckad]
level: practitioner
status: docs-checked
description: "Write Ingress rules correctly: host and wildcard matching, pathType Exact vs Prefix vs ImplementationSpecific semantics and precedence, IngressClass selection and defaultBackend."
sources: ["https://kubernetes.io/docs/concepts/services-networking/ingress/#path-types", "https://kubernetes.io/docs/concepts/services-networking/ingress/#default-backend", "https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-class"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ingress rules, pathTypes and default backend

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata: {name: shop, namespace: shop}
spec:
  ingressClassName: example-class
  defaultBackend:
    service: {name: not-found, port: {number: 80}}
  tls:
  - hosts: [shop.example.com]
    secretName: shop-tls
  rules:
  - host: shop.example.com
    http:
      paths:
      - {path: /api, pathType: Prefix, backend: {service: {name: api, port: {number: 8080}}}}
      - {path: /healthz, pathType: Exact, backend: {service: {name: api, port: {name: http}}}}
      - {path: /, pathType: Prefix, backend: {service: {name: web, port: {number: 80}}}}
  - host: "*.shop.example.com"
    http:
      paths:
      - {path: /, pathType: Prefix, backend: {service: {name: tenant-router, port: {number: 80}}}}
```

## pathType semantics
Every path needs a `pathType`; `Exact`, `Prefix` and `ImplementationSpecific` are supported.
| pathType | Matches | Example |
|---|---|---|
| `Exact` | the exact URL path, case-sensitive | rule `/foo`: `/foo` yes, `/foo/` no |
| `Prefix` | element-wise prefix, split on `/` | rule `/aaa/bb` does not match `/aaa/bbb`; rules `/foo` and `/foo/` both match `/foo` and `/foo/` |
| `ImplementationSpecific` | up to the IngressClass implementation | varies |
When several paths match, the longest matching path wins; if still equal, `Exact` beats `Prefix`.

## Hosts
- Exact host, or a wildcard that covers a single DNS label: `*.foo.com` matches `bar.foo.com`
  but not `baz.bar.foo.com` and not `foo.com`.
- A rule without `host` applies to all inbound HTTP traffic.

## IngressClass and defaults
- `ingressClassName` refers to an IngressClass resource. An IngressClass annotated
  `ingressclass.kubernetes.io/is-default-class: "true"` is used for Ingresses that do not set a
  class. The `kubernetes.io/ingress.class` annotation, used before Kubernetes 1.18, is deprecated.
- `.spec.defaultBackend` handles requests that match no rule; an Ingress with no rules must
  set it. If it is unset, handling of unmatched requests is up to the controller (controllers
  often have their own default backend setting).
- Service backends are in the same namespace as the Ingress; in `port`, use either `name` or
  `number`.

## Verify
```bash
kubectl describe ingress shop -n shop
```
- [ ] Each path routes as expected, including edge cases (trailing slash, near-miss prefixes, unknown host).

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the Ingress concept page: pathType table and examples, precedence rule, hostname wildcard table, default backend behaviour, IngressClass default annotation and the deprecated annotation. Removed controller-specific claims (ingress-nginx regex behaviour, per-Ingress default backend scope) and replaced the ingress-nginx class name.

Method: documentation only; no commands were run.
