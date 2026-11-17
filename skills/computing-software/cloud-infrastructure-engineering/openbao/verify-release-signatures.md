---
id: computing-software.cloud-infrastructure-engineering.openbao.verify-release-signatures
name: verify-release-signatures
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, checksum, signature, cosign, gpg]
level: practitioner
status: docs-checked
description: "Verify an OpenBao release download with the SHA-256 checksums file, GPG signature and Cosign keyless sigstore bundle."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/install.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verifying an OpenBao release

Download the release tarball plus `checksums.txt`, `checksums.txt.gpgsig` and `checksums.txt.sigstore.json`.

## Checksum

```
sha256sum --ignore-missing --check checksums.txt
```

## GPG

Import the OpenBao public key, then verify:

```
gpg2 --import <public-key-file>
gpg2 --verify checksums.txt.gpgsig checksums.txt
```

gpg may warn the key is not certified by a trusted signature; the docs' sample output shows this warning.

## Cosign (keyless)

Use `cosign verify-blob` with `--bundle checksums.txt.sigstore.json`, the GitHub Actions OIDC issuer, and a certificate identity regex. Releases are produced only from the protected `main` or `release/...` branches.

Gotchas:

- Pinning a fixed `--certificate-identity` instead of a regex enforces one specific branch.
- A wrong branch or mismatched signature gives an error from cosign.
- Keyless verification is built into Cosign; the separate Rekor CLI is no longer needed.

## Checked

2026-11-04. Confirmed against the Checksum and Signature Verification sections of the Installing OpenBao page: the downloaded files, sha256sum command, gpg2 import and verify, cosign verify-blob with the bundle, issuer and identity regex, the main and release branches, the fixed certificate identity option and the Rekor note. Removed an unsupported verification-order sentence and an unsupported explanation of the gpg warning.

Method: documentation only; no commands were run.
