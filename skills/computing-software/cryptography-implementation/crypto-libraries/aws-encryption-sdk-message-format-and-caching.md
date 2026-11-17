---
id: computing-software.cryptography-implementation.crypto-libraries.aws-encryption-sdk-message-format-and-caching
name: aws-encryption-sdk-message-format-and-caching
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, aws-esdk-message-format, aws-encryption-sdk, data-key-caching, envelope-encryption, kms]
level: advanced
status: docs-checked
description: "Understand the AWS Encryption SDK message format and data key caching: header with encrypted data keys, framing, signature footer, and caching CMM limits."
sources: ["https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/message-format.html", "https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/data-key-caching.html", "https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/supported-algorithms.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Encryption SDK message format and caching

## Message layout
- **Header**: version (v2 for committing suites), algorithm suite ID, message ID, encryption context (plain,
  authenticated), encrypted data keys (count, then each key), content type (framed or nonframed), frame length, and header
  authentication. v2 (algorithm suites with key commitment) drops the type, reserved and IV-length fields and adds
  algorithm suite data carrying the key commitment value.
- **Body**: use framed data (nonframed is legacy only); each frame is encrypted separately with its own IV, a
  sequence number starting at 1, and a final frame. The frame length is a header field (4 bytes).
- **Footer**: present only for signing suites; a digital signature over header and body. The recommended default
  suite is AES-GCM 256 with HKDF (SHA-384), ECDSA P-384 signing and key commitment (HKDF SHA-512); look up the
  suite constants in the SDK for your language.

Consequences: the ciphertext is self-describing and portable across languages; the encryption context is visible
to anyone with the ciphertext, so never put secrets in it.

## Signed versus unsigned suites
Signed suites stop holders of the decryption key from forging messages that look like they came from a writer.
Use an unsigned suite only when the users who encrypt and those who decrypt are equally trusted. Key-committing
suites add 30 bytes to the message and take longer to process, but make each ciphertext decrypt to one plaintext.

## Data key caching (caching CMM / hierarchical keyring)
- Reuses a data key for multiple messages to reduce KMS calls; off by default (a new data key is generated per
  encryption). Use it only when performance requires, with the smallest caching that meets the goal.
- The caching CMM enforces security thresholds you set (maximum age, messages and bytes per data key; parameter
  names differ by language, see the developer guide's threshold page).
- Reduces cryptographic isolation: one exposed data key reveals all messages using it. The AWS KMS Hierarchical
  keyring is an alternative caching solution in newer SDK versions; content it encrypts can only be decrypted
  with a Hierarchical keyring.

## Verify
- [ ] Decrypt path checks expected encryption context keys and values; commitment policy is set
  deliberately (it decides whether key-committing suites are used).

## Checked
2026-10-28. Confirmed against the AWS Encryption SDK developer guide pages Message format, Supported algorithm
suites and Data key caching: format versions 1 and 2, header fields, framing and final frame, footer only for
signing suites, ECDSA P-384 default suite, +30 bytes for key commitment, caching off by default, Hierarchical
keyring alternative. Removed: 4096-byte default frame, 2^32 message limit, parameter and suite constant names, the
commitment policy constant and the DynamoDB branch-key remark (not on these pages).
Method: documentation only; no commands were run.
