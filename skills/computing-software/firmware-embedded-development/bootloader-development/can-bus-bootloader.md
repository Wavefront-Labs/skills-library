---
id: computing-software.firmware-embedded-development.bootloader-development.can-bus-bootloader
name: can-bus-bootloader
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [firmware-transport, can-bootloader, uds-flashing, iso-14229, request-download, transfer-data, node-addressing, openblt, firmware-embedded-development]
level: advanced
status: draft
description: "Design a CAN bootloader for multi-node systems: node addressing, UDS-style RequestDownload/TransferData sequence, ISO-TP framing, and safe behaviour on a live bus."
sources:
  - https://www.iso.org/standard/72439.html
  - https://www.feaser.com/openblt/doku.php
  - https://www.st.com/resource/en/application_note/an3154-can-protocol-used-in-the-stm32-bootloader-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CAN bus bootloader

**Goal:** reflash one node among many on a shared CAN bus (vehicle, robot, industrial
machine) from a service tool, without disturbing the rest of the network.

## Protocol options
- **UDS (ISO 14229) over ISO-TP**: automotive standard. Sequence:
  `DiagnosticSessionControl (0x10 02 programming)` -> `SecurityAccess (0x27 seed/key)` ->
  `RoutineControl (0x31 erase memory)` -> `RequestDownload (0x34 addr, size)` ->
  `TransferData (0x36, block sequence counter)` x N -> `RequestTransferExit (0x37)` ->
  `RoutineControl (check dependencies / CRC)` -> `ECUReset (0x11)`.
- **CANopen** (CiA 302 program download via SDO to object 0x1F50).
- Open-source: OpenBLT (XCP-based, many MCUs), or the STM32 ROM CAN bootloader (AN3154) where
  available (limited: fixed IDs and bitrate).

## Design points
- **Addressing:** every node needs a unique request/response ID pair (e.g. 0x700 + node, 0x780 +
  node); node ID from DIP switches, EEPROM or a production step. Two nodes with the same ID in
  bootloader mode both answer and corrupt each other's transfers.
- **Bitrate:** bootloader must use the network's bitrate and sample point (don't assume 500 k
  if the machine runs 250 k).
- **Entering the bootloader:** app receives a "go to programming session" request, sets a magic
  word in no-init RAM and resets; bootloader also stays active for N ms after power-up for
  recovery of a broken app.
- **Bus etiquette:** while one node is flashed, others keep running; the tool should put the
  rest of the network in a quiet mode (UDS `CommunicationControl 0x28`) to free bandwidth and
  avoid timing issues.
- **Throughput:** ISO-TP with 8-byte classic CAN at 500 kbit/s achieves ~20-30 KB/s at best;
  CAN FD with 64-byte frames 5-10x more. Use BS=0 and minimal STmin if the receiver can keep up
  with flash writes (buffer a sector in RAM).
- **Integrity:** CRC or signature over the whole image checked before marking valid; block
  sequence counter (wraps 0xFF -> 0x00) detects lost/duplicate TransferData.
- **SecurityAccess** seed/key prevents casual reprogramming; combine with signed images for
  real security.

## Verify
- [ ] Flash one node while others run: no error frames or timeouts on other nodes' traffic.
- [ ] Power loss mid-transfer: node comes up in bootloader and accepts a retry.
- [ ] Two nodes accidentally given the same ID are detected (tool checks for duplicate responses).
