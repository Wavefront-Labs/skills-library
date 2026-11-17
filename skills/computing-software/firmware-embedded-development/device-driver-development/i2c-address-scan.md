---
id: computing-software.firmware-embedded-development.device-driver-development.i2c-address-scan
name: i2c-address-scan
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [i2c-address-scan, i2c, 10-bit-addressing, reserved-addresses, i2cdetect, firmware-embedded-development]
level: practitioner
status: gated
description: "Scan an I2C bus safely from firmware or Linux (i2cdetect), skip reserved addresses, handle 7-bit vs 8-bit address confusion and 10-bit addressing, and read the results."
sources:
  - https://manpages.debian.org/bookworm/i2c-tools/i2cdetect.8.en.html
  - https://github.com/STMicroelectronics/stm32l4xx_hal_driver
  - https://docs.kernel.org/i2c/dev-interface.html
  - https://www.nxp.com/docs/en/user-guide/UM10204.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bus scanning and 10-bit addressing

## Firmware scan (STM32 HAL)
```c
void i2c_scan(I2C_HandleTypeDef *h) {
    for (uint16_t a = 0x08; a <= 0x77; a++) {               /* skip reserved 0x00-0x07, 0x78-0x7F */
        if (HAL_I2C_IsDeviceReady(h, (uint16_t)(a << 1), 2, 5) == HAL_OK)
            printf("found 0x%02X\r\n", a);
    }
}
```
HAL takes the address **shifted left by one** (8-bit form). Passing `0x68` instead of `0x68 << 1`
scans the wrong address: the most common "device not found" bug. Datasheets mix forms: "0xD0
write / 0xD1 read" is 7-bit 0x68.

`IsDeviceReady` sends the address with write bit and checks for ACK, then a STOP. Some devices
misbehave on a bare address-write (a few EEPROMs start a write cycle, some sensors lock up):
`i2cdetect` documents that its default probe uses whichever SMBus command it believes safest for each
address, and that its `-r` (receive byte) and `-q` (quick write) probes are not recommended because they can
lock write-only chips or corrupt some EEPROMs.

## Linux
```sh
i2cdetect -l                 # list buses
i2cdetect -y 1               # scan bus 1; UU = address in use by a kernel driver
i2cdetect -y -r 1            # receive-byte probe (not recommended, see above)
i2cdetect -F 1               # show the adapter's supported functionality
```

## Reserved addresses (7-bit)
The table follows the I2C-bus specification UM10204 (gated: unconfirmed, source is paywalled or blocked).
| Range | Use |
|---|---|
| 0x00 | general call / START byte |
| 0x01 | CBUS |
| 0x02 | different bus format |
| 0x03 | future |
| 0x04-0x07 | Hs-mode controller code |
| 0x78-0x7B | 10-bit address prefix (11110xx) |
| 0x7C-0x7F | device ID / future |

## 10-bit addressing
First byte `11110 A9 A8 R/W`, second byte A7..A0 (gated: unconfirmed, source is paywalled or blocked). Rare in practice; the MCU peripheral must be
configured for it (`I2C_ADDRESSINGMODE_10BIT` for the target side; for controller transfers set
`CR2.ADD10` on STM32 I2C v2). Linux: the adapter must support `I2C_FUNC_10BIT_ADDR`; i2c-dev needs the `I2C_TENBIT` ioctl.

## Reading scan results
- Nothing found: check pull-ups, power to the device, SDA/SCL swapped, bus stuck low (scope first).
- Every address ACKs: SDA stuck low or missing pull-up (the controller reads low as ACK).
- Unexpected extra address: device with configurable address pins floating, or a device that
  answers at two addresses (some PMICs, EEPROMs with multiple blocks).

## Verify
- [ ] Scan output matches the schematic's address list.
- [ ] Scan never hangs: every transaction has a timeout and the bus recovers if a device holds SDA.

## Checked

2026-10-27, i2c-tools i2cdetect manual page (Debian bookworm), STM32L4 HAL and CMSIS header (master), Linux Documentation/i2c/dev-interface.rst (v7.3).
Confirmed in the i2cdetect page: -l, -y, -r (receive byte, not recommended), -q, -F, UU meaning a driver is using the address, default range 0x08 to 0x77. Confirmed in the STM32L4 HAL: HAL_I2C_IsDeviceReady and the note that the 7-bit datasheet address must be shifted left, I2C_ADDRESSINGMODE_10BIT, I2C_CR2_ADD10. Confirmed in dev-interface.rst: I2C_TENBIT and I2C_FUNC_10BIT_ADDR. The reserved-address table and the 10-bit first-byte format are marked gated because UM10204 could not be read as text. Corrected the claim that i2cdetect uses a quick read on 0x30-0x37 and 0x50-0x5F by default (not in the manual; -r is receive byte). Removed the I2C_M_TEN flag and the 24C16 address example.

Method: documentation only; no commands were run.
