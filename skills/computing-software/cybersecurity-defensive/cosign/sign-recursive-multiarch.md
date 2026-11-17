---
id: computing-software.cybersecurity-defensive.cosign.sign-recursive-multiarch
name: sign-recursive-multiarch
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, recursive-signing, multi-arch, image-index]
level: practitioner
status: docs-checked
description: "Sign a multi-arch image index and every referenced platform image with cosign sign --recursive, and what the flag does and does not cover."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recursive signing of multi-arch images

```
cosign sign --key cosign.key --recursive <MULTI-ARCH IMAGE DIGEST>
```

Flag `-r, --recursive`: "if a multi-arch image is specified, additionally sign each discrete image". The docs example describes it as signing the multi-arch image AND all referenced, discrete images.

Pass the multi-arch image by digest (`@sha256:...`), as the sign page's warning says. The example uses `--key cosign.key`.

## Checked

2026-11-04. Confirmed on the cosign sign reference page: the `-r, --recursive` text, the example "sign a multi-arch container image AND all referenced, discrete images" and the digest warning. Removed: the claims about what happens without the flag, per-digest signature lookup and the number of signature tags created (none on the page).

Method: documentation only; no commands were run.
