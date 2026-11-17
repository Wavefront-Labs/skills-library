---
id: computing-software.devops-ci-cd.tilt.tilt-choosing-clusters
name: tilt-choosing-clusters
category: computing-software
field: devops-ci-cd
product: tilt
tags: [choosing-clusters, tilt, kubernetes, local-cluster]
level: practitioner
status: docs-checked
description: "Pick a Kubernetes cluster for Tilt development and make Tilt accept it: allow remote contexts, and configure registry discovery."
sources:
  - "https://docs.tilt.dev/choosing_clusters.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a Tilt dev cluster

Goal: pick a cluster that suits the team, then make Tilt accept it and find its image registry.

## Picking one

- Kind: runs Kubernetes in a Docker container; creating a cluster takes about 20 seconds. Use `ctlptl` to set it up with a registry. Without a registry Tilt falls back to the slower `kind load`.
- Docker for Desktop: easiest on macOS; built images are available in-cluster with no push, but it is resource-intensive.
- MicroK8s: recommended most often for Ubuntu; `microk8s.enable registry` gives a local registry.
- Minikube: higher fidelity, more options, more overhead; `ctlptl` can set it up with a registry.
- k3d: runs k3s in Docker, starts in under 5 seconds, and has a built-in local registry designed to work with Tilt.
- Rancher Desktop: uses k3s, has no local registry out of the box.
- Remote clusters (EKS, AKS, GKE): recommended only for large teams with a dev infrastructure team. Use a remote registry and set up `live_update`.

## Allowing a cluster

By default Tilt refuses a remote cluster and errors at start. Allow it explicitly in the Tiltfile:

```python
allow_k8s_contexts('my-cluster-name')
```

To disable the check and add your own validation:

```python
allow_k8s_contexts(k8s_context())
local('./validate-dev-cluster.sh')
```

## Registry discovery (custom local clusters)

Tilt supports two generic discovery protocols; configure the registry manually if they fail.

1. Standard protocol: a ConfigMap `local-registry-hosting` in namespace `kube-public`, with `data` key `localRegistryHosting.v1` containing `host: "localhost:5000"`.
2. Legacy annotations on the node: `tilt.dev/registry` (host as seen locally) and `tilt.dev/registry-from-cluster` (host as seen from the cluster; defaults to the first if omitted).
3. Manual, in the Tiltfile:

```python
default_registry('gcr.io/my-personal-registry')
```

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/choosing_clusters.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
