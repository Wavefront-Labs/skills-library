---
id: computing-software.software-engineering.mobile-development.secure-storage-and-permissions
name: secure-storage-and-permissions
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, keychain, keystore, encryptedsharedpreferences, biometric-auth, runtime-permissions, android, ios, secure-storage, token-storage, app-transport-security]
level: advanced
status: draft
description: "Store tokens/secrets on-device with Keychain (iOS) and Keystore-backed EncryptedSharedPreferences (Android), and request runtime permissions without over-asking."
sources: ["Apple docs - Keychain Services", "Android developer docs - Security best practices, EncryptedSharedPreferences, Runtime Permissions", "OWASP Mobile Application Security Testing Guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure storage and permissions — where tokens live, and when to ask for access

**Goal:** persist auth tokens and secrets so they survive app restarts without being
readable by another app or a rooted/jailbroken device's filesystem browse, and
request permissions in a way that doesn't tank opt-in rates or get the app rejected.

## 1. Never put secrets in plain SharedPreferences/UserDefaults or app-bundled files
`SharedPreferences` (Android) and `UserDefaults` (iOS) are plaintext on-disk (XML/
plist) — readable by anyone with filesystem access (a rooted device, a backup
extraction tool, or another process in some misconfigurations). The same applies to
hardcoding an API key in app resources/source: it's trivially extractable by
decompiling the APK/IPA, so it should never be treated as a real secret in the first
place — client-side "secrets" are really just obfuscation, not security; the actual
secret (a server-side API key with real privileges) belongs on your backend, not the
client.

## 2. iOS: Keychain, with the right accessibility level
```swift
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "authToken",
    kSecValueData as String: tokenData,
    kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
]
SecItemAdd(query as CFDictionary, nil)
```
Keychain items are encrypted at rest and tied to the device's Secure Enclave-backed
keys. The accessibility attribute matters: `...ThisDeviceOnly` variants prevent the
item from being included in iCloud Keychain sync/device-to-device restore, which is
usually correct for a session token that shouldn't silently reappear on a different
device. `WhenUnlocked` vs `AfterFirstUnlock` trades off: the former is more secure
(inaccessible while locked, including to background processes) but means a
background-refresh task running while the device is locked can't read it — pick
based on whether the token must be usable from background work.

## 3. Android: Keystore-backed EncryptedSharedPreferences (or DataStore + Tink)
```kotlin
val masterKey = MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build()
val prefs = EncryptedSharedPreferences.create(
    context, "secure_prefs", masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)
```
The encryption key itself is generated and held in the hardware-backed Android
Keystore (never extractable, even with root, on devices with proper hardware
support) — the app only ever gets ciphertext/plaintext through the API, never the
raw key. Note: `EncryptedSharedPreferences` is deprecated in favor of Jetpack
`DataStore` combined with manual Tink-based encryption as of recent AndroidX
guidance — check current docs before starting a new project, as this area has moved;
either way, the principle (hardware-backed key, app never touches raw key material)
is what matters.

## 4. Biometric-gated access for sensitive actions
Both platforms support requiring Face ID/Touch ID or Android biometric prompt before
releasing a Keychain/Keystore item (`kSecAttrAccessControl` with biometry on iOS;
`setUserAuthenticationRequired` on the Android key) — this adds a hardware-enforced
gate beyond app-level logic (a jailbreak bypassing your app's own "check PIN" logic
in code doesn't bypass the Secure Enclave/TEE's biometric gate on the key itself).

## 5. Runtime permissions: ask in context, not at launch
Requesting every permission (camera, location, notifications) immediately on first
launch, before the user has any reason to want them, produces the lowest opt-in rate
and the most app-store/privacy-review scrutiny. Best practice on both platforms: ask
at the moment the feature needing it is invoked ("tap to add a photo" → then request
camera), with a short in-app explanation of why, before the OS permission dialog
appears (so a denial can be followed by a clear in-app message rather than a silent
broken feature). Check the current permission state before requesting — re-prompting
a user who already denied (especially "don't ask again" on Android) without sending
them to Settings is a dead end that should be handled distinctly in the UI.

## Gotchas
- iOS Keychain items can persist across app deletion/reinstall unless explicitly
  cleared — a "logged out" state after reinstall that unexpectedly still has a token
  is a common bug; clear relevant Keychain items on logout, and consider whether
  first-launch-after-install should proactively clear stale items.
- Android backup (`android:allowBackup="true"`, the default) can include
  SharedPreferences in auto-backup unless explicitly excluded — exclude sensitive
  files via backup rules even when using EncryptedSharedPreferences, since backup
  extraction tools target the backup, not necessarily the live encrypted store.
- Requesting a permission the app doesn't actually need (broad location when
  approximate suffices, full photo library access when just picking one image via
  the system picker would need no permission at all) is both a privacy problem and an
  app-review rejection risk on both stores.

## Verify
- [ ] No auth token, API secret, or PII is stored in plaintext SharedPreferences,
      UserDefaults, or bundled app resources — confirmed by inspecting the actual
      storage file/plist on a test device.
- [ ] Keychain/Keystore accessibility level matches the actual need (background
      access vs locked-only), not left at a default without consideration.
- [ ] Every permission request happens in context with a clear reason, confirmed by
      checking the request is not fired on app launch for a feature the user hasn't
      touched yet.
- [ ] Logout clears any persisted Keychain/Keystore token, verified by checking
      storage after logging out on a test device.

Related: computing-software.software-engineering.mobile-development.app-lifecycle-and-offline-sync,
computing-software.software-engineering.api-design.idempotency-and-pagination
