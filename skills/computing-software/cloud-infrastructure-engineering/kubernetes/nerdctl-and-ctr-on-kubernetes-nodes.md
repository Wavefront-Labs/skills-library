---
id: computing-software.cloud-infrastructure-engineering.kubernetes.nerdctl-and-ctr-on-kubernetes-nodes
name: nerdctl-and-ctr-on-kubernetes-nodes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, container-runtime, nerdctl, containerd-namespaces, crictl, containerd]
level: practitioner
status: docs-checked
description: "Use ctr and nerdctl against containerd on Kubernetes nodes: the k8s.io namespace, listing and pulling images, and when to prefer crictl."
sources: ["https://github.com/containerd/nerdctl/blob/main/docs/command-reference.md", "https://github.com/containerd/nerdctl/blob/main/docs/build.md", "https://github.com/containerd/containerd/blob/main/docs/hosts.md", "https://github.com/containerd/containerd/blob/main/docs/namespaces.md", "https://kubernetes.io/docs/tasks/debug/debug-cluster/crictl/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ctr and nerdctl on Kubernetes nodes

## Namespaces
containerd isolates clients by namespace. The CRI plugin (what the kubelet uses) works in
`k8s.io`. Images pulled into another namespace such as `default` are invisible to Kubernetes.
```bash
sudo ctr namespaces ls          # for example default, moby, k8s.io
```

## ctr (ships with containerd, low level)
```bash
sudo ctr -n k8s.io images ls
sudo ctr -n k8s.io images pull registry.example.com/app:1.2.3      # reads hosts.toml directories only with --hosts-dir
sudo ctr -n k8s.io containers ls
sudo ctr -n k8s.io tasks ls
```
`ctr` reads registry host configuration (`hosts.toml`) only when you pass `--hosts-dir`, so a
pull with it does not exercise the same configuration the kubelet's CRI pulls use.

## nerdctl (Docker-compatible CLI)
```bash
sudo nerdctl --namespace k8s.io ps -a
sudo nerdctl --namespace k8s.io images
sudo nerdctl --namespace k8s.io logs <container-id>
sudo nerdctl --namespace k8s.io build -t app:dev .     # needs BuildKit set up
```

## Which tool when
| Task | Tool |
|---|---|
| Kubernetes pod/container debugging (pods, logs, exec, pulls through CRI config) | `crictl` |
| Import or export image tarballs | `ctr -n k8s.io images import/export` |
| Docker-like local workflows, compose, build | `nerdctl` |
| Inspect containerd internals (snapshots, leases, content) | `ctr` |

## Gotchas
- Containers started with ctr or nerdctl are not Kubernetes pods; the kubelet does not manage them.
- `nerdctl -n` is a deprecated alias of `--namespace`; use the long form.
- Removing images from `k8s.io` can break pod restarts on nodes without registry access.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- `nerdctl --namespace` (and `-n` as a deprecated alias), `nerdctl namespace ls` listing `default`, `moby` and `k8s.io`:
  nerdctl command reference (main branch).
- `nerdctl build` relies on BuildKit: nerdctl `docs/build.md`.
- `ctr images pull --hosts-dir` for `hosts.toml` registry configuration: containerd `docs/hosts.md`.
- `ctr` subcommands for images import/export, containers and tasks exist: containerd `cmd/ctr` source tree; `k8s.io`
  namespace referenced in containerd `docs/namespaces.md`.
- crictl role in node debugging: Kubernetes crictl task page.
- Removed: the unverified claims about the kubelet garbage-collecting foreign containers, in-use snapshot refusal and
  `-q`/`head` listing options.

Method: documentation only; no commands were run.
