---
id: computing-software.software-engineering.tauri.tauri-app-store
name: tauri-app-store
category: computing-software
field: software-engineering
product: tauri
tags: [app-store, tauri, altool]
level: advanced
status: docs-checked
description: "Build, sign and upload a Tauri macOS or iOS app to the Apple App Store with provisioning profile, entitlements, productbuild and altool."
sources:
  - "https://v2.tauri.app/distribute/app-store/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri App Store distribution

Requires the Apple Developer program, macOS and iOS code signing, and a Mac build machine. Register the app in App Store Connect; its Bundle ID must match `tauri.conf.json > identifier`.

## Icons and version

After `tauri ios init`, update icons with `tauri icon /path/to/app-icon.png --ios-color '#fff'`. `CFBundleVersion` derives from `version`; override with `bundle > iOS > bundleVersion` or `bundle > macOS > bundleVersion` (for example `"100"`). `tauri ios build --open` opens Xcode.

## macOS setup

- Set `bundle > category` (for example `"Utility"`).
- Create an App ID and a "Mac App Store Connect" provisioning profile; include it with `bundle > macOS > files`: `"embedded.provisionprofile": "path/to/profile-name.provisionprofile"`.
- `src-tauri/Info.plist` with `ITSAppUsesNonExemptEncryption` set to false (or true if the app uses encryption).
- `Entitlements.plist` with `com.apple.security.app-sandbox` true, `com.apple.application-identifier` `$TEAM_ID.$IDENTIFIER` and `com.apple.developer.team-identifier` `$TEAM_ID`; reference via `bundle > macOS > entitlements`. The app must work in an App Sandbox.
- Optionally keep these in `src-tauri/tauri.appstore.conf.json` and pass `--config`.

## macOS build and upload

```sh
tauri build --bundles app --target universal-apple-darwin
xcrun productbuild --sign "<certificate signing identity>" --component "target/universal-apple-darwin/release/bundle/macos/$APPNAME.app" /Applications "$APPNAME.pkg"
xcrun altool --upload-app --type macos --file "$APPNAME.pkg" --apiKey $APPLE_API_KEY_ID --apiIssuer $APPLE_API_ISSUER
```

The PKG must be signed with a Mac Installer Distribution certificate. For Apple Silicon only, set `minimumSystemVersion` to `12.0` and adjust the target.

## iOS build and upload

```sh
tauri ios build --export-method app-store-connect
xcrun altool --upload-app --type ios --file "src-tauri/gen/apple/build/arm64/$APPNAME.ipa" --apiKey $APPLE_API_KEY_ID --apiIssuer $APPLE_API_ISSUER
```

## Authentication

Create an App Store Connect key (Integrations, Individual Keys, Developer access). `APPLE_API_ISSUER` is the Issuer ID; `APPLE_API_KEY_ID` is the Key ID. Save the key as `AuthKey_<APPLE_API_KEY_ID>.p8` in `./private_keys`, `~/private_keys`, `~/.private_keys` or `~/.appstoreconnect/private_keys`. Approved uploads appear in TestFlight.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/distribute/app-store/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
