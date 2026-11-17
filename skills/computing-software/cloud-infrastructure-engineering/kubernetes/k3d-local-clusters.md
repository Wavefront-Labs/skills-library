---
id: computing-software.cloud-infrastructure-engineering.kubernetes.k3d-local-clusters
name: k3d-local-clusters
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, edge-lightweight-distros, k3d, k3s, local-development, ci]
level: practitioner
status: docs-checked
description: "Run k3s clusters in Docker with k3d for local development and CI: multi-node clusters, port mapping, a local registry, image import and config files."
sources: ["https://k3d.io/stable/", "https://k3d.io/stable/usage/configfile/", "https://k3d.io/stable/usage/registries/", "https://github.com/k3d-io/k3d/blob/main/docs/usage/commands/k3d_cluster_create.md", "https://github.com/k3d-io/k3d/blob/main/docs/usage/k3s.md", "https://kind.sigs.k8s.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# k3d clusters in Docker

k3d runs k3s server and agent nodes as Docker containers. Clusters are throwaway, which suits
laptops and CI.

## Create
```bash
k3d cluster create dev \
  --servers 1 --agents 2 \
  -p "8080:80@loadbalancer" -p "8443:443@loadbalancer" \
  --registry-create dev-registry:0.0.0.0:5000 \
  --k3s-arg "--disable=traefik@server:*" \
  --image rancher/k3s:<k3s-tag>
```
Port mappings go through k3d's load-balancer container to the cluster's ingress or LoadBalancer
Services (k3s servicelb, klipper-lb).

## Images
```bash
docker build -t app:dev . && k3d image import app:dev -c dev        # no registry needed
docker tag app:dev localhost:5000/app:dev && docker push localhost:5000/app:dev
# in-cluster reference: dev-registry:5000/app:dev
```

## Config file (repeatable)
```yaml
apiVersion: k3d.io/v1alpha5
kind: Simple
metadata: {name: dev}
servers: 1
agents: 2
image: rancher/k3s:<k3s-tag>
ports:
- {port: 8080:80, nodeFilters: [loadbalancer]}
registries:
  create: {name: dev-registry, host: "0.0.0.0", hostPort: "5000"}
options:
  k3s:
    extraArgs:
    - {arg: --disable=traefik, nodeFilters: ["server:*"]}
```
`k3d cluster create --config k3d.yaml`.

## Housekeeping
```bash
k3d cluster list
k3d cluster stop dev && k3d cluster start dev
k3d cluster delete dev
k3d kubeconfig merge dev --kubeconfig-switch-context
```

## Compared with kind
kind bootstraps each node with kubeadm (closer to production for conformance-style tests); k3d is
lighter and ships k3s extras (servicelb, local-path-provisioner, Traefik). Pick kind to test upstream behaviour,
k3d for fast inner-loop work.

## Verify
`kubectl get nodes` shows 3 Ready nodes and `curl localhost:8080` reaches the ingress controller (Traefik is disabled above, so
install your own first).

## Checked
2026-10-27, against k3d docs on main (k3d-io/k3d `docs/usage/`) and the kind README. Confirmed: `--registry-create NAME[:HOST][:HOSTPORT]`, `--k3s-arg ARG@NODEFILTER`, `-p ...@loadbalancer`, `-i/--image`; config `apiVersion: k3d.io/v1alpha5`, `kind: Simple`, `ports[].nodeFilters`, `registries.create` (`name`, `host`, `hostPort`), `options.k3s.extraArgs`; `k3d image import -c`; `k3d kubeconfig merge --kubeconfig-switch-context`; the cluster list/start/stop/delete commands; k3s bundles servicelb, local-path-provisioner and Traefik; kind bootstraps nodes with kubeadm.
Method: documentation only; no commands were run.
