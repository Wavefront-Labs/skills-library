---
id: computing-software.firmware-embedded-development.device-driver-development.diagnosing-can-error-frames
name: diagnosing-can-error-frames
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [can-error-frame, can-bus, lec, bit-error, stuff-error, ack-error, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Diagnose CAN error frames by type (bit, stuff, form, ACK, CRC) using the last error code, scope captures and counters, and map each to its usual cause."
sources:
  - https://github.com/torvalds/linux/blob/master/include/uapi/linux/can/error.h
  - https://docs.kernel.org/networking/can.html
  - https://github.com/STMicroelectronics/stm32g4xx_hal_driver
  - https://github.com/linux-can/can-utils
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing error frames

When a node detects an error it transmits an error flag,
destroying the frame; the transmitter retries. Each controller records the **last error code
(LEC)**: read it (STM32 bxCAN `ESR.LEC`, FDCAN `PSR.LEC`/`DLEC`, Linux `candump -e` error class; `CAN_ERR_BUSERROR` can flood, so filter it)
before guessing.

## Error types and usual causes
| Error | Detected by | Most likely cause |
|---|---|---|
| **ACK error** | transmitter: no dominant bit in ACK slot (`CAN_ERR_ACK`, location `CAN_ERR_PROT_LOC_ACK`) | no other node on the bus, others at a different bit rate, others in silent/listen-only or bus-off, broken CANH/CANL |
| **Bit error** | transmitter: read back differs from sent (`CAN_ERR_PROT_BIT`, `_BIT0`, `_BIT1`) | transceiver problem, short to supply, two nodes with the same ID sending different data, reflections |
| **Stuff error** | receiver: bit-stuffing rule violated (`CAN_ERR_PROT_STUFF`) | bit rate mismatch, wrong sample point, noise, missing termination |
| **Form error** | fixed-format field of the frame wrong (`CAN_ERR_PROT_FORM`) | bit timing/clock tolerance, reflections, oscillator drift |
| **CRC error** | receiver: CRC mismatch | noise, EMC, marginal timing at high bit rates (CAN FD data phase) |

## Workflow
1. **Counters**: TEC and REC. TEC rising only on one node = that node's TX path or nobody ACKing.
   REC rising on all nodes = shared physical problem or a foreign node at the wrong rate.
2. **LEC** per error to classify (table above).
3. **Scope with CAN decode** (or differential probe on CANH-CANL): check bit time, look at where
   in the frame the error flag starts, ringing on edges, recessive level not returning to ~0 V.
4. **Termination** (60 Ohm with power off), stub lengths, ground offset between nodes (the common-mode
   range of transceivers is limited; see the datasheet).
5. **Clock**: nodes using RC oscillators (HSI) instead of crystals exceed CAN's oscillator
   tolerance. Use HSE/crystal for CAN.
6. **Bit timing**: sample points should match across nodes (use the value your network specification gives); different
   tq/prescaler choices at the "same bit rate" can still disagree on sample point.

## Error state reminder
REC or TEC >= 128: error passive (Linux `CAN_ERROR_PASSIVE_THRESHOLD`); >= 96 is the warning level.
TEC >= 256 is bus-off (`CAN_BUS_OFF_THRESHOLD`); the controller stops transmitting until it recovers
(automatically or by software restart, see the controller's manual).

## Verify
- [ ] Error counters stay at 0 for an hour under full bus load after the fix.
- [ ] Scope shows clean edges and correct bit time; all nodes' sample points documented.

## Checked

2026-10-27, Linux kernel (mainline v7.3), can-utils and STM32G4 HAL (master).
Confirmed in include/uapi/linux/can/error.h: CAN_ERR_PROT_BIT/FORM/STUFF/BIT0/BIT1, CAN_ERR_ACK, CAN_ERR_PROT_LOC_ACK, CAN_ERR_BUSERROR (may flood), and the 96/128/256 state thresholds. Confirmed in can-utils candump: -e shows error frames. Confirmed in stm32g4xx_hal_fdcan.c: FDCAN_PSR_LEC, FDCAN_PSR_DLEC and the ECR error counters. Removed the 6-dominant-bit error flag, the 6-equal-bits stuffing description, the CRC/ACK delimiter and EOF list, the common-mode voltage range, the oscillator tolerance percentage, the CiA 87.5 percent figure and the 128 x 11 recovery rule because ISO and CiA documents and transceiver datasheets were not read.

Method: documentation only; no commands were run.
