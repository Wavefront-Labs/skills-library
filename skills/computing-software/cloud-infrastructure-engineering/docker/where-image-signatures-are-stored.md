---
id: computing-software.cloud-infrastructure-engineering.docker.where-image-signatures-are-stored
name: where-image-signatures-are-stored
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, image-signing, signature-storage, sig-tags, oci-referrers, cosign, notation]
level: advanced
status: docs-checked
description: "Know where cosign and Notation put signatures (.sig tags vs OCI 1.1 referrers), how to list and copy them with images, and how cleanup and mirroring can silently drop them."
sources: ["https://github.com/sigstore/cosign/blob/main/specs/SIGNATURE_SPEC.md", "https://github.com/opencontainers/distribution-spec/blob/main/spec.md#listing-referrers", "https://notaryproject.dev/docs/user-guides/how-to/manage-signatures/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Where image signatures are stored

## cosign (default: tag scheme)
For image digest `sha256:abc...`, cosign pushes an OCI artifact tagged
`sha256-abc....sig` in the **same repository**. Attestations go to `sha256-abc....att`,
attached SBOMs to `.sbom`.
```bash
cosign triangulate reg.example.com/app:1.4.0            # prints the .sig tag reference
cosign tree reg.example.com/app:1.4.0                   # signatures, attestations, SBOMs
crane ls reg.example.com/app
```
Optional: `COSIGN_REPOSITORY=reg.example.com/signatures` stores them in a separate repo
(verifiers must set the same variable).

## OCI 1.1 referrers (Notation, newer cosign modes, ORAS)
The signature manifest points at the image digest as its subject; the registry indexes it so clients call
`GET /v2/<repo>/referrers/<digest>`. If the referrers API returns 404, clients must fall back to the
referrers tag schema, a tag derived from the digest that holds an index of referrers. Notation uses the tag
schema by default and the Referrers API only with its experimental `--allow-referrers-api` flag.
```bash
oras discover --format tree reg.example.com/app@sha256:<digest>
notation ls reg.example.com/app@sha256:<digest>
```

## Moving images without losing signatures
| Tool | Signatures copied? |
|---|---|
| `docker pull` + `docker push` | No |
| `crane copy` (single ref) | Copies the image and retains its digest; does not copy `.sig` tags |
| `cosign copy src dst` | Yes, but the command is deprecated (use `oras cp -r`, or `cosign save` / `cosign load`) |
| `oras cp -r` | Yes (copies the artifact and its referrers; marked Preview) |
| `skopeo copy` | Copies signatures only in its own signature formats; check `--all` and the signature options |
| Harbor replication | Replicates matching resources and their associated Cosign signatures |

## Cleanup and mirroring pitfalls
- Tag-based retention rules see `.sig`, `.att` and `.sbom` tags as ordinary tags, so exclude them (or
  keep them paired with the images they sign) in tag-based rules.
- A signature is bound to the image digest: re-pushing after a format conversion changes the digest and the
  old signature no longer applies.

## Verify after any copy
```bash
cosign verify --certificate-identity-regexp '<identity-regexp>' --certificate-oidc-issuer '<issuer-url>' dst.example.com/app@sha256:<digest>
```

## Checked

2026-10-26. Documentation release: sigstore/cosign main (specs/SIGNATURE_SPEC.md and source for the .sig, .att and .sbom suffixes, COSIGN_REPOSITORY and the copy command), OCI distribution-spec main (referrers API and tag-schema fallback), oras-project/oras main (cp and discover commands), notaryproject docs, Harbor website docs, checked 2026-10-26. Confirmed: the sha256-<digest>.sig tag scheme with .att and .sbom suffixes, COSIGN_REPOSITORY override, cosign triangulate and tree commands, referrers endpoint and 404 fallback, Notation default and experimental Referrers API flag, oras cp -r and discover. Fixed: cosign copy is marked deprecated in the source, and `oras discover -o` is deprecated in favour of `--format`. Removed unconfirmed claims: pull-through cache behaviour for signature tags, skopeo sync signature copying, and a grep on suffixes.

Method: documentation only; no commands were run.
