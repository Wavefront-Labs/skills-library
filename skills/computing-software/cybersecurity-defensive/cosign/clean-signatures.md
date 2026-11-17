---
id: computing-software.cybersecurity-defensive.cosign.clean-signatures
name: clean-signatures
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, clean, delete-signatures, registry-cleanup]
level: practitioner
status: docs-checked
description: "Remove cosign signatures, attestations or referrers from an image with cosign clean, selecting the type and skipping the confirmation with -f."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_clean.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cosign clean

"Remove all signatures from an image."

```
cosign clean <IMAGE>
cosign clean --type attestation <IMAGE>
cosign clean -f --type signature <IMAGE>
```

- `--type CLEAN_TYPE`: `signature`, `attestation`, `referrer`, `sbom` (deprecated) or `all` (default).
- `-f, --force`: do not prompt for confirmation.
- Registry auth and TLS flags and `--k8s-keychain` are available.

Careful: the default type is `all`, so a bare `cosign clean` removes every type. Add `--type` for anything narrower.

Why it exists: README says signatures are separate registry objects with only a weak reference to the image, so deleting an image does not remove them and they are not garbage collected. Clean them explicitly.

## Checked

2026-11-04. Confirmed on the cosign clean reference page (description, `--type` values with default all and sbom deprecated, `-f, --force`, registry flags, `--k8s-keychain`) and in the README (signatures are separate objects with a weak reference and are not deleted or garbage-collected with the image). Removed: the `.sig` tag remark, the claim that a bare clean removes only signatures and attestations, and the after-cleaning verify prediction.

Method: documentation only; no commands were run.
