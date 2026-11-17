---
id: computing-software.cloud-infrastructure-engineering.longhorn.install-with-kubectl
name: install-with-kubectl
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [kubectl, install, manifest, longhorn-system, ui-access]
level: intro
status: docs-checked
description: "Install Longhorn 1.13.0 from the release manifest with kubectl, watch pods in longhorn-system and choose an Ingress or HTTPRoute for the UI."
sources:
  - https://longhorn.io/docs/1.13.0/deploy/install/install-with-kubectl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: install Longhorn from the YAML manifest.

Each node must meet the installation requirements; optionally run `longhornctl` to check for issues.

```bash
kubectl apply -f https://raw.githubusercontent.com/longhorn/longhorn/v1.13.0/deploy/longhorn.yaml
kubectl get pods --namespace longhorn-system --watch
kubectl -n longhorn-system get pod
```

Expect `Running` pods including `longhorn-ui`, `longhorn-manager`, `longhorn-global-manager`, `longhorn-driver-deployer`, `longhorn-csi-plugin`, the `csi-*` components, `instance-manager` and `engine-image`.

UI: authentication is not enabled by default. Set up an Ingress controller. The install page itself mentions NGINX with basic auth; separate pages under Accessing the UI cover Traefik with basic auth and Gateway API HTTPRoute.

Then follow the Accessing the UI steps.

Kubernetes below v1.25 with Pod Security Policy enabled also needs:

```bash
kubectl apply -f https://raw.githubusercontent.com/longhorn/longhorn/master/deploy/podsecuritypolicy.yaml
```

Use the Helm install instead when you want to customise settings through chart values.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/deploy/install/install-with-kubectl/

Changed: the cited page mentions only NGINX; Traefik and HTTPRoute are described as separate pages under Accessing the UI.

Method: documentation only; no commands were run.
