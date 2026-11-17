---
id: computing-software.firmware-embedded-development.bootloader-development.chunk-ack-update-protocol
name: chunk-ack-update-protocol
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [chunk-ack-protocol, firmware-transport, custom-update-protocol, sequence-numbers, offset-based-transfer, firmware-embedded-development]
level: advanced
status: draft
description: "Design a custom firmware transfer protocol for UART, BLE, RS-485 or radio links: offset-addressed chunks, CRC per frame, acks with resume offset, flow control and timeouts."
sources:
  - https://docs.zephyrproject.org/latest/services/device_mgmt/smp_protocol.html
  - https://www.st.com/resource/en/application_note/an3155-usart-protocol-used-in-the-stm32-bootloader-stmicroelectronics.pdf
  - https://infocenter.nordicsemi.com/topic/sdk_nrf5_v17.1.0/lib_dfu_transport.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Chunk acknowledgement and resume protocol

Before inventing a protocol, check whether SMP/MCUmgr, YMODEM, USB DFU or the vendor ROM
protocol fits. When it doesn't (proprietary radio, multi-drop RS-485, a host app constraint),
these design rules avoid the classic failures.

## Message set (minimal)
| Message | Fields |
|---|---|
| `START` | image size, image digest (SHA-256), version, chunk size proposal |
| `START_ACK` | accepted chunk size, **resume offset** (0 or where a previous attempt stopped), status |
| `DATA` | offset (u32), length, payload, CRC-16/32 over header+payload |
| `DATA_ACK` | next expected offset, status (OK, CRC error, flash error, out of order) |
| `END` | (none) |
| `END_ACK` | verification result (digest/signature OK, bad) |
| `ABORT` | reason |

## Principles
- **Address chunks by byte offset, not sequence number**: duplicates and retransmissions become
  idempotent ("write at offset X" twice is harmless), and resume is just "next expected offset".
- **Ack carries the next expected offset**: the sender always knows where to continue, even after
  losing acks.
- **CRC per frame** on links without their own integrity (UART, raw radio); still verify the
  whole image digest at END.
- **Flow control**: one chunk in flight (stop-and-wait) is simplest; a window of N chunks raises
  throughput on high-latency links (BLE, satellite). The receiver advertises how many it can buffer.
- **Flash timing**: the receiver may need tens of ms to erase a sector; let it answer `BUSY`
  or delay the ack instead of the sender timing out. Pre-erase the slot at START if possible.
- **Timeouts and retries** on the sender with a retry limit, then ABORT; the receiver times out
  an abandoned session and keeps the resume offset persisted.
- **Framing**: COBS or SLIP with length + CRC on byte streams; on BLE, chunk size = ATT MTU - 3
  minus header.
- **Security**: integrity in transit is not authenticity. The bootloader verifies the image
  signature regardless of transport; authenticate the session if update triggering must be restricted.
- **Versioned protocol**: a version byte in START so host tools and devices can evolve.

## Test matrix
Dropped frames, duplicated frames, reordered frames, corrupted bytes, sender restart mid-transfer,
receiver reset mid-transfer, power loss during flash write, wrong image (digest/signature fails).
Fuzz the frame parser.

## Verify
- [ ] Automated test with an impairment layer (random drop/corrupt 5%) completes 100 transfers with correct digests.
- [ ] Resume after receiver reset continues from the persisted offset.
