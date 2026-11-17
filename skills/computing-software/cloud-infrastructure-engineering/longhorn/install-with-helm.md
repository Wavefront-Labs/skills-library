---
id: computing-software.cloud-infrastructure-engineering.longhorn.install-with-helm
name: install-with-helm
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [helm, install, longhorn-system, ingress, psp]
level: intro
status: docs-checked
description: "Install Longhorn 1.13.0 with Helm into longhorn-system, verify pods, and note the unauthenticated UI and the PSP value for old clusters."
sources:
  - https://longhorn.io/docs/1.13.0/deploy/install/install-with-helm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: install Longhorn with Helm.

Prerequisites: a Kubernetes cluster whose nodes meet the installation requirements, and Helm v3.0 or later. Optionally run `longhornctl` to check the environment first.

```bash
helm repo add longhorn https://charts.longhorn.io
helm repo update
helm install longhorn longhorn/longhorn \
  --namespace longhorn-system --create-namespace --version 1.13.0
kubectl -n longhorn-system get pod
```

Customise initial settings with Helm options or by editing the deployment configuration file.

Kubernetes older than v1.25 with the Pod Security Policy admission controller enabled: set the Helm value `enablePSP` to `true` to install the `longhorn-psp` PodSecurityPolicy.

UI access: authentication to the Longhorn UI is not enabled by default. Set up an Ingress controller; for NGINX with basic auth see the Longhorn guide for creating an Ingress with basic authentication. Then follow the Accessing the UI steps.

Check that all pods reach `Running` before creating volumes.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/deploy/install/install-with-helm/

No claim needed changing.

Method: documentation only; no commands were run.
