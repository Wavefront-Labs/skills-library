---
id: computing-software.firmware-embedded-development.low-power-design.sensor-interrupt-wakeup
name: sensor-interrupt-wakeup
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [sensor-interrupt-wake, wake-on-motion, accelerometer-interrupt, latched-interrupt, sensor-fifo-watermark, int-pin, low-power, firmware-embedded-development]
level: practitioner
status: draft
description: "Let sensors wake the MCU: wake-on-motion thresholds, latched vs pulsed INT, FIFO watermarks, clearing interrupt source registers, and the INT-already-asserted race."
sources:
  - https://www.st.com/resource/en/application_note/an5005-lis2dw12-alwayson-3d-accelerometer-stmicroelectronics.pdf
  - https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bma400-ds000.pdf
  - https://www.st.com/resource/en/datasheet/lis3dh.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sensor interrupt wake-up

Let the sensor watch the world in its own microamp mode and wake the MCU only when something
happens.

## Common sensor features
- **Wake-on-motion / activity:** accelerometers (LIS2DW12, BMA400, LIS3DH) compare high-pass
  filtered acceleration to a threshold for N samples at a low ODR; BMA400 does this at ~1 uA.
- **FIFO watermark:** sensor buffers samples and asserts INT when N are stored; MCU wakes once per
  batch instead of per sample.
- **Data-ready:** one wake per sample; only for low rates.
- **Threshold/window:** temperature/humidity/light sensors with high/low alarms (TMP117 ALERT,
  OPT3001 INT).

## Configuration checklist (LIS3DH-style)
1. Set a low ODR (10-25 Hz) and low-power mode.
2. Enable the high-pass filter for the interrupt path so gravity does not trigger.
3. Threshold (`INT1_THS`, LSB depends on full scale: 16 mg at +/-2 g) and duration (`INT1_DURATION`
   in 1/ODR units) to reject knocks.
4. Route the function to INT1 (`CTRL_REG3`), set OR/AND axis combination (`INT1_CFG`).
5. **Latch** the interrupt (`CTRL_REG5.LIR_INT1`) so the line stays asserted until read; the MCU
   cannot miss a pulse that happened while it was waking.
6. INT polarity and push-pull/open-drain (`CTRL_REG6` / sensor-specific) to match the MCU wake pin.

## MCU side
- Wake pin configured for the sensor's active level (see wake-up pins skill).
- On wake: read the interrupt source register (`INT1_SRC`) to clear the latch and learn the axis;
  failing to read it leaves INT asserted, so the next sleep entry wakes immediately (level wake)
  or never (edge wake missed).
- Before sleeping: read source register, check the INT pin level is inactive, then sleep.
- I2C/SPI bus to the sensor must stay in a non-leaking state during sleep (pull-ups on idle-high
  lines fine; do not drive SCL low).

## Gotchas
- Sensor reset/brownout clears its configuration; the MCU must reconfigure after its own POR and
  detect sensor POR (WHO_AM_I + config readback) after brownouts.
- Threshold set during development on a desk is often too sensitive in a vehicle or too dull on a
  wrist; make it a configurable parameter.
- Sensor FIFO overrun when the MCU wakes late: use stream mode and check overrun flag.

## Verify
- [ ] Shake test wakes reliably; resting device does not wake over 24 h.
- [ ] Interrupt latch cleared on each wake (INT pin returns inactive).
