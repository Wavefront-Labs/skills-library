---
id: computing-software.digital-privacy-hygiene.phishing-awareness.verifying-download-signatures-and-hashes
name: verifying-download-signatures-and-hashes
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, download-verification, malicious-downloads, malvertising]
level: practitioner
status: draft
description: "Verify downloaded software with SHA-256 checksums, GPG signatures, Windows Authenticode and macOS codesign, and know what each check proves."
sources:
  - "https://learn.microsoft.com/powershell/module/microsoft.powershell.utility/get-filehash"
  - "https://learn.microsoft.com/powershell/module/microsoft.powershell.security/get-authenticodesignature"
  - "https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Verifying download signatures and hashes

**Goal:** the installer you run is the one the developer published.

## What each check proves
| Check | Proves | Weakness |
|---|---|---|
| Checksum (SHA-256) from same site | File wasn't corrupted | If the site is compromised, both file and hash are swapped |
| Checksum from a separate channel | Integrity + some authenticity | Channel trust |
| GPG signature with a known key | Authentic from key holder | Need to get the right key once |
| Authenticode (Windows) / codesign + notarisation (macOS) | Signed by named developer, checked by OS | Stolen signing certs happen |

## Commands
```
# Windows
Get-FileHash .\setup.exe -Algorithm SHA256
certutil -hashfile setup.exe SHA256
Get-AuthenticodeSignature .\setup.exe | Format-List Status, SignerCertificate
# macOS
shasum -a 256 App.dmg
codesign -dv --verbose=4 /Applications/App.app
spctl -a -vv /Applications/App.app      # "accepted source=Notarized Developer ID"
# Linux
sha256sum -c SHA256SUMS
gpg --verify SHA256SUMS.sig SHA256SUMS
```
Compare the hash character by character (or with the `-c` mode); "close enough" is not a match.

## Workflow
Download from the official site (typed URL, not search ads), verify signature/hash, then install. Prefer package
managers (winget, Homebrew, apt) and app stores, which verify for you.

## Gotchas
- A valid signature from an unexpected publisher name is a red flag (malware signed by a random company).
- Windows SmartScreen "unrecognised app" doesn't mean malicious, but an unsigned installer for popular software is suspicious.
