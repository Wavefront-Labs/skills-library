---
id: computing-software.cloud-infrastructure-engineering.docker.saving-multiple-images-with-compression
name: saving-multiple-images-with-compression
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-save, docker-load, save-multiple-images, multi-image-tar, zstd, save-gzip, air-gapped, offline-images]
level: practitioner
description: "Bundle many images into one docker save tar sharing layers, compress with gzip/pigz/zstd, stream over ssh, and load with tags intact."
sources: ["https://docs.docker.com/reference/cli/docker/image/save/", "https://docs.docker.com/reference/cli/docker/image/load/", "https://docs.docker.com/reference/cli/docker/container/export/", "https://github.com/containers/skopeo/blob/main/docs/skopeo-copy.1.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Saving multiple images into one compressed tar

## One archive for several images
```sh
docker save -o bundle.tar app/api:1.4.0 app/worker:1.4.0 postgres:16 redis:7
```
`docker save` accepts several image names and tags. Always save by **name:tag**; saving by image
ID gives an archive without tag information.

From a Compose project:
```sh
docker compose config --images | sort -u | xargs docker save -o stack.tar
```

## Compression
`docker save` writes a plain tar to `-o` or stdout; compress it with any tool.
`docker load` accepts input compressed with gzip, bzip2, xz or zstd, from a file or stdin.
```sh
docker save app/api:1.4.0 app/worker:1.4.0 | gzip > bundle.tar.gz
docker save ... | zstd -T0 -o bundle.tar.zst
docker load -i bundle.tar.zst
zstd -dc bundle.tar.zst | docker load
```
Docker's reference shows `docker save myimage:latest | gzip > myimage_latest.tar.gz`.

## Streaming host to host
```sh
docker save app/api:1.4.0 | zstd -T0 | ssh target 'zstd -dc | docker load'
docker save app/api:1.4.0 | docker -H ssh://target load
```

## Multi-platform caveat
`docker save` saves all platform variants present in the local image store; `--platform`
selects variants (API 1.48 or later) and errors if one is missing. See
`save-and-load-specific-platforms`. For true multi-arch bundles straight from a registry use
`skopeo copy --all docker://... oci-archive:bundle.tar`.

## Gotchas
- `docker load` prints `Loaded image: name:tag` per image (`-q` suppresses it); check them in scripts.
- `docker export` is different (a container's filesystem, no image tags) - not a substitute.

## Verify
```sh
docker load -i bundle.tar.zst && docker images
```

## Checked

2026-10-26 against Docker CLI reference data (docker/docs main, 2026-10-23), containerd image store page, skopeo, containers-transports and crane documentation. Confirmed: docker save multiple names, -o and stdout use, gzip example, docker load accepting gzip, bzip2, xz and zstd, load -q, --platform behaviour and API 1.48 minimum, docker export description, skopeo --all. Removed unconfirmed compression ratios, pigz/zstd level suggestions, the free-space rule and the tar/jq manifest check.

Method: documentation only; no commands were run.
