---
id: computing-software.firmware-embedded-development.iot-protocols.oscore-basics
name: oscore-basics
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [oscore-basics, coap-security, coap, oscore, rfc8613, iot-protocols]
level: practitioner
status: docs-checked
description: "OSCORE object security: Protect CoAP messages end to end through proxies."
sources:
  - https://www.rfc-editor.org/rfc/rfc8613
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSCORE object security

**Goal:** Protect CoAP messages end to end through proxies (RFC 8613, Object Security for Constrained RESTful Environments).

## Steps
1. OSCORE protects the CoAP message with a COSE object using an AEAD algorithm; the default is AES-CCM-16-64-128 (COSE algorithm encoding 10), with HKDF SHA-256 as the default key derivation.
2. The security context holds Master Secret, Master Salt (optional), Sender ID, Recipient ID, optional ID Context, derived Sender and Recipient Keys, a Common IV, a Sender Sequence Number and, on a server, a Replay Window.
3. The OSCORE option is CoAP option number 9 (critical, safe to forward, 0-255 bytes). It carries the OSCORE flag bits, Partial IV and the sender's `kid`.
4. Message fields are in classes: Class E (encrypted and integrity protected, "inner"), Class I (integrity protected only; none are currently defined) and Class U (unprotected, "outer", visible to proxies). Uri-Path and Uri-Query are Class E.
5. An AEAD nonce MUST NOT be used more than once per AEAD key, and the Sender Sequence Number MUST be atomic. The Sender Sequence Number is initialised to 0.
6. The server keeps a replay window per recipient context to reject replayed requests.

## Gotcha
If the security context is stored only in RAM, an unplanned reboot loses the mutable part of it. The RFC requires that an endpoint with its context in nonvolatile memory MUST NOT reuse a previous Sender Sequence Number and MUST NOT accept previously received messages again; see its security considerations on losing state before designing reboot behaviour.

## Verify
- [ ] A proxy cannot read the inner payload or inner options
- [ ] A replay of an old request is rejected
- [ ] The sequence number state survives reboot (or the context is re-established safely)

## Checked
2026-11-09. Read RFC 8613: default algorithm, security context parameters, OSCORE option number 9 and its properties, message field classes, nonce uniqueness and atomic sequence number, initial sequence number 0, the nonvolatile-context rule. Removed: EDHOC/RFC 9528 step (not in RFC 8613), the RFC 7252 source (not used) and the "persist before use" wording (the RFC states the nonvolatile rule only).
Method: documentation only; no commands were run.
