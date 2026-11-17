---
id: computing-software.cloud-infrastructure-engineering.docker.nerdctl-and-ctr-for-containerd
name: nerdctl-and-ctr-for-containerd
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, containerd, nerdctl, nerdctl-compose, ctr-vs-nerdctl, crictl, kubernetes-nodes, namespaces]
level: practitioner
description: "Work directly with containerd using nerdctl (Docker-compatible CLI and compose) versus ctr and crictl, including namespaces like k8s.io and moby."
sources: ["https://github.com/containerd/nerdctl/blob/main/docs/command-reference.md", "https://github.com/containerd/nerdctl", "https://github.com/containerd/containerd/blob/main/docs/namespaces.md", "https://github.com/containerd/containerd/blob/main/docs/getting-started.md", "https://github.com/kubernetes-sigs/cri-tools/blob/master/docs/crictl.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nerdctl and ctr for containerd

## Which CLI
| Tool | For | Notes |
|---|---|---|
| `nerdctl` | humans; Docker-compatible UX | `run -p`, `build` (needs buildkitd), `compose`, optional rootless, lazy pulling |
| `ctr` | containerd debugging | low-level client shipped with containerd |
| `crictl` | Kubernetes nodes via CRI | CLI for CRI-compatible runtimes (cri-tools) |

## Namespaces matter
containerd isolates clients by namespace:
- `k8s.io` - kubelet/CRI images and containers
- `moby` - Docker Engine's containers (when Docker uses containerd)
- `default` - the default namespace
```sh
sudo ctr namespaces ls
sudo nerdctl --namespace k8s.io images          # what kubelet pulled
sudo ctr -n k8s.io images ls -q
```
Image names and metadata are separate per namespace, so an image loaded into `default` is not visible in
`k8s.io`; load it with `--namespace k8s.io`. `nerdctl -n` is a deprecated alias of `--namespace`;
`CONTAINERD_NAMESPACE` sets the default namespace for ctr.

## nerdctl day-to-day
```sh
nerdctl run -d --name web -p 8080:80 nginx:1.27
nerdctl ps; nerdctl logs web; nerdctl exec -it web sh
nerdctl build -t app:dev .                       # needs buildkitd running
nerdctl compose up -d                            # Docker Compose support; check the compat table for gaps
nerdctl --namespace k8s.io load -i app.tar       # side-load into a k8s node
nerdctl image convert --estargz --oci app:dev app:esgz   # eStargz for lazy pulling
```
`--estargz` must be used together with `--oci`. Rootless mode is optional (see the nerdctl rootless doc).
Networking uses CNI (`--network` accepts bridge, host, none, container:<name>, ns:<path> or a CNI network name); `nerdctl network ls`.

## ctr essentials
```sh
sudo ctr images pull docker.io/library/alpine:3.20        # full reference required
sudo ctr run --rm -t docker.io/library/alpine:3.20 t1 sh
sudo ctr -n k8s.io images import app.tar
sudo ctr -n k8s.io images export out.tar docker.io/org/app:1
sudo ctr tasks ls; sudo ctr snapshots ls
```
ctr pull commands take a full image reference (as in `docker.io/library/redis:alpine` in the containerd
getting-started guide), `--user User[:password]` for registry credentials and `--hosts-dir` for
per-registry `hosts.toml` configuration.

## crictl
```sh
sudo crictl ps; sudo crictl pods; sudo crictl logs <ctr>; sudo crictl inspecti <image>
sudo crictl rmi <image>
```
Configure the endpoint in `/etc/crictl.yaml` (default config file, `--config`/`-c`) with `runtime-endpoint: unix:///run/containerd/containerd.sock`, or pass `--runtime-endpoint`. `crictl rmi <tag>` removes the whole image with all of its tags.

## Verify
`sudo nerdctl --namespace k8s.io images` lists a side-loaded image; a pod with
`imagePullPolicy: Never` can then use it.

## Checked
Documentation release: containerd/nerdctl v2.4.1 (README, docs/command-reference.md, global flags), containerd v2.4.2 (docs/namespaces.md, docs/getting-started.md, cmd/ctr source) and kubernetes-sigs/cri-tools docs/crictl.md, checked 2026-10-26.
Confirmed: nerdctl `build` needs buildkitd; `compose`; `image convert --estargz --oci`; `load -i`; `--namespace` and deprecated `-n`; network options; ctr `--user`, `--hosts-dir`, `images import|export`; crictl `/etc/crictl.yaml` `runtime-endpoint`, `inspecti`, `rmi`; namespaces `default`, `moby`, `k8s.io`.
Corrected: `nerdctl -n` is deprecated; `crictl rmi --prune` is not in the documentation read and was removed; `crictl rmi` by tag removes all tags.
Removed as unsupported: "no registry auth helpers", `ctr` lacks Docker Hub shorthand (docs use full references), "no Swarm deploy keys", `containerd-rootless-setuptool.sh` name and `/opt/cni/bin` path, `imagePullPolicy` outcome claim wording.
Method: documentation only; no commands were run.
