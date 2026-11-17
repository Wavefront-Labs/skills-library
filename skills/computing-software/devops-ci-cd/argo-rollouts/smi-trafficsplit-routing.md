---
id: computing-software.devops-ci-cd.argo-rollouts.smi-trafficsplit-routing
name: smi-trafficsplit-routing
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [smi, trafficsplit, service-mesh-interface, linkerd, rootservice, traffic-routing, argo-rollouts]
level: advanced
status: docs-checked
description: "Drive an SMI TrafficSplit from a canary Rollout, noting that the SMI spec is archived."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/smi/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Service Mesh Interface (SMI) is a standard API implemented by meshes such as Linkerd. The docs note that the CNCF archived the SMI spec and recommend looking at Gateway API, Project Gamma and the Argo Rollouts Gateway API plugin instead.

With SMI the controller creates and manipulates a TrafficSplit. You provide canary and stable Services and optionally a root Service and a split name:

```yaml
canary:
  canaryService: canary-svc
  stableService: stable-svc
  trafficRouting:
    smi:
      rootService: root-svc                           # optional
      trafficSplitName: rollout-example-traffic-split # optional
```

How it works: the controller first adds the ReplicaSet pod template hash to each Service selector so canary and stable Services reach only their ReplicaSets. It then creates a TrafficSplit whose backends are those two Services, with weights taken from the current canary step. The TrafficSplit root service is `stableService` unless `rootService` is set. If `trafficSplitName` is omitted the Rollout name is used. If a TrafficSplit of that name exists and is not owned by the Rollout, the Rollout enters an error state.

Clients must call the root Service so the mesh can apply the split.

If you are starting fresh, prefer a Gateway API plugin (see traffic-router-plugins) over SMI.

The controller defaults to the `v1alpha1` TrafficSplit API version; the `--traffic-split-api-version` controller flag changes it.

Verify: the TrafficSplit's backend weights track the rollout steps.

## Checked

2026-11-08. Confirmed against the Argo Rollouts SMI page (read in full): archived SMI spec notice, TrafficSplit creation, selector hash updates, root service and name defaults, error state on foreign TrafficSplit, default v1alpha1 API version.

Removed or corrected: replaced the unsourced kubectl get trafficsplit verify command.

Method: documentation only; no commands were run.
