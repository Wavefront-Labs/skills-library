---
id: computing-software.firmware-embedded-development.device-driver-development.i2c-target-slave-mode
name: i2c-target-slave-mode
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [i2c-target, i2c, i2c-slave, register-file-emulation, clock-stretching-target, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Implement an MCU as an I2C target exposing a register file: address match, repeated-start read pointer, NOSTRETCH trade-offs, and ISR timing so hosts never read garbage."
sources:
  - https://github.com/STMicroelectronics/cmsis_device_l4/blob/master/Include/stm32l476xx.h
  - https://github.com/STMicroelectronics/stm32l4xx_hal_driver
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/i2c.h
  - https://docs.kernel.org/i2c/slave-interface.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# I2C target (slave) mode

Common in co-processor designs: a small MCU acts like a sensor with a register map for a host
(Linux SoC, another MCU). The host does `write reg_addr` then `repeated start + read N`.

## Protocol model (register file)
```
Host write:  S addr+W ACK reg ACK [data ACK ...] P   -> set pointer, optional writes (auto-increment)
Host read:   S addr+W ACK reg ACK Sr addr+R ACK data ACK data NACK P
```
Target state: `ptr` (register pointer), `first_byte` flag. On address-match with write
direction, the next received byte is the pointer; subsequent bytes are writes at `ptr++`.
On address-match with read direction, transmit from `ptr++`.

## STM32 (I2C v2) interrupt skeleton
```c
void I2C1_EV_IRQHandler(void) {
    uint32_t isr = I2C1->ISR;
    if (isr & I2C_ISR_ADDR) {
        bool read = isr & I2C_ISR_DIR;
        if (read) { I2C1->ISR |= I2C_ISR_TXE; }      /* flush TXDR so the first byte is fresh */
        else      { first = true; }
        I2C1->ICR = I2C_ICR_ADDRCF;                   /* releases SCL stretching */
    }
    if (isr & I2C_ISR_RXNE) {
        uint8_t b = (uint8_t)I2C1->RXDR;
        if (first) { ptr = b; first = false; } else { regs_write(ptr++, b); }
    }
    if (isr & I2C_ISR_TXIS) { I2C1->TXDR = regs_read(ptr++); }
    if (isr & I2C_ISR_STOPF) { I2C1->ICR = I2C_ICR_STOPCF; commit_writes(); }
    if (isr & I2C_ISR_NACKF) { I2C1->ICR = I2C_ICR_NACKCF; }   /* host ended the read */
}
```
Enable `ADDRIE | RXIE | TXIE | STOPIE | NACKIE`, set `OAR1 = OA1EN | (addr << 1)`.

## Clock stretching
With stretching enabled (default), the peripheral holds SCL low until firmware services ADDR,
TXIS or RXNE: safe even with slow ISRs. Some hosts handle stretching poorly (check the host controller's documentation). With `NOSTRETCH`, data
must be ready *before* the clock edge: preload TXDR and service in well under one bit time
(2.5 us at 400 kHz), or you get an overrun/underrun (`OVR`) and the host reads wrong data.

## Design tips
- Keep register reads side-effect free except designated FIFO/status registers; hosts retry reads.
- Make multi-byte values atomic: latch a snapshot when the pointer is set to the first byte.
- Provide an interrupt/data-ready GPIO to the host instead of polling.
- Handle bus errors (`BERR`, `ARLO`) and timeouts (SMBus `TIMEOUT` feature) so the target never
  holds SDA low forever.
- Zephyr: `i2c_target_register()` with `struct i2c_target_callbacks` (`write_requested`, `write_received`, `read_requested`, `read_processed`, `stop`).

## Verify
- [ ] From the host (for example Linux i2c-dev or i2c-tools), a register write then repeated-start read returns the expected values repeatedly.
- [ ] Logic analyser shows stretching durations; no wrong bytes in reads under ISR load.

## Checked

2026-10-27, STM32L4 CMSIS device header and HAL (master), Zephyr include/zephyr/drivers/i2c.h (main), Linux Documentation/i2c/slave-interface.rst (v7.3).
Confirmed in stm32l476xx.h: I2C_ISR_ADDR, DIR, TXE, RXNE, TXIS, STOPF, NACKF, OVR, BERR, ARLO, TIMEOUT; I2C_ICR_ADDRCF, STOPCF, NACKCF; I2C_OAR1_OA1EN; I2C_CR1_NOSTRETCH, TXIE, RXIE, ADDRIE, NACKIE, STOPIE; I2C_TIMEOUTR. Confirmed in the L4 HAL: TXDR flush through the TXE flag (ISR |= TXE) and clearing ADDR through ICR. Confirmed in Zephyr i2c.h: i2c_target_register and the five callback names. The 2.5 us figure is the 400 kHz period. Removed the Raspberry Pi stretching claim, the 0xFF read claim and the i2c-tools command lines (tool not read).

Method: documentation only; no commands were run.
