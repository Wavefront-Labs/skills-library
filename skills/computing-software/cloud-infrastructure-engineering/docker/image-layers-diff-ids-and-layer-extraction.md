---
id: computing-software.cloud-infrastructure-engineering.docker.image-layers-diff-ids-and-layer-extraction
name: image-layers-diff-ids-and-layer-extraction
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, image-inspect, layer-inspection, rootfs-layers, diff-ids, layer-extraction, extract-layer, oci-image-spec]
level: advanced
description: "Tell RootFS diff_ids from compressed manifest layer digests and chain IDs, map layers to history, and extract one layer's files for forensics."
sources: ["https://github.com/opencontainers/image-spec/blob/main/config.md", "https://github.com/opencontainers/image-spec/blob/main/layer.md", "https://github.com/opencontainers/image-spec/blob/main/manifest.md", "https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_blob.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RootFS layers, diff_ids and extracting a layer

## Three different hashes for "the same" layer
| Hash | Of what | Where |
|---|---|---|
| **diff_id** | uncompressed tar | image config `rootfs.diff_ids` |
| **layer digest** | compressed blob (gzip/zstd) | manifest `layers[].digest` |
| **chain id** | `Digest(ChainID(parent) + " " + DiffID(layer))`; the first layer's chain id is its diff_id | derived; identifies the applied stack of layers |

The OCI layer media types include plain tar, `+gzip` and `+zstd`, so the same uncompressed
layer can have different blob digests depending on compression, while its diff_id stays the
same.

```sh
crane manifest registry.example.com/app:1      # layers[].digest are the blob digests
crane config registry.example.com/app:1        # rootfs.diff_ids and history
```
In the image config, `history` entries with `empty_layer: true` (ENV, LABEL, CMD...) produce
no filesystem layer; skip them to align non-empty history entries with `diff_ids` in order.

## Extracting a single layer
Remote, no pull:
```sh
crane blob registry.example.com/app@sha256:<layer-digest> > layer.tar.gz
```
(`crane blob` writes the blob's bytes to stdout; extract it with the tool matching its media
type, gzip or zstd.) A local image can be written to a tar archive with `docker save`, which
streams a tarred repository. To flatten the whole filesystem instead, `crane export` and
`docker export` both exist.

## Whiteouts
Per the OCI image spec, a deleted path appears in a later layer as a whiteout entry named
`.wh.<basename>`, and `.wh..wh..opq` is an opaque whiteout that hides all siblings from lower
layers. When extracting a single layer manually, interpret whiteouts or you may see files
that do not exist in the running container.

## Uses
- Finding which layer added a secret or a huge file, then which instruction (history index).
- Proving a CVE-flagged file is in the base layers, not yours.
- Verifying two builds produce identical layers (compare diff_ids).

## Verify
The digest of the uncompressed layer tar equals its diff_id; the digest of the compressed blob
equals the manifest's layer digest.

## Checked
Date: 2026-10-26. Documentation: opencontainers/image-spec config.md (diff_ids, ChainID recursion, `empty_layer`) and layer.md (media types, whiteouts); crane docs (blob, manifest, config, export exist); docker/docs `docker save` reference. Confirmed: the three hashes and the chain id recursion, whiteout and opaque-whiteout names, media types, command existence. Removed as unconfirmed: the jq pipelines, `docker image inspect` template, the claim about the layout and compression of `docker save` output, the multi-tool blob-sharing consequence, and the `crane blob | tar` pipes (replaced by saving the blob).
Method: documentation only; no commands were run.
