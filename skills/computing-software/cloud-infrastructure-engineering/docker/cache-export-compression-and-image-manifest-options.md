---
id: computing-software.cloud-infrastructure-engineering.docker.cache-export-compression-and-image-manifest-options
name: cache-export-compression-and-image-manifest-options
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, remote-cache, image-manifest-cache, oci-mediatypes, cache-to, registry-cache, ecr]
level: advanced
status: docs-checked
description: "Tune registry cache export: image-manifest=true with oci-mediatypes for registries like ECR, compression (gzip, zstd, estargz) and level, ignore-error, and mode trade-offs."
sources: ["https://docs.docker.com/build/cache/backends/registry/", "https://docs.docker.com/build/cache/backends/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cache export compression and image-manifest options

## Parameters of type=registry cache-to
| Parameter | Values | Purpose |
|---|---|---|
| `ref` | `reg/app:cache` | Where the cache is stored |
| `mode` | `min` (default), `max` | `max` also exports intermediate stage layers |
| `oci-mediatypes` | `true` (default), `false` | Use OCI media types in exported manifests |
| `image-manifest` | `true` (default), `false` | With OCI media types, generate an image manifest instead of an image index for the cache image |
| `compression` | `gzip` (default), `estargz`, `zstd` | Compression type of cache layers |
| `compression-level` | `0..22` | Compression level |
| `force-compression` | `true`/`false` (default `false`) | Forcibly apply the compression |
| `ignore-error` | `true`/`false` (default `false`) | Ignore errors caused by failed cache exports |

Since BuildKit v0.21 `image-manifest` is enabled by default; on older BuildKit versions set it
explicitly. The `ref` must not be the same as the location you push the image to.

## Registries that reject image indexes
With OCI media types the cache image is an image index unless `image-manifest` is enabled.
Some registries, such as Amazon ECR, do not support the image index media type
(`application/vnd.oci.image.index.v1+json`). For ECR or any registry without index support set
`image-manifest=true` (the default since BuildKit v0.21), as in:
```bash
docker buildx build \
  --cache-to type=registry,ref=111122223333.dkr.ecr.eu-west-1.amazonaws.com/app:cache,mode=max,image-manifest=true,oci-mediatypes=true \
  --cache-from type=registry,ref=111122223333.dkr.ecr.eu-west-1.amazonaws.com/app:cache \
  -t 111122223333.dkr.ecr.eu-west-1.amazonaws.com/app:1.4 --push .
```

## Compression
`compression=zstd` (or `estargz`) is selected on `--cache-to`; the options are the same as the
exporter compression options and are supported by the `local` and `registry` backends. When
importing, BuildKit detects the media types itself.
```bash
--cache-to type=registry,ref=reg/app:cache,mode=max,compression=zstd,compression-level=3
```

## Cache export should not break builds
```bash
--cache-to type=registry,ref=reg/app:cache,mode=max,ignore-error=true
```
A registry hiccup during cache export otherwise fails an otherwise successful build. Pair
with monitoring so silent cache failures do not linger.

## Verify
```bash
docker buildx imagetools inspect --raw reg.example.com/app:cache
```
The raw manifest's `mediaType` shows whether the cache was stored as an image manifest or an
index.

## Gotchas
- `min` is typically smaller (faster import/export, lower storage cost); `max` is more likely to
  produce cache hits. Set registry retention on cache tags.
- The `registry` backend works with the default `docker` driver only when the containerd image
  store is enabled; otherwise use a `docker-container` builder (`docker buildx create --use`).
- If the `--cache-from` ref does not exist, cache import fails but the build continues.

## Checked

Checked 2026-10-23 against the Docker docs cache backends pages (index and registry; docker/docs main branch).

- Parameter names, values and defaults of `type=registry` (`mode`, `oci-mediatypes`, `image-manifest`, `compression`, `compression-level` 0..22, `force-compression`, `ignore-error`).
- `image-manifest` enabled by default since BuildKit v0.21; the ECR image-index limitation.
- Compression and OCI media type options apply to the `local` and `registry` backends; docker driver needs the containerd image store for registry cache.
- Removed the `uncompressed` value, the gzip/zstd level split, the Harbor/Artifactory claims, the zstd speed claims, the `ignore-error` guidance about monitoring and the `jq` / `grep` verification commands.

Method: documentation only; no commands were run.
