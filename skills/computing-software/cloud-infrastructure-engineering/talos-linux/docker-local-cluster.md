---
id: computing-software.cloud-infrastructure-engineering.talos-linux.docker-local-cluster
name: docker-local-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [docker, talosctl-cluster-create, local-cluster, ci, testing, container-platform]
level: intro
status: docs-checked
description: "Create a throwaway Talos cluster in Docker with talosctl cluster create docker: requirements, caveats, endpoints, multiple clusters, br_netfilter and the manual docker run."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/platform-specific-installations/local-platforms/docker.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos in Docker targets CI pipelines and local testing. Requirements: Docker 18.03 or newer and a recent `talosctl`. Because Talos runs as a container, `upgrade`, `reset` and similar APIs do not apply, and on a Mac VIPs are unsupported.

Create and use:

```bash
talosctl cluster create docker
```

Your `talosconfig` and `kubeconfig` are updated automatically; startup can take a minute or more. Set target nodes with `talosctl config nodes 10.5.0.2 10.5.0.3`. Talos and Kubernetes APIs are mapped to random host ports: see `talosctl config info` (Endpoints) and `talosctl cluster show` (KUBERNETES ENDPOINT). List containers with `talosctl containers` (add `--namespace=cri` for Kubernetes workloads).

If Flannel fails with `Failed to check br_netfilter`, load the host module: `sudo modprobe br_netfilter`. On Docker Desktop for macOS, a missing socket may need `sudo ln -s "$HOME/.docker/run/docker.sock" /var/run/docker.sock`.

Several clusters need a unique name (default `talos-default`) and CIDR (default `10.5.0.0/24`). The page's multi-cluster create example omits the `docker` subcommand that its first example uses; add it if the command is rejected:

```bash
talosctl cluster create --name cluster2 --cidr 10.6.0.0/24
talosctl cluster destroy --name cluster2
talosctl --context cluster2 version
kubectl --context admin@cluster2 get nodes
```

Clean up with `talosctl cluster destroy`.

A single container can be run by hand with `docker run --rm -it --name tutorial --hostname talos-cp --read-only --privileged --security-opt seccomp=unconfined` plus tmpfs mounts for `/run`, `/system`, `/tmp`, volumes for state and `/var`, and `-e PLATFORM=container`. Its machine config should enable host DNS with `forwardKubeDNSToHost` so DNS reaches Docker's resolver.

## Checked

2026-11-04. Requirements, caveats, create/destroy commands, multi-cluster flags, br_netfilter note and the manual run description confirmed on the Docker page.

Method: documentation only; no commands were run.
