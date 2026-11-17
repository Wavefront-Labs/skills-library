---
id: computing-software.cryptography-implementation.applied-cryptography.blind-index-encrypted-search
name: blind-index-encrypted-search
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, data-at-rest-encryption, blind-index, searchable-encryption, hmac, field-level-encryption, normalisation, truncation, leakage]
level: advanced
status: docs-checked
description: "Search encrypted fields with blind indexes: keyed hash of normalised values, separate index keys, truncation to tune false positives, and the leakage you accept."
sources: ["https://paragonie.com/blog/2017/05/building-searchable-encrypted-databases-with-php-and-sql", "https://ciphersweet.paragonie.com/security", "https://docs.aws.amazon.com/database-encryption-sdk/latest/devguide/beacons.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blind indexes for encrypted search

Store the field encrypted with a randomized AEAD, and next to it a blind
index: `HMAC(index_key, normalise(value))`. To search, compute the same HMAC of
the query value and look it up. The database gets an index it can use; the
ciphertext stays non-deterministic.

## Build it

```python
import hmac, hashlib, unicodedata
def normalise_email(v: str) -> bytes:
    return unicodedata.normalize("NFKC", v).strip().casefold().encode()
def blind_index(index_key: bytes, value: bytes, bits: int = 32) -> bytes:
    full = hmac.new(index_key, b"users.email|" + value, hashlib.sha256).digest()
    return full[: bits // 8]
```

- **Key**: separate from the encryption key, derived per column and tenant
  (HKDF with `info = "bidx|users.email|tenant-42"`). Leaking the index key lets
  an attacker brute-force low-entropy values offline; it must not also decrypt.
- **Normalisation**: decide case, whitespace, Unicode form, phone/number
  formats once and apply it at write and query time. Mismatch = missed rows.
- **Slow hash option**: for low-entropy fields (names, dates of birth) use a
  memory-hard KDF (e.g. Argon2 with the column key as static salt) instead of HMAC to
  raise offline brute-force cost; costs latency per query.
- **Truncation**: Paragon suggests truncating blind indexes to e.g. 16, 32 or
  64 bits and treating them like a Bloom filter. Collisions return extra
  candidate rows that you decrypt and filter in the app, which deliberately
  adds false positives. Choose the length against your row count and the leakage
  you accept.

## Compound matching

- Compound indexes: HMAC over several fields (e.g. `lastname|birthyear`) for
  combined filters. The AWS Database Encryption SDK calls these compound beacons;
  its standard beacons do equality searches.
- Every extra index leaks more; Paragon advises creating indexes only for
  serious business needs and logging access aggressively.

## Leakage

A full-length HMAC is deterministic, so the database shows which rows share a
value and preserves the frequency distribution (AWS beacons page). Blind indexes
can also reveal real-world metadata such as two people sharing an address
(Paragon). Truncation and partitioning reduce frequency leakage.

## Verify

- [ ] Index key is distinct from the encryption key and per column.
- [ ] Normalisation function is shared code used by write and query paths.
- [ ] Query returns correct rows after app-side decrypt-and-filter of collisions.
- [ ] Field entropy reviewed; low-entropy fields use slow hash or no index.

## Checked

2026-11-01. Confirmed in Paragon Initiative's blind-indexing article (keyed hash in a separate column, key distinct from
the encryption key, key-stretching with the key as static salt for sensitive data, truncation to 16/32/64 bits, a
distinct key per index, metadata leakage), the CipherSweet security page (truncated keyed hashes, per-index keys from
HKDF, slow indexes via a KDF) and the AWS Database Encryption SDK beacons page (deterministic HMAC beacons keep
frequency distribution, standard equality and compound beacons, partitions). Removed: the bucket-size rule of thumb,
prefix-index advice, the no-range/sorting line and the boolean/enum claim, not stated in these pages. Code is an
illustrative sketch.
Method: documentation only; no commands were run.
