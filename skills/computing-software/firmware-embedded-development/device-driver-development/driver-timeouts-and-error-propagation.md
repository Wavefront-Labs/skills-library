---
id: computing-software.firmware-embedded-development.device-driver-development.driver-timeouts-and-error-propagation
name: driver-timeouts-and-error-propagation
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [driver-timeout, interrupt-driven, bounded-wait, error-recovery, retry-policy, firmware-embedded-development]
level: practitioner
status: draft
description: "Bound every hardware wait in drivers with a timeout, recover the peripheral to a known state on failure, and propagate errors so the right layer decides on retries."
sources:
  - https://www.st.com/resource/en/user_manual/um1884-description-of-stm32l4l4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
  - https://docs.zephyrproject.org/latest/hardware/peripherals/i2c.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Driver timeouts and error propagation

`while (!(I2C1->ISR & I2C_ISR_TXIS)) {}` hangs forever if the device NACKs, the bus is stuck, or
the clock to the peripheral is off. In the field that means a watchdog reset loop at best.

## Bound every wait
```c
static int wait_flag(volatile uint32_t *reg, uint32_t mask, uint32_t timeout_us) {
    uint32_t t0 = micros();
    while ((*reg & mask) == 0) {
        if ((uint32_t)(micros() - t0) > timeout_us) return -ETIMEDOUT;
    }
    return 0;
}
```
- Use a timebase that works with interrupts disabled (free-running timer, DWT), not a tick
  counter incremented in an ISR you may have masked.
- Size the timeout from the protocol: an I2C byte at 100 kHz takes 90 us; allow clock stretching
  (SMBus caps it at 25 ms); a flash sector erase may take seconds (datasheet max, not typ).
- Also check error flags inside the loop (NACKF, BERR, ARLO) to fail fast instead of waiting out
  the timeout.

## Recover to a known state
After a timeout or error the peripheral is often in an intermediate state. Recovery per type:
- I2C: generate STOP, disable/enable `PE` (software reset), bus recovery (9 SCL pulses) if SDA stuck.
- SPI: wait BSY or disable SPE, flush FIFOs, raise CS.
- UART: clear error flags; abort DMA; restart reception.
- Peripheral reset via `RCC->xxxRSTR` and reinit when all else fails.
Leave the driver in IDLE so the next call can proceed.

## Propagate, don't decide
- The driver returns `-ETIMEDOUT`, `-EIO`, `-ENXIO` (no ACK) and records detail; it does not
  retry endlessly or reset the system.
- The device layer (sensor driver) may retry a few times for transient errors.
- The application decides policy: degrade, alert, power-cycle the sensor via a load switch.
- Count errors by type; expose counters for diagnosis.

## HAL notes
HAL functions take a `Timeout` in ms (`HAL_MAX_DELAY` = forever, avoid in production) and use
`HAL_GetTick()`, which stops when SysTick is masked or its priority is below the caller's. A HAL
call from an ISR with higher priority than SysTick never times out.

## Verify
- [ ] grep for unbounded `while` loops on peripheral flags: none remain.
- [ ] Disconnect the device / short SDA: driver returns an error within the timeout and works again once fixed.
