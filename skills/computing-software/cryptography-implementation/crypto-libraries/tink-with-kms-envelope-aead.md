---
id: computing-software.cryptography-implementation.crypto-libraries.tink-with-kms-envelope-aead
name: tink-with-kms-envelope-aead
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, tink-kms, tink, envelope-encryption, kms-envelope-aead, keyset-encryption, google-cloud-kms, aws-kms, high-level-crypto]
level: practitioner
status: draft
description: "Use Google Tink with a KMS: KmsEnvelopeAead for data, encrypting keysets under a KMS key, key URIs for GCP and AWS, associated data and rotation."
sources: ["https://developers.google.com/tink/client-side-encryption", "https://developers.google.com/tink/key-management-overview", "https://developers.google.com/tink/encrypt-keyset"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tink with KMS envelope AEAD

Two ways to combine Tink with a cloud KMS:

## 1. KmsEnvelopeAead (KMS wraps a fresh DEK per message)
Java:
```java
AeadConfig.register();
KmsClient kms = new GcpKmsClient().withDefaultCredentials();
String kekUri = "gcp-kms://projects/p/locations/global/keyRings/r/cryptoKeys/k";
Aead remote = kms.getAead(kekUri);
Aead envelope = KmsEnvelopeAead.create(PredefinedAeadParameters.AES256_GCM, remote);
byte[] ct = envelope.encrypt(plaintext, associatedData);
```
Ciphertext = length || wrapped DEK || AES-GCM ciphertext. One KMS call per encrypt and per decrypt; good for
low-volume, high-value data. AWS key URIs look like `aws-kms://arn:aws:kms:region:acct:key/id`.

## 2. Encrypted keyset (KMS wraps the Tink keyset once)
```java
KeysetHandle handle = KeysetHandle.generateNew(PredefinedAeadParameters.AES256_GCM);
String encrypted = TinkJsonProtoKeysetFormat.serializeEncryptedKeyset(handle, remote, "orders-keyset".getBytes());
// store `encrypted`; at startup:
KeysetHandle loaded = TinkJsonProtoKeysetFormat.parseEncryptedKeyset(encrypted, remote, "orders-keyset".getBytes());
Aead aead = loaded.getPrimitive(RegistryConfiguration.get(), Aead.class);
```
One KMS call at startup; all data operations local and fast. Rotation: add a new key to the keyset, make it primary,
re-serialize; old ciphertexts still decrypt because the key ID prefix selects the key.

## Choosing
| Situation | Use |
|---|---|
| Few large-value records, want KMS audit per decrypt | KmsEnvelopeAead |
| High throughput | Encrypted keyset |
| Need crypto-shredding per tenant | One keyset or KEK per tenant |

## Gotchas
- Associated data passed to `serializeEncryptedKeyset` must match on parse; use it to bind keyset identity.
- Never store keysets with `CleartextKeysetHandle` in production.
- KMS client credentials must be scoped to encrypt/decrypt on the one key.

## Verify
- [ ] Decrypt fails with wrong associated data.
- [ ] Keyset rotation test: old ciphertext decrypts after a new primary key is added.
