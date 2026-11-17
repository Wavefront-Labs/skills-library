---
id: computing-software.networking-hardware-and-wireless.traefik.provider-kubernetes-ingress-and-gateway
name: provider-kubernetes-ingress-and-gateway
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, kubernetes-ingress, gateway-api, httproute, ingress, provider]
level: practitioner
status: docs-checked
description: "Choose between the Traefik Kubernetes Ingress and Gateway API providers and enable each, noting the experimentalChannel CRD requirement."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/providers/kubernetes/kubernetes-ingress.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/providers/kubernetes/kubernetes-gateway.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# provider kubernetes ingress and gateway
The `kubernetesIngress` provider implements the Ingress spec. Its limits: the `spec.rules.http.paths.backend.resource` form is not supported, so use `backend.service`; and the Ingress API is frozen, so the docs recommend the Gateway provider for new work. The `kubernetesGateway` provider implements the Gateway API standard channel (v1.6.3 in these docs), supporting HTTPRoute core features and some extended ones such as `BackendTLSPolicy`, `GRPCRoute`, `ListenerSet` and `TLSRoute`.

```bash
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.6.3/standard-install.yaml
```
```yaml
providers:
  kubernetesIngress: {}
  kubernetesGateway: {}
```
Gotcha: the `experimentalChannel` option makes Traefik watch `TCPRoute` and `TLSRoute`, which need the Experimental channel CRDs (`experimental-install.yaml`). Enabling it without them prevents the Kubernetes Gateway provider from starting, so no Gateway API resource is served at all, not only `TCPRoute` and `TLSRoute`.

## Checked
2026-11-03. Confirmed against the Traefik Kubernetes Ingress and Gateway provider reference pages: the unsupported `backend.resource` form, the frozen Ingress API and Gateway recommendation, Gateway API standard v1.6.3 with its supported resources, and the `experimentalChannel` warning. Removed: the claim that other providers keep running and the kubectl Verify step.
Method: documentation only; no commands were run.


