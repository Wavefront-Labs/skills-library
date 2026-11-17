---
id: computing-software.cryptography-implementation.applied-cryptography.mobile-local-storage-encryption
name: mobile-local-storage-encryption
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, ios-data-protection, android-keystore, keychain, mobile-storage, file-protection]
level: practitioner
status: draft
description: "Encrypt mobile local data: iOS Data Protection classes and Keychain accessibility, Android Keystore with Jetpack Security replacements, and backups."
sources: ["https://support.apple.com/guide/security/data-protection-overview-secf6276da8a/web", "https://developer.android.com/privacy-and-security/keystore", "https://mas.owasp.org/MASVS/controls/MASVS-STORAGE-1/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mobile local storage encryption

## iOS
- File protection classes: `.complete` (unavailable while locked), `.completeUnlessOpen`,
  `.completeUntilFirstUserAuthentication` (default), `.none`.
  ```swift
  try data.write(to: url, options: .completeFileProtection)
  ```
- Keychain accessibility: `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` for secrets that must not migrate to
  backups or new devices; `AfterFirstUnlock` for background tasks.
- Background tasks cannot read `.complete` files while locked; pick the class per use.

## Android
- File-based encryption protects data at rest by default (credential-encrypted storage after unlock).
- For app-level encryption, generate an AES-GCM key in Android Keystore (`KeyGenParameterSpec`,
  `setIsStrongBoxBacked(true)` when available) and encrypt files or SharedPreferences values with it.
- Jetpack Security `EncryptedSharedPreferences`/`EncryptedFile` are deprecated (2025); use Keystore directly or
  Tink with an Android Keystore KEK.

## Backups
- iOS: `ThisDeviceOnly` items are excluded from migration; exclude files with `isExcludedFromBackup`.
- Android: `android:allowBackup="false"` or `dataExtractionRules` to exclude secrets; Keystore keys never back up,
  so encrypted data restored elsewhere is unreadable (handle gracefully).

## Verify
- [ ] MASVS-STORAGE tests: no secrets in plain files, logs or backups on a jailbroken/rooted test device.
