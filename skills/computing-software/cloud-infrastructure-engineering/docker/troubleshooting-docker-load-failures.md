---
id: computing-software.cloud-infrastructure-engineering.docker.troubleshooting-docker-load-failures
name: troubleshooting-docker-load-failures
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-load, load-troubleshooting, docker-archive, oci-layout, air-gapped, image-export]
level: practitioner
status: docs-checked
description: "Fix docker load errors: unexpected EOF, invalid tar header, no such file manifest.json, untagged loads, export vs save mix-ups, compression, and disk space during import."
sources: ["https://docs.docker.com/reference/cli/docker/image/load/", "https://docs.docker.com/reference/cli/docker/image/import/", "https://github.com/opencontainers/image-spec/blob/main/image-layout.md", "https://github.com/containers/image/blob/main/docs/containers-transports.5.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting docker load

Docker's reference for `docker load`: it loads an image or repository from a tar archive (even if
compressed with gzip, bzip2, xz or zstd) from a file or stdin, and restores both images and tags.
Start from what the archive actually is.

| Symptom | Likely cause | Fix |
|---|---|---|
| Archive not recognised / invalid tar | Not a tar, truncated, or compressed with a tool `load` does not handle | `file img.tar`; compare checksums on both ends; decompress first if it is not one of the four formats above |
| Archive came from `docker export` | `export` writes a container filesystem, not an image | Use `docker import img.tar name:tag` instead |
| Image loads without a tag | Archive saved by image ID | `docker tag <id> name:tag`; save by name next time (`docker save name:tag`) |
| `exec format error` after load | Wrong architecture saved | Save with `--platform` (see `save-and-load-specific-platforms`) |
| `requested platform (...) not found: image might be filtered out` | `docker load --platform` asked for a platform the archive lacks | Pick a platform present in the archive, or re-create the archive with all platforms |
| `no space left on device` | Not enough space for the extracted layers | Free space under the daemon's data root; stream from the source instead of copying the archive first |

## Know what you have
```bash
file img.tar
tar -tf img.tar | head
```
A Docker archive from `docker save` contains `manifest.json`; an OCI image layout contains
`oci-layout` and `index.json` (see the OCI image-layout spec); an export tarball is a root
filesystem. To convert between formats use `skopeo copy`, which supports `docker-archive:` and
`oci-archive:` transports.

## Robust transfer recipe
```bash
docker save app:1.4 | zstd -T0 > app-1.4.tar.zst
sha256sum app-1.4.tar.zst > app-1.4.tar.zst.sha256
# target
sha256sum -c app-1.4.tar.zst.sha256 && zstd -dc app-1.4.tar.zst | docker load
```

## Gotchas
- `docker load` restores the tags stored in the archive, so an existing tag of the same name
  on the target is moved to the loaded image.
- `--platform` on `load` needs API version 1.48 or later.

## Checked

2026-10-26 against Docker CLI reference data (docker/docs main, 2026-10-23), containerd image store page, skopeo, containers-transports and crane documentation. Confirmed: docker load description and accepted compression formats, --platform error text, API 1.48 minimum, docker import description, skopeo transports docker-archive and oci-archive. Removed unconfirmed exact error strings (unexpected EOF, tar header, open /var/lib/docker/tmp), the rsync and old-engine OCI advice, the parallel-load timeout and the rootless store note.

Method: documentation only; no commands were run.
