---
id: computing-software.cryptography-implementation.applied-cryptography.binding-context-with-associated-data
name: binding-context-with-associated-data
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, aead, associated-data, associated-data-binding, aad, context-binding, cut-and-paste-attack, field-level-encryption]
level: practitioner
status: docs-checked
description: "Bind ciphertexts to their context with AEAD associated data: which fields to include, canonical encoding, and stopping cut-and-paste swaps between rows."
sources: ["https://www.rfc-editor.org/rfc/rfc5116", "https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/concepts.html#encryption-context", "https://developers.google.com/tink/aead"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binding context with associated data

An AEAD authenticates its associated data (AD) without encrypting it. If
you encrypt record fields without AD, an attacker with database write
access can move a valid ciphertext from one row to another (copy the
admin's encrypted `role` into their own row) and it still decrypts.
AD makes the ciphertext valid only in its intended context.

## What to put in AD

Include everything that identifies where the ciphertext belongs and how
to read it, as long as the decryptor can reconstruct it without trusting
the ciphertext:

- table / collection and column name;
- the row's primary key or immutable record id;
- tenant or user id;
- ciphertext format version and key id (if not already in an authenticated header).

Do not include mutable values (e.g. `updated_at`), or decryption breaks on
every update.

## Encode it unambiguously

Concatenating strings is ambiguous (`"ab"+"c"` equals `"a"+"bc"`). Use a
fixed, length-prefixed encoding:

```python
import struct
def ad(*parts: bytes) -> bytes:
    return b"".join(struct.pack(">I", len(p)) + p for p in parts)

aad = ad(b"v1", b"users", b"ssn", str(user_id).encode())
ct = AESGCM(key).encrypt(nonce, ssn.encode(), aad)
```

JSON is acceptable only with a canonical form both sides produce
byte-for-byte; a length-prefixed tuple is simpler.

## API notes

- AWS Encryption SDK: the encryption context is the AD. It is not secret: it appears in plaintext in the message
  header and may appear in audit logs such as CloudTrail. On decrypt, verify the returned context contains what you
  supplied on encrypt before using the plaintext.
- Tink: AEAD associated data is optional, authenticated but not encrypted, and decryption succeeds only if the same
  data is passed to both encrypt and decrypt. Tink's own example uses a user id as AD so medical history cannot be
  moved between users.
- Other libraries: check how your AEAD API takes AD (typically a separate argument or an update call).

## Pitfalls

- AD is not secret; do not put sensitive values there expecting secrecy.
- Empty AD on decrypt when encrypt used AD gives an authentication failure,
  which is the point; do not "retry without AD".
- Migrating existing data to AD requires a re-encryption pass with a format
  version bump so readers know which rule applies.

## Verify

- [ ] Test: swapping ciphertexts between two rows fails decryption.
- [ ] AD encoding is length-prefixed and versioned.
- [ ] AD fields are immutable for the life of the ciphertext.

## Checked

2026-11-01. Confirmed in the Tink AEAD page (AD authenticated not encrypted, must match on decrypt, user-id example)
and the AWS Encryption SDK concepts page (encryption context not secret, visible in header and CloudTrail, verify on
decrypt); RFC 5116 is the AEAD interface reference. Removed: OpenSSL and Java call names and the KMS key-policy
condition key, which were not in the cited pages.
Method: documentation only; no commands were run.
