---
id: computing-software.cryptography-implementation.key-management.pkcs11-key-attributes-and-non-extractability
name: pkcs11-key-attributes-and-non-extractability
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, hsm-integration, pkcs11-attributes, pkcs11, cka-sensitive, cka-extractable, non-extractable-keys, pkcs11-tool]
level: advanced
status: docs-checked
description: "Set PKCS#11 key attributes so HSM keys stay inside: SENSITIVE, EXTRACTABLE, usage flags, wrap templates, and checking ALWAYS_SENSITIVE and NEVER_EXTRACTABLE."
sources: ["https://docs.oasis-open.org/pkcs11/pkcs11-spec/v3.1/os/pkcs11-spec-v3.1-os.html", "https://github.com/OpenSC/OpenSC/wiki/Using-pkcs11-tool-and-OpenSSL"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PKCS#11 key attributes and non-extractability

An HSM only protects keys whose attributes say so. Attributes are set at
generation or unwrap time and some can only be tightened afterwards.

## Attributes that matter

| Attribute | Set | Meaning |
|---|---|---|
| `CKA_TOKEN` | TRUE | Stored on the token (FALSE = session object) |
| `CKA_PRIVATE` | TRUE | Requires login to access |
| `CKA_SENSITIVE` | TRUE | Value never revealed in plaintext; can go FALSE -> TRUE only |
| `CKA_EXTRACTABLE` | FALSE | Cannot be wrapped out; can go TRUE -> FALSE only |
| `CKA_MODIFIABLE` | FALSE | Attributes frozen |
| `CKA_COPYABLE` | FALSE | `C_CopyObject` cannot clone it with weaker attributes |
| `CKA_SIGN`/`CKA_DECRYPT`/`CKA_WRAP`/`CKA_UNWRAP`/`CKA_DERIVE` | only what is needed | Usage separation |
| `CKA_WRAP_WITH_TRUSTED` | TRUE | Can be wrapped only by keys with `CKA_TRUSTED` |
| `CKA_ID`, `CKA_LABEL` | set | How applications find the key |

Read-only evidence: `CKA_ALWAYS_SENSITIVE` and `CKA_NEVER_EXTRACTABLE` are
TRUE only if the key was generated that way and never relaxed. Check them
when auditing keys you did not create.

## Generate correctly

```c
CK_BBOOL t = CK_TRUE, f = CK_FALSE;
CK_ATTRIBUTE priv[] = {
  {CKA_TOKEN,&t,1},{CKA_PRIVATE,&t,1},{CKA_SENSITIVE,&t,1},
  {CKA_EXTRACTABLE,&f,1},{CKA_SIGN,&t,1},{CKA_DECRYPT,&f,1},
  {CKA_LABEL,"web-tls",7},{CKA_ID,id,sizeof id} };
C_GenerateKeyPair(h, &mech, pub, npub, priv, 8, &hPub, &hPriv);
```

```bash
pkcs11-tool --module $MOD --login --keypairgen --key-type RSA:2048 \
  --label web-tls --id 01   # add attribute flags from `pkcs11-tool --help`
pkcs11-tool --module $MOD --login --list-objects --type privkey   # inspect flags
```

Always inspect the attributes of the generated key.

## Wrap and unwrap

- If keys must move between HSMs (backup, migration), mark KEKs
  `CKA_TRUSTED` and data keys `CKA_WRAP_WITH_TRUSTED`; use
  `CKA_UNWRAP_TEMPLATE` so unwrapped keys get SENSITIVE/non-extractable.
- Vendor HSMs may add their own controls; use them.

## Verify

- [ ] Attempting `C_GetAttributeValue(CKA_VALUE)` on a key does not return the key bytes.
- [ ] `C_WrapKey` on a production key fails unless by a trusted KEK.
- [ ] Audit lists ALWAYS_SENSITIVE and NEVER_EXTRACTABLE TRUE for all keys.

## Checked

2026-11-01. Confirmed in the PKCS#11 v3.1 spec: CKA_SENSITIVE FALSE to TRUE only; CKA_EXTRACTABLE cannot change once FALSE; CKA_WRAP_WITH_TRUSTED, CKA_TRUSTED, CKA_UNWRAP_TEMPLATE, CKA_COPYABLE (cannot be set TRUE again), CKA_ALWAYS_SENSITIVE, CKA_NEVER_EXTRACTABLE. OpenSC wiki: `--keypairgen`, `--key-type`, `--label`, `--id`, `--login`, `--list-objects --type privkey`. Removed: EC `--usage-sign`/`--sensitive` flags (not on the page), named vendors, a specific error code, SoftHSM source.
Method: documentation only; no commands were run.
