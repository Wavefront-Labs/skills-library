---
id: computing-software.cloud-infrastructure-engineering.docker.skopeo-transports-docker-archive-oci-and-dir
name: skopeo-transports-docker-archive-oci-and-dir
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, skopeo, docker-archive, dir-transport, oci-layout, oci-archive, air-gapped, image-export]
level: advanced
description: "Move images between registries, tarballs, OCI layouts and directories without a daemon using skopeo transports docker://, docker-archive:, oci:, oci-archive: and dir:."
sources: ["https://github.com/containers/image/blob/main/docs/containers-transports.5.md", "https://github.com/containers/skopeo/blob/main/docs/skopeo-copy.1.md", "https://docs.docker.com/reference/cli/docker/buildx/build/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# skopeo transports

| Transport | Example | Notes |
|---|---|---|
| `docker://` | `docker://registry.example.com/app:1` | registry |
| `docker-archive:` | `docker-archive:app.tar:app:1` | `docker save` formatted file; a write holds a single image |
| `oci-archive:` | `oci-archive:app.tar:app:1` | tar of an OCI image layout |
| `oci:` | `oci:./layout:app:1` | OCI image layout directory; reference `app:1` is stored as the `org.opencontainers.image.ref.name` annotation |
| `dir:` | `dir:./app-1` | manifest, layer tarballs and signatures as individual files; non-standardized, for debugging or inspection |
| `docker-daemon:` | `docker-daemon:app:1` | image in the local Docker daemon |
| `containers-storage:` | `containers-storage:app:1` | local containers storage (Podman/CRI-O) |

## Common moves
```sh
# registry -> docker load-able tar (single platform)
skopeo copy --override-arch arm64 docker://nginx:1.27 docker-archive:nginx-arm64.tar:nginx:1.27
# registry -> OCI layout with ALL platforms (air-gap bundle)
skopeo copy --all docker://nginx:1.27 oci:./bundle:nginx:1.27
skopeo copy --all docker://redis:7 oci:./bundle:redis:7        # same layout, shared blobs
# OCI layout -> internal registry on the other side
skopeo copy --all oci:./bundle:nginx:1.27 docker://registry.internal/mirror/nginx:1.27
# dir: one file per component, for inspection
skopeo copy docker://alpine:3.20 dir:./alpine
# local daemon -> registry without docker push
skopeo copy docker-daemon:app:dev docker://registry.example.com/app:dev
```
`--dest-compress-format` takes `gzip`, `zstd` or `zstd:chunked` (`zstd:chunked` is incompatible with
encrypting images); `--preserve-digests` fails if the digest cannot be preserved, and does not
change what is copied (combine it with `--all`).

## Choosing
- Need multi-arch or exact digests preserved: `oci:` / `oci-archive:` with `--all` and `--preserve-digests`.
- Need `docker load` on the far side: `docker-archive:` (one image per file).
- `buildx --output type=oci,dest=app.tar` produces an OCI archive directly from a build;
  `--build-context x=oci-layout:///abs/path/bundle@sha256:<digest>` consumes a layout.

## Gotchas
- Without `--all`, `skopeo copy` copies only the image for the current OS and architecture of a
  manifest list (change it with `--override-os`, `--override-arch`, `--override-variant`).
- A write to a `docker-archive:` or `oci-archive:` destination completely overwrites the path
  (unless the tool documents otherwise), so use a fresh path per image.
- Copying with changed compression or manifest format can change digests; deploy by digest only
  after the final push, or use `--preserve-digests`, which fails if it cannot keep them.

## Verify
`skopeo inspect --raw oci:./bundle:nginx:1.27` shows the image index listing every platform you copied; with
`--preserve-digests` the copy fails rather than silently changing digests.

## Checked

2026-10-25, against the containers-image `containers-transports.5` and skopeo `skopeo-copy.1` and `skopeo-inspect.1` man pages and the buildx build reference. Confirmed: the seven transports and their descriptions, reference handling for `oci:`, `--all`, `--preserve-digests` semantics, `--dest-compress-format` values, `--override-os/arch/variant`, overwrite behaviour of archive destinations, `oci-layout:///path` build context, `skopeo inspect --raw`. Removed as unconfirmed: the dir layout detail (manifest.json, sha256sum pipeline), the digest-change-on-recompress claim stated as fact, and the crane/jq verification.

Method: documentation only; no commands were run.
