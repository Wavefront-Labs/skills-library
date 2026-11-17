---
id: computing-software.cloud-infrastructure-engineering.kubernetes.containerd-config-and-registry-mirrors
name: containerd-config-and-registry-mirrors
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, containerd, containerd-config, hosts-toml, registry-mirror, config-toml, cri, insecure-registry]
level: practitioner
status: docs-checked
description: "Configure containerd for Kubernetes: config.toml essentials (sandbox image, SystemdCgroup, config_path) and per-registry mirrors, CA and auth via certs.d hosts.toml."
sources: ["https://github.com/containerd/containerd/blob/main/docs/hosts.md", "https://github.com/containerd/containerd/blob/main/docs/cri/config.md", "https://kubernetes.io/docs/setup/production-environment/container-runtimes/#containerd"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# containerd config.toml and registry mirrors

## Baseline config (containerd 1.7, config version 2)
```toml
version = 2
[plugins."io.containerd.grpc.v1.cri"]
  sandbox_image = "registry.k8s.io/pause:3.10.2"   # tag shown in containerd's docs; match your Kubernetes release
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
    SystemdCgroup = true
  [plugins."io.containerd.grpc.v1.cri".registry]
    config_path = "/etc/containerd/certs.d"
```
containerd 2.x uses `version = 3` and plugin IDs `io.containerd.cri.v1.images` /
`io.containerd.cri.v1.runtime` (the sandbox image becomes `pinned_images.sandbox` under the images
plugin); run `containerd config migrate` to convert. Newer daemons (2.3+) also define `version = 4`.
`containerd config dump` shows the effective merged config; check it after edits, then
`systemctl restart containerd`.

## Mirrors with hosts.toml (the supported way)
The old `registry.mirrors`, `registry.auths` and `registry.configs` properties are deprecated (not removed in 2.0). One directory per
upstream registry:
```toml
# /etc/containerd/certs.d/docker.io/hosts.toml
server = "https://registry-1.docker.io"

[host."https://harbor.internal/v2/dockerhub-proxy"]
  capabilities = ["pull", "resolve"]
  ca = "/etc/containerd/certs.d/harbor-ca.crt"
  override_path = true            # mirror path already includes /v2/<project>
```
```toml
# /etc/containerd/certs.d/registry.internal:5000/hosts.toml  (private, self-signed)
server = "https://registry.internal:5000"
[host."https://registry.internal:5000"]
  capabilities = ["pull", "resolve", "push"]
  ca = "/etc/pki/internal-ca.crt"
  # skip_verify = true    # lab only
```
`_default/hosts.toml` is the fallback for any registry without its own directory. Updates under the
`certs.d` directory do not need a containerd restart.

## Test (bypass kubelet)
```bash
crictl pull docker.io/library/nginx:1.27
ctr -n k8s.io images pull --hosts-dir /etc/containerd/certs.d docker.io/library/nginx:1.27   # ctr needs --hosts-dir to use hosts.toml
```

## Gotchas
- Hosts are tried in the order listed. `server` is the upstream default; leave it out of
  hosts.toml if the upstream must not be used.
- Auth: the CRI `auths` property is deprecated, so use kubelet image pull secrets; hosts.toml
  offers a static `[header]` table.
- A `sandbox_image` that differs from what your Kubernetes release expects causes extra pulls of the
  pause image.

## Verify
- [ ] `containerd config dump | grep -E 'config_path|SystemdCgroup|sandbox'` as intended.
- [ ] `crictl pull` of a docker.io image succeeds with the internet egress blocked.

## Checked

2026-10-26, against containerd docs on main (latest commit 2026-10-21; RELEASES.md lists config versions up to 4 and containerd 2.3) and the Kubernetes website container-runtimes page. Confirmed: hosts.toml fields (`server`, `capabilities`, `ca`, `skip_verify`, `override_path`, `[header]`), `_default` fallback, no restart for certs.d updates, `ctr --hosts-dir`, deprecation of CRI `mirrors`/`auths`/`configs`, config version 3 plugin ids. Removed the unconfirmed journalctl filter, the restart-keeps-containers note and the kubeadm preflight claim.

Method: documentation only; no commands were run.
