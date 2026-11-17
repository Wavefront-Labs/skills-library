---
id: computing-software.cloud-infrastructure-engineering.metallb.install-by-manifest-or-kustomize
name: install-by-manifest-or-kustomize
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, manifest, kustomize, install, frr-k8s, native, metallb-system, controller, speaker]
level: practitioner
status: docs-checked
description: "Install MetalLB with plain manifests or Kustomize for the FRR-K8s, native or deprecated FRR backend, what components appear, and why to pin a stable release."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/installation/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install by manifest or Kustomize

Manifests (from the main branch):
```bash
# FRR-K8s mode (recommended)
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/main/config/manifests/metallb-frr-k8s.yaml
# Native mode: lightweight, built-in BGP (no BFD, no IPv6 BGP)
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/main/config/manifests/metallb-native.yaml
# FRR mode (deprecated)
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/main/config/manifests/metallb-frr.yaml
```
These deploy from the main development branch; the docs urge cloud operators to deploy a stable released version in production.

Kustomize (`kustomization.yml`):
```yaml
namespace: metallb-system
resources:
  - github.com/metallb/metallb/config/frr-k8s?ref=main
```
Use `config/native` or `config/frr` (deprecated) for the other backends.

Result in namespace `metallb-system`: `controller` Deployment (assigns IPs), `speaker` DaemonSet (speaks the protocols), service accounts and RBAC. No configuration is included, so MetalLB stays idle until you apply CRs (`computing-software.cloud-infrastructure-engineering.metallb.ipaddresspool-definition`).

With Pod Security enforcement see `computing-software.cloud-infrastructure-engineering.metallb.pod-security-privileged-namespace`.

## Checked

2026-11-04. Confirmed against the MetalLB Installation page (manifest URLs, FRR-K8s recommended, native has no BFD or IPv6 BGP, FRR deprecated, main-branch warning, kustomize resource paths, components under metallb-system, no configuration included). Removed the unsupported "replace main with a release ref" instruction and the generic Check line.

Method: documentation only; no commands were run.
