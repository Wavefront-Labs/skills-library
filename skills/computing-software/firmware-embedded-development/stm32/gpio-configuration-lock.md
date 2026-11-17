---
id: computing-software.firmware-embedded-development.stm32.gpio-configuration-lock
name: gpio-configuration-lock
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-gpio, gpio-lock-register, lckr, lock-key-sequence, functional-safety, hal-gpio-lockpin, pin-config-protection, firmware-embedded-development]
level: advanced
status: gated
description: "Freeze safety-relevant STM32 pin configuration with the GPIO LCKR lock key sequence so errant code can't reconfigure it until reset."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/user_manual/um1725-description-of-stm32f4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPIO configuration lock (LCKR)

**Goal:** make the configuration of critical pins (motor gate drives, relay outputs,
safety inputs, the SWD pins) immutable after init, as functional-safety analyses often
require.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## What it locks
`MODER`, `OTYPER`, `OSPEEDR`, `PUPDR`, `AFRL/AFRH` for the selected pins of a port. It does
**not** lock the output data (`ODR`/`BSRR`): the pin can still be driven high/low. Unlock only
by MCU reset.

## Lock key sequence
Write `LCKK=1 + pin mask`, `LCKK=0 + mask`, `LCKK=1 + mask`, then two reads; the second read
of `LCKK` = 1 confirms. Any other access in between aborts the sequence.
```c
static int gpio_lock(GPIO_TypeDef *port, uint16_t pins) {
    uint32_t key = GPIO_LCKR_LCKK | pins;
    port->LCKR = key;
    port->LCKR = pins;
    port->LCKR = key;
    (void)port->LCKR;
    return (port->LCKR & GPIO_LCKR_LCKK) ? 0 : -1;
}
```
HAL: `HAL_GPIO_LockPin(GPIOB, GPIO_PIN_0 | GPIO_PIN_1)` returns `HAL_ERROR` if it didn't take.

## Using it well
- Call after **all** pin configuration is final, including late-initialised peripherals; a
  locked pin silently ignores later `HAL_GPIO_Init` calls, and the bug looks like a broken
  peripheral.
- Do the sequence with interrupts masked: an ISR touching the same port's LCKR (unlikely) or
  a debugger memory view refresh can break the sequence.
- Lock is per port: one call per port with the mask of pins to lock.
- Combine with a periodic self-test that reads back MODER/AFR of critical pins and compares
  to expected (IEC 60730 class B style), since lock prevents writes but not hardware faults.
- Low-power code that reconfigures pins to analog before Stop will fail on locked pins: plan
  which pins are locked versus power-managed.

## Verify
- [ ] Lock function returns success; a subsequent write to `MODER` for that pin reads back
      unchanged.
- [ ] Reset clears the lock (power-on and software reset paths both re-lock correctly).

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
