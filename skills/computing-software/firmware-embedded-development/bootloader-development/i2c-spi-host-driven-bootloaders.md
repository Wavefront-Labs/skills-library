---
id: computing-software.firmware-embedded-development.bootloader-development.i2c-spi-host-driven-bootloaders
name: i2c-spi-host-driven-bootloaders
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [i2c-bootloader, firmware-transport, stm32-i2c-bootloader, coprocessor-update, an4221, firmware-embedded-development]
level: advanced
status: draft
description: "Update a secondary MCU from a host processor over I2C or SPI: STM32 ROM I2C/SPI bootloader protocol (AN4221/AN4286), boot pin and reset control, and custom target-mode loaders."
sources:
  - https://www.st.com/resource/en/application_note/an4221-i2c-protocol-used-in-the-stm32-bootloader-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4286-spi-protocol-used-in-the-stm32-bootloader-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# I2C and SPI host-driven bootloaders

Typical in products where a Linux SoC or main MCU manages co-processors (motor controller, power
management MCU, sensor hub) with no separate update interface.

## Hardware hooks the host needs
- Control of the co-processor's **reset** (NRST) and **BOOT0** (or equivalent) pins via GPIOs,
  so the host can force the ROM bootloader even when the application is broken.
- The bus (I2C/SPI) routed to pins the ROM bootloader listens on (AN2606 lists exact pins and I2C
  addresses per part, e.g. I2C1 on PB6/PB7, 7-bit address per family like 0x56).

## STM32 ROM I2C protocol (AN4221) outline
```
host: [addr+W] cmd, ~cmd            device: ACK byte 0x79 (NACK 0x1F) read after each phase
GET (0x00), GET ID (0x02), READ MEMORY (0x11), WRITE MEMORY (0x31, max 256 B, 4-byte aligned address),
ERASE (0x44, extended with page lists or 0xFFFF mass erase), GO (0x21),
NO-STRETCH variants (0x32 write, 0x45 erase) for hosts that can't handle clock stretching
```
Each command: send opcode and its complement, poll for ACK (reading the ACK byte; the device may
NACK the address while busy with flash operations), send address with XOR checksum, poll ACK,
send data with checksum. Erase can take seconds: poll with a timeout.

## Linux host tooling
- `stm32flash` supports I2C (`stm32flash -a 0x56 /dev/i2c-1`) and UART.
- STM32CubeProgrammer CLI supports I2C/SPI through ST bridge hardware.
- Write your own with `ioctl(I2C_RDWR)` / spidev for production update daemons; keep it in the
  same repo as the co-processor firmware.

## Sequence
1. Host drives BOOT0 high, pulses NRST, waits for ROM startup (~few ms; check datasheet).
2. GET ID to confirm the part; mass or sector erase; write image in 256-byte blocks; read back
   and compare (or CRC command where available).
3. BOOT0 low, pulse reset (or GO command) to start the new application.
4. Application reports its version over the normal protocol; host confirms.

## Custom target-mode loader
If ROM bootloader pins conflict with the design, implement an I2C/SPI target in your own
bootloader (see I2C target mode) with the same structure: command, address, data, checksum, busy
status polling. Keep it in a write-protected region and enter it via a command or reset strap.

## Verify
- [ ] Host updates a co-processor with a blank, valid and corrupted application, recovering in every case.
- [ ] Power-cycle mid-update: next attempt succeeds via forced ROM boot.
