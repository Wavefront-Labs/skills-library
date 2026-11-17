---
id: computing-software.systems-network-administration.patch-management.verifying-patch-signatures-and-hashes
name: verifying-patch-signatures-and-hashes
category: computing-software
field: systems-network-administration
product: patch-management
tags: [patch-integrity, signature-verification, authenticode, gpgcheck, sha256, supply-chain, patch-acquisition]
level: practitioner
status: docs-checked
description: "Verify patch integrity before deployment: Authenticode on Windows packages, RPM/APT GPG checks, vendor hashes for network and firmware images, and on-device image verification."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/get-authenticodesignature
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash
  - https://manpages.debian.org/stable/apt/apt-secure.8.en.html
  - https://rpm-software-management.github.io/rpm/man/rpmkeys.8
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Verifying patch signatures and hashes

**Goal:** never deploy a tampered or corrupted update.

## Windows
```powershell
Get-AuthenticodeSignature <path-to-package.msu> | Format-List Status, SignerCertificate
# Status must be Valid and the signer Microsoft Corporation (or the expected vendor)
Get-FileHash .\vendor-fix.msi -Algorithm SHA256
```

## RPM-based Linux
```bash
grep -E 'gpgcheck|repo_gpgcheck' /etc/yum.repos.d/*.repo     # gpgcheck=1 everywhere
rpm -K package.rpm                                            # digests and signatures OK
rpmkeys --list
```
Never set `gpgcheck=0` to "fix" an install; import the vendor key from a trusted source instead.

## Debian/Ubuntu
APT verifies signed `Release`/`InRelease` files; per-repo keys are set with `Signed-By` (a keyring path or key fingerprints) in the sources entry. A missing-key error means the key must be imported, not that verification should be disabled.

## Network and firmware images
Compare the hash of the downloaded image with the value on the vendor portal (`sha512sum <image-file>` on Linux), then use the vendor's documented on-device verification command and image-signature checks before activating the image.

## Process
- Download only from vendor portals or your mirrored repositories; record source URL and hash in the change.
- Store vendor public keys in configuration management, not ad hoc.
- Re-verify after copying across air gaps or removable media.

## Verify
A deliberately modified test package is rejected by every deployment path.

## Checked
Date: 2026-10-27. Documentation checked: Microsoft Learn `Get-AuthenticodeSignature` (Status Valid, signer certificate) and `Get-FileHash` (SHA256 default), apt-secure(8) (signed `Release`/`InRelease`), sources.list(5) (`Signed-By`), rpm(8) and rpmkeys(8) (`-K`/`--checksig`, `--list`). Removed the Cisco-specific commands and example image name because Cisco's image-integrity page blocks automated access, plus the unconfirmed WSUS/ConfigMgr signature statement and the example KB file name.

Run 2026-11-01 (Windows PowerShell 5.1): `Get-FileHash <file> -Algorithm SHA256` matched certutil's digest, and `Get-AuthenticodeSignature` on a Microsoft-signed file gave Status Valid with the signer certificate; on a non-PE file it gave Status UnknownError. The rpm, apt and vendor-image commands were not run (not installed here), so the skill stays docs-checked.
Method: documentation plus the Windows commands run.
