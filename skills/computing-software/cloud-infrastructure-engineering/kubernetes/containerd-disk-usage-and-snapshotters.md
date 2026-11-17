---
id: computing-software.cloud-infrastructure-engineering.kubernetes.containerd-disk-usage-and-snapshotters
name: containerd-disk-usage-and-snapshotters
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, containerd, containerd-disk-usage, containerd-snapshotter, overlayfs, disk-pressure, crictl, stargz]
level: practitioner
status: docs-checked
description: "Find what fills /var/lib/containerd (images, snapshots, writable layers, logs), prune safely with crictl/ctr, and choose snapshotters (overlayfs, stargz/SOCI lazy pull)."
sources: ["https://github.com/containerd/containerd/blob/main/docs/snapshotters/README.md", "https://github.com/kubernetes-sigs/cri-tools/blob/master/docs/crictl.md", "https://github.com/containerd/stargz-snapshotter/blob/main/docs/overview.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# containerd disk usage and snapshotters

## Where the space goes
| Path | Content |
|---|---|
| `/var/lib/containerd/io.containerd.content.v1.content/blobs` | compressed image layers (content store) |
| `/var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots` | unpacked layers **and** containers' writable layers |
| `/var/log/pods`, `/var/log/containers` | container logs |
| `/var/lib/kubelet/pods/*/volumes` | emptyDir and other node-local volumes |
Images are stored twice (compressed blob + unpacked snapshot) unless the CRI images option
`discard_unpacked_layers` (default `false`) is enabled, which lets GC remove layers from the content
store after they are unpacked.

## Investigate
```bash
du -xh --max-depth=2 /var/lib/containerd | sort -h | tail
crictl imagefsinfo
crictl images
crictl stats -a                         # container resource usage statistics
```
A huge writable layer usually means an app writing to its container filesystem instead of a volume;
set `ephemeral-storage` limits or `readOnlyRootFilesystem: true`.

## Prune safely
```bash
crictl rmi <image>                      # removes the image and ALL of its tags (CRI limitation)
crictl ps -a                            # list exited containers before removing any
```
Do not delete files under `/var/lib/containerd` while containerd is running. To rebuild a node's
state: drain, stop kubelet and containerd, wipe `/var/lib/containerd`, start, uncordon (images
re-pull).

## Snapshotters
- **overlayfs**: the default core snapshotter (comparable to Docker's overlay2 driver).
- **native**: plain file copying (comparable to Docker's vfs driver).
- Also core: `blockfile`, `devmapper`, `btrfs`, `zfs`, `erofs`; `aufs` was removed in 2.0.
- **stargz / nydus / overlaybd** are non-core proxy-plugin snapshotters. Stargz lazily pulls eStargz
  images by mounting layers from the registry; it runs as the `containerd-stargz-grpc` daemon, is
  registered under `[proxy_plugins.stargz]` with `root` set, and selected with `snapshotter =
  "stargz"` in the CRI containerd config.
- Put `/var/lib/containerd` on its own volume to separate it from the rest of the node.

## Verify
- [ ] Node disk alerts fire before the kubelet's eviction thresholds.
- [ ] No container has an unexpectedly large writable layer (`crictl stats -a`).

## Checked

2026-10-26, against containerd docs on main (latest commit 2026-10-21; RELEASES.md lists config versions up to 4 and containerd 2.3) and the Kubernetes website container-runtimes page, the crictl user guide (cri-tools) and the stargz-snapshotter overview. Confirmed: core and non-core snapshotter list and defaults, `discard_unpacked_layers` semantics, `crictl imagefsinfo`/`stats`/`rmi` and the rmi all-tags warning, stargz proxy plugin configuration. Removed the unconfirmed `--prune` flag, `ctr snapshots usage` pipeline, SOCI details, xfs ftype and alert thresholds. Directory layout under /var/lib/containerd is not covered by the stability guarantees in RELEASES.md.

Method: documentation only; no commands were run.
