---
id: computing-software.cloud-infrastructure-engineering.docker.signing-digests-and-multi-arch-indexes
name: signing-digests-and-multi-arch-indexes
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, image-signing, sign-by-digest, recursive-signing, cosign, multi-arch, manifest-list]
level: advanced
status: docs-checked
description: "Sign the immutable thing: resolve tags to digests, sign the multi-arch index vs each platform manifest (cosign --recursive), and how verifiers resolve platform pulls."
sources: ["https://docs.sigstore.dev/cosign/signing/signing_with_containers/", "https://github.com/sigstore/cosign/blob/main/doc/cosign_sign.md", "https://github.com/opencontainers/image-spec/blob/main/image-index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signing digests and multi-arch indexes

## Why digests
A signature binds to a manifest digest. `cosign sign app:latest` resolves the tag **at that
moment**; if someone pushes a new `latest` between your build and the sign step, you sign
their image. The `cosign sign` reference says to sign by digest (`@sha256:...`) rather than by tag. Always:
```bash
DIGEST=sha256:<digest>                                # the build step's digest output
cosign sign --yes reg.example.com/app@$DIGEST
```

## Multi-arch images
A multi-arch tag points to an **index**; each platform has its own manifest digest.
| Signed object | Verifies when a client checks... |
|---|---|
| Index digest only | The tag / index digest (what most humans and admission controllers check) |
| Each platform manifest (`--recursive`) | A platform-specific digest, e.g. after a node resolved `linux/arm64` |

```bash
cosign sign --yes --recursive reg.example.com/app@sha256:<index-digest>   # index + every child
cosign tree reg.example.com/app@sha256:<index-digest>                      # what is attached where
```

How verifiers behave:
- A verifier that checks the index digest is satisfied by a signature on the index.
- A verifier that checks the platform manifest a node actually pulled needs that manifest
  signed too: use `--recursive` (documented as "if a multi-arch image is specified,
  additionally sign each discrete image").

## Attestations on multi-arch images
BuildKit stores SBOM and provenance attestations as separate manifests referenced from the
index. Check with `cosign tree` which objects carry signatures after signing.

## Gotchas
- `imagetools create` merging per-runner digests creates a **new** index digest; sign after the
  merge, not the per-platform pushes (or both).
- Copying images with tools that rewrite manifests changes digests, and a signature binds to a
  digest; compare digests after any copy and re-sign if they differ.
- Pin deployments by digest (`app@sha256:...`) so what is verified is what runs.

## Checked
Documentation release: cosign v3.1.4 `cosign sign` reference and docs.sigstore.dev signing-containers page, checked 2026-10-26.
Confirmed: sign by digest guidance; `-r/--recursive` meaning; `cosign tree`; signatures stored as OCI 1.1 referrers.
Removed as unsupported by the docs: "cosign 2.x warns" version gate, `crane digest` example, Kyverno and policy-controller verification behaviour, "`--platform` workflows", the claim that signing the index covers attestation manifests, and `crane copy`/`oras cp`/`cosign copy` byte-preservation claims.
Method: documentation only; no commands were run.
