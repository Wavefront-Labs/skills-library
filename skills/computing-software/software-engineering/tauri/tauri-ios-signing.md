---
id: computing-software.software-engineering.tauri.tauri-ios-signing
name: tauri-ios-signing
category: computing-software
field: software-engineering
product: tauri
tags: [ios-signing, tauri, provisioning-profile]
level: practitioner
status: docs-checked
description: "Sign a Tauri iOS app automatically through Xcode and an App Store Connect API key, or manually with a certificate and provisioning profile."
sources:
  - "https://v2.tauri.app/distribute/sign/ios/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri iOS code signing

Goal: sign an iOS app for the App Store or device install. Requires the Apple Developer program and an Apple device to sign on. You need a bundle identifier registered in App Store Connect, a signing certificate and a provisioning profile linking them; Xcode can manage these or you can provide them manually.

## Automatic signing (default)

Xcode registers the bundle identifier, manages capabilities and picks a certificate for the export method. Locally, add your account in Xcode: `Xcode > Settings`, Accounts tab, `+`.

In CI create an App Store Connect API key (Users and Access, Integrations tab, Add, Admin access) and set:

- `APPLE_API_ISSUER`: the Issuer ID above the keys table.
- `APPLE_API_KEY`: the Key ID column value.
- `APPLE_API_KEY_PATH`: path to the downloaded private key (downloadable once, visible after a page reload).

## Manual signing

Provide via environment variables:

- `IOS_CERTIFICATE`: base64 of the certificate exported from Keychain.
- `IOS_CERTIFICATE_PASSWORD`: its export password.
- `IOS_MOBILE_PROVISION`: base64 of the provisioning profile.

Create an Apple Distribution certificate on the Certificates page, install it, export the key as `.p12` from Keychain Access, then:

```
base64 -i <path-to-certificate.p12> | pbcopy
```

Certificate type per export method: debugging uses Apple Development or iOS App Development; app-store-connect and ad-hoc use Apple Distribution or iOS Distribution.

For the profile, create an App ID whose Bundle ID matches the `identifier` config, then create a provisioning profile (an "App Store Connect" profile for App Store distribution) linked to the App ID and certificate. Download it and run:

```
base64 -i <path-to-profile.mobileprovision> | pbcopy
```

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/distribute/sign/ios/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
