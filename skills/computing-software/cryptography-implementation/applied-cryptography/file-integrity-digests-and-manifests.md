---
id: computing-software.cryptography-implementation.applied-cryptography.file-integrity-digests-and-manifests
name: file-integrity-digests-and-manifests
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, file-integrity-digest, sha256sum, checksum-manifest, sha256, release-verification]
level: practitioner
status: draft
description: "Produce and verify file integrity digests: SHA-256 checksum manifests, sha256sum -c, signing the manifest, and why bare checksums beside downloads prove little."
sources: ["https://www.gnu.org/software/coreutils/manual/html_node/sha2-utilities.html", "https://www.gnu.org/software/coreutils/manual/html_node/md5sum-invocation.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# File integrity digests and manifests

## Create and check
```sh
sha256sum dist/* > SHA256SUMS
sha256sum -c SHA256SUMS            # OK / FAILED per file, exit 1 on any failure
sha256sum -c --ignore-missing SHA256SUMS
shasum -a 256 -c SHA256SUMS        # macOS
Get-FileHash file.zip -Algorithm SHA256   # PowerShell
```
Format is `<hex>  <name>` (two spaces; `*` instead of the second space marks binary mode).

## Make it mean something
- A checksum on the same server as the file only detects corruption, not tampering. Sign the manifest:
  `gpg --detach-sign --armor SHA256SUMS`, `minisign -Sm SHA256SUMS`, or `cosign sign-blob`.
- Publish the signing public key out of band; verify signature first, then the hashes.
- Use SHA-256 or SHA-512. MD5 and SHA-1 manifests are collision-prone and should be regenerated.

## Integrity monitoring
- For directories at rest, AIDE/Tripwire style databases store per-file digests; protect the database and
  rerun from read-only media.
- For deduplicated or large data, keep per-chunk digests or a Merkle tree so partial verification works.

## Pitfalls
- Comparing hex case-sensitively or with trailing whitespace; normalise or use `-c`.
- Line endings converted by git or FTP change the digest; transfer in binary.
- Hashing a symlink target vs the link.

## Verify
- [ ] Manifest signature verifies with the published key.
- [ ] `sha256sum -c` exits 0 in CI after download.
