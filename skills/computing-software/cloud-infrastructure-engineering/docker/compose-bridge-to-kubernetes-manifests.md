---
id: computing-software.cloud-infrastructure-engineering.docker.compose-bridge-to-kubernetes-manifests
name: compose-bridge-to-kubernetes-manifests
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose-to-kubernetes, compose-bridge, kustomize, kubernetes-migration, docker-desktop]
level: advanced
status: docs-checked
description: "Convert Compose apps to Kubernetes with Docker Compose Bridge: docker compose bridge convert, the Docker Desktop kustomize overlay, custom transformation images and review points."
sources: ["https://docs.docker.com/compose/bridge/", "https://docs.docker.com/compose/bridge/usage/", "https://docs.docker.com/compose/bridge/customize/", "https://docs.docker.com/reference/cli/docker/compose/bridge/convert/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compose Bridge to Kubernetes manifests

Compose Bridge converts a Compose model into deployment formats such as Kubernetes
manifests plus a Kustomize overlay. It requires Docker Desktop 4.43.0 or later (per the
Docker docs feature banner). A transformation is a Docker image that receives the fully
resolved Compose model as `/in/compose.yaml` and writes any files under `/out`. The default
transformation is `docker/compose-bridge-kubernetes`, built on Go templates that you can
replace or extend.

## Convert
```bash
docker compose bridge convert                 # reads compose.yaml in the current directory
kubectl apply -k out/overlays/desktop/        # needs Kubernetes enabled in Docker Desktop
```
Output goes to `out/` by default (`-o`/`--output` changes it). Other `convert` flags:
`-t`/`--transformation` (repeatable), `--templates` (directory of templates) and `-y`/`--yes`
(accept the output-directory overwrite prompt in scripts).

The default transformation produces, per the usage page: a Namespace, a ConfigMap entry per
Compose config, Deployments for services, Services for exposed ports, `LoadBalancer`
Services for published ports, NetworkPolicies replicating the Compose network topology,
PersistentVolumeClaims for volumes (the `hostpath` storage class so Docker Desktop manages
them) and Secrets. It also supplies a Kustomize overlay for Docker Desktop. The generated
Secrets are described as designed for local use in a testing environment.

## Customise
```bash
docker compose bridge transformations create --from docker/compose-bridge-kubernetes my-template
# edit the extracted templates (Go template syntax), then package the image
docker build --tag mycompany/transform --push .
docker compose bridge convert --transformation mycompany/transform
```
`transformations create` extracts the templates into a directory named after your template,
with a Dockerfile you use to build your own transformation image. You can pass
`--transformation` more than once to apply several transformations (for example the default
plus one that adds Ingress objects from `x-` extension attributes). Template helper
functions include `seconds`, `uppercase`, `title`, `safe`, `truncate`, `join`, `base64`,
`map`, `indent` and `helmValue`. A transformation can also wrap another tool (the docs show
a Kompose-based one) as long as it reads `/in/compose.yaml` and writes under `/out`.

## Review before production
- Probes: map healthchecks to readiness and liveness probes deliberately; the default
  output is aimed at local Docker Desktop use.
- Resources: set requests and limits.
- Storage: the default PVCs use the Docker Desktop `hostpath` storage class; choose real
  storage classes and access modes for a cluster.
- Secrets: generated Secrets carry your values (encoded); do not commit them, use your
  secret manager.
- Security context: add runAsNonRoot, readOnlyRootFilesystem and dropped capabilities
  through a custom transformation.

## Gotchas
- Check `docker compose bridge convert --help` for the flags in your Docker Desktop
  version.
- Services that only have `build:` need images pushed to a registry the cluster can pull
  from (Kubernetes pulls images, it does not build them).

## Checked
Date 2026-10-23. Method: documentation only; no commands were run.
Docker docs (docker/docs main) Compose Bridge overview, usage and customize pages, and the
Compose v5.6.1 `docker compose bridge convert` reference: `convert` options (`-o` default
`out`, `--templates`, `-t`/`--transformation`, `-y`), `/in/compose.yaml` and `/out` contract,
default transformation image name, the resources the default transformation produces, the
`kubectl apply -k out/overlays/desktop/` step, `transformations create --from`, helper
function list, and the Docker Desktop 4.43.0 requirement. Removed: the `base/` directory
layout, the `my-template/templates` path, the `compose-bridge-company` registry example and
probe and resource-mapping claims that the docs do not make.
