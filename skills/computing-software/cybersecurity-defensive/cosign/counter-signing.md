---
id: computing-software.cybersecurity-defensive.cosign.counter-signing
name: counter-signing
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, counter-signing, triangulate, signature-signing, base-image]
level: sme
status: docs-checked
description: "Counter-sign a cosign signature artifact so a second party attests to the signature itself, using annotations and a tag on the .sig manifest."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Counter-signing

Signature artifacts are also registry objects, so they can be signed. The result protects the signature set and the artifact it references.

README procedure:

1. Sign with a memorable annotation: `cosign sign --key cosign.key -a sig=original $IMAGE_URI_DIGEST`.
2. Find the signature manifest and give it a tag: `crane tag $(cosign triangulate $IMAGE_URI) mysignature`.
3. Sign that: `cosign sign --key cosign.key -a sig=counter dlorenc/demo:mysignature`.
4. Verify: `cosign verify --key cosign.pub dlorenc/demo:mysignature` returns an `Optional` section with `sig: counter`.

The signature manifest then shows layers with media type `application/vnd.oci.descriptor.v1+json` and the signature annotation `dev.sigstore.cosign/signature`.

`cosign triangulate $IMAGE_URI` supplies the signature manifest reference that `crane tag` tags in step 2.

Gotchas:
- Step 3 signs by tag in the README; prefer the digest from step 2 (the same rule as everywhere).
- The README has a TODO linked to issue 2333 in this flow.
- Related idea in the README, base image signing: sign the ordered base layers and attach the signature as annotation `dev.cosign.signature.baseimage` on the last base layer. It is described as a "rough idea", not a feature.

## Checked

2026-11-08. Read in full: the cosign README (raw, sigstore/cosign), including the Counter-Signing and Base Image/Layer Signing sections. Confirmed every step, annotation and media type above. Reworded the `triangulate` line, which the README shows only inside the `crane tag` step.

Method: documentation only; no commands were run.
