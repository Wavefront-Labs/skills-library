---
id: computing-software.systems-network-administration.pki-tls-administration.hsm-pkcs11-integration
name: hsm-pkcs11-integration
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [hsm-pkcs11-integration, pki-hsm, hsm, pkcs11, softhsm, kms, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Wire a CA or signing service to an HSM through PKCS#11: sensitive, non-extractable keys, SO and user roles, protected PIN entry, and testing."
sources:
  - https://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HSM integration with PKCS#11
Goal: the CA private key never leaves the hardware boundary.

What PKCS#11 v2.40 (Cryptoki base spec) defines:
- Key attributes: `CKA_SENSITIVE` (CK_TRUE if the key is sensitive; default CK_FALSE for secret keys) and `CKA_EXTRACTABLE` (CK_TRUE if the key can be wrapped). If `CKA_SENSITIVE` is CK_TRUE or `CKA_EXTRACTABLE` is CK_FALSE, certain attributes of the private key cannot be revealed in plaintext outside the token. Generate CA keys on the token with `CKA_SENSITIVE=true` and `CKA_EXTRACTABLE=false`.
- Audit attributes: `CKA_ALWAYS_SENSITIVE` and `CKA_NEVER_EXTRACTABLE` record that a key has always been sensitive and never extractable. A key imported with `C_CreateObject` has both set to CK_FALSE, so a key you imported cannot later prove it was never exposed; generate on the token instead.
- Wrapping: `C_WrapKey` requires `CKA_EXTRACTABLE` CK_TRUE on the key to wrap and `CKA_WRAP` on the wrapping key; a key with `CKA_EXTRACTABLE` CK_FALSE fails with `CKR_KEY_UNEXTRACTABLE`. A non-extractable key therefore cannot be wrapped into a backup.
- Users: `CKU_SO` (Security Officer) and `CKU_USER` are the user types; `C_InitToken` and `C_InitPIN` set up the token and the normal user's PIN.
- Protected authentication path: a token flag (`CKF_PROTECTED_AUTHENTICATION_PATH`) meaning a user can log in without passing a PIN through the Cryptoki library, such as a PIN pad. Prefer it where the HSM offers it.
- Slots: a slot ID is a value assigned by the system and a slot with ID 0 need not exist; look slots up with `C_GetSlotList` rather than assuming slot 0.
- `CKA_PRIVATE` marks a private object, readable only after login.

Practice (not from the spec): prototype with a software token such as SoftHSM before hardware, pin the module path in configuration, and re-test signing after firmware or library upgrades. Plan high availability up front: because non-extractable keys cannot be wrapped for backup, use the HSM vendor's clustering or backup procedure.

Verify:
- [ ] The key's attributes show sensitive and non-extractable when listed with your PKCS#11 tool.
- [ ] The CA signs a test certificate using the token.

## Checked
Checked against the PKCS#11 v2.40 base specification (attribute tables for private and secret keys, `C_WrapKey`, `C_CreateObject`, user types, slot IDs, protected authentication path).
Removed: the `softhsm2-util`, `pkcs11-tool` and OpenSSL pkcs11-provider commands and the libp11 source (tool syntax and library paths not covered by the cited spec), the "sign usage only" attribute, and the partition and quorum claims.
Method: docs-only read of cited pages, 2026-11-08
