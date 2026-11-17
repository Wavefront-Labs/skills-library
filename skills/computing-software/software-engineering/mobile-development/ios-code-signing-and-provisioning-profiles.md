---
id: computing-software.software-engineering.mobile-development.ios-code-signing-and-provisioning-profiles
name: ios-code-signing-and-provisioning-profiles
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-release, ios, ios-code-signing, provisioning-profiles, certificates, entitlements, xcodebuild]
level: practitioner
status: draft
description: "Untangle iOS code signing: certificates, App IDs, entitlements and provisioning profiles, automatic vs manual signing, CI keychains and fixing common signing errors."
sources:
  - https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases
  - https://developer.apple.com/help/account/manage-provisioning-profiles/create-an-app-store-provisioning-profile
  - https://developer.apple.com/documentation/technotes/tn3125-inside-code-signing-provisioning-profiles
  - https://docs.fastlane.tools/actions/match/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# iOS code signing and provisioning profiles

**Goal:** builds sign reliably on every developer machine and CI runner, for development, TestFlight/App Store and ad hoc distribution.

## 1. The pieces
| Piece | What it is |
|---|---|
| Certificate + private key | Identity: "Apple Development" or "Apple Distribution". The private key lives in the keychain of whoever created it. |
| App ID (bundle ID) | `com.acme.app`, with enabled capabilities (Push, App Groups, Sign in with Apple, iCloud). |
| Entitlements | `.entitlements` file declaring capabilities the binary claims; must be a subset of what the profile allows. |
| Provisioning profile | Signed by Apple: ties App ID + certificate(s) + (for dev/ad hoc) device UDIDs + entitlements. Types: Development, Ad Hoc, App Store, Enterprise. |
Every app extension (widgets, notification service, share) needs its **own** App ID and profile.

## 2. Automatic vs manual signing
- Automatic (Xcode manages certs/profiles with your team): best for development and small teams. In CI: `xcodebuild -allowProvisioningUpdates` with an App Store Connect API key (`-authenticationKeyPath ... -authenticationKeyID ... -authenticationKeyIssuerID ...`).
- Manual: explicit profile per target and configuration (`PROVISIONING_PROFILE_SPECIFIER`, `CODE_SIGN_IDENTITY`). Predictable for CI; pair with fastlane match.

## 3. fastlane match (shared signing for teams/CI)
```bash
fastlane match init              # git repo / S3 / GCS storage, encrypted with MATCH_PASSWORD
fastlane match development
fastlane match appstore --app_identifier com.acme.app,com.acme.app.widget
fastlane match appstore --readonly   # on CI: never create or revoke
```
One distribution certificate shared by the team instead of each developer creating their own (accounts are limited to a few distribution certs).

## 4. CI keychain (without match)
```bash
security create-keychain -p "$KC_PASS" build.keychain
security set-keychain-settings -lut 21600 build.keychain
security unlock-keychain -p "$KC_PASS" build.keychain
security import dist.p12 -k build.keychain -P "$P12_PASS" -T /usr/bin/codesign
security set-key-partition-list -S apple-tool:,apple: -s -k "$KC_PASS" build.keychain
security list-keychains -d user -s build.keychain login.keychain
cp AppStore.mobileprovision ~/Library/MobileDevice/Provisioning\ Profiles/
xcodebuild -scheme App -configuration Release -archivePath build/App.xcarchive archive
xcodebuild -exportArchive -archivePath build/App.xcarchive -exportOptionsPlist ExportOptions.plist -exportPath build/
```
`ExportOptions.plist`: `method` (`app-store-connect`, `release-testing`, `debugging`, `enterprise`), `teamID`, and per-bundle `provisioningProfiles` for manual signing.

## 5. Diagnose
```bash
security find-identity -v -p codesigning
security cms -D -i profile.mobileprovision | plutil -p -       # decode a profile: entitlements, devices, expiry, certs
codesign -dv --entitlements - --xml Payload/App.app              # what a built app actually claims
```
| Error | Usual cause |
|---|---|
| "No signing certificate found" | private key missing on this machine (cert created elsewhere) |
| "Provisioning profile doesn't include signing certificate" | profile generated before the cert; regenerate |
| "doesn't include the X entitlement" | capability enabled in Xcode but not on the App ID / profile outdated |
| "Errsec internal component" / codesign hangs on CI | keychain locked or partition list not set |
| Device can't install (dev/ad hoc) | UDID not in the profile |

## Gotchas
- Distribution certificates expire yearly, profiles too; expiry breaks CI on a random morning. Track dates (match handles renewal with `--force` when needed).
- Revoking a distribution cert does not remove apps from the App Store, but invalidates profiles using it; enterprise certs revocation kills installed apps.
- Keep `.p12` and match passphrases in the CI secret store, never in the repo unencrypted.

## Verify
- A clean CI runner archives and exports an IPA, `codesign -dv` shows the distribution identity and expected entitlements, and the build uploads to App Store Connect without signing warnings.
