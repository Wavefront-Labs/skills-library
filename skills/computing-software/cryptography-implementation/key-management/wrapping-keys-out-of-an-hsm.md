---
id: computing-software.cryptography-implementation.key-management.wrapping-keys-out-of-an-hsm
name: wrapping-keys-out-of-an-hsm
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, pkcs11-key-wrap, key-wrapping, hsm, pkcs11, aes-kwp, rfc-5649, ckm-rsa-aes-key-wrap, key-transfer, byok]
level: advanced
status: docs-checked
description: "Export and import keys between HSMs with PKCS#11 wrapping: CKM_AES_KEY_WRAP_KWP, RSA-AES wrap, CKA_WRAP_WITH_TRUSTED, wrap templates and key transfer."
sources: ["https://docs.oasis-open.org/pkcs11/pkcs11-spec/v3.1/pkcs11-spec-v3.1.html", "https://www.rfc-editor.org/rfc/rfc5649", "https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wrapping keys out of an HSM

## Attributes that control wrapping
| Attribute | On | Meaning |
|---|---|---|
| `CKA_EXTRACTABLE` | target key | Must be true to wrap it at all; false means it never leaves |
| `CKA_SENSITIVE` | target key | Value cannot be read in plaintext (wrapping still allowed if extractable) |
| `CKA_WRAP` / `CKA_UNWRAP` | wrapping key | Key may wrap / unwrap |
| `CKA_WRAP_WITH_TRUSTED` | target key | Only wrapping keys with `CKA_TRUSTED=true` may wrap it (default false) |
| `CKA_TRUSTED` | wrapping key | Lets the key wrap keys that have `CKA_WRAP_WITH_TRUSTED` set |
| `CKA_WRAP_TEMPLATE` / `CKA_UNWRAP_TEMPLATE` | wrapping key | Constrain which keys can be wrapped and the attributes of unwrapped keys |

Set `CKA_WRAP_WITH_TRUSTED` on keys you may need to move, so only SO-approved transport keys can export them.

## Mechanisms
- `CKM_AES_KEY_WRAP_KWP` (AES key wrap with padding, RFC 5649) - wraps key data of any length.
- `CKM_RSA_PKCS_OAEP` - wraps small keys under an RSA public key.
- `CKM_RSA_AES_KEY_WRAP` - a temporary AES key wraps the target with `CKM_AES_KEY_WRAP_KWP`, and the RSA public
  key wraps that temporary key. Check which wrap format a KMS import expects in its own docs.

## Flow (cross-vendor or HSM to KMS)
1. Destination generates an RSA wrapping key pair and exports the public key.
2. Source HSM imports that public key as a trusted wrapping key.
3. Source `C_WrapKey(CKM_RSA_AES_KEY_WRAP, wrappingPub, targetKey)` produces the blob.
4. Destination unwraps/imports; compare key check values on both sides.

## Gotchas
- Unwrapped keys inherit attributes from the unwrap template; set `CKA_EXTRACTABLE=false` on arrival if they should
  never move again.
- Wrapping a key under a weaker key reduces its security; use a wrapping key at least as strong as the target.

## Verify
- [ ] KCV matches after transfer.
- [ ] A non-trusted wrapping key fails to wrap a `CKA_WRAP_WITH_TRUSTED` key.

## Checked

2026-11-01. Confirmed in the PKCS #11 v3.1 spec: `CKA_TRUSTED`, `CKA_WRAP_WITH_TRUSTED` (default false),
`CKA_WRAP_TEMPLATE`, `CKM_RSA_AES_KEY_WRAP` construction using `CKM_AES_KEY_WRAP_KWP`; RFC 5649 for AES key wrap
with padding. Removed: pkcs11-tool wrap command, AWS BYOK parameter names, `CKM_AES_KEY_WRAP_PAD` and PKCS#8
claims, PCI wording, SO-only wording for `CKA_TRUSTED` on keys.
Method: documentation only; no commands were run.
