---
id: computing-software.cloud-infrastructure-engineering.docker.oci-image-layout-on-disk
name: oci-image-layout-on-disk
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, oci-image-layout, oci-layout, image-spec, blobs, index-json, skopeo, buildx]
level: advanced
status: docs-checked
description: "Understand and use the OCI image layout directory (oci-layout, index.json, blobs/sha256): produce it with buildx/skopeo, inspect it with jq, and consume it as a build context."
sources: ["https://github.com/opencontainers/image-spec/blob/main/image-layout.md", "https://docs.docker.com/build/exporters/oci-docker/", "https://github.com/containers/image/blob/main/docs/containers-transports.5.md", "https://docs.docker.com/reference/cli/docker/buildx/build/", "https://github.com/oras-project/oras/blob/main/cmd/oras/root/cp.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCI image layout on disk

## Structure
```text
mylayout/
├── oci-layout            {"imageLayoutVersion": "1.0.0"}
├── index.json            entry point: list of manifest/index descriptors (with ref names)
└── blobs/
    └── sha256/
        ├── 3f1c...       manifest JSON
        ├── 8a9b...       config JSON
        └── d4e5...       layer tar+gzip (or zstd)
```
Every file in `blobs/` is named by its digest. `index.json` tags entries with the annotation
`org.opencontainers.image.ref.name` (the "tag" inside the layout).

## Produce one
```bash
docker buildx build -o type=oci,dest=app.tar .               # tar of a layout
docker buildx build -o type=oci,dest=app-dir,tar=false .     # directory layout (tar parameter, default true)
skopeo copy docker://<image> oci:alpine-layout:<tag>          # oci:path[:reference] transport
```
The `oci` exporter uses OCI media types by default (`oci-mediatypes` defaults to true for `type=oci`).

## Inspect
Open `index.json` (an image index) and follow each descriptor digest to `blobs/<algorithm>/<hex>`:
manifest (or a nested index for multi-arch), then the config and layer blobs. Each blob file name is
its digest, so recomputing the SHA-256 of a file must give its name.

## Consume one
```bash
skopeo copy oci:alpine-layout:<tag> docker://reg.example.com/alpine:<tag>
docker buildx build --build-context base=oci-layout:///abs/path/alpine-layout:<tag> .   # FROM base
oras cp --from-oci-layout ./alpine-layout:<tag> reg.example.com/alpine:<tag>
```
`skopeo` also has an `oci-archive:path[:reference]` transport for a layout packed as a tar. Layouts
are a practical interchange format for air-gapped transfer.

## Gotchas
- With `oci:` as a source, if neither a reference nor `@source-index` is given, the path must
  contain exactly one image.
- `skopeo`'s `docker-archive:` transport is the `docker save` format, a different format from an
  OCI layout.
- Layouts can hold many images; blobs are content-addressed, so identical blobs are stored once.

## Checked

2026-10-25, against the OCI image-spec `image-layout.md`, Docker exporters docs (`oci` exporter parameters), buildx build reference (`oci-layout://` build context), containers-transports man page (`oci:`, `oci-archive:`, `docker-archive:`) and ORAS `cp` source. Confirmed: `oci-layout`, `index.json` and `blobs` structure, `tar=false`, `oci:path[:reference]`, `--build-context ...=oci-layout:///path:tag` (absolute path form), `oras cp --from-oci-layout`. Removed as unconfirmed: crane commands, the claim that `docker save` produces an OCI layout on the containerd image store, the `docker load` ref.name behaviour, jq/awk inspection pipelines, and diffoci.

Method: documentation only; no commands were run.
