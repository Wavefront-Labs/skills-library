---
id: computing-software.software-engineering.wails.macos-code-signing-ci
name: macos-code-signing-ci
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, code-signing, macos, notarization, gon, github-actions, ci]
level: practitioner
status: docs-checked
description: "Sign and notarize a Wails macOS app in GitHub Actions using a base64 p12 certificate, gon config, entitlements and a matching bundle ID in Info.plist."
sources: [https://wails.io/docs/guides/signing]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# macOS code signing and notarization in GitHub Actions

Goal: a signed, notarized `build/bin/app.app` from CI, using the `gon` tool.

## Secrets

Export the Apple certificate as .p12 and encode it: `base64 Certificates.p12 | pbcopy`. Create repo secrets: `APPLE_DEVELOPER_CERTIFICATE_P12_BASE64`, `APPLE_DEVELOPER_CERTIFICATE_PASSWORD`, and `APPLE_PASSWORD` (an app-specific password from your Apple ID account page).

## Workflow steps (after `wails build`)

```yaml
- name: MacOS download gon for code signing and app notarization
  if: matrix.platform == 'macos-latest'
  run: brew install Bearer/tap/gon
- name: Import Code-Signing Certificates for macOS
  if: matrix.platform == 'macos-latest'
  uses: Apple-Actions/import-codesign-certs@v1
  with:
    p12-file-base64: ${{ secrets.APPLE_DEVELOPER_CERTIFICATE_P12_BASE64 }}
    p12-password: ${{ secrets.APPLE_DEVELOPER_CERTIFICATE_PASSWORD }}
- name: Sign our macOS binary
  if: matrix.platform == 'macos-latest'
  run: gon -log-level=info ./build/darwin/gon-sign.json
```

## build/darwin/gon-sign.json

```json
{
  "source": ["./build/bin/app.app"],
  "bundle_id": "app.myapp",
  "apple_id": { "username": "my-appleid@email.com", "password": "your-app-specific-password", "provider": "ABCDE12345" },
  "sign": { "application_identity": "Developer ID Application: Human User" }
}
```
`source` is the app to sign, `provider` is your team ID, `application_identity` is your developer identity. Find both with `security find-identity -v -p codesigning`. The `@env:` syntax of Apple's deprecated altool is no longer available since Apple moved to notarytool.

## Entitlements and Info.plist

Add an `entitlements.plist` listing what your app needs (the example enables app-sandbox, network client/server, user-selected and downloads read-write file access). `Info.plist` `CFBundleIdentifier` must equal the `bundle_id` in `gon-sign.json`.

## Gotcha

Apple processing can take minutes to hours. A combined Windows + macOS workflow is in the source page; for Windows see `computing-software.software-engineering.wails.windows-code-signing-ci`.

Do not commit real passwords in the gon file; the page's file shows placeholders.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Code Signing" guide (macOS section; Windows section also read).

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
