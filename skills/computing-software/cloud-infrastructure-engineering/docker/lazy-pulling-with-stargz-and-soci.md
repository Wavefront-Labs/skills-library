---
id: computing-software.cloud-infrastructure-engineering.docker.lazy-pulling-with-stargz-and-soci
name: lazy-pulling-with-stargz-and-soci
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, storage-driver, stargz, lazy-pulling, soci, estargz, containerd-snapshotter, startup-time]
level: sme
status: docs-checked
description: "Start large containers before the image finishes downloading: eStargz images via buildx compression, the stargz and SOCI containerd snapshotters, and where Docker supports them."
sources: ["https://github.com/containerd/stargz-snapshotter", "https://github.com/awslabs/soci-snapshotter", "https://docs.docker.com/build/exporters/#compression", "https://docs.docker.com/engine/storage/containerd/", "https://github.com/containerd/stargz-snapshotter/blob/main/docs/overview.md", "https://github.com/containerd/stargz-snapshotter/blob/main/docs/INSTALL.md", "https://github.com/awslabs/soci-snapshotter/blob/main/docs/cli-usage.md", "https://github.com/awslabs/soci-snapshotter/blob/main/docs/pull-modes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lazy pulling with stargz and SOCI

Lazy pulling lets containers start before their images are fully downloaded: a remote
snapshotter fetches layer data from the registry as the container needs it. It can help most for
large images where little of the content is read at startup.

## Two approaches
| | eStargz (stargz-snapshotter) | SOCI (soci-snapshotter) |
|---|---|---|
| Image change | Layers re-compressed as seekable eStargz (still valid gzip) | `soci create`: none (separate index artifacts); `soci convert` produces a SOCI-enabled image |
| Build | `buildx --output ...,compression=estargz` | `soci create` then `soci push` (Index Manifest v1), or `soci convert` (v2; the SOCI docs recommend it for production) |
| Index storage | Inside layers (TOC) | SOCI index artifacts in the registry; the snapshotter finds them via the OCI Referrers API or its fallback, or via a digest passed in |
| Daemon | `containerd-stargz-grpc` | `soci-snapshotter-grpc` (CLI: `soci`) |

## eStargz build
```bash
docker buildx build \
  --output type=image,name=reg.example.com/ml:1.0,push=true,compression=estargz,force-compression=true,oci-mediatypes=true .
```
`compression` selects the algorithm (`estargz` accepts levels 0-9), `force-compression=true`
re-compresses layers imported from a previous image, and `oci-mediatypes=true` selects OCI media
types. Optional: `ctr-remote images optimize` (stargz-snapshotter) converts images into eStargz.

## Running lazily
- Install the snapshotter daemon (`containerd-stargz-grpc` or `soci-snapshotter-grpc`) and
  register it as a proxy plugin in containerd's `config.toml`:
```toml
[proxy_plugins.stargz]
  type = "snapshot"
  address = "/run/containerd-stargz-grpc/containerd-stargz-grpc.sock"
```
- Kubernetes (containerd CRI): set `snapshotter = "stargz"` (or `soci`) in the CRI plugin config.
- `ctr-remote run --snapshotter=stargz ...` is the stargz-snapshotter docs' example.
- Docker Engine: needs the containerd image store (`"features": {"containerd-snapshotter": true}`
  in `daemon.json` on upgraded installs). Docker's docs say it enables lazy pulling by default when
  configured to use the `nydus`, `overlaybd`, `soci` or `stargz` snapshotter; with `overlayfs` it
  downloads all layers first. Lazily pulled images can be missing content locally, so `docker save`
  can fail or produce an incomplete archive without reporting an error, and `docker push` cannot upload
  missing layers.

## Measure
Time the same container start (image pulled and started) once with the default `overlayfs`
snapshotter and once with the lazy snapshotter, from a cold node, on your own images.


## Gotchas
- Lazy-pulled data is fetched from the registry on demand, so registry availability and latency
  affect the running container; workloads that read most of the image gain little.
- Plain gzip layers cannot be mounted remotely by the stargz snapshotter and are downloaded in full
  (Docker's docs).
- `skopeo copy --dest-compress-format` also lists `zstd:chunked`, a separate seekable format.

## Checked

2026-10-25, against Docker's containerd image store docs (lazy pulling, saving and pushing), buildx exporters docs (compression, force-compression, oci-mediatypes), stargz-snapshotter overview and INSTALL docs (proxy plugin socket, CRI snapshotter), soci-snapshotter CLI usage, getting-started and pull-modes docs. Confirmed: `proxy_plugins.stargz` config and socket path, CRI `snapshotter = "stargz"`, `ctr-remote run --snapshotter=stargz`, buildx estargz compression options, `soci create`/`soci push` (Index Manifest v1) and `soci convert` (v2), SOCI referrers lookup, Docker lazy pulling behaviour and its limits for `docker save`/`docker push`. Corrected: Docker Engine does support lazy pulling with the containerd image store (the earlier text said support was limited). Removed as unconfirmed: the startup-read-fraction claim, the 'typical users' row, nerdctl commands and benchmark script, eStargz size claim, Podman remark.

Method: documentation only; no commands were run.
