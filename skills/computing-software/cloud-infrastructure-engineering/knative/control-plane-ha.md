---
id: computing-software.cloud-infrastructure-engineering.knative.control-plane-ha
name: control-plane-ha
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [high-availability, leader-election, disable-ha, activator-hpa, replicas]
level: advanced
status: docs-checked
description: "Scale controllers for HA, disable leader election and size the activator HPA."
sources:
  - https://knative.dev/docs/serving/config-ha/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep the Serving control plane and activator available through disruptions.

Active/passive HA uses leader election: controller instances run in advance and compete for a shared lock; the holder serves while the others stand by. Leader election is enabled by default for all Serving components, but HA is effectively off by default because each component runs one replica.

Disable leader election by passing `--disable-ha`; the option goes away when HA graduates to stable.

Control plane: for any deployment in `knative-serving` (or `kourier-system`) except the activator:

```bash
kubectl -n knative-serving scale deployment <deployment-name> --replicas=2
```

Two replicas enable HA, higher values add more (for example 3 controllers), and one disables HA. Scaling down the autoscaler may give inaccurate autoscaling for some Revisions for up to the `stable-window`, because ownership of its Revisions moves when a pod terminates.

Data plane: the activator is scaled by a Kubernetes HPA. Inspect it with `kubectl get hpa activator -n knative-serving`. Default minReplicas and maxReplicas are `1` and `20`. Change them with:

```bash
kubectl patch hpa activator -n knative-serving -p '{"spec":{"minReplicas":9,"maxReplicas":19}}'
```

Set both equal to pin a value. Run at least 3 activators in production to avoid a single point of failure when scaling from zero.

## Checked

2026-11-04. Confirmed against the Serving high-availability configuration page (knative/docs source): leader election on by default with one replica per component, `--disable-ha` and its removal when HA is stable, scaling any deployment in `knative-serving` or `kourier-system` except the activator, 2 replicas enables HA and 1 disables it, the autoscaler `stable-window` caveat, the activator HPA defaults of `1` and `20`, the patch command, and the recommendation of at least 3 activators. Nothing removed.

Method: documentation only; no commands were run.
