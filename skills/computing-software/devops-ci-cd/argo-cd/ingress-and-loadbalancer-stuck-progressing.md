---
id: computing-software.devops-ci-cd.argo-cd.ingress-and-loadbalancer-stuck-progressing
name: ingress-and-loadbalancer-stuck-progressing
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, ingress-progressing, health-status-progressing, resource-health]
level: practitioner
status: docs-checked
description: "Fix Argo CD apps stuck Progressing because an Ingress or LoadBalancer Service never gets status.loadBalancer: controller publish settings, ingress class, overriding health."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/health/#ingress", "https://argo-cd.readthedocs.io/en/stable/faq/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ingress and LoadBalancer stuck Progressing

Argo marks `Ingress` and `Service type=LoadBalancer` Healthy only when
`status.loadBalancer.ingress` has at least one entry. If it stays empty the app stays Progressing.

## Causes and fixes
The Argo CD docs note that some ingress controllers (they name contour and traefik) do not update `status.loadBalancer.ingress`, so the Ingress stays Progressing. Check that your controller publishes an address to the Ingress status, that a controller claims the Ingress (`ingressClassName`), and, for a Service, that the cloud load balancer was provisioned (`kubectl describe svc` events). Fix status publishing first.

## Override health when status is never set
```yaml
# argocd-cm
resource.customizations.health.networking.k8s.io_Ingress: |
  hs = {}
  hs.status = "Healthy"
  hs.message = "Ingress health not tracked"
  return hs
```
Scope narrowly: better to fix publishing than to blanket-mark all ingresses healthy.

## Check
```bash
kubectl get ingress -A -o wide          # ADDRESS column empty?
kubectl get svc -A | grep pending
```

## Verify
- [ ] ADDRESS populated; app turns Healthy without overrides.

## Checked
2026-10-28. Confirmed on the Argo CD health page and FAQ: Ingress and Service LoadBalancer health depends on a non-empty `status.loadBalancer.ingress` with a hostname or IP; some ingress controllers (contour, traefik) do not update it, leaving the Ingress Progressing; custom health overrides use `resource.customizations.health.<group>_<kind>` with `hs.status` and `hs.message`.
Removed (not confirmed): the controller-specific flags (`--publish-service`, Helm values, Traefik `ingressEndpoint`), MetalLB and kube-vip advice, and the `argocd app wait --health` timeout remark.

Method: documentation only; no commands were run.
