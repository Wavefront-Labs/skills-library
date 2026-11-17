---
id: computing-software.firmware-embedded-development.iot-protocols.coap-message-format
name: coap-message-format
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [coap-message-format, coap-messages, coap, rfc7252, options, iot-protocols]
level: practitioner
status: docs-checked
description: "CoAP message format: Decode a CoAP datagram by hand."
sources:
  - https://www.rfc-editor.org/rfc/rfc7252
  - https://www.rfc-editor.org/rfc/rfc7641
  - https://www.rfc-editor.org/rfc/rfc7959
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CoAP message format

**Goal:** Decode a CoAP datagram by hand.

## Steps
1. Header 4 bytes: Ver (2 bits, =1), Type (2 bits: CON 0, NON 1, ACK 2, RST 3), TKL (4 bits), Code (class.detail e.g. 0.01 GET, 0.02 POST, 2.05 Content, 4.04 Not Found), Message ID (16 bits)
2. Then token (0-8 bytes), options as delta-encoded type/length, then 0xFF marker and payload
3. Option numbers: Uri-Path 11, Content-Format 12, Uri-Query 15, Observe 6, Block2 23, Block1 27
4. Content-Format 0 text/plain, 40 link-format

## Gotcha
Message ID matches messages (ack/dedup), token matches request to response; confusing them breaks piggybacked and separate responses.

## Verify
- [ ] Hand decode matches Wireshark
- [ ] Option deltas sum to expected numbers
- [ ] 0xFF only present with payload

## Checked

2026-11-03. Confirmed in RFC 7252, RFC 7641 and RFC 7959: header fields, token length 0-8, code classes, 0xFF payload marker, option numbers 11, 12, 15 (7252), 6 (7641), 23 and 27 (7959), Content-Format 0 and 40. Removed: Content-Format 60 CBOR (not in these RFCs).
Method: documentation only; no commands were run.
