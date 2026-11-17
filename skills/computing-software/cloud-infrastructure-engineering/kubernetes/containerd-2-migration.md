---
id: computing-software.cloud-infrastructure-engineering.kubernetes.containerd-2-migration
name: containerd-2-migration
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, container-runtime, containerd-2, containerd-config-migration, containerd]
level: practitioner
status: docs-checked
description: "Upgrade nodes from containerd 1.7 to 2.x: config version 3 migration, removed features, CRI plugin path changes, and a node-by-node rollout with verification."
sources: ["https://github.com/containerd/containerd/blob/main/docs/containerd-2.0.md", "https://github.com/containerd/containerd/blob/main/RELEASES.md", "https://github.com/containerd/containerd/blob/main/docs/cri/config.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating to containerd 2.x

## What changes
- Config `version = 3` (containerd 2.0); CRI plugin split into `io.containerd.cri.v1.runtime` and
  `io.containerd.cri.v1.images`. The daemon migrates older configs in memory on every start and
  leaves the file unchanged; `containerd config migrate` writes the latest version out. RELEASES.md
  now lists `version = 4` (minimum containerd 2.3.0), so a migrated file may not load on an older
  daemon; keep the old file until you no longer need to roll back.
- Removed in 2.0: `aufs` snapshotter, `io.containerd.runtime.v1.linux` and `io.containerd.runc.v1`
  shims, the CRI v1alpha2 API, the `cri-containerd-*` release bundles. Docker Schema 1 pulls are
  disabled by default (re-enable with `CONTAINERD_ENABLE_DEPRECATED_PULL_SCHEMA_1_IMAGE=1`).
- Deprecated, not removed, in 2.0: CRI registry `mirrors`, `auths` and `configs`; use `config_path`
  with `hosts.toml` and kubelet image pull secrets.
- Behaviour changes: CRI containers get unprivileged ports and ICMP by default
  (`enable_unprivileged_ports` / `enable_unprivileged_icmp` = `false` reverts), and the default seccomp
  profile no longer allows `io_uring_*` syscalls.
- Sandbox image moves to `[plugins.'io.containerd.cri.v1.images'.pinned_images] sandbox = "..."`.

## Migrate the config
```bash
containerd --version
containerd config migrate > ./config-migrated.toml   # run with the 2.x binary against the current file
diff <(containerd config dump) ./config-migrated.toml | less
```
Check that these survive: `SystemdCgroup = true`, registry `config_path`, sandbox image
(`pinned_images`), any extra runtimes.

## Roll out node by node
```bash
kubectl drain <n> --ignore-daemonsets --delete-emptydir-data
sudo systemctl stop kubelet containerd
# install containerd 2.x, runc (user namespaces need runc 1.2.0 or later) and CNI plugins
# separately, then place the migrated config
sudo systemctl start containerd && sudo systemctl start kubelet
kubectl uncordon <n>
```
Test GPU and sandboxed runtime nodes separately; any tool that edits `config.toml` (for example a
GPU runtime installer) must write the config version your daemon expects.

## Verify
```bash
kubectl get node <n> -o jsonpath='{.status.nodeInfo.containerRuntimeVersion}'   # containerd://2.x
sudo crictl info                                    # runtimes appear under config.containerd.runtimes
sudo crictl pull registry.example.com/app:tag      # mirrors still applied
journalctl -u containerd --since -10m
```
`ctr deprecations list` (containerd >= 1.6.27 and >= 1.7.12, and 2.x; `--format json` for machine
output) reports deprecated features in use; run it before upgrading.

## Checked

2026-10-26, against containerd docs on main (latest commit 2026-10-21; RELEASES.md lists config versions up to 4 and containerd 2.3) and the Kubernetes website container-runtimes page. Confirmed: config version 3 and CRI plugin split, automatic in-memory migration and `containerd config migrate`, the 2.0 removal and deprecation lists (registry mirrors are deprecated, not removed), `ctr deprecations list` backport versions, runc 1.2.0 for user namespaces, `pinned_images.sandbox` key. Removed unconfirmed jq and grep filters and the nvidia-specific version claim.

Method: documentation only; no commands were run.
