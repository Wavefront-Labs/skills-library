---
id: computing-software.devops-ci-cd.argo-rollouts.istio-subset-level-traffic-splitting
name: istio-subset-level-traffic-splitting
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [istio, destinationrule, subsets, virtualservice, traffic-splitting, canarysubsetname, argo-rollouts]
level: advanced
status: docs-checked
description: "Split traffic between Istio DestinationRule subsets using one unmodified Service."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/istio/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Subset-level splitting (available since v1.0) uses a single Service that targets the Rollout pods and is not modified by the controller. You deploy a Rollout, a Service, a VirtualService and a DestinationRule.

```yaml
trafficRouting:
  istio:
    virtualService:
      name: rollout-vsvc
      routes:
        - primary
    destinationRule:
      name: rollout-destrule
      canarySubsetName: canary
      stableSubsetName: stable
```

The VirtualService route has two destinations with the same `host` and `subset` values equal to the two subset names, weights starting at 100 (stable) and 0 (canary). The DestinationRule declares both subsets with labels:

```yaml
spec:
  host: rollout-example
  subsets:
    - name: canary
      labels: {app: rollout-example}
    - name: stable
      labels: {app: rollout-example}
```

During the update the controller changes the VirtualService weights and injects the canary and stable `rollouts-pod-template-hash` labels into the DestinationRule subsets.

The docs also allow additional subset DestinationRules, for example to send another API path to a service run by Argo Rollouts and a service using an experimental image.

Choose subset-level when you do not want the controller changing Service selectors. Choose host-level for parity with other routers.

Verify: `kubectl get destinationrule rollout-destrule -o yaml` shows hash labels on both subsets mid-rollout.

## Checked
2026-11-08. Confirmed against the Argo Rollouts Istio page: subset-level splitting since v1.0, the unmodified single Service, the Rollout, VirtualService and DestinationRule fields, initial weights, hash label injection into subsets, and additional subset DestinationRules. Nothing removed.
Method: documentation only; no commands were run.
