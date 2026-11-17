---
id: computing-software.software-engineering.mobile-development.android-app-signing-and-app-bundles
name: android-app-signing-and-app-bundles
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-release, android, android-app-signing, android-app-bundle, play-app-signing, keystore, bundletool]
level: practitioner
status: docs-checked
description: "Sign Android releases correctly: upload key vs Play App Signing key, keystores and CI secrets, building and testing App Bundles with bundletool, and key rotation or loss."
sources:
  - https://developer.android.com/studio/publish/app-signing
  - https://support.google.com/googleplay/android-developer/answer/9842756
  - https://developer.android.com/tools/bundletool
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Android app signing and App Bundles

**Goal:** releases signed with keys you cannot lose, uploaded as AABs, and tested exactly as Play will deliver them.

## 1. Two keys with Play App Signing
- **App signing key**: signs what users install. Held by Google.
- **Upload key**: you sign the AAB with it before upload; Google uses the upload certificate to verify your identity and signs the APKs it distributes with the app signing key.
If the upload key leaks or is lost, Google can reset the upload key; the app signing key (and users' updates) are unaffected. That is the main safety benefit.

## 2. Create and store the upload key
```bash
keytool -genkeypair -v -keystore upload.jks -alias upload -keyalg RSA -keysize 4096 -validity 10000
```
Never commit the keystore or passwords. In CI keep the keystore and passwords in the CI secret store.
```kotlin
android {
    signingConfigs {
        create("release") {
            storeFile = file(System.getenv("UPLOAD_KEYSTORE") ?: "upload.jks")
            storePassword = System.getenv("UPLOAD_STORE_PASSWORD")
            keyAlias = "upload"
            keyPassword = System.getenv("UPLOAD_KEY_PASSWORD")
        }
    }
    buildTypes { release { signingConfig = signingConfigs.getByName("release") } }
}
```

## 3. Build and inspect the bundle
```bash
./gradlew bundleRelease                          # app/build/outputs/bundle/release/app-release.aab
jarsigner -verify -verbose app-release.aab | tail -3
bundletool build-apks --bundle=app-release.aab --output=app.apks \
  --ks=upload.jks --ks-key-alias=upload --ks-pass=file:store.pwd --connected-device
bundletool install-apks --apks=app.apks          # install the split APKs Play would serve to this device
```
Testing the AAB this way catches missing resources in splits (language/density) that a universal debug APK hides.

## 4. Things that depend on the signing certificate
- API providers (Google Sign-In, Firebase, Maps) that ask for a certificate fingerprint: the Play Console app signing page (Release > Setup > App signing) shows the MD5, SHA-1 and SHA-256 fingerprints of both the upload and app signing certificates. Register the app signing key's, plus the debug/upload ones for testing.

## 5. Key reset
If the upload key is lost or compromised, request an upload key reset in Play Console; the app signing key is secured by Google, so you can keep shipping updates to the same app. For app signing key changes, follow the Play Console help page and re-register any new fingerprints with API providers.

## Gotchas
- Losing a self-managed app signing key (legacy apps not enrolled) means you can never update the app; enrol in Play App Signing.
- Android Studio creates a debug keystore at `$HOME/.android/debug.keystore` on first run, so its certificate differs per machine; fingerprints registered for it will not match teammates' builds.

## Verify
- `bundletool build-apks` + `install-apks` installs and runs the release build on a device, Play Console's Play app signing page shows the upload key fingerprint matching your keystore, and API-restricted services work on the Play-installed build.

## Checked
2026-11-01. Confirmed against the Android app-signing page and the bundletool page: upload key vs app signing key roles, upload key reset, MD5/SHA-1/SHA-256 fingerprints on the Play Console app signing page, debug keystore location, bundletool build-apks flags (--ks, --ks-pass pass:/file:, --ks-key-alias, --connected-device) and install-apks. Removed (not confirmed on those pages): key sizes, hybrid/v3.x rotation enforcement by Android version, App Links statement, versionCode rules, get-size.
Method: documentation only; no commands were run.
