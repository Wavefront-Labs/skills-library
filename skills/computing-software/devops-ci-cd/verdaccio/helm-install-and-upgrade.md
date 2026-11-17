---
id: computing-software.devops-ci-cd.verdaccio.helm-install-and-upgrade
name: helm-install-and-upgrade
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [helm, kubernetes, chart, helm-chart, charts-verdaccio-org, image-tag, helm-upgrade]
level: practitioner
status: docs-checked
description: "Deploy Verdaccio on Kubernetes with the official Helm 3 chart: add the repo, install, pin image.tag, upgrade, uninstall, and run a local example."
sources:
  - https://verdaccio.org/docs/kubernetes/
  - https://verdaccio.org/docs/installation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Helm 3 is assumed (no Tiller). The chart lives in `verdaccio/charts`.

```
helm repo add verdaccio https://charts.verdaccio.org
helm repo update
helm install npm verdaccio/verdaccio          # release name npm
```
Pin the image with `image.tag` (see the Docker tags):
```
helm install npm --set image.tag=6 verdaccio/verdaccio
helm install npm --set image.tag=6.10.3 verdaccio/verdaccio
helm install npm --set image.tag=7.x-next verdaccio/verdaccio
```
Upgrade and remove:
```
helm upgrade npm verdaccio/verdaccio
helm uninstall npm      # deletes all resources, including published packages
```
Start from the worked example `docker-examples/v7/kubernetes/helm` (a `values.yaml` and README with persistence, resource limits, an Ingress block and an inline `config.yaml`; it pins the 7.x-next image, change `image.tag` to 6 for the stable line). It also works for a local cluster.

Gotchas:
- The NGINX ingress default body-size is 1MB (see helm-custom-config-and-secrets).

Rancher users can see the community `verdaccio-rancher` project.

## Checked

2026-11-04. Confirmed against the Verdaccio Kubernetes and Installation pages (chart repo, Helm 3 without Tiller, release name, image.tag forms, upgrade, uninstall deleting packages, docker-examples/v7/kubernetes/helm, 1MB NGINX ingress body size, verdaccio-rancher). Removed: the unsupported claim that uninstall spares packages when storage persists outside the release.
Method: documentation only; no commands were run.
