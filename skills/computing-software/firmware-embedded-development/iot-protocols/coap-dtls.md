---
id: computing-software.firmware-embedded-development.iot-protocols.coap-dtls
name: coap-dtls
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [coap-dtls, coap-security, coap, dtls, coaps, psk, iot-protocols]
level: practitioner
status: docs-checked
description: "CoAP over DTLS: Secure CoAP with DTLS 1.2 and choose credentials."
sources:
  - https://www.rfc-editor.org/rfc/rfc7252#section-9
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CoAP over DTLS

**Goal:** Secure CoAP with DTLS 1.2 and choose credentials.

## Steps
1. coaps:// uses UDP port 5684
2. RFC 7252 defines four security modes: NoSec, PreSharedKey, RawPublicKey and Certificate; NoSec and RawPublicKey are the ones mandatory to implement
3. PreSharedKey implementations must support the cipher suite TLS_PSK_WITH_AES_128_CCM_8
4. Prefer a unique PSK per device: a key shared by more than two entities only proves group membership, not a specific peer

## Gotcha
A shared PSK across the fleet means one extracted device key compromises all; derive or provision per-device keys.

## Verify
- [ ] Handshake succeeds only with the right key
- [ ] Per-device PSK

## Checked

2026-11-03. Confirmed in RFC 7252 section 9: coaps default UDP port 5684, the four security modes, mandatory-to-implement modes, PSK mode cipher suite, key-sharing caveat. Removed: Connection ID (RFC 9146), session resumption and DTLS 1.3 claims (outside the sources read).
Method: documentation only; no commands were run.
