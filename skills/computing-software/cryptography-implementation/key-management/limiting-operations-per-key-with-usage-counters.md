---
id: computing-software.cryptography-implementation.key-management.limiting-operations-per-key-with-usage-counters
name: limiting-operations-per-key-with-usage-counters
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, key-usage-counter, usage-limits, key-rotation, aes-gcm, cryptoperiod, metrics, key-wearout]
level: advanced
status: verified
description: "Enforce per-key usage limits by counting encryptions, bytes and signatures, rotating automatically before AEAD or cryptoperiod limits are reached."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "https://csrc.nist.gov/pubs/sp/800/38/d/final", "https://www.rfc-editor.org/rfc/rfc9001#section-6.6"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Limiting operations per key with usage counters

Time-based cryptoperiods ignore volume. SP 800-57 Part 1 Rev. 5 section 5.3.1 lists "the volume of data flow or the number of transactions" and "the maximum number of invocations to avoid nonce reuse" among the cryptoperiod factors, and
SP 800-38D section 8.3 caps AES-GCM at 2^32 invocations of the authenticated encryption function per key when IVs are random (all IV lengths and instances combined).

## What to count
| Key kind | Counter | Typical limit |
|---|---|---|
| AES-GCM, random 96-bit IV | messages | well below 2^32 (e.g. 2^30) |
| AES-GCM, any IV | bytes per message, failed decrypts | 2^39-256 bits per message; integrity limits |
| Stateful hash-based signature key | signatures | tree capacity |
| Session / channel key | records or bytes | protocol rekey limit |
| Data key from KMS | objects encrypted | your policy (e.g. one per object or per N objects) |

## Implementation patterns
- **Local data keys:** keep an in-memory counter per data key; request a new data key from KMS when it reaches the
  threshold (the AWS Encryption SDK caching CMM does this with `max_messages_encrypted` and `max_bytes_encrypted`).
- **Shared keys across replicas:** count in a shared store with atomic increments (Redis `INCRBY`, a DB sequence),
  or allocate blocks of budget to each replica.
- **Long-lived master keys:** do not encrypt data directly; derive or wrap per-object keys so the master key's count
  stays tiny.

```python
class CountingKey:
    def __init__(self, key, limit): self.key, self.n, self.limit = key, 0, limit
    def use(self):
        self.n += 1
        if self.n > self.limit:
            raise RuntimeError("key usage limit reached; rotate")
```

## Monitoring
- Export counters as metrics labelled with key version.
- Alert at 50% and 80% of limit; auto-rotate at a fixed threshold.

## Verify
- [ ] Load test reaches the threshold and observes automatic rotation with no failed requests.
- [ ] Counters survive restarts (persisted or reset with a new key on startup).
