---
id: computing-software.cloud-infrastructure-engineering.docker.remote-image-inspect-and-copy-with-skopeo-and-crane
name: remote-image-inspect-and-copy-with-skopeo-and-crane
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, skopeo-inspect, crane-manifest, crane-copy, skopeo-copy, retag, registry, image-inspect, multi-arch]
level: practitioner
description: "Inspect manifests and configs remotely and copy or retag images between registries with crane and skopeo, keeping multi-arch indexes and digests intact."
sources: ["https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane.md", "https://github.com/containers/skopeo/blob/main/docs/skopeo-copy.1.md", "https://github.com/containers/skopeo/blob/main/docs/skopeo-inspect.1.md", "https://docs.docker.com/reference/cli/docker/buildx/imagetools/create/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote inspect and copy with skopeo and crane

**Why:** `docker pull` + `docker tag` + `docker push` downloads every layer and, by default, handles a single
platform. Registry-to-registry tools copy blobs directly and can preserve the index and its digest.

## Inspect without pulling

```sh
crane digest nginx:1.27                       # digest of the reference (index digest for multi-arch)
crane manifest nginx:1.27                     # the manifest or index JSON
crane config nginx:1.27 --platform linux/arm64
crane ls registry.example.com/app             # tags
skopeo inspect docker://nginx:1.27            # low-level information about the image in the registry
skopeo inspect --raw docker://nginx:1.27      # raw manifest or index
skopeo list-tags docker://registry.example.com/app
docker buildx imagetools inspect nginx:1.27
```

## Copy and retag

```sh
crane copy docker.io/library/nginx:1.27 registry.example.com/mirror/nginx:1.27
crane tag registry.example.com/app:sha-3f2a1c 1.4.0          # tag a remote image without downloading it
skopeo copy --all docker://nginx:1.27 docker://registry.example.com/mirror/nginx:1.27
skopeo sync --src docker --dest docker nginx registry.example.com/mirror   # all images found at the source
docker buildx imagetools create -t registry.example.com/app:1.4.0 registry.example.com/app:sha-3f2a1c
```

- `crane copy` copies an image while retaining the digest value; `--all-tags` copies every tag.
- `skopeo copy` of a multi-arch image copies only the image matching the system platform by default
  (`--multi-arch system`). Use `--all` (or `--multi-arch all`) to copy the whole list. `index-only` and
  platform lists create sparse manifest lists that usually fail unless the images already exist at the
  destination.
- Promotion (`staging` -> `prod`) by digest, `crane copy reg/app@sha256:... reg-prod/app:1.4.0`, keeps the
  bits you tested.

## Auth

`crane auth login <registry>` logs in. skopeo's default credentials file on Linux is
`${XDG_RUNTIME_DIR}/containers/auth.json` (`--authfile`, `--src-authfile`, `--dest-authfile`); it also offers
`--src-creds`, `--dest-creds`, `--src-tls-verify` and `--dest-tls-verify` for lab registries.

## Gotchas

- Signatures and attestations stored beside an image (for example cosign `sha256-<digest>.sig` tags, or
  referrers) are separate objects; copy them with a tool that copies referrers (`oras cp -r`) and verify in
  the destination.
- Docker Hub pulls count toward rate limits whichever tool you use.

## Verify

`crane digest` of the source and destination are identical; compare the manifest entries of both with
`crane manifest`.

## Checked

2026-10-26. Documentation release: go-containerregistry crane docs and skopeo man pages (copy, inspect, sync) at main, docker/docs buildx imagetools reference, oras-project/oras main, checked 2026-10-26. Confirmed: crane digest, manifest, config --platform, ls, copy (retains digest, --all-tags), tag (no download), auth login; skopeo inspect and --raw, list-tags, copy --all and --multi-arch semantics, sync --src --dest syntax, default auth file path and the creds and TLS flags; oras cp -r for referrers. Removed unconfirmed claims: jq pipelines, crane reading ~/.docker/config.json, skopeo falling back to docker's config, the claim that crane copy keeps the index by default beyond the digest-retention statement, the imagetools same-repo restriction, and `cosign copy` (deprecated in the cosign source).

Method: documentation only; no commands were run.
