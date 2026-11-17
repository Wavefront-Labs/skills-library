---
id: computing-software.cybersecurity-defensive.cosign.signature-tag-storage
name: signature-tag-storage
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, signature-tag, tag-based-discovery, sig-suffix, oci-registry]
level: advanced
status: docs-checked
description: "Where cosign stores image signatures in a registry: the sha256-DIGEST.sig tag scheme, the OCI manifest layout, race conditions and why signatures outlive images."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/specs/SIGNATURE_SPEC.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tag-based signature discovery

Resolve the image tag to a digest, replace the `:` with `-`, append `.sig`:

`sha256:97fc...` becomes tag `sha256-97fc....sig` in the same repository (the spec's example uses a gcr.io repo). README shorthand: `s/:/-/g` and `s/@/:/g`.

Layout (OCI Image Manifest V1): one manifest per signed object; the payload is a blob referenced as a layer with media type `application/vnd.dev.cosign.simplesigning.v1+json`; the base64 signature is an annotation on that layer (`dev.cosignproject.cosign/signature` in the spec text). Several signatures can live in one manifest.

Consequences:
- Signing does not mutate the signed object.
- Race: multiple signatures are a "read-append-write" operation, so concurrent signers can lose one; the last write wins.
- Signatures are weakly linked, so deleting the image does not delete them (use `cosign clean`).
- They can be copied to another environment, but not automatically.
- Can store them elsewhere with `COSIGN_REPOSITORY` (see cosign-repository-env).
- The spec says implementations MAY use other discovery mechanisms; tag-based must be supported.

## Checked

2026-11-04. Confirmed in the cosign Signature Specification (tag-based discovery rules and example, OCI Image Manifest V1 layout, payload layer media type, signature annotation key, same or different repository, rationale on racy multiple signatures and no mutation) and in the README (weak reference, not garbage-collected, race wording, `s/:/-/g` shorthand, COSIGN_REPOSITORY). Removed: the advice to serialise signing jobs.

Method: documentation only; no commands were run.
