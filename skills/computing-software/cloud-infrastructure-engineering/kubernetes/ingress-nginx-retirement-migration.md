---
id: computing-software.cloud-infrastructure-engineering.kubernetes.ingress-nginx-retirement-migration
name: ingress-nginx-retirement-migration
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, ingress, ingress-nginx-retirement, ingress-nginx, gateway-api, ingress2gateway]
level: practitioner
status: docs-checked
description: "Plan the move off the retired community ingress-nginx controller: inventory annotations, pick a Gateway API or Ingress replacement and cut over safely."
sources: ["https://github.com/kubernetes/ingress-nginx", "https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/", "https://github.com/kubernetes-sigs/ingress2gateway", "https://github.com/kubernetes-sigs/ingress2gateway/blob/main/pkg/i2gw/providers/ingressnginx/README.md", "https://gateway-api.sigs.k8s.io/implementations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating off ingress-nginx

The Kubernetes community ingress-nginx project (kubernetes/ingress-nginx) was retired: the
project README (and the November 2025 Kubernetes blog post it links) says best-effort maintenance
continues until March 2026, after which there are no further releases, bugfixes or security
updates. Existing deployments are not broken and the Helm charts and images remain available,
but they run unpatched code at the cluster edge.

## 1. Inventory
```bash
kubectl get ingress -A                                               # note the CLASS column (nginx)
kubectl get ingress -A -o yaml                                       # list the nginx.ingress.kubernetes.io/ annotations in use
kubectl -n ingress-nginx get cm ingress-nginx-controller -o yaml     # global config
```
The annotation list decides difficulty. The ingress2gateway ingress-nginx provider README lists
which annotations it converts; for example canary weight and header matching, `rewrite-target`
(without capture-group references) and `backend-protocol` are converted, while annotations such
as `canary-by-cookie`, `canary-by-header-pattern`, `proxy-redirect-from` and `custom-headers`
are recognized but not converted. Anything not listed there, including snippet annotations,
needs manual re-implementation.

## 2. Choose a target
- Gateway API implementation (pick one from the implementations list on gateway-api.sigs.k8s.io):
  the direction the ingress-nginx README itself recommends.
- Another maintained Ingress controller: smaller change, but annotations are controller-specific.

## 3. Convert
```bash
ingress2gateway print --providers=ingress-nginx -A > gateway-resources.yaml
```
Review output; unconverted annotations produce warnings. Re-implement them as route filters,
policies or implementation-specific CRDs.

## 4. Cut over
Run both controllers side by side with separate load balancers, test with
`curl --resolve host:443:<new-lb-ip>`, then move DNS with a low TTL. Keep the old controller until
traffic on it reaches zero (its metrics show request counts).

## Verify
All hosts answer through the new LB with the same status codes, redirects, TLS certificates and
auth behaviour; the old controller logs no requests for a full business cycle.

## Checked
2026-10-26. Checked against the ingress-nginx README and the ingress2gateway README and ingress-nginx provider README (repositories kubernetes/ingress-nginx, last commit 2026-03-23, and kubernetes-sigs/ingress2gateway, last commit 2026-07-07). Confirmed: retirement announcement (best-effort maintenance until March 2026, afterwards no releases, bugfixes or security updates; existing deployments keep working and artifacts stay available); `ingress2gateway print --providers=ingress-nginx` with `-A` for all namespaces; the provider converts canary weight and header annotations, `rewrite-target` (to a URLRewrite filter, without capture-group references) and `backend-protocol` (GRPC to GRPCRoute, HTTPS to BackendTLSPolicy) and warns on unconverted annotations. Corrected: canary and rewrite-target do have conversions. Removed as unconfirmed: the F5 distinction, the named replacement controllers and the jq inventory pipelines.
Method: documentation only; no commands were run.
