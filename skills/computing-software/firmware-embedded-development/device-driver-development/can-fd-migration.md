---
id: computing-software.firmware-embedded-development.device-driver-development.can-fd-migration
name: can-fd-migration
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [can-bus, can-fd, brs, bit-rate-switch, dlc, fdcan, message-ram, transmitter-delay-compensation, iso-can-fd, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Move a classic CAN design to CAN FD: data-phase timing, BRS, DLC to length mapping, FDCAN message RAM, transceiver choice and mixed-network pitfalls."
sources:
  - https://docs.kernel.org/networking/can.html
  - https://github.com/torvalds/linux/blob/master/drivers/net/can/dev/length.c
  - https://github.com/STMicroelectronics/stm32g4xx_hal_driver
  - https://github.com/linux-can/can-utils
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CAN FD migration

**Goal:** use CAN FD's up to 64-byte payloads and faster data phase without breaking the
bus or misreading frame lengths.

## What changes
- **Two bitrates:** arbitration phase (e.g. 500 kbit/s, same rules as classic CAN) and data
  phase (e.g. 2 or 5 Mbit/s) when the **BRS** bit is set. Configure both: on STM32 FDCAN,
  `NominalPrescaler/NominalTimeSeg1/2` and `DataPrescaler/DataTimeSeg1/2`.
- **DLC is not the byte count above 8:** DLC 9..15 map to 12, 16, 20, 24, 32, 48, 64 bytes.
  Pad payloads to the next valid size; never send DLC 9 expecting 9 bytes.
- **ISO vs non-ISO CAN FD:** the ISO 11898-1:2015 variant is the Linux default; the 2012 whitepaper
  variant is non-ISO (some controllers are fixed non-ISO, some switch with `fd-non-iso`). Use one
  variant on the whole bus.

## Hardware
- The transceiver must be rated for your data rate (check its datasheet for CAN FD support).
- Topology matters more: long stubs and star wiring ring at high data rates. Keep stubs short and
  terminate correctly.
- Use **transmitter delay compensation** at high data rates (STM32 FDCAN
  `HAL_FDCAN_ConfigTxDelayCompensation` + `HAL_FDCAN_EnableTxDelayCompensation`; Linux: omit
  `tdc-mode` to let the kernel choose, or set `tdc-mode auto` with `tdco`).

## FDCAN message RAM (STM32G4)
Filters, RX FIFOs and TX buffers share a message RAM. In the G4 HAL the layout is fixed by the
`SRAMCAN_*` constants, per FDCAN instance. Other MCAN-based parts let you size the sections and
element size yourself; check the part's reference manual.

## Mixed networks
A classic CAN 2.0 controller does not understand FD frames; every node on a bus carrying FD
frames must be FD-capable or FD-tolerant (check each controller's datasheet). Common migration:
keep legacy nodes on a separate segment.

## Linux
```
ip link set can0 type can bitrate 500000 sample-point 0.8 dbitrate 2000000 dsample-point 0.75 fd on
candump -x can0        # shows BRS/ESI flags
cansend can0 123##1AABBCCDD   # '##' marks an FD frame, next nibble = flags (1 = BRS)
```

## Verify
- [ ] Logic analyser / scope shows the faster data phase inside frames with BRS.
- [ ] Frames with 12, 20, 64 byte payloads round-trip with correct length.
- [ ] No error frames under load with all real nodes connected.

## Checked

2026-10-27, Linux kernel (mainline v7.3), can-utils and STM32G4 HAL (master).
Confirmed in drivers/net/can/dev/length.c: DLC 9..15 map to 12, 16, 20, 24, 32, 48, 64 bytes. Confirmed in Documentation/networking/can.rst: dbitrate/dsample-point/fd on, up to 64 payload bytes, ISO (default) versus non-ISO variants and fd-non-iso, and the tdc-mode rules. Confirmed in can-utils: candump -x prints rx/tx brs esi, and cansend ## frames with a flags nibble where 1 is BRS. Confirmed in stm32g4xx_hal_fdcan.c: the TDC functions and the fixed SRAMCAN_* message RAM layout. Removed the ISO stuff-bit-counter detail, the remote-frame statement, the named transceivers, the 1 Mbit/s TDC threshold, the H7 2560 word figure and the truncation claim because no source was read.

Method: documentation only; no commands were run.
