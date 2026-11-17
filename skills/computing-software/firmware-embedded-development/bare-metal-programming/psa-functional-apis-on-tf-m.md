---
id: computing-software.firmware-embedded-development.bare-metal-programming.psa-functional-apis-on-tf-m
name: psa-functional-apis-on-tf-m
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [psa-api, tf-m, psa-crypto, internal-trusted-storage, initial-attestation, firmware-embedded-development]
level: advanced
status: draft
description: "Use PSA Crypto, Internal Trusted Storage, Protected Storage and Initial Attestation from the non-secure app on Trusted Firmware-M: key handles, persistence, and error codes."
sources:
  - https://arm-software.github.io/psa-api/crypto/
  - https://trustedfirmware-m.readthedocs.io/en/latest/
  - https://arm-software.github.io/psa-api/storage/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PSA Functional APIs on TF-M

TF-M runs secure partitions that implement the PSA Certified APIs. The non-secure application
links the TF-M "interface" library and calls the same functions it would call on any PSA
implementation (Mbed TLS also implements PSA Crypto in a single world).

## PSA Crypto: keys stay in the secure world
```c
#include <psa/crypto.h>
psa_status_t st = psa_crypto_init();

psa_key_attributes_t a = PSA_KEY_ATTRIBUTES_INIT;
psa_set_key_type(&a, PSA_KEY_TYPE_ECC_KEY_PAIR(PSA_ECC_FAMILY_SECP_R1));
psa_set_key_bits(&a, 256);
psa_set_key_usage_flags(&a, PSA_KEY_USAGE_SIGN_HASH);
psa_set_key_algorithm(&a, PSA_ALG_ECDSA(PSA_ALG_SHA_256));
psa_set_key_lifetime(&a, PSA_KEY_LIFETIME_PERSISTENT);
psa_set_key_id(&a, 0x10001);                 /* persistent IDs: application range 0x00000001-0x3FFFFFFF */

psa_key_id_t key;
st = psa_generate_key(&a, &key);             /* private key never leaves the secure partition */
size_t sig_len;
st = psa_sign_hash(key, PSA_ALG_ECDSA(PSA_ALG_SHA_256), hash, 32, sig, sizeof sig, &sig_len);
```
After reboot, use the same ID directly (`psa_sign_hash(0x10001, ...)`); no reload needed.
`psa_export_public_key` gives the public half (for CSR or cloud registration).

## Storage
- **ITS** (Internal Trusted Storage, `psa_its_set/get/remove`): small secrets in on-chip flash
  owned by the secure world; no encryption by default (relies on isolation).
- **PS** (Protected Storage, `psa_ps_set/get`): larger data, encrypted and authenticated, may live
  in external flash, with optional rollback protection.
```c
psa_ps_set(UID_WIFI_CREDS, len, buf, PSA_STORAGE_FLAG_NONE);
```
UIDs are per-client: the same UID from different partitions refers to different objects.

## Initial Attestation
`psa_initial_attest_get_token(challenge, 32, token, sizeof token, &len)` returns a signed CBOR
(EAT) token with boot measurements, implementation ID and instance ID. A verifier service checks
it with the device's attestation public key. Challenge sizes must be 32, 48 or 64 bytes.

## Error handling
`PSA_SUCCESS` = 0; common failures: `PSA_ERROR_NOT_PERMITTED` (usage flags), `PSA_ERROR_INVALID_HANDLE`,
`PSA_ERROR_ALREADY_EXISTS` (persistent ID taken: destroy or reuse), `PSA_ERROR_INSUFFICIENT_MEMORY`
(TF-M crypto partition heap: `CRYPTO_ENGINE_BUF_SIZE` in the TF-M build config),
`PSA_ERROR_NOT_SUPPORTED` (algorithm not enabled in the TF-M Mbed TLS config).

## Verify
- [ ] Sign with a persistent key, reboot, verify the signature with the exported public key.
- [ ] PS data survives reboot and fails authentication when the backing flash is tampered with.
