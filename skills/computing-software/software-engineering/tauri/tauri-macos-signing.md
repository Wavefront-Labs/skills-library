---
id: computing-software.software-engineering.tauri.tauri-macos-signing
name: tauri-macos-signing
category: computing-software
field: software-engineering
product: tauri
tags: [macos-signing, tauri, notarization]
level: practitioner
status: docs-checked
description: "Code sign and notarize a Tauri macOS app locally or in CI, including certificate export, notarization credentials and ad-hoc signing."
sources:
  - "https://v2.tauri.app/distribute/sign/macos/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri macOS code signing

Goal: sign (and notarize) a macOS build so it is not flagged as broken when downloaded.

## Prerequisites

An Apple Developer account (paid, or free for testing only) and an Apple device to sign on. A free account cannot notarize.

## Certificate

Generate a Certificate Signing Request on your Mac, then on the Certificates, IDs & Profiles page create a certificate: `Apple Distribution` for the App Store, `Developer ID Application` for outside it (only the `Account Holder` can create Developer ID certificates). Download the `.cer` and open it to install into the keychain.

## Configure Tauri

Locally, find the signing identity with `security find-identity -v -p codesigning` and set `tauri.conf.json > bundle > macOS > signingIdentity` or the `APPLE_SIGNING_IDENTITY` env var.

For CI, export the certificate from Keychain Access as `.p12`, then:

```sh
openssl base64 -A -in /path/to/certificate.p12 -out certificate-base64.txt
```

Put that text in `APPLE_CERTIFICATE` and the export password in `APPLE_CERTIFICATE_PASSWORD`.

## Notarization

Required with a Developer ID Application certificate. Provide credentials either way:

- App Store Connect API: `APPLE_API_ISSUER` (Issuer ID above the keys table), `APPLE_API_KEY` (Key ID), `APPLE_API_KEY_PATH` (downloaded private key file; downloadable once).
- Apple ID: `APPLE_ID`, `APPLE_PASSWORD` (an app-specific password), `APPLE_TEAM_ID`.

Then rerun the build, e.g. `pnpm tauri build --bundles dmg`. Append `--skip-stapling` to skip stapling on an initial pass.

## Ad-hoc signing

Without an Apple identity, set `"signingIdentity": "-"`. Useful on Apple Silicon where all internet apps must be signed, but users must still allow the app in Privacy & Security settings.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/distribute/sign/macos/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
