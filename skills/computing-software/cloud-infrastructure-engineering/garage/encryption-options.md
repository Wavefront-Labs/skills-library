---
id: computing-software.cloud-infrastructure-engineering.garage.encryption-options
name: encryption-options
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [encryption, sse-c, luks, client-side-encryption]
level: advanced
status: docs-checked
description: "See what Garage encrypts itself, what it leaves to you, and where SSE-C, LUKS and TLS fit."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/cookbook/encryption/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Garage's encryption posture, per the cookbook:

- RPC between nodes is always encrypted. Clear-text RPC is impossible, which is why `rpc_secret` is mandatory. A Secret Handshake protocol implementation is used.
- Its HTTP API endpoints are clear text, and built-in TLS is not planned.
- At rest, standard S3 requests are stored in plain text. SSE-C is supported: the client sends keys in a header on each request, Garage encrypts or decrypts at that moment and discards the key. Only the node receiving that request (possibly a gateway) ever sees the key, so untrusted nodes are tolerable as long as SSE-C requests are not sent to them. It does not suit a model where the server itself is untrusted.
- Server-managed SSE-S3 style encryption is not planned, largely because of key management questions.

What to add yourself: for client traffic, a TLS reverse proxy, a local gateway on localhost, or an encrypted overlay such as Wireguard. For stolen disks, LUKS full-disk encryption, which does not protect against malicious sysadmins or remote attackers. For those threats, encrypt on the client side before upload.

## Checked

2026-11-04. Read the Encryption page in full. Confirmed RPC encryption, clear-text HTTP endpoints, SSE-C behaviour, the SSE-S3 position and the three external options. Nothing removed.
Method: documentation only; no commands were run.
