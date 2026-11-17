---
id: computing-software.cloud-infrastructure-engineering.docker.image-save-load-and-air-gapped-transfer
name: image-save-load-and-air-gapped-transfer
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-save, docker-load, image-export, air-gapped, offline-images, docker-export, docker-import, tarball, skopeo, oci-layout, crane, offline-registry]
level: practitioner
status: docs-checked
description: "Moving images into air-gapped environments: docker save/load vs export/import, multi-image tarballs, compression, preserving digests with skopeo/crane OCI layouts, and seeding an offline registry."
sources: ["https://docs.docker.com/reference/cli/docker/image/save/", "https://docs.docker.com/reference/cli/docker/image/load/", "https://docs.docker.com/reference/cli/docker/container/export/", "https://docs.docker.com/reference/cli/docker/image/import/", "https://github.com/containers/skopeo/blob/main/docs/skopeo-copy.1.md", "https://github.com/containers/image/blob/main/docs/containers-transports.5.md", "https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_pull.md", "https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_push.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image save/load and air-gapped transfer

**Goal:** get an image (and the platforms you need) onto a host with no registry access, and
know which of the four tar commands you actually want.

## save/load vs export/import — not interchangeable
| Command | Operates on | Produces |
|---|---|---|
| `docker save` | image(s) | tar archive of the image(s) with tags; all platform variants present locally, or those selected with `--platform` |
| `docker load` | save tarball | restores images and tags (accepts gzip, bzip2, xz and zstd compressed input) |
| `docker export` | a *container* | tar of the container's filesystem; volume contents are not exported |
| `docker import` | filesystem tarball | a filesystem image; Dockerfile instructions can be applied with `--change` |

`export`/`import` is for "snapshot this container's filesystem", not for moving images:
the result does not carry the original image configuration unless you re-apply it with
`--change`. Air-gapped shipping is `save`/`load`.

## Basic transfer
```bash
# online side
docker pull --platform linux/amd64 nginx:1.27          # pull the platform the target runs
docker save nginx:1.27 redis:7 postgres:16 | gzip > bundle.tar.gz   # multiple images, one tar
# offline side
docker load -i bundle.tar.gz          # prints "Loaded image: nginx:1.27" per image
```
- `docker save` takes several names and tags in one call, and `docker save -o file.tar`
  writes to a file. `docker load -q` suppresses the output.
- Save by **name:tag**; saving by image ID gives an archive without tag information, so
  expect to `docker tag` after loading.
- Pipe over SSH to skip the intermediate file: `docker save app:1.0 | ssh host docker load`.
- Save and load accept `--platform os[/arch[/variant]]` (API 1.48 or later, so Engine 28+):
  see `save-and-load-specific-platforms`.

## Keeping digests with registry-to-file tools
`docker save` and `docker load` restore images and tags, but the docs do not promise that a
later push reproduces the original registry manifest digest. If a policy pins
`image@sha256:...`, copy with a registry-to-registry tool that documents digest handling:
```bash
skopeo copy --all --preserve-digests docker://nginx:1.27 oci-archive:nginx.tar
skopeo copy --all --preserve-digests docker://nginx:1.27 dir:./nginx
# offline:
skopeo copy --all --preserve-digests oci-archive:nginx.tar docker://registry.internal/nginx:1.27
```
`--all` copies every image of a multi-platform list, and `--preserve-digests` makes skopeo
fail if the digest cannot be preserved. A write to an `oci-archive:` destination replaces the
file with the single provided image. `crane pull` has `--format` (`tarball`, `legacy` or
`oci`) and `--platform` (default all); `crane push PATH IMAGE` reads a directory as an OCI
image layout and any other path as a docker-style tarball (see the crane docs for the exact
arguments).

With buildx you can also build straight to an OCI archive:
`docker buildx build --platform linux/amd64,linux/arm64 -o type=oci,dest=app.tar .`.

## Seeding an offline registry
On the air-gapped network, run a registry (`registry:2`, Harbor or Zot), then `skopeo copy`
or `docker load && docker tag && docker push` each bundle in, and point hosts at it with
`registry-mirrors` and/or `insecure-registries` in `daemon.json` (the latter only for a plain
HTTP registry). For Kubernetes nodes that use containerd, load with `ctr -n k8s.io images import
bundle.tar` or `nerdctl load`.

## Verify
```bash
docker load -i bundle.tar.gz
docker image inspect nginx:1.27 --format '{{.Id}}'
docker run --rm nginx:1.27 nginx -v
```

## Checked

2026-10-26 against Docker CLI reference data (docker/docs main, 2026-10-23), containerd image store page, skopeo, containers-transports and crane documentation. Confirmed: docker save/load behaviour and options (--platform, -o, -i, -q, compression formats accepted by load, API 1.48 minimum for --platform), export and import descriptions, skopeo copy --all and --preserve-digests, containers-transports oci-archive/dir semantics, crane pull --format and --platform and crane push PATH rules. Removed unconfirmed claims about digest recomputation by the Engine, layer deduplication and size ratios, attestation transfer, the containerd-store multi-platform load rule, and the kubelet loading detail.

Method: documentation only; no commands were run.
