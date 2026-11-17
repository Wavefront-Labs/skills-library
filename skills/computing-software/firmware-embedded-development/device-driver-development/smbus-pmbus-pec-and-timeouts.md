---
id: computing-software.firmware-embedded-development.device-driver-development.smbus-pmbus-pec-and-timeouts
name: smbus-pmbus-pec-and-timeouts
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [smbus-pec, i2c, smbus, pmbus, crc-8, bus-timeout, firmware-embedded-development]
level: advanced
status: gated
description: "Talk to SMBus/PMBus devices (battery gauges, PMICs, power supplies): transaction types, CRC-8 PEC, 25-35 ms timeout, ALERT#, and PMBus LINEAR11/16 number formats."
sources:
  - https://github.com/torvalds/linux/blob/master/Documentation/i2c/smbus-protocol.rst
  - https://github.com/torvalds/linux/blob/master/drivers/i2c/i2c-core-smbus.c
  - https://github.com/torvalds/linux/blob/master/drivers/hwmon/pmbus/pmbus_core.c
  - https://github.com/torvalds/linux/blob/master/drivers/power/supply/sbs-battery.c
  - https://smbus.org/specs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SMBus and PMBus (PEC and timeouts)

SMBus is I2C with stricter rules: defined transaction types, a timeout, optional packet error
checking (PEC), and an alert line. PMBus adds a command set for power conversion on top.

## Differences from plain I2C
The clock, timeout and voltage-level figures in this table come from the SMBus specification (gated: unconfirmed, source is paywalled or blocked); the transaction list and the alert protocol are confirmed in the Linux SMBus documentation.
| Item | SMBus |
|---|---|
| Clock | 10 kHz min (devices may reset if the clock stops), 100 kHz / 400 kHz / 1 MHz classes |
| Timeout | a device holding SCL low > 25 ms (tTIMEOUT) must be considered failed; devices reset their interface at 25-35 ms |
| Levels | fixed thresholds (VIL 0.8 V, VIH 1.35 V for 3.3 V class) vs I2C's VDD-relative |
| Transactions | Quick, Send/Receive Byte, Write/Read Byte/Word, Block Write/Read (count byte first), Process Call |
| ALERT# | open-drain interrupt; host reads the Alert Response Address (0x0C (gated: unconfirmed, source is paywalled or blocked)) to find the source |

## PEC (CRC-8)
Polynomial x^8 + x^2 + x + 1 (0x07), init 0, no reflection, computed over **every byte including
address bytes** (with R/W bit) of the transaction:
```c
uint8_t smbus_crc8(uint8_t crc, const uint8_t *p, size_t n) {
    while (n--) { crc ^= *p++; for (int i = 0; i < 8; i++) crc = (crc & 0x80) ? (uint8_t)((crc << 1) ^ 0x07) : (uint8_t)(crc << 1); }
    return crc;
}
/* Read Word with PEC from device 0x0B, command 0x09 (Voltage) */
uint8_t frame[] = { 0x0B << 1, 0x09, (0x0B << 1) | 1, lo, hi };
bool ok = smbus_crc8(0, frame, sizeof frame) == pec_received;
```
STM32 I2C v2 has hardware PEC (`CR1.PECEN`, `CR2.PECBYTE`).
Linux: `ioctl(fd, I2C_PEC, 1)` on an i2c-dev file, or `client->flags |= I2C_CLIENT_PEC` in a driver; the kernel computes it with `i2c_smbus_pec()`.

## Timeouts in firmware
Implement both: the controller aborts any transaction exceeding the SMBus timeout (about 25 ms (gated: unconfirmed, source is paywalled or blocked)), and a
bus-recovery routine (clock out up to 9 pulses, then STOP) runs after a timeout. STM32 I2C v2 has a `TIMEOUTR`
register (`TIMOUTEN`, `TEXTEN`) and an `ISR.TIMEOUT` flag for hardware timeout detection.

## PMBus numeric formats
- **LINEAR11** (most READ_ commands): 16-bit word, upper 5 bits signed exponent N, lower 11 bits
  signed mantissa Y. `value = Y * 2^N`.
```c
float lin11(uint16_t w) { int16_t y = (int16_t)(w << 5) >> 5; int8_t n = (int8_t)((int16_t)w >> 11); return ldexpf(y, n); }
```
- **LINEAR16** (VOUT): unsigned mantissa, exponent from `VOUT_MODE` (command 0x20) low 5 bits.
- **DIRECT**: `value = (Y * 10^-R - b) / m` with coefficients from `COEFFICIENTS` or the datasheet.

## Smart batteries (SBS)
Gauges at address 0x0B (gated: unconfirmed, source is paywalled or blocked): `Temperature()` 0x08, `Voltage()` 0x09, `Current()` 0x0A (signed), `RelativeStateOfCharge()`
0x0D (percent). The register numbers match the Linux `sbs-battery` driver; units are defined by the Smart Battery
specification (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] PEC matches the device on read and a deliberately wrong PEC on write is NACKed/flagged.
- [ ] Unplugging the device mid-transaction recovers within the timeout without hanging.
- [ ] LINEAR11 decode of `READ_VIN` matches a multimeter.

## Checked

2026-10-27, Linux kernel (mainline v7.3) and STM32L4 CMSIS header (master).
Confirmed in drivers/i2c/i2c-core-smbus.c: PEC polynomial 0x107 (x^8 + x^2 + x + 1) processed MSB first from an initial value of 0 by i2c_smbus_pec(), and i2c_smbus_msg_pec() includes the address byte (with the R/W bit) first. Confirmed in Documentation/i2c/smbus-protocol.rst: Block transactions and the SMBus alert protocol. Confirmed in dev-interface.rst: I2C_PEC ioctl; i2c.h: I2C_CLIENT_PEC. Confirmed in drivers/hwmon/pmbus/pmbus_core.c: LINEAR11 decode (exponent = signed top 5 bits, mantissa = signed low 11 bits), LINEAR16 (exponent = signed low 5 bits of VOUT_MODE, mode in the top 3 bits), DIRECT (X = 1/m * (Y * 10^-R - b)), and in pmbus.h: VOUT_MODE 0x20, COEFFICIENTS 0x30, READ_VIN 0x88. Confirmed in sbs-battery.c: register numbers 0x08, 0x09, 0x0A, 0x0D. Confirmed in stm32l476xx.h: PECEN, PECBYTE, TIMEOUTR, TIMEOUT flag. The clock, timeout, voltage-level and Alert Response Address figures, the gauge address and Smart Battery units are marked gated because the SMBus and Smart Battery specifications could not be read. Removed the claim that many gauges require PEC once sealed and the tLOW:SEXT remark.

Method: documentation only; no commands were run.
