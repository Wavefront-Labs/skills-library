---
id: computing-software.cloud-infrastructure-engineering.docker.loading-local-images-into-kind-and-k3d
name: loading-local-images-into-kind-and-k3d
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, kubernetes-migration, kind-load, k3d, minikube, local-registry, imagepullpolicy]
level: practitioner
status: docs-checked
description: "Test locally built images on kind, k3d or minikube without pushing: kind load, k3d image import, local registries, imagePullPolicy pitfalls with :latest, and multi-arch notes."
sources: ["https://kind.sigs.k8s.io/docs/user/quick-start/#loading-an-image-into-your-cluster", "https://kind.sigs.k8s.io/docs/user/local-registry/", "https://k3d.io/stable/usage/commands/k3d_image_import/", "https://minikube.sigs.k8s.io/docs/handbook/pushing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loading local images into kind and k3d

Cluster nodes run their own containerd; they cannot see images in your Docker image store.

## kind
```bash
docker build -t app:dev .
kind load docker-image app:dev --name dev           # copies into every node of cluster "dev"
kind load image-archive app.tar --name dev          # from docker save output
docker exec -it dev-control-plane crictl images | grep app
```

## k3d
```bash
k3d image import app:dev -c dev
```

## minikube
```bash
minikube image load app:dev
# or build straight into the cluster's daemon/containerd
minikube image build -t app:dev .
```
minikube's docs: the default runtime is containerd, and `imagePullPolicy: Always` must be
turned off (`IfNotPresent` or `Never`) or locally built images are not used.

## Checked
2026-10-31. Confirmed: kind quick-start loading section (`kind load docker-image`, `image-archive`, `--name`, `crictl images`, pull-policy note) and local-registry page (port 5001, `hosts.toml`); minikube pushing handbook (`image load`, `image build`, pull policy). Removed: k3d registry commands (the import page read does not cover them), the multi-arch, containerd-store and Tilt/Skaffold notes, and `rollout restart` advice.
Method: documentation only; no commands were run.

## The imagePullPolicy trap
- Tag `:latest` (or no tag) defaults to `imagePullPolicy: Always` (otherwise `IfNotPresent`):
  the node tries to pull and fails even though you loaded the image.
- Use a non-latest tag (`app:dev`, `app:$(git rev-parse --short HEAD)`) or set
  `imagePullPolicy: IfNotPresent` / `Never` explicitly.
- kind's docs advise a unique tag per build (`kind load docker-image my-custom-image:unique-tag`).

## Local registry for kind (faster for frequent rebuilds)
The kind local-registry page provides a script that runs a registry on port 5001, connects it
to the cluster network and writes containerd `hosts.toml` on nodes; then `docker push
localhost:5001/app:dev` and use `localhost:5001/app:dev` in manifests.

## Gotchas
