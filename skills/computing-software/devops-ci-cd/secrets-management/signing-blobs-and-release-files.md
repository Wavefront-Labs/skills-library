---
id: computing-software.devops-ci-cd.secrets-management.signing-blobs-and-release-files
name: signing-blobs-and-release-files
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, artifact-signing, cosign, cosign-sign-blob, cosign-verify-blob, sigstore-bundle, release-assets, checksums, sha256sums, goreleaser-signing, binary-signing, verify-downloads]
level: advanced
status: gated
description: "Sign release binaries, tarballs and checksum files with cosign sign-blob (keyless or KMS), ship .sigstore.json bundles with the release, and give users a one-line verify command."
sources: ["https://docs.sigstore.dev/cosign/signing/signing_with_blobs/", "https://docs.sigstore.dev/cosign/verifying/verify/", "https://goreleaser.com/customization/sign/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signing blobs and release files

## Sign the checksum file, not every binary
```bash
sha256sum dist/*.tar.gz dist/*.zip > dist/SHA256SUMS
# keyless (CI with OIDC: GitHub id-token: write, GitLab SIGSTORE_ID_TOKEN)
cosign sign-blob --yes --bundle dist/SHA256SUMS.sigstore.json dist/SHA256SUMS
# or with a KMS key
cosign sign-blob --yes --key awskms:///alias/release --bundle dist/SHA256SUMS.sigstore.json dist/SHA256SUMS
```
The **bundle** (`--bundle`) is a Sigstore bundle (`application/vnd.dev.sigstore.bundle.v0.3+json`, run on cosign v3.1.3) with the signature, the Rekor
entry and timestamp data, plus the Fulcio certificate for keyless or the public key for `--key` signing, in one file; ship it next to the artifact. Older flows used separate
`--output-signature x.sig --output-certificate x.pem`; bundles are simpler and verify
offline.

## User-side verification (put this in the README)
```bash
cosign verify-blob dist/SHA256SUMS \
  --bundle SHA256SUMS.sigstore.json \
  --certificate-identity "https://github.com/acme/tool/.github/workflows/release.yml@refs/tags/v1.4.0" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
sha256sum --ignore-missing -c SHA256SUMS
```
For key-based: `cosign verify-blob --key cosign.pub --bundle ... SHA256SUMS` (run: `Verified OK`; one appended byte gave `invalid signature when validating ASN.1 encoded signature`).
With `--use-signing-config=false --tlog-upload=false` the bundle has no log entry and verifies only with `--insecure-ignore-tlog=true`.
On v3, `--output-signature` without `--bundle` is rejected (`must specify --bundle with --new-bundle-format`); keyless signing, the identity flags and GoReleaser/`gh attestation` rows are (gated: unconfirmed, needs a CI OIDC token and accounts).

## GoReleaser
```yaml
signs:
  - cmd: cosign
    signature: "${artifact}.sigstore.json"
    artifacts: checksum
    args: ["sign-blob", "--yes", "--bundle=${signature}", "${artifact}"]
```

## Choices
- Signing every artifact individually is fine for a handful; checksum-file signing scales
  and also gives integrity for downloads via `sha256sum -c`.
- GitHub alternative: `actions/attest-build-provenance` creates Sigstore-backed
  attestations verified with `gh attestation verify file --repo acme/tool`; both can
  coexist.
- GPG signatures (`.asc`) are still expected by some distros/package managers; add them if
  your consumers require them, but key distribution is on you.

## Gotchas
- Sign **after** the final bytes exist; re-zipping or notarising (macOS) afterwards
  invalidates the signature. Notarise first, then checksum and sign.
- Identity for tag-triggered releases contains the tag ref; document a regexp
  (`--certificate-identity-regexp '^https://github.com/acme/tool/.github/workflows/release.yml@refs/tags/v'`).
- `--yes` is needed in CI (no prompt for the transparency log upload).

## Verify
Download the release assets into an empty dir and run the README commands: `Verified OK`
then each file `OK`. Flip one byte in SHA256SUMS: verification fails.
