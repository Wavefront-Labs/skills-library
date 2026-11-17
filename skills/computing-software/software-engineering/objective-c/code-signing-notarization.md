---
id: computing-software.software-engineering.objective-c.code-signing-notarization
name: code-signing-notarization
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-security, code-signing-notarization]
level: advanced
status: draft
description: "Sign macOS apps with codesign and the hardened runtime, notarize with notarytool, staple the ticket and verify with spctl."
sources:
  - https://developer.apple.com/documentation/security
  - https://developer.apple.com/documentation/xcode
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Signing and notarization (macOS)
**Goal:** ship a Developer ID app that Gatekeeper accepts.

```bash
codesign --force --options runtime --timestamp --entitlements App.entitlements \
  --sign "Developer ID Application: Example Inc (TEAMID)" App.app
codesign --verify --deep --strict --verbose=2 App.app
ditto -c -k --keepParent App.app App.zip
xcrun notarytool submit App.zip --keychain-profile "notary-profile" --wait
xcrun stapler staple App.app
spctl --assess --type execute --verbose App.app
```
- Store credentials once with `xcrun notarytool store-credentials "notary-profile" ...`.
- Hardened runtime (`--options runtime`) is required for notarization; grant exceptions through entitlements only when needed (e.g. `com.apple.security.cs.allow-jit`).
- Sign nested code (frameworks, helpers) before the outer app; avoid `--deep` signing for production, sign each component.
- iOS apps use provisioning profiles and Xcode-managed signing; `xcodebuild -exportArchive` with an ExportOptions plist handles distribution signing.
- `security find-identity -v -p codesigning` lists usable identities.
- App Sandbox entitlement: `com.apple.security.app-sandbox`.

## Gotchas
- Missing timestamp or runtime flag causes notarization rejection; read the log with `notarytool log <id>`.
- Re-signing after modification invalidates the stapled ticket.

## Self-check
Run `spctl --assess` on the stapled app and confirm "accepted".
