---
id: computing-software.firmware-embedded-development.iot-protocols.coap-block1-block2
name: coap-block1-block2
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [coap-block1-block2, coap-blockwise, coap, block1, block2, szx, iot-protocols]
level: practitioner
status: docs-checked
description: "CoAP Block1 and Block2: Transfer payloads larger than one datagram."
sources:
  - https://www.rfc-editor.org/rfc/rfc7959
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CoAP Block1 and Block2

**Goal:** Transfer payloads larger than one datagram.

## Steps
1. Block2 (option 23) is for responses, Block1 (27) for request bodies
2. Option value = NUM (block number), M (more flag), SZX (size exponent) so block size = 2^(SZX+4), i.e. 16 to 1024 bytes
3. Client asks next block by repeating the GET with the next NUM
4. Server may reduce SZX and client adjusts
5. Size2 and Size1 options give total size
6. RFC 7959 cites avoiding IP fragmentation (IPv6 MTU of 1280) as a reason to limit datagram size; the largest block is 1024 bytes (SZX 6)

## Gotcha
Changing the underlying resource between blocks gives a corrupt file; use ETag to detect it.

## Verify
- [ ] 4 KB resource retrieved in 4 x 1024 blocks
- [ ] ETag mismatch aborts
- [ ] M flag clear on final block

## Checked

2026-11-03. Confirmed in RFC 7959: Block2 option 23 and Block1 option 27, block size 2**(SZX+4) with SZX 0 to 6 (16 to 1024 bytes), smaller SZX negotiation, Size1/Size2, ETag use across blocks. Reworded step 6 (MTU of 1280 is cited; the 1024-payload rule of thumb was not).
Method: documentation only; no commands were run.
