---
id: computing-software.software-engineering.tauri.tauri-android-signing
name: tauri-android-signing
category: computing-software
field: software-engineering
product: tauri
tags: [android-signing, tauri, keystore]
level: practitioner
status: docs-checked
description: "Create a Java keystore, add keystore.properties and wire Gradle so Tauri Android release builds are signed for Google Play."
sources:
  - "https://v2.tauri.app/distribute/sign/android/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri Android code signing

Goal: sign Android App Bundles and APKs, which must be signed before upload for distribution.

## Create a keystore

```sh
keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```

On Windows PowerShell use `$env:USERPROFILE\upload-keystore.jks` and add `-storetype JKS`. If `keytool` is not on PATH, look in the JDK bundled with Android Studio. Keep the keystore private; do not commit it to public source control.

## keystore.properties

Create `[project]/src-tauri/gen/android/keystore.properties` (also keep private):

```
password=<password defined when keytool was executed>
keyAlias=upload
storeFile=<location of the key store file>
```

In CI, generate it per job, for example with a base64 secret:

```yml
- name: setup Android signing
  run: |
    cd src-tauri/gen/android
    echo "keyAlias=${{ secrets.ANDROID_KEY_ALIAS }}" > keystore.properties
    echo "password=${{ secrets.ANDROID_KEY_PASSWORD }}" >> keystore.properties
    base64 -d <<< "${{ secrets.ANDROID_KEY_BASE64 }}" > $RUNNER_TEMP/keystore.jks
    echo "storeFile=$RUNNER_TEMP/keystore.jks" >> keystore.properties
```

## Gradle

Edit `[project]/src-tauri/gen/android/app/build.gradle.kts` (the one with a `buildTypes` block, in `app/`).

1. Add `import java.io.FileInputStream` at the top.
2. Before `buildTypes`, add a `signingConfigs` block with `create("release")` that loads `keystore.properties` via `rootProject.file` and `Properties()`, then sets `keyAlias` and `keyPassword` (the `keyAlias` and `password` entries), `storeFile = file(keystoreProperties["storeFile"] as String)` and `storePassword`.
3. In `buildTypes`, `getByName("release")` set `signingConfig = signingConfigs.getByName("release")`.

Release builds are then signed automatically. Google also offers Play App Signing for bundles distributed in the Play Store.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/distribute/sign/android/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
