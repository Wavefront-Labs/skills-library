---
id: computing-software.cryptography-implementation.secure-implementation.monitoring-decryption-failures
name: monitoring-decryption-failures
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, decryption-failure-monitoring, padding-oracle, error-oracle, rate-limiting, aead-usage-limits, security-monitoring, alerting]
level: practitioner
status: verified
description: "Detect oracle attacks and corruption by counting and rate-limiting decryption, MAC and signature failures per key and client, with alerts that leak nothing to callers."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html", "https://www.rfc-editor.org/rfc/rfc9001#section-6.6", "https://cwe.mitre.org/data/definitions/209.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring decryption failures

Oracle attacks (padding oracles, Bleichenbacher, invalid-curve, AEAD forgery attempts) need hundreds to millions of
queries that fail. Failures are signal: count them.

## What to count
| Metric | Labels |
|---|---|
| AEAD tag / MAC verification failures | key id/version, endpoint, client id or IP bucket |
| Signature verification failures | key id, issuer, endpoint |
| RSA decryption/padding failures | key id |
| Parse errors on decrypted data | endpoint |
Never label with plaintext, ciphertext or token values.

## Responses
- **Per client:** after N failures in a window, slow down (exponential backoff) or block; legitimate clients rarely
  fail repeatedly.
- **Per key:** alert when failures exceed a baseline; QUIC-style integrity limits require disabling a key after a
  bounded number of forgeries (RFC 9001 section 6.6: integrity limit 2^36 invalid packets for ChaCha20-Poly1305, 2^52 for AES-GCM).
- **Corruption vs attack:** a sudden spike across all clients after a deploy is usually a bug (wrong key version,
  encoding change); a steady stream from one source is an attack.

## Response to callers
Keep it uniform: same status code, same message, same timing for every failure type. Detailed reasons go only to
internal logs (and not the secret inputs).

## Implementation sketch
```python
# prometheus_client Counter with these labels exports decrypt_failures_total{key_version=..,endpoint=..} (run)
FAILS = Counter("decrypt_failures_total", "AEAD failures", ["key_version", "endpoint"])
def open_blob(blob, ad, client):
    try:
        return aead_open(blob, ad)
    except InvalidTag:
        FAILS.labels(key_version_of(blob), endpoint()).inc()
        limiter.hit(client)          # raises TooManyRequests beyond threshold
        raise DecryptError()          # generic
```

## Verify
- [ ] Dashboard shows failure rates per key; alert thresholds defined.
- [ ] Load test with random forgeries triggers client blocking without affecting others.
