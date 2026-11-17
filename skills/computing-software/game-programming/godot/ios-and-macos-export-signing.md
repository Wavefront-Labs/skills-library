---
id: computing-software.game-programming.godot.ios-and-macos-export-signing
name: ios-and-macos-export-signing
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-ios-export, macos-export, code-signing, notarization, game-programming]
level: practitioner
status: docs-checked
description: "Export Godot games for iOS and macOS: Xcode project export, team ID and provisioning profiles, macOS codesign and notarization with notarytool, and entitlements."
sources: ["https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_ios.html", "https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_macos.html", "https://docs.godotengine.org/en/stable/tutorials/export/running_on_macos.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iOS and macOS export, signing and notarization

**Goal:** builds that install on devices and open on other Macs without Gatekeeper blocks.

## iOS
Requires a Mac with Xcode and an Apple Developer account.
1. Export preset iOS: **App Store Team ID** (a malformed ID is a known cause of signing errors), the (Bundle) Identifier, and provisioning profile UUIDs for debug and release.
2. Export produces an **Xcode project** in the folder you choose; open it in Xcode, choose the team and build.
4. C# projects can be exported to iOS as of Godot 4.2; check the docs for the current support status and test early.

## macOS
Export preset macOS produces a single "Universal 2" `.app` bundle (x86_64 and ARM64), which can be exported as is, as a ZIP or as a DMG (DMG only when exporting from macOS).
- **Code signing**: Xcode codesign, or `rcodesign` (install it separately and set its path in Editor Settings > Export > macOS > rcodesign, then select it in Code Signing > Codesign). Notarization requires a valid Apple Developer ID certificate. Entitlements: Disable Library Validation is for GDExtension add-ons, ad-hoc signing or user-provided extensions; Allow JIT Code Execution is for add-ons with dynamic native code, per their documentation.
- **Notarization**: select `Xcode notarytool` in Notarization > Notarization, using an Apple ID app-specific password or an App Store Connect API key. Godot submits; the docs then staple the ticket (`xcrun stapler staple`, or `rcodesign staple` when using rcodesign):
```bash
xcrun notarytool submit MyGame.zip --apple-id dev@example.com --team-id ABCDE12345 --password <app-specific-pw> --wait
xcrun stapler staple MyGame.app
```
- Unsigned builds are blocked by Gatekeeper on other Macs; sign and notarize for public release.
- `.app` bundles exported from Windows lack the executable flag unless handled as the macOS export docs describe.

## Gotchas
- Sign GDExtension libraries with the same identity as the app.

## Verify
- [ ] `spctl -a -vv MyGame.app` reports "accepted, source=Notarized Developer ID".
- [ ] The iOS build installs and runs on a device.

## Checked

2026-10-28. Confirmed against: Exporting for iOS and macOS pages (App Store Team ID, Identifier, provisioning profile UUID options, Xcode project output, C# on iOS from 4.2, Universal 2 .app with ZIP/DMG, rcodesign installed separately and configured in Editor Settings, Xcode notarytool option, app-specific password or API key, stapling with xcrun stapler or rcodesign staple, Developer ID certificate required, Disable Library Validation and Allow JIT entitlements).

Removed or rewritten: claims that rcodesign is built in (it is installed separately), the NativeAOT/experimental wording, privacy usage strings, TestFlight and one-click deploy steps, the xattr workaround, Windows/Linux signing statement, bundle-ID and Mac App Store gotchas, and the allow_jit-for-C# advice.

Method: documentation only; no commands were run.
