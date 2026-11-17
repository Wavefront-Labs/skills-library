---
id: computing-software.messaging-and-integration.apache-pulsar.end-to-end-encryption
name: end-to-end-encryption
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [end-to-end-encryption, crypto-key-reader, session-key, ecdsa, rsa, encryption-key]
level: practitioner
status: docs-checked
description: "Encrypt Pulsar message payloads from producer to consumer with CryptoKeyReader and RSA or ECDSA key pairs; session key rotation and key-loss warning."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/security-encryption.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make message payloads unreadable by the broker or storage by encrypting on the producer and decrypting on the consumer.

Workflow: the producer generates a symmetric session key (for example AES) regularly, every 4 hours or after a certain number of messages, and encrypts payloads with it. It fetches the consumer's public key and encrypts the session key with an asymmetric algorithm (RSA or ECDSA key pair supplied by the application), adding an alias with the encrypted key to the message header. The consumer reads the header, decrypts the session key with its private key, then decrypts the payload.

Warnings from the page: Pulsar does not store the encryption key anywhere; if you lose or delete the private key the messages are irretrievably lost. Key management is isolated behind the `CryptoKeyReader` interface, which only provides access to public keys; for production implement it against a cloud key management service. For cross-application consumption, either add the consumer application's public key to the producer's keys or give consumers access to one of the producer's private keys.

Prerequisites: Java, Python, C++ and Node.js clients 2.7.1 or later; Go client 0.6.0 or later.

Create keys:
```shell
openssl genrsa -out test_rsa_privkey.pem 2048
openssl rsa -in test_rsa_privkey.pem -pubout -outform PEM -out test_rsa_pubkey.pem
openssl ecparam -name secp521r1 -genkey -param_enc explicit -out test_ecdsa_privkey.pem
openssl ec -in test_ecdsa_privkey.pem -pubout -outform pem -out test_ecdsa_pubkey.pem
```
Java: set `.cryptoKeyReader(keyReader)` on producer, consumer and reader builders, and `.addEncryptionKey("myappkey")` on the producer. `RawFileKeyReader` in the example is not provided by Pulsar; implement `CryptoKeyReader` yourself. Python: built-in `CryptoKeyReader('test_rsa_pubkey.pem', 'test_rsa_privkey.pem')` with `encryption_key='myappkey'` on `create_producer` and `crypto_key_reader=...` on subscribe and reader. C++: `DefaultCryptoKeyReader`, `producerConf.addEncryptionKey("myappkey")`.

## Checked

2026-11-03. Confirmed against the pulsar-site page security-encryption: workflow and 4-hour/message-count session key rotation, key-loss and CryptoKeyReader notes, client version prerequisites, openssl key commands and the Java, Python and C++ snippets. Removed the invented Verify step.

Method: documentation only; no commands were run.
