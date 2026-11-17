---
id: computing-software.cloud-infrastructure-engineering.docker.oras-manifest-and-index-operations
name: oras-manifest-and-index-operations
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, oras, oras-manifest, oci-artifacts, oci-index, manifest-fetch, discover]
level: advanced
status: docs-checked
description: "Work with raw OCI manifests using oras: manifest fetch/push/delete, fetching configs and blobs, discovering referrers, and assembling an index from existing manifests."
sources: ["https://github.com/oras-project/oras/blob/main/cmd/oras/root/manifest/fetch.go", "https://github.com/oras-project/oras/blob/main/cmd/oras/root/manifest/push.go", "https://github.com/oras-project/oras/blob/main/cmd/oras/root/manifest/index/create.go", "https://github.com/oras-project/oras/blob/main/cmd/oras/root/manifest/index/update.go", "https://github.com/oras-project/oras/blob/main/cmd/oras/root/discover.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# oras manifest and index operations

`oras push/pull` handle files. The `oras manifest`, `oras blob` and `oras discover` commands
give direct control over registry objects, useful for debugging and for building artifacts
other tools do not support.

## Read
```bash
oras manifest fetch --pretty reg.example.com/app:1.2                  # manifest or index
oras manifest fetch --descriptor reg.example.com/app:1.2              # digest, size, mediaType
oras manifest fetch --platform linux/arm64 reg.example.com/app:1.2    # resolve a platform from an index
oras manifest fetch-config reg.example.com/app:1.2 | jq .config
oras blob fetch --output layer.tgz reg.example.com/app@sha256:<layer-digest>
oras discover reg.example.com/app:1.2                                 # signatures, SBOMs attached via referrers
oras repo tags reg.example.com/app
```

## Write
```bash
# push a hand-written manifest (blobs must already exist in the repo)
oras manifest push reg.example.com/app:custom manifest.json \
  --media-type application/vnd.oci.image.manifest.v1+json
# delete by tag or digest (asks for confirmation unless forced)
oras manifest delete reg.example.com/app@sha256:<digest>
# copy with referrers to another registry ([Preview] flag)
oras cp -r reg.example.com/app:1.2 backup.example.com/app:1.2
```

## Build an index from separate manifests
```bash
oras manifest index create reg.example.com/tool:1.0 1.0-linux-amd64 1.0-linux-arm64
oras manifest index update reg.example.com/tool:1.0 --add 1.0-windows-amd64
```
The source manifests are given as tags or digests in the same repository as the target
(`<target>[:<tag>] <sources>...`); `index update` is marked experimental and also supports
`--merge`, `--remove` (digests only), `--tag` and `--artifact-type`. `--output <path>` (or `-`
for stdout) writes the index instead of pushing it.

## Useful flags
`--plain-http` for HTTP registries, `--insecure` to allow connections to a registry with an
invalid or missing certificate, `--oci-layout` to operate on a local OCI layout directory instead of a registry,
`--descriptor` on `manifest fetch`, `push` and `delete` to print the descriptor, `--pretty` for
readable JSON.

## Gotchas
- A manifest refers to blobs by digest, so the blobs it references must already exist in the
  repository before `manifest push`; push them with `oras blob push`.
- Some registries may reject unknown `artifactType` or config media types; test on a scratch
  repository first.
- `manifest push` can use `--distribution-spec v1.1-referrers-api` or `v1.1-referrers-tag` to
  select how a manifest with a `subject` is registered.

## Checked
Documentation release: oras v1.3.6 source (cmd/oras/root/manifest/*.go, cp.go, discover.go) command help and examples, checked 2026-10-26.
Confirmed: `manifest fetch` flags `--descriptor`, `--platform`, `--pretty`, `--media-type`, `--output`; `manifest push --media-type`; `manifest delete` aliases and `--descriptor`; `manifest index create` and `update` argument forms (sources as tags or digests in the same repository), `--add`, `--merge`, `--remove`, `--tag`, `--artifact-type`, `--output`; `oras cp -r` ([Preview]); `oras blob fetch --output`; `--distribution-spec` values.
Corrected: index create/update sources are repository-relative tags or digests, not full references; `oras discover -o` is deprecated.
Removed as unsupported: the `MANIFEST_BLOB_UNKNOWN` error text, `docker buildx imagetools create` equivalence, "platform info comes from each manifest's config" and the orphaned-referrers claim.
Method: documentation only; no commands were run.
