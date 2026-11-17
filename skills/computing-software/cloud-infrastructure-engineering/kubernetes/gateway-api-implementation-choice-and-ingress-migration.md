---
id: computing-software.cloud-infrastructure-engineering.kubernetes.gateway-api-implementation-choice-and-ingress-migration
name: gateway-api-implementation-choice-and-ingress-migration
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, gateway-api, envoy-gateway, nginx-gateway-fabric, ingress2gateway, ingress-migration, istio, cilium]
level: practitioner
status: docs-checked
description: "Choose a Gateway API implementation (Envoy Gateway, NGINX Gateway Fabric, Istio, Cilium, cloud) and migrate Ingresses with ingress2gateway and a parallel cutover."
sources: ["https://gateway-api.sigs.k8s.io/guides/getting-started/migrating-from-ingress/", "https://gateway-api.sigs.k8s.io/guides/getting-started/migrating-from-ingress-nginx/", "https://github.com/kubernetes-sigs/ingress2gateway", "https://github.com/kubernetes-sigs/gateway-api/tree/main/conformance/reports", "https://gateway.envoyproxy.io/docs/api/extension_types/", "https://cert-manager.io/docs/usage/gateway/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a Gateway API implementation and migrating from Ingress

## Choosing
Check the implementations page for **conformance reports** per Gateway API version and
profile (Core, Extended features like `HTTPRouteRequestMirror`, `GRPCRoute`, `TLSRoute`).
| Implementation | Notes |
|---|---|
| Envoy Gateway | has its own policy CRDs (BackendTrafficPolicy, ClientTrafficPolicy, SecurityPolicy with JWT and OIDC settings, rate limiting) |
| NGINX Gateway Fabric | NGINX data plane |
| Istio | one API surface for ingress and mesh (GAMMA, Mesh conformance profile) |
| Cilium | Gateway API support inside the Cilium CNI |
| GKE Gateway, AWS (aws-load-balancer-controller), Kong, Traefik, Linkerd, kgateway | each has a conformance report in the Gateway API repo (v1.6) |

Check the conformance report of the exact release before choosing; the table lists names, not endorsements.
Decision criteria: conformance level for features you need, policy attachment for auth/rate
limits (implementation-specific CRDs = lock-in), multi-tenancy (one Gateway per team vs shared),
operational familiarity, and whether each Gateway spins up a cloud LB (cost).

## Migrating Ingress → Gateway API
```bash
go install github.com/kubernetes-sigs/ingress2gateway@v1.0.0   # or brew install ingress2gateway, or a release binary
ingress2gateway print --providers=ingress-nginx -A > gateway-resources.yaml
ingress2gateway print --providers=ingress-nginx --namespace shop --input-file ingress.yaml
```
It reads Ingress resources (from the cluster, or `--input-file`) and prints Gateway and HTTPRoute
resources to stdout (`-o yaml|json|kyaml`), warning about untranslated fields and unsupported
features; map those by hand to filters or implementation policies. Add `--allow-experimental-gw-api` to
include experimental fields such as URLRewrite in the output. v1.0 targets Gateway API v1.5.0 output.

Cutover plan:
1. Install the Gateway implementation alongside ingress-nginx; create Gateway with a **new**
   LB address.
2. Apply generated HTTPRoutes; test with `curl --resolve host:443:<new-lb-ip>`.
3. Move DNS per hostname (low TTL first), watch error rates on both.
4. Delete Ingress objects after traffic drains; keep cert-manager working (Gateway annotation
   `cert-manager.io/cluster-issuer` plus cert-manager's `config.gatewayAPI.enabled: true`).
5. Remove ingress-nginx.

## Gotchas
- Regex paths: `RegularExpression` path matching is implementation-specific support; rewrite routes to
  PathPrefix/Exact where possible.
- Default backends and catch-all routes need explicit HTTPRoutes.
- TLS passthrough uses `TLSRoute` (Standard channel since Gateway API v1.5.0).

## Verify
- [ ] Every Ingress host has an Accepted HTTPRoute; synthetic checks green on the new LB before DNS cutover.

## Checked

Documentation release: Gateway API docs (kubernetes-sigs/gateway-api site/content and apis/v1, latest release v1.6.3, repo commit 2026-10-23; v1.7.0 is at release-candidate stage). ingress2gateway repo README (last commit 2026-07-07), Envoy Gateway extension_types (repo commit 2026-10-25).
Confirmed: conformance report directories per implementation under conformance/reports (v1.6); Envoy Gateway policy CRD names and JWT/OIDC/RateLimit types; ingress2gateway install methods, `print` flags (`--providers` required, `-A`, `--namespace`, `--input-file`, `-o`, `--allow-experimental-gw-api`) and version support; cert-manager Gateway API enablement; TLSRoute channel.
Removed: per-vendor "fit" claims and Azure/HAProxy/Contour/GKE descriptions that the docs do not cover, the `proxy-body-size` mapping, and `--enable-gateway-api` (current cert-manager docs use `config.gatewayAPI.enabled`).

Method: documentation only; no commands were run.
