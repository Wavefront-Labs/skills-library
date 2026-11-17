---
id: computing-software.cryptography-implementation.key-management.hardware-backed-mobile-keys
name: hardware-backed-mobile-keys
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, strongbox, secure-enclave, android-keystore, key-attestation, hardware-backed-keys, mobile]
level: advanced
status: draft
description: "Keep mobile keys in hardware: iOS Secure Enclave P-256 keys, Android Keystore StrongBox, attestation, user-authentication binding and what cannot be stored there."
sources: ["https://developer.apple.com/documentation/security/protecting-keys-with-the-secure-enclave", "https://developer.android.com/privacy-and-security/keystore", "https://source.android.com/docs/security/features/keystore/attestation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hardware-backed mobile keys

## iOS Secure Enclave
- Supports only NIST P-256 private keys (ECDSA signing and ECDH); keys never leave the enclave.
  ```swift
  let access = SecAccessControlCreateWithFlags(nil, kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
                                               [.privateKeyUsage, .biometryCurrentSet], nil)!
  let attrs: [String: Any] = [kSecAttrKeyType as String: kSecAttrKeyTypeECSECPrimeRandom,
    kSecAttrKeySizeInBits as String: 256, kSecAttrTokenID as String: kSecAttrTokenIDSecureEnclave,
    kSecPrivateKeyAttrs as String: [kSecAttrIsPermanent as String: true, kSecAttrAccessControl as String: access]]
  let key = SecKeyCreateRandomKey(attrs as CFDictionary, nil)
  ```
- CryptoKit: `SecureEnclave.P256.Signing.PrivateKey()`. For AES, wrap a symmetric key with ECIES using the
  enclave key.

## Android Keystore
- TEE-backed by default; `setIsStrongBoxBacked(true)` uses a separate secure element (Pixel Titan M, others).
  StrongBox supports fewer algorithms (RSA 2048, P-256, AES, HMAC-SHA256) and is slower; catch
  `StrongBoxUnavailableException` and fall back.
- `setUserAuthenticationRequired(true)` with `setUserAuthenticationParameters(timeout, AUTH_BIOMETRIC_STRONG)`.
- Key attestation: `setAttestationChallenge(nonce)` and verify the certificate chain server-side against Google's
  attestation roots, checking `securityLevel` and the revocation list.

## Pitfalls
- Biometric enrolment changes invalidate `.biometryCurrentSet` / `setInvalidatedByBiometricEnrollment` keys;
  handle re-enrolment.
- Keys do not survive device migration or factory reset; design recovery.

## Verify
- [ ] Attestation verified server-side; key generation path tested on devices without StrongBox.
