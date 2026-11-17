---
id: computing-software.networking-hardware-and-wireless.traefik.provider-kubernetes-crd
name: provider-kubernetes-crd
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, kubernetes, ingressroute, crd, middleware-crd, rbac]
level: practitioner
status: docs-checked
description: "Run the kubernetesCRD provider: install the CRDs and RBAC first, then route with IngressRoute and Middleware custom resources."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/providers/kubernetes/kubernetes-crd.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# provider kubernetes crd
The `kubernetesCRD` provider reads Traefik custom resources such as `IngressRoute` and `Middleware`. With the Helm chart it is enabled by default. Without Helm you must add or update all Traefik resource definitions and the RBAC for them.

```bash
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v3.8/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v3.8/docs/content/reference/dynamic-configuration/kubernetes-crd-rbac.yml
```
```yaml
providers:
  kubernetesCRD: {}
```
Gotchas: the reference says that when you install without Helm, or upgrade with Helm, you must add or update the definitions and the RBAC for the Traefik custom resources. The URLs above name v3.8; use the version that matches your Traefik release. `allowCrossNamespace` (default false) lets IngressRoutes reference resources in other namespaces, and `namespaces` limits the namespaces watched (empty watches all).

## Checked
2026-11-03. Confirmed against the Traefik Kubernetes CRD provider reference page: Helm default, the definition and RBAC `kubectl apply` URLs (v3.8), `namespaces` and `allowCrossNamespace`. Removed: the claims about validation and listing failures after an upgrade, the namespace-scoping hedge and the kubectl Verify step.
Method: documentation only; no commands were run.


