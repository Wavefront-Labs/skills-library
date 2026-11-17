---
id: computing-software.firmware-embedded-development.stm32.hal-i2c-memory-read-write
name: hal-i2c-memory-read-write
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-hal-uart, hal-i2c-mem-read, hal-i2c-mem-write, devaddress-shift, memaddsize, eeprom-page-write, hal-i2c-isdeviceready, i2c-timing-register, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use STM32 HAL I2C memory APIs correctly: shifted 7-bit addresses, register address size, EEPROM page boundaries and write cycle polling, timing register setup and error recovery."
sources:
  - https://www.st.com/resource/en/user_manual/um1884-description-of-stm32l4l4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4235-i2c-timing-configuration-tool-for-stm32f3xxxx-and-stm32f0xxxx-microcontrollers-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HAL I2C memory read/write

**Goal:** reliable register and EEPROM access over I2C with the STM32 HAL, avoiding the
address and timing mistakes that cause NACKs and corrupt data.

## API
```c
#define SENSOR_ADDR (0x44 << 1)          /* HAL wants the 7-bit address shifted left */
uint8_t buf[6];
HAL_StatusTypeDef st = HAL_I2C_Mem_Read(&hi2c1, SENSOR_ADDR, 0x28 | 0x80 /*auto-inc*/,
                                         I2C_MEMADD_SIZE_8BIT, buf, sizeof buf, 10 /*ms*/);
HAL_I2C_Mem_Write(&hi2c1, EEPROM_ADDR, 0x0100, I2C_MEMADD_SIZE_16BIT, data, 16, 20);
```
`Mem_Read` does: START, address+W, register address (1 or 2 bytes), repeated START,
address+R, data, STOP: the standard combined format for register reads.

## Common mistakes
- **Unshifted address** (`0x44` instead of `0x88`): HAL sends the wrong address, every call
  returns `HAL_ERROR` with `HAL_I2C_ERROR_AF` (ack failure). `HAL_I2C_IsDeviceReady(&hi2c1,
  addr, 3, 10)` in a scan loop over `addr = i << 1` quickly finds the real address.
- **Wrong `MemAddSize`**: 24C32+ EEPROMs need 16-bit addresses; smaller ones 8-bit (with upper
  address bits in the device address).
- **EEPROM page boundaries**: a write that crosses a page (e.g. 32 bytes on 24C32) wraps to the
  start of the page and overwrites data. Split writes at page boundaries.
- **EEPROM write cycle**: after each page write the chip NACKs for up to 5 ms (tWR). Poll with
  `HAL_I2C_IsDeviceReady(&hi2c1, addr, 10, 10)` before the next access instead of a fixed
  delay.
- **Timeout too short** for the bus speed and length: 100 kHz x 64 bytes ~ 6 ms.

## Timing register (F0/F3/F7/G0/G4/L4/H7 "I2Cv2")
`hi2c.Init.Timing` is a packed PRESC/SCLDEL/SDADEL/SCLH/SCLL value that depends on I2C kernel
clock, speed, rise/fall times. Don't hand-compute: use CubeMX or the I2C timing tool (AN4235).
Changing the I2C clock source without recalculating = wrong bus speed or protocol violations.

## Error recovery
On `HAL_ERROR`/`HAL_BUSY` with `BUSY` flag stuck (slave holding SDA low after a reset mid-
transfer): de-init, clock out 9 SCL pulses as GPIO, generate STOP, re-init
(`HAL_I2C_DeInit`/`HAL_I2C_Init`). Without this, the bus stays dead until power cycle.

## Verify
- [ ] Logic analyser decode shows correct address, register, repeated start.
- [ ] EEPROM test writing across page boundaries reads back correctly.
- [ ] Bus recovery path tested by resetting the MCU mid-transfer.

## Checked

2026-10-31: Confirmed `HAL_I2C_Mem_Read`/`Mem_Write` signatures, `I2C_MEMADD_SIZE_8BIT`/`16BIT`, `HAL_I2C_IsDeviceReady`, the `HAL_ERROR`/`HAL_BUSY`/`HAL_OK` status values, `HAL_I2C_ERROR_AF` and the packed `Timing` field of `I2C_InitTypeDef` against STMicroelectronics HAL/LL driver and CMSIS device headers on GitHub (stm32l4xx/stm32f4xx/stm32g4xx/stm32u5xx hal_driver, cmsis-device-l4/f4/g4/h7/f1), the ST PDFs fetched this batch (AN2867, AN4759, AN4621, AN2834, AN4031, AN4435, UM1724, STM32L476RG / STM32F407VG / STM32F103C8 datasheets) and the Mbed-TLS v2.28.9 headers (stm32l4xx_hal_i2c.h/_ex.h, stm32l4xx_hal_def.h, stm32l4xx_ll_i2c.h; AN4235 is the cited timing tool note). The EEPROM page/tWR examples describe external EEPROM chips and stay as hedged external-device guidance.

Method: documentation only; no commands were run.
