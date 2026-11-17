---
id: computing-software.cryptography-implementation.applied-cryptography.versioned-ciphertext-format
name: versioned-ciphertext-format
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, data-at-rest-encryption, ciphertext-format, crypto-agility, key-id, header-authentication, serialization, versioning]
level: advanced
status: docs-checked
description: "Design a stored ciphertext envelope: version byte, key id, nonce, ciphertext, tag, header covered by AAD, fixed parsing rules, so algorithms and keys can rotate later."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html", "https://developers.google.com/tink/wire-format", "https://github.com/fernet/spec/blob/master/Spec.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Versioned ciphertext format

Every stored ciphertext will outlive the algorithm or key that made it. A small
self-describing header lets you rotate keys and change algorithms without
guessing what a blob is.

## Recommended layout

```
| ver (1) | key_id (4 or 16) | nonce (12 or 24) | ciphertext (n) | tag (16) |
  \------------- header, passed as AAD ------------/
```

- **ver**: identifies algorithm + layout (0x01 = AES-256-GCM, 4-byte key id,
  12-byte nonce). Never reuse a version number for a different meaning.
- **key_id**: points into your keyring / KMS key version. Tink uses a 5-byte
  prefix (0x01 + 4-byte key id); Fernet uses version 0x80 + timestamp + IV.
- **nonce**: fixed length per version.
- **AAD = header bytes** plus external context (table/column/row id). This
  authenticates version and key id: an attacker cannot downgrade the version
  byte or point to a different key without failing the tag check.

## Parsing rules

1. Read `ver`; unknown version -> reject (never fall back to "try all").
2. Lengths come from the version table, not from attacker-supplied length
   fields, unless you need variable-length headers (then length-prefix and
   bounds-check).
3. Look up key by `key_id`; unknown id -> reject (do not try every key -
   that costs CPU and can become an oracle).
4. Decrypt with AAD = header || context. On failure return a single generic
   error.

## Text storage

Encode the whole blob with base64url (no padding) or store binary in a
`BYTEA/VARBINARY` column. Don't base64 parts separately and join with ':'
unless the format specifies escaping; it invites parsing ambiguity.

## Migration from an unversioned format

A magic first byte only works if legacy blobs can never start with it; when
legacy blobs begin with a random IV, any byte value is possible. Safer: mark
format out of band (new column, per-row flag, or separate table) until all
data is re-encrypted, then drop the legacy path.

## Verify

- [ ] Version table documented: algorithm, key id size, nonce size, tag size.
- [ ] Flipping the version byte or key id causes authentication failure, not a different decryption path.
- [ ] Unknown version and unknown key id are rejected without trial decryption.
- [ ] Round-trip tests exist for every version still readable.

## Checked

- 2026-11-01. Confirmed: Tink output prefix is 5 bytes, a 0x01 version byte plus a 4-byte key id, and is not authenticated (Tink wire format page); Fernet token is Version, Timestamp, IV, Ciphertext, HMAC with version 0x80 (Fernet spec).
- The layout and field sizes above are an illustrative design, not a standard; the parsing rules are design advice.

Method: documentation only; no commands were run.
