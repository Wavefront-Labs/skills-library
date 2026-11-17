---
id: computing-software.cybersecurity-defensive.cosign.sign-bundle-output
name: sign-bundle-output
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, bundle, sigstore-json, offline-verification]
level: practitioner
status: docs-checked
description: "Write all verification material to a single file with --bundle on cosign sign, sign-blob and attest, and verify with it later, including the sigstore.json convention."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign-blob.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bundle output

`--bundle string`: "write everything required to verify the image to FILE" (sign), blob (sign-blob, attest-blob).

Blob workflow from the README:

```
cosign sign-blob artifact --bundle artifact.sigstore.json --yes
cosign verify-blob artifact --bundle artifact.sigstore.json \
  --certificate-identity "https://github.com/ORG/REPO/.github/workflows/release.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
```

The verify-blob docs call the bundle the "preferred way to provide verification material": it contains the signature, certificate and transparency log proof.

Notes:
- With `--signing-config`, sign-blob requires `--bundle` so the new-format verification material has somewhere to go.
- Inspect a bundle with `cosign bundle inspect`; upgrade older ones with `bundle upgrade`.

## Checked

2026-11-04. Confirmed on the cosign sign and sign-blob reference pages (`--bundle` descriptions, `--signing-config` requires `--bundle` on sign-blob), the verify-blob page (preferred way, bundle contents) and the README keyless blob example. Removed: the shipping advice, the no-network-lookup claim and the offline trusted-root remark.

Method: documentation only; no commands were run.
