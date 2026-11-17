---
id: computing-software.cryptography-implementation.key-management.pkcs11-mechanism-selection
name: pkcs11-mechanism-selection
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, pkcs11-mechanisms, pkcs11, hsm, pkcs11-tool, ckm-aes-gcm, rsa-oaep, rsa-pss, ecdsa, mechanism-info]
level: advanced
status: docs-checked
description: "List and choose PKCS#11 mechanisms on an HSM or token: pkcs11-tool -M, mechanism flags and key sizes, GCM/OAEP/PSS parameter structs and vendor quirks."
sources: ["https://docs.oasis-open.org/pkcs11/pkcs11-spec/v3.1/pkcs11-spec-v3.1.html", "https://docs.oasis-open.org/pkcs11/pkcs11-curr/v3.0/pkcs11-curr-v3.0.html", "https://github.com/OpenSC/OpenSC/wiki/Using-pkcs11-tool-and-OpenSSL"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PKCS#11 mechanism selection

## List what the token supports
```
pkcs11-tool --module <path-to-pkcs11-module> -M
```
The output lists each mechanism with its key-size range and capability flags.
In code: `C_GetMechanismList` then `C_GetMechanismInfo` for `ulMinKeySize`, `ulMaxKeySize` and flags
(`CKF_ENCRYPT`, `CKF_SIGN`, `CKF_WRAP`, `CKF_DERIVE`, `CKF_HW`). The spec says key size units are
mechanism-dependent (bits or bytes); for RSA mechanisms they are modulus bits.

## Common choices
| Need | Mechanism | Parameters |
|---|---|---|
| Symmetric AEAD | `CKM_AES_GCM` | `CK_GCM_PARAMS` (pIv, ulIvLen, pAAD, ulAADLen, ulTagBits) |
| RSA encryption/wrap | `CKM_RSA_PKCS_OAEP` | `CK_RSA_PKCS_OAEP_PARAMS` (hashAlg, mgf, source) |
| RSA signature | `CKM_SHA256_RSA_PKCS_PSS` or `CKM_RSA_PKCS_PSS` (hash outside) | `CK_RSA_PKCS_PSS_PARAMS` (hashAlg, mgf, sLen) |
| ECDSA | `CKM_ECDSA_SHA256` or `CKM_ECDSA` (you hash) | Output is r and s concatenated, not DER |
| EdDSA | `CKM_EDDSA` | optional `CK_EDDSA_PARAMS` for ph/ctx |
| HMAC | `CKM_SHA256_HMAC` | none |
| ECDH | `CKM_ECDH1_DERIVE` | `CK_ECDH1_DERIVE_PARAMS` (kdf, public data) |

## Vendor quirks
- For message-based AES-GCM the spec lets the module generate the IV (`ivGenerator`) and return the whole IV in
  `pIv`; check which generator modes your token accepts.
- ECDSA signatures are the concatenation of r and s, each padded to the same length, not DER; X.509 and OpenSSL
  expect DER (convert, or let the pkcs11 provider do it).
- Mechanism types at `CKM_VENDOR_DEFINED` and above are reserved for token vendors and are not portable.

## Verify
- [ ] Mechanism list captured per HSM firmware version in the design doc.
- [ ] Integration tests exercise each mechanism with the exact parameter structs used in production.

## Checked

2026-11-01. Confirmed in the PKCS #11 v3.1 and v3.0 specs: mechanism names, `CK_RSA_PKCS_OAEP_PARAMS`, PSS and
EdDSA parameter structs, GCM `ulIvLen`/`ulTagBits`, mechanism-dependent `ulMinKeySize` units, ECDSA r and s
concatenation, vendor-defined mechanism range. Removed: softhsm path and sample output, `ulIvBits` header
claim, FIPS-mode disabled-mechanism list, `pkcs11-tool -M` output details beyond the flag itself.
Method: documentation only; no commands were run.
