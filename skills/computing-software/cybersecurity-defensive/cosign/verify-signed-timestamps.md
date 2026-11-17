---
id: computing-software.cybersecurity-defensive.cosign.verify-signed-timestamps
name: verify-signed-timestamps
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, use-signed-timestamps, rfc3161, trusted-root, timestamp-verification]
level: advanced
status: docs-checked
description: "Verify RFC 3161 signed timestamps and use a Sigstore trusted root with cosign verify, including the known 'threshold not met' error and its fix."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signed timestamps and trusted root

Flags on verify, verify-attestation, verify-blob, verify-blob-attestation:
- `--use-signed-timestamps`: verify rfc3161 timestamps.
- `--trusted-root`: path to a Sigstore TrustedRoot JSON file.

```
cosign verify --trusted-root trusted_root.json <IMAGE>
cosign verify --use-signed-timestamps --certificate-identity ... --certificate-oidc-issuer ... <IMAGE>
```

README troubleshooting:
- Error `failed to verify timestamps: threshold not met for verified log entry integrated timestamps: 0 < 1` means the signature may require RFC3161 timestamp support. Upgrade to the most recent cosign, or with Cosign 2.6.x use `--use-signed-timestamps`.
- Error `no signatures found` may mean the signature requires Rekor v2 support; upgrade.

A trusted root holds the keys and certificates of Fulcio, Rekor, the CT log and timestamp authorities. For the public-good instance it comes from the TUF repository (`cosign initialize`); for a private deployment build it with `cosign trusted-root create`.

Signing side: provide timestamp authority settings (see blob-timestamp-authority).

## Checked

2026-11-04. Confirmed in the cosign README troubleshooting (both error strings, the upgrade and Cosign 2.6.x `--use-signed-timestamps` remedies, the Rekor v2 note), on the cosign verify, verify-attestation, verify-blob pages (`--use-signed-timestamps`, `--trusted-root`), the trusted-root create page (`--fulcio`, `--rekor`, `--ctfe`, `--tsa`) and the initialize page (TUF repository).

Method: documentation only; no commands were run.
