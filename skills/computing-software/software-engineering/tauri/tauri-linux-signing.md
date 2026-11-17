---
id: computing-software.software-engineering.tauri.tauri-linux-signing
name: tauri-linux-signing
category: computing-software
field: software-engineering
product: tauri
tags: [linux-signing, tauri, appimage-signature]
level: practitioner
status: docs-checked
description: "Embed a GPG signature in a Tauri AppImage with environment variables, and validate it with the AppImage validate tool."
sources:
  - "https://v2.tauri.app/distribute/sign/linux/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri Linux code signing (AppImage)

Goal: let end users verify a Tauri Linux artifact is genuine. Signing is not required to deploy on Linux; it only adds trust.

## Create a key

Use gpg or gpg2 and back up the private and public keys securely:

```sh
gpg2 --full-gen-key
```

## Sign during the build

Set these environment variables:

- `SIGN`: `1` to sign the AppImage.
- `SIGN_KEY`: optional specific GPG Key ID.
- `APPIMAGETOOL_SIGN_PASSPHRASE`: the key password. If unset, gpg shows a dialog; you must set it in CI/CD.
- `APPIMAGETOOL_FORCE_SIGN`: by default the AppImage is generated even if signing fails; set `1` to exit on errors.

Show the embedded signature:

```sh
./src-tauri/target/release/bundle/appimage/$APPNAME_$VERSION_amd64.AppImage --appimage-signature
```

Replace `$APPNAME` and `$VERSION` with your values.

## The signature is not verified automatically

AppImage does not validate the signature itself, so it cannot be relied on to detect tampering. Users must verify manually with the AppImage validate tool, which requires you to publish your key ID on an authenticated channel (for example your website served via TLS).

## Validate

Download a `validate-$PLATFORM.AppImage` (the AppImage validate tool; the Tauri page links the download), then:

```sh
chmod +x validate-$PLATFORM.AppImage
./validate-$PLATFORM.AppImage $TAURI_OUTPUT.AppImage
```

A valid signature prints "Validation result: validation successful" with the signing key fingerprints.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/distribute/sign/linux/ (page text including code blocks and tabs read in full).
Corrected: the page links the AppImage validate tool download without naming the release; wording now says so.
Method: documentation only; no commands were run.
