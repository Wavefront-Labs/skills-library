---
id: computing-software.cybersecurity-defensive.cosign.blob-timestamp-authority
name: blob-timestamp-authority
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, tsa, timestamp-authority, timestamp-client-cert, rfc3161]
level: advanced
status: docs-checked
description: "Configure mTLS to an RFC 3161 timestamp authority when signing with cosign sign, sign-blob, attest and attest-blob."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign-blob.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_attest-blob.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timestamp authority connection flags

The signing commands expose four flags for the connection to a TSA server (RFC 3161 timestamp authority, mTLS):

- `--timestamp-client-cacert` CA certificate (PEM) for the TSA connection
- `--timestamp-client-cert` client certificate (PEM)
- `--timestamp-client-key` private key (PEM), used together with the client cert
- `--timestamp-server-name` SAN to use as the `ServerName` in tls.Config to verify the mTLS connection

The same four flags appear, with identical help text, in the options of `cosign sign`, `cosign sign-blob`, `cosign attest-blob` and `cosign attest`. The `sign`, `sign-blob` and `attest-blob` pages also list `--signing-config` (path to a signing config file) and `--trusted-root` ("optional path to a TrustedRoot JSON file to verify a signature after signing"). The pages show no worked example using the timestamp flags and do not say where the TSA address is set.

## Checked

2026-11-04. Confirmed against the cosign sign, sign-blob and attest-blob docs: the four flag names and help text, and that they appear on all three. Removed: the invented sign-blob example, the claim about where the TSA URL comes from (`--tsa`, `--tsa-config` in signing-config create), the verify advice with cross-references, and the "no default TSA" line. The attest page also lists the four flags but is not a listed source.
Method: documentation only; no commands were run.
