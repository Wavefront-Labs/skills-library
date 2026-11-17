---
id: computing-software.cybersecurity-defensive.cosign.bundle-create
name: bundle-create
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, bundle-create, sigstore-bundle, rekor, rfc3161-timestamp]
level: advanced
status: docs-checked
description: "Assemble a Sigstore protobuf bundle from an artifact, signature, certificate or attestation with cosign bundle create, including Rekor lookup options."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_bundle_create.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_bundle.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bundle create

```
cosign bundle create --artifact <path> --signature <sig> --certificate <cert> --out bundle.sigstore.json
cosign bundle create --artifact <path> --attestation <att> --out bundle.sigstore.json
```

Flags:
- `--artifact` artifact file; `--attestation` attestation file.
- `--signature`: base64-encoded signature (over the attestation in DSSE format, per the help text).
- `--certificate`: signing certificate, "likely from Fulcio".
- `--key`, `--sk`, `--slot`: public key file, KMS URI, Kubernetes Secret or hardware key, for key-based signatures.
- `--bundle`: path to an old format bundle.
- `--rfc3161-timestamp`: path to a timestamp file.
- `--rekor-url` (default `https://rekor.sigstore.dev`); `--ignore-tlog` when the signature was not uploaded.
- `--out`: output path.

The examples build a bundle from a signature and certificate, or from an attestation. Inspect the result with `cosign bundle inspect bundle.sigstore.json` (see bundle-inspect-upgrade).

## Checked

2026-11-04. Confirmed on the cosign bundle create reference page: both examples, and every listed flag with its description and defaults. Removed: the claim that it converts older cosign output for `verify-blob --bundle` (not stated on the page).

Method: documentation only; no commands were run.
