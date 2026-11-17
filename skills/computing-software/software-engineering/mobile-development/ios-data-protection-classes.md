---
id: computing-software.software-engineering.mobile-development.ios-data-protection-classes
name: ios-data-protection-classes
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, ios, data-protection, file-protection, keychain-accessibility, masvs-storage, encryption-at-rest]
level: practitioner
status: draft
description: "Choose iOS Data Protection classes for files and Keychain items: when data is readable, background-access trade-offs, and how to set and verify them."
sources: ["https://developer.apple.com/documentation/uikit/protecting-the-user-s-privacy/encrypting-your-app-s-files", "https://support.apple.com/guide/security/data-protection-overview-secf6276da8a/web", "https://mas.owasp.org/MASVS/05-MASVS-STORAGE/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# iOS Data Protection classes

Files and Keychain items are encrypted with keys tied to the passcode and the device; the class decides when the key is available.

| File protection | Readable | Keychain equivalent |
|---|---|---|
| `.completeFileProtection` | only while unlocked | `kSecAttrAccessibleWhenUnlocked` |
| `.completeFileProtectionUnlessOpen` | files opened while unlocked stay accessible; new files can be created while locked | no direct match |
| `.completeFileProtectionUntilFirstUserAuthentication` | after first unlock since boot (system default for app files) | `...AfterFirstUnlock` |
| `.none` | always | n/a |

Add `...ThisDeviceOnly` Keychain variants to keep items out of backups and device migration.

## Set it
```swift
try data.write(to: url, options: .completeFileProtection)
try FileManager.default.setAttributes(
    [.protectionKey: FileProtectionType.complete], ofItemAtPath: url.path)

let query: [String: Any] = [
  kSecClass as String: kSecClassGenericPassword,
  kSecAttrAccount as String: "refresh-token",
  kSecValueData as String: tokenData,
  kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
]
SecItemAdd(query as CFDictionary, nil)
```
Project-wide default: enable the Data Protection capability (entitlement `com.apple.developer.default-data-protection`).

## Gotchas
- Background tasks (silent push, background fetch, location) run while locked; `complete` protection makes those reads fail. Use `AfterFirstUnlock` for data needed in background.
- Check `UIApplication.shared.isProtectedDataAvailable` or observe `protectedDataDidBecomeAvailableNotification` before reading protected files.
- Data Protection does not stop a jailbroken, unlocked device or user-space attackers; it is one layer (MASVS-STORAGE).

Verify: write a file with `.complete`, lock the device and trigger a background read; expect a read error. Print `attributesOfItem(atPath:)[.protectionKey]` to confirm the class.
