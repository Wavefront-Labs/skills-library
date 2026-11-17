---
id: computing-software.devops-ci-cd.argo-rollouts.alb-ingress-traffic-routing
name: alb-ingress-traffic-routing
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [aws, alb, ingress, aws-load-balancer-controller, weighted-target-groups, rootservice, argo-rollouts]
level: advanced
status: docs-checked
description: "Use the AWS Load Balancer Controller for canary traffic splitting with an action annotation injected into the Ingress."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/alb/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requires AWS Load Balancer Controller v1.1.5 or newer. An ALB splits traffic with weighted target groups; the controller supports this through the annotation `alb.ingress.kubernetes.io/actions.<service-name>`, which Argo Rollouts injects and updates with the desired weights.

```yaml
canary:
  canaryService: canary-service
  stableService: stable-service
  trafficRouting:
    alb:
      ingress: ingress          # or ingresses: [a, b]
      servicePort: 443
      rootService: root-service  # optional
```

The Ingress rule must target the service named by `rootService` (or `stableService` if omitted) with `port.name: use-annotation`, which tells the AWS controller to read the action annotation. Rollouts also adds `rollouts.argoproj.io/managed-alb-actions` for bookkeeping; on Rollout deletion the action reverts to 100% stable.

`rootService` supports a pattern of one Ingress with three rules to reach canary, stable and root separately for testing.

Other options: `annotationPrefix` when your AWS controller uses a custom `--annotations-prefix`; a custom ingress class; sticky sessions need target group stickiness configured, since two target groups are used.

Blue-green with ALB cannot avoid a chance of downtime because the controller does not update target groups atomically.

Verify: `kubectl get ingress ingress -o yaml` shows the action JSON with canary and stable weights.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/alb/, https://argo-rollouts.readthedocs.io/en/stable/features/specification/.

Removed or corrected: nothing; claims matched.

Method: documentation only; no commands were run.
