---
id: computing-software.firmware-embedded-development.bootloader-development.coap-block-wise-firmware-transfer
name: coap-block-wise-firmware-transfer
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [coap-block-transfer, firmware-transport, rfc7959, block2-option, constrained-networks, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Fetch firmware over CoAP with block-wise transfer (RFC 7959 Block2): block size choice, sequential GETs with resume, ETag checks, and retransmission over lossy UDP links."
sources:
  - https://www.rfc-editor.org/rfc/rfc7959
  - https://www.rfc-editor.org/rfc/rfc7252
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CoAP block-wise firmware transfer

CoAP runs over UDP (often DTLS) on constrained networks: NB-IoT, LTE-M, Thread/6LoWPAN.
Messages must fit one datagram, so large resources are transferred in blocks with the **Block2**
option (responses) defined in RFC 7959.

## Block2 basics
Option value encodes `NUM` (block number), `M` (more blocks follow) and `SZX` (size exponent):
block size = 2^(SZX+4), i.e. 16, 32, ..., 1024 bytes. The client requests block NUM with its
preferred SZX; the server may answer with a smaller size and the client adapts.
```
GET /fw/acme-2.4.1.bin   Block2: NUM=0, SZX=6 (1024 B)
2.05 Content             Block2: NUM=0, M=1, SZX=6   ETag: 0x5a3c   payload[1024]
GET /fw/acme-2.4.1.bin   Block2: NUM=1, SZX=6
...
2.05 Content             Block2: NUM=N, M=0          payload[last]
```

## Choosing block size
- Fit inside the link MTU without IP fragmentation: constrained links such as 6LoWPAN need small
  blocks, higher-MTU links tolerate larger ones. Measure your path MTU and pick the largest SZX
  that stays inside it.
- With DTLS, subtract the record overhead from the datagram budget.

## Reliability and resume
- Use **Confirmable** messages (CON): CoAP retransmits with exponential backoff
  (RFC 7252 defaults: ACK_TIMEOUT 2 seconds, MAX_RETRANSMIT 4; tune for high-latency links).
- Resume is natural: store the next block number in persistent storage per erase block written,
  restart from the block number that corresponds to the stored offset after a reset.
- Check the **ETag** (or a manifest digest) on each response; if it changes mid-download, the
  resource changed: restart.
- Write blocks to the inactive slot in order; verify the full image hash/signature at the end.

## Implementations
Use a CoAP library that implements RFC 7959 on both client and server, and test against a second
independent implementation.

## Verify
- [ ] Download over an emulated lossy, high-latency link completes and the hash matches.
- [ ] Resume after reset continues from the stored block without re-downloading completed blocks.

## Checked
2026-10-31. Confirmed against RFC 7959 (Block2 option with NUM, M and SZX; block size 2**(SZX+4); ETag handling across blocks) and RFC 7252 (ACK_TIMEOUT 2 seconds, MAX_RETRANSMIT 4). Removed the 6LoWPAN and NB-IoT block-size numbers, DTLS overhead figure, 10 s timeout suggestion, Zephyr coap_client and tool names, the Observe remark and the netem parameters, none of which the fetched pages state.
Method: documentation only; no commands were run.
