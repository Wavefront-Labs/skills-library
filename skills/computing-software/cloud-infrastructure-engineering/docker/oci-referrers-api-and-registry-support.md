---
id: computing-software.cloud-infrastructure-engineering.docker.oci-referrers-api-and-registry-support
name: oci-referrers-api-and-registry-support
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, oci-artifacts, referrers-api, oci-referrers, subject-field, artifact-support, zot, distribution-spec]
level: advanced
description: "Understand OCI 1.1 subject and the referrers API, the tag-schema fallback, and test which registries (zot, Harbor, cloud) support artifacts properly."
sources: ["https://github.com/opencontainers/distribution-spec/blob/main/spec.md", "https://github.com/opencontainers/image-spec/blob/main/manifest.md", "https://github.com/oras-project/oras/blob/main/cmd/oras/root/attach.go", "https://github.com/oras-project/oras/blob/main/cmd/oras/root/cp.go", "https://github.com/oras-project/oras/blob/main/cmd/oras/root/discover.go"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OCI referrers API and registry support

## The model
OCI 1.1 added to manifests:
- `subject`: descriptor of the manifest this one refers to (signature, SBOM, attestation).
- `artifactType`: what the artifact is.

and to the distribution API:
```
GET /v2/<name>/referrers/<digest>[?artifactType=<type>]
```
returning an OCI image index whose `manifests[]` are the manifests whose `subject` is `<digest>`.
If the `artifactType` query filter is applied, the response carries the header
`OCI-Filters-Applied: artifactType`. A registry that supports the API must not answer `404` to a
referrers request for a repository it finds.
```sh
oras discover --format json registry.example.com/team/app@sha256:<digest>
```

## The fallback (referrers tag schema)
Registries without the API: the client pushes the referrer, then pulls, updates and pushes back an
index at a tag of the form `<algorithm>-<hex>` (for example `sha256-<digest-hex>`) listing the
referrers. When pushing a manifest with `subject`, a registry that processed it itself returns the
header `OCI-Subject: <subject digest>`; if that header is missing the client must use the fallback.
The client updates the list itself (it may use conditional requests to avoid overwriting a
concurrent change), and those tags show up in tag listings.

## Checking a registry
```sh
oras attach --artifact-type application/vnd.test.v1 reg/repo:tag test.txt
oras discover reg/repo:tag                      # works either way
```
A `GET /v2/<repo>/referrers/<digest>` answering `200` means the API is supported (a supporting
registry may not answer `404`); with `404`, clients use the tag fallback. `oras attach` can force a
method with `--distribution-spec v1.1-referrers-api` or `v1.1-referrers-tag`. Check support for your
registry and version in that registry's documentation; this skill does not list versions.

## Why it matters
- Signature verification and SBOM discovery tools that use the referrers API depend on it.
- `oras cp -r` (`--recursive`, marked Preview) copies an artifact together with its referrer
  artifacts; confirm that any other copy tool you use does the same before relying on it.

## Verify
Referrers listed via the API match `oras discover`; after copying to another registry, the
same discover call returns the same artifact digests.

## Checked

2026-10-25, against the OCI distribution-spec `spec.md` (referrers API, `OCI-Subject`, `OCI-Filters-Applied`, referrers tag schema), image-spec `manifest.md` (`subject`, `artifactType`) and ORAS source (`attach`, `cp`, `discover`). Confirmed: `GET /v2/<name>/referrers/<digest>` with the `artifactType` filter, index response, fallback tag schema, client behaviour without `OCI-Subject`, `oras attach --distribution-spec v1.1-referrers-api|v1.1-referrers-tag`, `oras cp -r`. Removed as unconfirmed: the registry support list, the `crane copy` and garbage-collection claims, the zot quick start, the crane and jq commands, and the 'race-prone' wording (the spec says clients may use conditional requests).

Method: documentation only; no commands were run.
