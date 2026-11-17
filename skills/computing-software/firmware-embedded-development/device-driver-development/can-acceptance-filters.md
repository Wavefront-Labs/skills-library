---
id: computing-software.firmware-embedded-development.device-driver-development.can-acceptance-filters
name: can-acceptance-filters
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [can-bus, can-acceptance-filter, mask-mode, list-mode, filter-bank, standard-id, extended-id, rx-fifo, hal-can-configfilter, firmware-embedded-development]
level: practitioner
status: gated
description: "Configure CAN hardware acceptance filters (mask vs list mode, 11/29-bit IDs, FIFO assignment) so the CPU only sees the frames it needs."
sources:
  - https://docs.kernel.org/networking/can.html
  - https://github.com/STMicroelectronics/stm32f4xx_hal_driver
  - https://github.com/STMicroelectronics/stm32g4xx_hal_driver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CAN acceptance filters

**Goal:** have the controller drop irrelevant frames in hardware. On a busy bus
software filtering wastes CPU and can overflow RX FIFOs.

## Mask vs list mode
- **Mask mode:** accept if `(rx_id & mask) == (filter_id & mask)` (the same rule SocketCAN and
  can-utils use). One bank covers a range.
- **List (identifier) mode:** accept only exact IDs. The bank scale (`FilterScale`, 16 or 32 bit)
  decides how many IDs one bank holds; see the reference manual.

## bxCAN register layout (32-bit scale)
In the HAL, `FilterIdHigh`/`FilterMaskIdHigh` hold the MSBs and the `Low` fields the LSBs of a 32-bit
bank. Standard ID at bits 31:21, extended ID at bits 31:3, IDE at bit 2, RTR at bit 1
(gated: unconfirmed, source is paywalled or blocked; check the filter register description in the
reference manual):
```c
CAN_FilterTypeDef f = {0};
f.FilterBank = 0;
f.FilterMode = CAN_FILTERMODE_IDMASK;
f.FilterScale = CAN_FILTERSCALE_32BIT;
f.FilterIdHigh   = (0x120 << 5);          // std ID 0x120 into bits 31:21 (high half)
f.FilterMaskIdHigh = (0x7F0 << 5);        // accept 0x120-0x12F
f.FilterMaskIdLow  = (1u << 2) | (1u << 1); // also require IDE=0, RTR=0
f.FilterFIFOAssignment = CAN_RX_FIFO0;
f.FilterActivation = ENABLE;
f.SlaveStartFilterBank = 14;              // dual-CAN parts: banks 14..27 belong to CAN2
HAL_CAN_ConfigFilter(&hcan1, &f);
```
Forgetting to include IDE in the mask lets an extended frame with matching high bits through.

## Design rules
- Classic "TX works, RX never fires" bug: check that a filter bank is configured and activated
  (`FilterActivation = ENABLE`). For bring-up, one mask-mode bank with mask 0 should accept everything
  (mask semantics as above).
- Split traffic over FIFO0/FIFO1 by priority (e.g. NMT/heartbeat to FIFO0, bulk data to
  FIFO1) so a flood of one class can't overflow the other.
- FDCAN (STM32G4) has separate standard and extended filters plus a global filter
  (`HAL_FDCAN_ConfigGlobalFilter` with `NonMatchingStd` and `NonMatchingExt`) deciding what happens to
  non-matching frames: choose the behaviour explicitly.
- On Linux SocketCAN, filters are per socket: `setsockopt(s, SOL_CAN_RAW, CAN_RAW_FILTER,
  &rfilter, sizeof rfilter)` with `can_id`/`can_mask`. The SocketCAN documentation treats controller hardware filters as a
  dedicated embedded tuning measure, not part of the multi-user model.

## Verify
- [ ] Inject frames with `cansend`/a USB-CAN adapter just inside and just outside the range;
      only the expected ones arrive.
- [ ] Extended frames with matching upper bits are rejected when only standard IDs are wanted.
- [ ] No FIFO overrun (`HAL_CAN_ERROR_RX_FOV0`) under worst-case bus load.

## Checked

2026-10-27, Linux kernel (mainline v7.3) and STM32 HAL sources (master).
Confirmed in stm32f4xx_hal_can.h/.c: CAN_FilterTypeDef fields (FilterIdHigh = MSBs for 32-bit, FilterBank 0..27 on dual-CAN parts, SlaveStartFilterBank with lower banks assigned to the master), CAN_FILTERMODE_IDMASK, CAN_RX_FIFO0, HAL_CAN_ConfigFilter, HAL_CAN_ERROR_RX_FOV0. Confirmed in stm32g4xx_hal_fdcan.c: HAL_FDCAN_ConfigGlobalFilter with NonMatchingStd/NonMatchingExt. Confirmed in Documentation/networking/can.rst: can_filter id/mask semantics with CAN_SFF_MASK, per-socket filters and the stance on controller hardware filters. The raw bit positions of the bxCAN filter registers (bits 31:21, 31:3, IDE, RTR) are gated because the reference manual was not read. Removed the frame-rate figure and the list-mode capacity claim.

Method: documentation only; no commands were run.
