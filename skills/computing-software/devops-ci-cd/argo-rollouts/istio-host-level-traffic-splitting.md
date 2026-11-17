---
id: computing-software.devops-ci-cd.argo-rollouts.istio-host-level-traffic-splitting
name: istio-host-level-traffic-splitting
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [istio, virtualservice, host-level, traffic-splitting, canaryservice, stableservice, argo-rollouts]
level: advanced
status: docs-checked
description: "Split canary traffic with Istio by weighting a VirtualService between canary and stable Services."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/istio/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Host-level splitting needs a Rollout, a canary Service, a stable Service and a VirtualService.

```yaml
strategy:
  canary:
    canaryService: canary-svc     # required
    stableService: stable-svc     # required
    trafficRouting:
      istio:
        virtualService:
          name: rollout-vsvc      # required
          routes:
            - primary             # optional if one route, required otherwise
```

The VirtualService needs an HTTP route named as referenced, with two destinations whose `host` values match `canaryService` and `stableService`. Istio requires weights to total 100, so start with stable 100 and canary 0:

```yaml
http:
  - name: primary
    route:
      - destination: {host: stable-svc}
        weight: 100
      - destination: {host: canary-svc}
        weight: 0
```

If the VirtualService is in a different namespace, reference it as `rollout-vsvc.<namespace>`; likewise include the namespace in destination hosts.

During an update the controller keeps changing the canary and stable Service selectors to the matching `rollouts-pod-template-hash`, and rewrites `spec.http[].route[].weight` to the desired canary weight. It makes no other assumptions, so you can add rewrites or other VirtualService config.

Only traffic inside the mesh follows the strategy; pods excluded (for example `sidecar.istio.io/inject="false"`) follow default Kubernetes balancing.

Verify with `kubectl get virtualservice rollout-vsvc -o yaml` while paused at a weight step.

## Checked
2026-11-08. Confirmed against the Argo Rollouts Istio page: required resources and Rollout fields, the VirtualService route and destination hosts, weights totalling 100, namespace-qualified names, the controller selector and weight updates, the freedom to add other VirtualService config, and the in-mesh-only note. Nothing removed.
Method: documentation only; no commands were run.
