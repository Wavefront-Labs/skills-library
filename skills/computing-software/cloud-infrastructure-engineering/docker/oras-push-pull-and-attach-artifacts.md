---
id: computing-software.cloud-infrastructure-engineering.docker.oras-push-pull-and-attach-artifacts
name: oras-push-pull-and-attach-artifacts
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, oras, oci-artifacts, oci-artifact, oras-push, artifact-type, media-types, oras-attach, cosign-attach]
level: advanced
description: "Store arbitrary files in an OCI registry with oras push/pull, set artifactType and layer media types, and attach SBOMs or signatures to an image."
sources: ["https://github.com/oras-project/oras/blob/main/cmd/oras/root/push.go", "https://github.com/oras-project/oras/blob/main/cmd/oras/root/attach.go", "https://github.com/oras-project/oras/blob/main/cmd/oras/root/pull.go", "https://github.com/oras-project/oras/blob/main/cmd/oras/root/discover.go", "https://github.com/opencontainers/image-spec/blob/main/manifest.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# oras push/pull and attaching artifacts

## Push and pull files
```sh
oras login registry.example.com
oras push registry.example.com/configs/policy:v3 \
  --artifact-type application/vnd.acme.policy.v1 \
  policy.rego:application/vnd.acme.policy.rego.v1 \
  data.json:application/json \
  --annotation "org.opencontainers.image.source=https://github.com/acme/policy"
oras pull registry.example.com/configs/policy:v3 -o ./policy
oras manifest fetch --pretty registry.example.com/configs/policy:v3
```
- Each file becomes a layer with the media type after `:`; default
  `application/vnd.oci.image.layer.v1.tar`.
- `--artifact-type` sets the manifest `artifactType` (OCI 1.1). Clients filter on it, so use
  a vendor-specific reverse-DNS string.
- `oras pull -o <dir>` writes files into the output directory (default `.`); `--allow-path-traversal`
  is needed to store files outside it and `--keep-old-files` refuses to overwrite.
- `oras cp` (alias `copy`) copies artifacts between registries; `oras repo tags`, `oras discover`.

## Attach to an existing image
```sh
oras attach registry.example.com/app:1.4.0 \
  --artifact-type application/spdx+json sbom.spdx.json:application/spdx+json
oras discover registry.example.com/app:1.4.0
oras pull registry.example.com/app@sha256:<referrer-digest>
```
`attach` creates a manifest whose `subject` points to the image digest - the image itself
is untouched, so its digest and signatures stay valid.

cosign equivalent:
```sh
cosign attest --predicate sbom.spdx.json --type spdxjson registry.example.com/app@sha256:...
```
Prefer signed attestations (`cosign attest`) over unsigned attachments. Select how referrers
are stored with `--distribution-spec v1.1-referrers-api` or `v1.1-referrers-tag` on `oras attach`.

## Registry support
`oras attach` relies on the OCI 1.1 `subject` field and the referrers API; where a registry lacks
the API, `--distribution-spec v1.1-referrers-tag` uses the referrers tag schema instead. Check
your registry's documentation for OCI 1.1 support before relying on either mode.

## Verify
`oras discover registry.example.com/app:1.4.0` lists the attached artifact with its type;
`oras pull` writes the files into the output directory.

## Checked
Documentation release: oras v1.3.6 source (cmd/oras/root push.go, attach.go, pull.go, cp.go, discover.go, manifest/fetch.go) command help and examples, checked 2026-10-26.
Confirmed: `oras push` `<file>[:<type>]` syntax, default layer media type `application/vnd.oci.image.layer.v1.tar`, `--artifact-type`, `--annotation`; `oras attach --artifact-type`, `--distribution-spec v1.1-referrers-api|v1.1-referrers-tag`; `oras pull -o` output directory and `--allow-path-traversal`, `--keep-old-files`; `cp` alias `copy`; `oras manifest fetch --pretty`; `oras discover` default tree output (`-o` is deprecated in favour of `--format`).
Removed as unsupported: the title-annotation restore detail, the registry product list, the "falls back to sha256-digest tag" claim for unknown media types, the `cosign attach sbom` line and the byte-identical `sha256sum` claim.
Method: documentation only; no commands were run.
