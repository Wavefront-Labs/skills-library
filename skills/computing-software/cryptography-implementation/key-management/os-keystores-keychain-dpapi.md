---
id: computing-software.cryptography-implementation.key-management.os-keystores-keychain-dpapi
name: os-keystores-keychain-dpapi
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-storage, secret-storage, os-keystore, keychain, dpapi, secret-service, android-keystore, secure-enclave, keyring]
level: practitioner
status: draft
description: "Store app secrets and keys in the OS keystore (macOS/iOS Keychain, Windows DPAPI/CNG, Linux Secret Service, Android Keystore) with the right access scope and its limits."
sources: ["https://developer.apple.com/documentation/security/keychain_services", "https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata", "https://specifications.freedesktop.org/secret-service-spec/latest/", "https://developer.android.com/privacy-and-security/keystore"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OS keystores

Desktop and mobile apps should not invent key storage. Each OS has a keystore
that ties secrets to the user login, device, or hardware.

| Platform | API | Protection |
|---|---|---|
| macOS / iOS | Keychain Services (`SecItemAdd`), CryptoKit `SecureEnclave.P256` | Login keychain / data protection classes; Secure Enclave keys never leave hardware |
| Windows | DPAPI `CryptProtectData` / .NET `ProtectedData.Protect`; CNG KSP (`NCryptCreatePersistedKey`) with TPM provider | User or machine master key derived from logon credentials; TPM-backed keys non-exportable |
| Linux desktop | Secret Service (libsecret, GNOME Keyring, KWallet); `secret-tool` CLI | Unlocked at login; any process of the same user can read |
| Linux kernel | `keyctl` keyrings | In-kernel, per session/user; not persistent across reboot |
| Android | Android Keystore (`KeyGenParameterSpec`, StrongBox) | TEE/StrongBox-backed, non-exportable, can require user auth |
| Cross-platform libs | Python `keyring`, Rust `keyring`, Electron `safeStorage` | Wrap the above |

## Patterns

- Store a random **wrapping key** in the keystore and use it to encrypt the
  app's data/database (e.g. SQLCipher key in Keychain). Do not put large data
  in the keystore.
- Prefer non-exportable hardware keys for signing/auth (Secure Enclave,
  Android Keystore with `setIsStrongBoxBacked(true)`, Windows TPM KSP); do the
  crypto in the keystore.
- Pick the access scope deliberately:
  - iOS: `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` - not included in
    backups, unavailable while locked. `AfterFirstUnlock` for background tasks.
  - DPAPI: `CurrentUser` scope by default; `LocalMachine` lets any process on
    the machine decrypt. Add `optionalEntropy` as an app-specific secondary
    secret (weak, but stops trivial cross-app reads).
  - Android: `setUserAuthenticationRequired(true)` for keys that should need
    biometrics/PIN.

## Limits

- Same-user malware can usually read Keychain/Secret Service/DPAPI-user
  secrets (with prompts on macOS for other apps' items). Keystores defend
  against offline disk theft and other users, not a compromised session.
- DPAPI blobs are decryptable by domain backup keys in AD environments.
- Headless Linux servers often lack an unlocked Secret Service; use a KMS,
  TPM or systemd credentials (`systemd-creds encrypt`) instead.

## Verify

- [ ] No secrets in plain config/prefs files (check app data dirs, plist, registry).
- [ ] Access scope matches background-access needs and backup policy.
- [ ] Hardware-backed keys show as non-exportable (e.g. `KeyInfo.isInsideSecureHardware`).
