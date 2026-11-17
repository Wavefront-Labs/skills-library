---
id: computing-software.firmware-embedded-development.device-driver-development.interrupt-dma-i2c-transactions
name: interrupt-dma-i2c-transactions
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [i2c-interrupt-transfer, i2c-dma, i2c-driver, repeated-start, transaction-queue, nack-handling, bus-recovery, async-driver, firmware-embedded-development]
level: advanced
status: draft
description: "Write a non-blocking I2C master driver: interrupt state machine or DMA for write-then-read with repeated start, NACK/timeout/arbitration errors, queued transactions and callbacks."
sources:
  - https://www.nxp.com/docs/en/user-guide/UM10204.pdf
  - https://www.st.com/resource/en/application_note/an4235-i2c-timing-configuration-tool-for-stm32f3xxxx-and-stm32f0xxxx-microcontrollers-stmicroelectronics.pdf
  - https://docs.zephyrproject.org/latest/hardware/peripherals/i2c.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interrupt/DMA driven I2C transactions

**Goal:** I2C transfers that do not busy-wait the CPU: start a transaction, get a callback
with success or a precise error, and let several drivers share the bus.

## Transaction model
Describe work as a list of messages, like Linux `i2c_msg` / Zephyr `i2c_msg`:
```c
typedef struct { uint8_t *buf; uint16_t len; uint8_t flags; } i2c_msg_t;   /* flags: READ, STOP */
typedef struct { uint8_t addr; i2c_msg_t *msgs; uint8_t n; void (*done)(int err, void *ctx); void *ctx; } i2c_xfer_t;
```
A register read is two messages: write `{reg}` with no STOP, then read `{data, len}` with
STOP - the driver emits a **repeated START** between them, so no other master can grab the
bus and the device keeps its register pointer.

## Interrupt state machine (classic I2C peripheral)
States: `START_SENT -> ADDR_SENT -> TX_DATA / RX_DATA -> (RESTART) -> STOP`.
- Event interrupt: on SB send address; on ADDR clear it (read SR1 then SR2 on STM32F1/F4
  style IP); on TXE write next byte; on RXNE read; on BTF finish.
- Reading N bytes: ACK must be cleared **before** the last byte is received (for N=1 before
  clearing ADDR, for N=2 using POS) - the most common source of hangs on old ST I2C IP.
- Newer IP (STM32 I2C v2, nRF TWIM, NXP LPI2C) automates this with a byte count (NBYTES,
  AUTOEND/RELOAD) - far simpler; prefer it.

## DMA
Use DMA for payloads beyond a few bytes: interrupt-driven phases set up address and
direction, DMA moves data, the transfer-complete or I2C STOP interrupt finishes. Some IPs
need the last byte(s) handled manually for NACK generation; check the reference manual.

## Errors to surface (never just "failed")
- **Address NACK** (`-ENXIO`): device absent or busy (EEPROM write cycle) - caller may retry.
- **Data NACK** (`-EIO`).
- **Arbitration lost** (`-EAGAIN`): retry after bus free (see `i2c-multi-master-arbitration`).
- **Bus error / timeout** (`-ETIMEDOUT`): run bus recovery - reconfigure SCL as GPIO, clock up
  to 9 pulses until SDA releases, generate STOP, reinit the peripheral.
Always arm a software timeout per transaction; a stuck slave holding SDA low otherwise blocks
forever with interrupts quiet.

## Sharing the bus
Queue transactions and run them one at a time from the driver (FIFO of `i2c_xfer_t`), or
serialise with an RTOS mutex around a blocking wrapper that waits on a semaphore given by
the `done` callback. Never call `done` with the driver lock held.

## Verify
- [ ] Logic analyser shows `S addr+W reg Sr addr+R data... P` for register reads.
- [ ] Unplugging the device yields address NACK error, not a hang.
- [ ] Forcing SDA low recovers within the timeout.
