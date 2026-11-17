---
id: computing-software.cybersecurity-defensive.cosign.simple-signing-payload
name: simple-signing-payload
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, simple-signing, payload, critical-type, sha256]
level: sme
status: docs-checked
description: "The Simple Signing JSON payload cosign signs for images, its fixed type string, the digest chain Sign(sha256(payload(sha256(manifest)))) and why hash agility is pinned."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/specs/SIGNATURE_SPEC.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Simple Signing payload

Media type: `application/vnd.dev.cosign.simplesigning.v1+json`. Content (Red Hat simple signing):

```
{"critical":{"identity":{"docker-reference":"testing/manifest"},
 "image":{"Docker-manifest-digest":"sha256:20be...fe55"},
 "type":"cosign container image signature"},
 "optional":{"creator":"atomic","timestamp":1458239713}}
```

Rules from the spec:
- `critical.type` is `cosign container image signature`.
- `critical.identity.docker-reference` is ignored.
- User claims (from `-a key=value`) go in `optional`.
- The payload MUST hold the image digest because signatures are detached.

Hashing: no algorithm is stored. The digest must use the same algorithm as the registry (sha256 in practice). The binding is `Sign(sha256(SimpleSigningPayload(sha256(Image Manifest))))`. Allowing another outer hash would only alter the outer layer, since the manifest is always referenced by sha256, so the spec pins it to cut attack surface.

Inspect a payload without signing: `cosign generate $IMAGE_URI_DIGEST` (README).

The spec says `docker-reference` is ignored; the digest is what links the payload to the image.

## Checked

2026-11-04. Confirmed in the cosign Signature Specification (payload media type, critical.type, ignored docker-reference, optional claims, example, hashing section with the Sign(sha256(...)) chain and the sha256 manifest reference, rationale for pinning the hash) and in the README (`cosign generate`). Removed: the inference that a verifier cannot bind signatures to repository names.

Method: documentation only; no commands were run.
