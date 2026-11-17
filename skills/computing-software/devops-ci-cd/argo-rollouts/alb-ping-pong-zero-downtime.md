---
id: computing-software.devops-ci-cd.argo-rollouts.alb-ping-pong-zero-downtime
name: alb-ping-pong-zero-downtime
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [aws, alb, pingpong, readiness-gates, zero-downtime, canary, argo-rollouts]
level: sme
status: docs-checked
description: "Use the ping-pong service pair so ALB pod readiness gates still work during canary promotion."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/alb/
  - https://argo-rollouts.readthedocs.io/en/stable/features/specification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
AWS recommends pod readiness gate injection for the AWS Load Balancer Controller in IP mode. The catch is that changing a Service `spec.selector` prevents the controller from mutating readiness gates onto pods. Normal promotion changes the stable Service selector, so gates are lost.

The ping-pong feature (since v1.2) avoids selector changes. Two persistent Services alternate roles: at any moment one acts as stable and the other as canary. At the end of promotion 100% of traffic goes to the canary Service (say pong), and then the Rollout swaps roles so pong becomes the stable Service. Selectors keep their labels throughout, so readiness gates can be injected. The Rollout status tracks the stable one in `status.canary.currentPingPong`.

```yaml
strategy:
  canary:
    pingPong:
      pingService: ping-service
      pongService: pong-service
    trafficRouting:
      alb:
        ingress: ingress
        servicePort: 80
        rootService: root-service   # required when ping-pong is enabled
```

When `pingPong` is set, `canaryService` and `stableService` are not required. The spec comments say it supports ALB, Istio and plugin-based routers, intended for zero-downtime rollouts of long-lived TCP or gRPC connections.

Verify with `kubectl get rollout NAME -o jsonpath='{.status.canary.currentPingPong}'` before and after a promotion; it should flip.

## Checked
2026-11-08. Confirmed against the Argo Rollouts ALB page and Rollout Specification page: readiness gate injection and the selector-change problem, ping-pong since v1.2, the role swap and `status.canary.currentPingPong`, the `pingPong` fields, `rootService` required with ping-pong, no need for `canaryService` and `stableService`, and ALB, Istio and plugin router support. Nothing removed.
Method: documentation only; no commands were run.
