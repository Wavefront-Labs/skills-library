---
id: computing-software.cloud-infrastructure-engineering.kubernetes.feature-gates-lifecycle-and-enabling
name: feature-gates-lifecycle-and-enabling
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, feature-gates, feature-gate-lifecycle, alpha-features, beta-features, kubeadm, version-skew]
level: advanced
status: docs-checked
description: "Enable/disable Kubernetes feature gates consistently across apiserver, controller-manager, scheduler and kubelet, and plan for the alpha-beta-GA-removal lifecycle on upgrades."
sources: ["https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/", "https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates-removed/", "https://kubernetes.io/docs/tasks/administer-cluster/configure-feature-gates/", "https://kubernetes.io/docs/reference/using-api/deprecation-policy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Feature gates: lifecycle and enabling

## Lifecycle you plan against
| Stage | Default | Meaning |
|---|---|---|
| Alpha | off | may be buggy; support can be dropped without notice; short-lived test clusters only |
| Beta | usually on (beta API groups are off by default) | well tested; details may still change |
| GA (stable) | always on | cannot be disabled; the gate is no longer needed |
| Removed | - | no longer recognized as a valid feature gate |

The configure-feature-gates page notes that some GA gates can still be disabled, usually for one
minor release after GA, at the cost of conformance. Removed gates are listed on the
"feature gates removed" page; GA and deprecated gates are still recognized but change nothing.
The upgrade trap: a gate you set explicitly long ago may be removed in the target release, so
grep manifests and kubelet config for every explicit gate against the target release's tables
before each upgrade, and confirm a stale gate name does not stop a component starting.

## Setting gates per component
Each component reads its own gates; they are **not** shared. A feature spanning API and node must be
enabled on every relevant component, or you may see unexpected behaviour or errors. Replace
`FeatureName` below with a gate that is Alpha or Beta in your release (check the tables):
```yaml
# kubeadm ClusterConfiguration (v1beta4)
apiServer:
  extraArgs:
  - {name: feature-gates, value: "FeatureName=true"}
controllerManager:
  extraArgs:
  - {name: feature-gates, value: "FeatureName=true"}
scheduler:
  extraArgs:
  - {name: feature-gates, value: "FeatureName=true"}
---
# KubeletConfiguration
featureGates:
  FeatureName: true
```
kube-proxy takes gates in its ConfigMap (`featureGates:`) followed by a DaemonSet restart. Beta
features also need their API resources enabled with `--runtime-config` on the apiserver (beta
APIs are off by default since 1.24).

## Inspecting what is on
```bash
kubectl get --raw /metrics | grep kubernetes_feature_enabled      # metric available since 1.26; 1 = on, 0 = off
kubectl get --raw /api/v1/nodes/<node>/proxy/metrics | grep kubernetes_feature_enabled
kubectl get --raw /api/v1/nodes/<node>/proxy/configz | grep featureGates -A 5
```
With the `ComponentFlagz` gate on, a component's `/flagz` endpoint shows the flags it started with.

## Managed clusters
Managed control planes usually do not let you set control-plane gates; check the provider's
documentation.

## Gotchas
- Gates must agree across all replicas of a component and across the components that share a
  feature; verify with the metric on each apiserver and kubelet.
- Test disabling a gate as a rollback path in a non-production cluster before relying on it.

## Verify
- [ ] Pre-upgrade grep of manifests and kubelet config finds no gate removed in the target release.
- [ ] `kubernetes_feature_enabled` shows the same value on every apiserver and kubelet.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm source: feature-gates page (alpha, beta and GA meaning, beta APIs off by default, removed gates unrecognized), configure-feature-gates task page (kubeadm v1beta4 and kubelet examples, kube-proxy ConfigMap, kubernetes_feature_enabled since 1.26, configz, /flagz with ComponentFlagz, GA gates sometimes disableable for one release), kubeadm v1beta4 types (extraArgs is a list of name/value pairs) and per-gate stage data (InPlacePodVerticalScaling is GA from 1.35, so it was dropped as an example). Removed unconfirmed claims about removal timing, managed-cluster specifics and data pruning.

Method: documentation only; no commands were run.
