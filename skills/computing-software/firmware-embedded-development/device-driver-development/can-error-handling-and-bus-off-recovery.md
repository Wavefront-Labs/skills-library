---
id: computing-software.firmware-embedded-development.device-driver-development.can-error-handling-and-bus-off-recovery
name: can-error-handling-and-bus-off-recovery
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [can-bus, can-bus-off, tec, rec, error-passive, error-warning, abom, automatic-bus-off-management, ack-error, termination, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Handle CAN error states (active, passive, bus-off) correctly: read TEC/REC, recover from bus-off per ISO 11898, and find the wiring cause of error frames."
sources:
  - https://docs.kernel.org/networking/can.html
  - https://github.com/torvalds/linux/blob/master/include/uapi/linux/can/error.h
  - https://github.com/STMicroelectronics/stm32f4xx_hal_driver
  - https://github.com/STMicroelectronics/stm32g4xx_hal_driver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CAN error handling and bus-off recovery

**Goal:** a node that degrades gracefully on bus faults and rejoins the bus automatically,
without hammering a broken bus with retransmissions.

## Fault confinement states (ISO 11898-1)
| State | Condition | Behaviour |
|---|---|---|
| Error active | TEC and REC < 128 | sends active error flags |
| Error warning | either >= 96 | flag only, still active |
| Error passive | TEC or REC >= 128 | sends passive error flags |
| Bus-off | TEC > 255 (Linux: threshold 256) | node disconnects from the bus |
The thresholds 96, 128 and 256 are the ones Linux uses (`CAN_ERROR_WARNING_THRESHOLD`,
`CAN_ERROR_PASSIVE_THRESHOLD`, `CAN_BUS_OFF_THRESHOLD`). How a controller rejoins after bus-off is
defined by ISO 11898-1 and its reference manual; read the recovery rules there.

## Recovery policy
- bxCAN `AutoBusOff = ENABLE` (HAL `CAN_InitTypeDef`, automatic bus-off management) lets the
  hardware rejoin the bus. Without it, software must restart the controller.
- Do not rejoin instantly in a loop: a node with a wiring fault oscillates between bus-off
  and transmit, disturbing the bus. Prefer: on bus-off interrupt, log it, wait an increasing
  back-off (100 ms, 1 s, ...), then request recovery.
- Linux SocketCAN: `ip link set can0 type can restart-ms 100` for automatic restart, or
  `ip link set can0 type can restart` manually; watch `ip -s -d link show can0` for
  the `re-started` and `bus-off` counters. Error frames carry `CAN_ERR_BUSOFF` and `CAN_ERR_RESTARTED`.
- Pending TX mailboxes may be aborted on bus-off, depending on the controller; re-queue or drop
  according to message freshness (stale control setpoints should be dropped).

## Reading the cause
- **ACK error with a lone node** is normal: CAN needs at least one other node to ACK. A
  single node on the bench goes error-passive. Use loopback mode or add a second node.
- **Stuff/form/bit errors on every frame:** bitrate or sample point mismatch.
- **Errors increasing with cable length or node count:** termination. Measure CAN_H to CAN_L
  with power off: **60 ohm** = two 120 ohm terminators correct; 120 ohm = one missing;
  40 ohm = an extra one.
- **Errors only when a motor runs:** common-mode noise; check transceiver ground reference,
  use split termination (two resistors with a capacitor from the centre tap to ground; take the values from the transceiver datasheet).
- Read `ESR` (bxCAN: LEC last error code, TEC, REC; HAL flags `HAL_CAN_ERROR_EWG`, `_EPV`, `_BOF`) or FDCAN
  `ECR`/`PSR` (`FDCAN_PSR_LEC`, `FDCAN_ECR_TEC`) in the error
  interrupt and log them; counters tell you which side (TX or RX) is failing.

## Verify
- [ ] Short CAN_H to CAN_L briefly: node goes bus-off, then rejoins on its own after removal.
- [ ] Bus-off events are logged with TEC/REC and LEC.
- [ ] Termination measured at 60 ohm.

## Checked

2026-10-27, Linux kernel (mainline v7.3) and STM32 HAL sources (master).
Confirmed in include/uapi/linux/can/error.h: CAN_ERROR_WARNING_THRESHOLD 96, CAN_ERROR_PASSIVE_THRESHOLD 128, CAN_BUS_OFF_THRESHOLD 256, CAN_ERR_BUSOFF and CAN_ERR_RESTARTED. Confirmed in Documentation/networking/can.rst: restart-ms and manual restart, the re-started and bus-off statistics, ERROR-ACTIVE/PASSIVE/BUS-OFF states. Confirmed in the STM32F4 and G4 HAL: AutoBusOff, HAL_CAN_ERROR_BOF/EWG/EPV, CAN_ESR_BOFF, FDCAN_PSR_LEC, FDCAN_ECR_TEC. The termination figures (60, 120 and 40 ohm) are parallel-resistor arithmetic. Removed the TEC +8/-1 rule, the 128 x 11 recessive-bit recovery rule, the extra 8-bit wait and the 4.7 nF value because the ISO standard and reference manuals were not read.

Method: documentation only; no commands were run.
