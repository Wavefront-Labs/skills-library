---
id: computing-software.cloud-infrastructure-engineering.docker.containerd-config-toml-essentials
name: containerd-config-toml-essentials
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, containerd, containerd-config-toml, runtime, systemd-cgroup, registry-config-path, snapshotter]
level: advanced
status: docs-checked
description: "Read and edit /etc/containerd/config.toml: why Docker's package disables CRI, config dump/default, SystemdCgroup, registry config_path, runtimes and snapshotters by version."
sources: ["https://github.com/containerd/containerd/blob/main/docs/man/containerd-config.toml.5.md", "https://github.com/containerd/containerd/blob/main/docs/cri/config.md", "https://github.com/containerd/containerd/blob/main/docs/hosts.md", "https://docs.docker.com/engine/daemon/live-restore/", "https://docs.docker.com/engine/storage/containerd/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# containerd config.toml essentials

Docker uses containerd under the hood. The `/etc/containerd/config.toml` key `disabled_plugins`
lists plugin IDs that are not initialised (for example `disabled_plugins = ["cri"]`), and
`required_plugins` makes containerd exit if a plugin fails. Settings under
`io.containerd.grpc.v1.cri` (version 2) or `io.containerd.cri.v1.*` (version 3) belong to the CRI
plugin that kubelet uses; the containerd CRI docs note that CRI-created containers are not recognised
by other clients such as `ctr`, `nerdctl` and Docker/Moby. If your host's config disables `cri`, remove it
from `disabled_plugins` before configuring Kubernetes.

## See the effective config
```bash
containerd config default > default.toml        # every option with defaults
sudo containerd config dump                      # final main config with imported sub-config files
containerd config migrate                        # migrate the current config to the latest version
containerd --version
```
Config `version = 2` (containerd 1.x) and `version = 3` (introduced in containerd 2.0) use different
plugin paths; version 2 is still accepted and converted. The containerd man page for
`config.toml` describes version 4 as the latest config version, so check which version your
containerd release documents. Copy examples matching your version.

## Common edits (version 2 syntax)
```toml
version = 2

[plugins."io.containerd.grpc.v1.cri"]
  sandbox_image = "registry.k8s.io/pause:3.10.2"   # value shown in the containerd CRI docs

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
  SystemdCgroup = true          # must match kubelet cgroupDriver=systemd

[plugins."io.containerd.grpc.v1.cri".registry]
  config_path = "/etc/containerd/certs.d"     # per-registry hosts.toml mirrors and CAs

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runsc]
  runtime_type = "io.containerd.runsc.v1"     # gVisor RuntimeClass handler "runsc"
```
Version 3 moves CRI runtime settings under `[plugins."io.containerd.cri.v1.runtime"]` and
image settings under `[plugins."io.containerd.cri.v1.images"]` (the pause image becomes
`pinned_images.sandbox` and the registry `config_path` moves to
`[plugins."io.containerd.cri.v1.images".registry]`).

## Apply
```bash
sudo containerd config dump >/dev/null && sudo systemctl restart containerd
sudo ctr plugins ls                              # plugin status (alias: ctr plugin list)
```
Stopping the Docker daemon stops running containers unless `live-restore` is enabled in
`daemon.json`; plan a restart of the Docker host's containerd accordingly.

## Docker-specific notes
- Docker is configured through `daemon.json` (`runtimes`, `features.containerd-snapshotter`); you rarely need to edit
  containerd's own config for Docker alone. With the containerd image store enabled Docker uses the
  `overlayfs` snapshotter by default.
- containerd namespaces separate clients: nerdctl lists namespaces such as `default`, `moby` and `k8s.io`,
  and image names and metadata are separate per namespace.
- Do not point Kubernetes and Docker at the same containerd unless you understand namespace separation.

## Gotchas
- Check `ctr plugins ls` after editing; a plugin that is disabled or failed to load will not serve requests.
- `SystemdCgroup = true` must be paired with `cgroupDriver: systemd` in the `KubeletConfiguration` (unless the
  kubelet detects the driver from the CRI runtime, which the docs describe as an alpha feature in Kubernetes v1.28).

## Checked
Documentation release: containerd v2.4.2 (docs/cri/config.md, docs/man/containerd-config.toml.5.md, docs/hosts.md, docs/namespaces.md, cmd/containerd and cmd/ctr source), Docker docs (live-restore, containerd image store) and nerdctl v2.4.1 command reference, checked 2026-10-26.
Confirmed: `disabled_plugins` and `required_plugins`; `containerd config default|dump|migrate`; config version 3 introduced in 2.0 with version 2 still accepted; `SystemdCgroup` paths for versions 2 and 3; `sandbox_image` and `pinned_images.sandbox`; registry `config_path` for versions 2 and 3; `runtime_type = "io.containerd.runsc.v1"`; `ctr plugins list` alias `ls`; namespaces `default`, `moby`, `k8s.io` exist; default `overlayfs` snapshotter for Docker's containerd image store; daemon shutdown stops containers unless live-restore is enabled.
Corrected: the claim that restarting containerd or Docker is harmless is not supported (by default the daemon stopping stops containers); the Docker package default config content, `/var/lib/containerd` path and the "typo silently disables" statement were removed as unsupported.
Method: documentation only; no commands were run.
