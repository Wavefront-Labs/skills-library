---
id: computing-software.cybersecurity-defensive.trivy.verify-trivy-signatures-cosign-gpg
name: verify-trivy-signatures-cosign-gpg
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [cosign, signature-verification, sigstore, verify-blob, gpg, supply-chain-security, keyless]
level: advanced
status: docs-checked
description: "Verify Trivy container images with keyless cosign, release assets with sigstore bundles (v0.68.1+), and RPM packages with the published GPG key."
sources:
  - https://trivy.dev/latest/docs/getting-started/signature-verification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All Trivy binaries and container images are signed with Cosign.

Container image, keyless:
```shell
cosign verify aquasec/trivy:<version> \
  --certificate-identity-regexp 'https://github\.com/aquasecurity/trivy/\.github/workflows/.+' \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
```
A good result lists checks such as validated cosign claims, offline transparency-log verification and a certificate chained to trusted CAs.

Release assets: since Trivy v0.68.1 GitHub Releases ship sigstore signature bundles; separate `.sig` and `.pem` files are no longer published, and every asset has a matching `.sigstore.json`. Download both files, then (cosign v3.0.0 or later; with cosign v2.4.0+ add `--new-bundle-format`):
```shell
cosign verify-blob <path to asset> \
  --bundle <path to asset>.sigstore.json \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com \
  --certificate-identity 'https://github.com/aquasecurity/trivy/.github/workflows/reusable-release.yaml@refs/tags/<release tag>'
```
Expect `Verified OK`. The same applies to `.deb`, `.rpm` and `.zip`.

GPG for RPM and DEB: fetch `https://aquasecurity.github.io/trivy-repo/rpm/public.key`, run `rpm --import pub.key`, check with `rpm -q --queryformat "%{SUMMARY}\n" $(rpm -q gpg-pubkey)` (expect `gpg(trivy)`), then verify a downloaded package with `rpm -K trivy.rpm`, which should print `digests signatures OK`.

## Checked

2026-11-03. Read and confirmed against the Signature Verification page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
