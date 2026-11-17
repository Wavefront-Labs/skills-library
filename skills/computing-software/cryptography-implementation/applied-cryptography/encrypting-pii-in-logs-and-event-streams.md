---
id: computing-software.cryptography-implementation.applied-cryptography.encrypting-pii-in-logs-and-event-streams
name: encrypting-pii-in-logs-and-event-streams
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, event-stream-encryption, kafka, field-level-encryption, crypto-shredding, pii, logs]
level: advanced
status: draft
description: "Protect PII in logs and event streams (Kafka, Kinesis): field-level encryption at producers, tokenization, per-subject keys for erasure, and key rotation in consumers."
sources: ["https://docs.confluent.io/platform/current/security/csfle/overview.html", "https://docs.aws.amazon.com/streams/latest/dev/server-side-encryption.html", "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Encrypting PII in logs and event streams

Broker or disk encryption (Kinesis SSE, Kafka at-rest volumes) protects disks, not data from every consumer or
anyone with topic read access. Sensitive fields need protection inside the message.

## Patterns
- **Field-level encryption at producer**: encrypt PII fields with an AEAD data key wrapped by KMS; include key
  ID in headers. Confluent CSFLE does this via schema tags (`PII`) and encryption rules in Schema Registry.
- **Tokenization**: replace PII with tokens from a vault; consumers that need the value detokenize.
- **Per-subject keys (crypto-shredding)**: each user's fields use a key derived or stored per subject; deleting
  the key satisfies erasure across immutable logs and replicas.
- **Logs**: redact before emission; if retention of the value is required, encrypt it with a log-specific key.

## Implementation
- Bind context (topic, field name, subject ID) as AAD so ciphertext cannot be moved between fields.
- Cache unwrapped data keys with TTL to avoid KMS rate limits.
- Consumers keep old key versions to read historical offsets.

## Pitfalls
- Encrypting the partition key breaks ordering if it is randomized; use a deterministic token for keys.
- Dead-letter queues and stream processors (ksqlDB, Flink) that decrypt and re-emit in clear.

## Verify
- [ ] Sample topic dump shows no plaintext PII.
- [ ] Erasure test: deleting a subject key makes old events unreadable.
