---
id: computing-software.devops-ci-cd.argo-rollouts.nginx-ingress-traffic-routing
name: nginx-ingress-traffic-routing
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [nginx, ingress, canary-weight, stableingress, annotations, traffic-routing, argo-rollouts]
level: advanced
status: docs-checked
description: "Route canary traffic with NGINX Ingress by creating a canary Ingress with canary and canary-weight annotations."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/nginx/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The NGINX Ingress Controller sends traffic directly to pods through Ingress objects. Argo Rollouts creates a second, canary Ingress next to your stable one and updates its annotations as steps progress.

```yaml
canary:
  canaryService: canary-service   # required
  stableService: stable-service
  trafficRouting:
    nginx:
      stableIngress: primary-ingress   # or stableIngresses, not both
      annotationPrefix: customingress.nginx.ingress.kubernetes.io   # optional
      additionalIngressAnnotations:
        canary-by-header: X-Canary
        canary-by-header-value: iwantsit
      canaryIngressAnnotations:
        my-custom-annotation.mygroup.com/key: value
```

The controller always sets the annotations `canary: true` and `canary-weight: <num>` on the canary Ingress, using the default `nginx.ingress.kubernetes.io` prefix unless you set `annotationPrefix`. Weight is 0 when all traffic goes to stable.

`additionalIngressAnnotations` adds prefixed annotations (header or cookie routing); `canaryIngressAnnotations` adds full custom annotations of any group, and wins on collision.

The stable Ingress must be in the Rollout's namespace and route to the stable Service; the Rollout checks that.

Since v1.5, `stableIngresses` supports several NGINX controllers pointing at one service. By default the controller acts only on Ingresses with class or `ingressClassName` `nginx`; use `--nginx-ingress-classes` to change it (an empty string acts on Ingresses with no class).

`maxTrafficWeight` is supported for NGINX to change the weight denominator.

Verify: `kubectl get ingress -o yaml` shows the generated canary Ingress with its `canary-weight` annotation.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/nginx/, https://argo-rollouts.readthedocs.io/en/stable/features/specification/.

Removed or corrected: quoting of the canary annotation value; the claim that kubectl get ingress lists the weight.

Method: documentation only; no commands were run.
