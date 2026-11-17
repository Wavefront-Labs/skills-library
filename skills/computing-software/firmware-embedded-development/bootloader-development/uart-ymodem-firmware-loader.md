---
id: computing-software.firmware-embedded-development.bootloader-development.uart-ymodem-firmware-loader
name: uart-ymodem-firmware-loader
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [firmware-transport, ymodem, xmodem, uart-bootloader, crc16-ccitt, block-retransmit, teraterm-ymodem, firmware-embedded-development]
level: practitioner
status: draft
description: "Implement a UART firmware loader using YMODEM: block format, CRC-16, ACK/NAK flow, writing to flash as blocks arrive and validating the image before boot."
sources:
  - http://wiki.synchro.net/ref:ymodem
  - https://www.st.com/resource/en/application_note/an4657-stm32-inapplication-programming-iap-using-the-usart-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UART YMODEM firmware loader

**Goal:** a bootloader that accepts a firmware file from any terminal program (Tera Term,
ExtraPuTTY, `sb`/`lrzsz`) over a serial port, with error recovery.

## Protocol summary
- Receiver starts by sending `'C'` (request CRC mode) every ~1 s until the sender starts.
- Block 0: `SOH 00 FF` + filename `\0` + size in ASCII + padding (128 bytes) + CRC16.
- Data blocks: `SOH` (128 B) or `STX` (1024 B), block number, its complement, payload,
  CRC-16/CCITT (big-endian, poly 0x1021, init 0).
- Receiver replies `ACK` (0x06) or `NAK` (0x15); sender retransmits on NAK/timeout.
- End: `EOT`, receiver NAKs the first, ACKs the second, then sends `'C'`; sender sends an empty
  block 0 to end the batch.
- `CAN CAN` (0x18 0x18) aborts.
Last block is padded with 0x1A; use the file size from block 0 to know the real length.

## Receiver state machine essentials
```c
switch (hdr) {
case SOH: len = 128; break;
case STX: len = 1024; break;
case EOT: /* handle end */ break;
case CAN: /* abort */ break;
default:  flush_rx(); send(NAK); continue;
}
if (blk != (uint8_t)~blk_inv || crc16(data, len) != rx_crc) { send(NAK); continue; }
if (blk == (uint8_t)(expected - 1)) { send(ACK); continue; }   /* duplicate: ACK, don't rewrite */
if (blk != expected) { cancel(); }
flash_write(addr, data, len); addr += len; expected++; send(ACK);
```
The **duplicate block** case is critical: when an ACK is lost, the sender resends the previous
block, which must be acknowledged without writing it twice.

## Flash handling
- Erase the target slot up front (or sector-by-sector ahead of the write pointer) so erase time
  doesn't exceed the sender's ACK timeout (~10 s total, often 1 s per block). Long erases:
  erase before sending `'C'`.
- Write to a **staging slot**, not over the running image; only mark it bootable after the
  whole file arrives and its CRC/signature verifies.
- Reject files larger than the slot using the size in block 0 before erasing anything.

## Gotchas
- UART RX must not lose bytes during flash writes: on many MCUs the CPU stalls on flash
  programming; use DMA for RX or write from RAM-executed code; at 115200 baud a 1029-byte block
  takes ~90 ms.
- Terminal programs differ in timeouts; test with at least two.
- Expose the loader via a magic-word request from the app or a boot pin, plus a timeout that
  boots the app if nothing arrives.

## Verify
- [ ] Transfer with injected line noise (a few corrupted bytes) still completes via NAK retry.
- [ ] Cancelled transfer leaves the old image bootable.
- [ ] File of exactly N x 1024 bytes and one with a partial last block both verify.
