---
id: computing-software.cloud-infrastructure-engineering.istio.istio-configuration-profiles
name: istio-configuration-profiles
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, istio-profiles, profiles, demo-profile]
level: practitioner
status: docs-checked
description: "Pick the right Istio deployment and platform profile (default, demo, minimal, remote, ambient, empty, preview) and layer --set overrides after them."
sources: ["https://istio.io/latest/docs/setup/additional-setup/config-profiles/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Profiles are named groups of Helm value overrides built into the charts; they work with both helm and istioctl. There are two kinds, and using both is recommended: deployment profiles (`default`, `demo`, `minimal`, `remote`, `ambient`, `empty`, `preview`) and platform profiles (`gke`, `eks`, `openshift`, `k3d`, `k3s`, `microk8s`, `minikube`).

```sh
istioctl install --set profile=default --set values.global.platform=gke
helm install istiod istio/istiod -n istio-system --set profile=default --set global.platform=gke --wait
```

What each deployment profile is for (from the page):
- `default`: recommended for production and for primary clusters in a multicluster mesh.
- `demo`: showcases features with modest resources and is what the quick start installs; it enables high tracing and access logging, so it is not suitable for performance tests.
- `minimal`: same as default but only the control plane, so gateways can be configured with separate profiles.
- `remote`: a remote cluster managed by an external control plane or a primary cluster's control plane.
- `ambient`: for getting started with ambient mode.
- `empty`: deploys nothing; a base for custom configuration.
- `preview`: experimental features; stability, security and performance are not guaranteed.

Component selection (istioctl only): `default` installs istiod and istio-ingressgateway; `demo` adds istio-egressgateway; `minimal` installs only istiod; `ambient` installs istiod, CNI and ztunnel. With helm you install each component yourself, passing the same profile and platform to every chart.

Gotcha: a `--set` flag placed after the profile overrides any value the profile sets, so put your overrides after `profile=`.

## Checked

2026-11-03. Confirmed against the Istio Installation Configuration Profiles page: profile names and descriptions, the component table, helm and istioctl examples, override ordering. Removed: the `istioctl profile dump/diff` verify steps, the claim that an earlier flag is overwritten, `kubectl get deploy` verify step and the drift-record advice.
Method: documentation only; no commands were run.
