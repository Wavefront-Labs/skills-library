---
id: computing-software.cybersecurity-defensive.cosign.bundle-oci-referrers
name: bundle-oci-referrers
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, bundle-spec, referrers-api, bundle-annotations, artifact-type, oci-referrers]
level: sme
status: docs-checked
description: "How Sigstore bundles are stored on images: artifactType manifest with subject, referrers API and tag fallback, and the dev.sigstore.bundle annotations."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/specs/BUNDLE_SPEC.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bundles as OCI referrers (spec)

Publish: upload the JSON bundle as a blob, then PUT a manifest:
- `artifactType` and layer `mediaType`: `application/vnd.dev.sigstore.bundle.v0.3+json`
- `config`: the empty descriptor (`application/vnd.oci.empty.v1+json`, size 2)
- one layer pointing at the bundle blob; optional layer annotation `org.opencontainers.image.title` as `{algo}-{hex}.sigstore.json` (hyphen, valid on Windows, works with `oras pull`)
- `subject`: digest and mediaType of the image described.

Registries with the referrers API list it under the subject automatically. Without it, create or update an image index tagged with the digest, `sha256-<hex>` (referrers tag schema).

Retrieve: `GET /v2/<repo>/referrers/<digest>`; a 404 means no referrers API, so fall back to `GET /v2/<repo>/manifests/sha256-<hex>`.

Annotations on the items of the index `manifests` list:
- `dev.sigstore.bundle.content`: `message-signature` or `dsse-envelope`
- `dev.sigstore.bundle.predicateType`: the in-toto predicate, for DSSE bundles
- `org.opencontainers.image.created`: RFC 3339 time

Use `cosign tree` or `--registry-referrers-mode` to look for them.

## Checked

2026-11-04. Confirmed in the cosign Bundle Specification: publishing steps (blob, manifest with artifactType, empty config of size 2, single layer, subject), referrers API and referrers tag fallback, retrieval with 404 fallback, the three annotations and the `org.opencontainers.image.title` layer annotation; and on the cosign tree and sign pages (`--registry-referrers-mode`). Removed: the claim that a 404 on the fallback tag means nothing is attached.

Method: documentation only; no commands were run.
