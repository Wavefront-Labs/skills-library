---
id: computing-software.software-engineering.wails.mac-app-store-submission
name: mac-app-store-submission
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, macos, app-store, codesign, entitlements, sandbox, productbuild]
level: practitioner
status: docs-checked
description: "Submit a Wails app to the Mac App Store: certificates, provisioning profile, sandbox entitlements, codesign and productbuild, and Transporter upload."
sources: [https://wails.io/docs/guides/mac-appstore]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: produce a signed `.pkg` and get it to App Store Connect.

## Prerequisites
Apple Developer account, Xcode command line tools, and certificates, identifiers and app record created in the portal.

## Portal setup
1. Developer account, Certificates, Identifiers & Profiles: register an App ID in the form `com.example.app`.
2. Generate Mac App Store Distribution certificates (the application cert and a separate installer cert); import both into Keychain.
3. App Store Connect: register the app with that bundle ID, fill in screenshots/descriptions, create a version.
4. Profiles: add a Mac App Store Distribution provisioning profile, profile type Mac, choose the App ID and the Mac App Distribution certificate, name it `embedded`, download.

## Sandbox entitlements
Apps must run in Apple's App Sandbox. Create `build/darwin/entitlements.plist` (recommended path). Page example (from RiftShare) enables `com.apple.security.app-sandbox`, `network.client`, `network.server`, `files.user-selected.read-write`, `files.downloads.read-write`, plus `com.apple.application-identifier` = `TEAM_ID.APP_NAME` and `com.apple.developer.team-identifier` = `TEAM_ID`. Replace the Team ID and app name; include only the entitlements your app needs.

Put the provisioning profile at the project root as `embedded.provisionprofile`.

## Build and sign (run from project root)
```bash
APP_CERTIFICATE="3rd Party Mac Developer Application: YOUR NAME (CODE)"
PKG_CERTIFICATE="3rd Party Mac Developer Installer: YOUR NAME (CODE)"
APP_NAME="YourApp"

wails build -platform darwin/universal -clean
cp ./embedded.provisionprofile "./build/bin/$APP_NAME.app/Contents"
codesign --timestamp --options=runtime -s "$APP_CERTIFICATE" -v --entitlements ./build/darwin/entitlements.plist "./build/bin/$APP_NAME.app"
productbuild --sign "$PKG_CERTIFICATE" --component "./build/bin/$APP_NAME.app" /Applications "./$APP_NAME.pkg"
```
Certificate names must match the strings shown in Keychain. Result: a signed pkg in the project root.

## Upload
Install Transporter from the Mac App Store, sign in, click + and add the `.pkg`. In App Store Connect select the version, and under Build pick the uploaded package, then submit for review (page expects a few business days).

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Mac App Store Guide".

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
