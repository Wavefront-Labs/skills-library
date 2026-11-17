---
id: computing-software.firmware-embedded-development.device-driver-development.can-bit-timing-and-sample-point
name: can-bit-timing-and-sample-point
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [can-bus, can-bit-timing, sample-point, time-quanta, prescaler, tseg1, tseg2, sjw, bxcan, fdcan, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Calculate CAN bit timing registers (prescaler, TSEG1, TSEG2, SJW) for a bitrate and sample point that interoperate on a real bus, and diagnose timing mismatches."
sources:
  - https://docs.kernel.org/networking/can.html
  - https://github.com/STMicroelectronics/stm32f4xx_hal_driver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CAN bit timing and sample point

**Goal:** register values that give the exact bitrate and a sample point every node agrees
on. Wrong sample points work on a 1 m bench bus and fail at 40 m with more nodes.

## The bit (ISO 11898-1)
A bit = `SYNC_SEG (1 tq) + PROP_SEG + PHASE_SEG1 + PHASE_SEG2`, in time quanta (tq).
Most controllers merge PROP+PHASE1 into **TSEG1**.
```
tq          = prescaler / f_can_clock
bit time    = (1 + TSEG1 + TSEG2) * tq
sample point = (1 + TSEG1) / (1 + TSEG1 + TSEG2)
```

## Worked example: 500 kbit/s, about 87.5 %, 42 MHz APB1 (STM32F4 bxCAN)
Need `f/(prescaler * N) = 500k` with integer N: 42 MHz / 500 k = 84 = 6 x 14.
Prescaler 6, N = 14 tq: TSEG1 = 11, TSEG2 = 2 gives (1+11)/14 = 85.7 %; 16 tq is not possible
with 84 (bxCAN TSEG1 goes 1..16 and TSEG2 1..8). With prescaler 4, N = 21: TSEG1 = 17, TSEG2 = 3 gives 18/21 = 85.7 %. Pick the
combination closest to the target with the **most tq** (finer resynchronisation). The HAL
writes `Prescaler - 1` into the BTR register and takes SJW and TSEG1/TSEG2 as the constants `CAN_SJW_1TQ..4TQ`,
`CAN_BS1_1TQ..16TQ` and `CAN_BS2_1TQ..8TQ`.

## Choosing the sample point
- Take the sample point from the specification of your network (CANopen CiA 301, SAE J1939, or the
  device vendor); those documents are not freely readable, so confirm the value there.
- **Every node must be close to the same sample point**; mixing 75 % and 87.5 % on a long
  bus causes intermittent error frames.

## SJW
Resynchronisation jump width: choose it within the controller's range (Linux prints it, e.g.
`sjw 1..4` for an SJA1000); a larger SJW tolerates more oscillator mismatch. CAN needs a tight
oscillator tolerance, so **don't run CAN from an internal RC oscillator** (HSI): use a crystal (HSE).

## CAN FD
The data phase has its own bit timing (`dbitrate`, `dsample-point`) and, at high data rates, needs
**transmitter delay compensation** (TDC): the secondary sample point is TDCV + TDCO. On Linux, omit
`tdc-mode` and the kernel decides and picks a default TDCO (the recommended method); `tdc-mode auto`
needs `tdco`, `tdc-mode manual` needs `tdco` and `tdcv`.

## Diagnosing
- Controller enters error-passive / bus-off immediately: bitrate wrong; scope one bit width
  (2 us at 500 k).
- Works with one partner but not another: sample point mismatch or oscillator tolerance.
- Use loopback / silent-loopback mode first to validate the controller without the bus.
- Linux: `ip -details link show can0` prints computed tq, prop-seg, phase-seg1/2, sjw and
  sample point, handy to cross-check your numbers.

## Verify
- [ ] Bit width measured on scope equals 1/bitrate within 0.1 %.
- [ ] Sample point documented and matches the network's spec (CiA/J1939).
- [ ] Clock source is a crystal.

## Checked

2026-10-27, Linux kernel documentation (mainline v7.3) and STM32 F4 HAL source (master).
Confirmed in Documentation/networking/can.rst: ip -details link output lists tq, prop-seg, phase-seg1/2, sjw and sample point, per-controller tseg/sjw ranges (sja1000: tseg1 1..16, tseg2 1..8, sjw 1..4), and the TDC rules (SSP = TDCV + TDCO, tdc-mode omitted/off/auto/manual). Confirmed in stm32f4xx_hal_can.h/.c: CAN_SJW_1TQ..4TQ, CAN_BS1_1TQ..16TQ, CAN_BS2_1TQ..8TQ and the Prescaler - 1 write to BTR. The tq/sample-point arithmetic was recomputed. Removed the CiA 301 and J1939 sample-point figures, the oscillator tolerance percentages, the bxCAN BTR bit positions and the DBTP and TDC offset formula because no free source was read.

Method: documentation only; no commands were run.
