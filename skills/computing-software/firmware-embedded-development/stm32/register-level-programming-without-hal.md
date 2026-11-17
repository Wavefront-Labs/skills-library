---
id: computing-software.firmware-embedded-development.stm32.register-level-programming-without-hal
name: register-level-programming-without-hal
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32, register-level, ll-library, cmsis, hal-overhead, bare-register-access, rcc-direct, gpio-moder-direct, peripheral-init-order, reference-manual, interrupt-latency-reduction, firmware-embedded-development]
level: advanced
status: gated
description: "Write STM32 peripheral init against CMSIS registers or LL instead of HAL for latency- or flash-constrained code, and the clock-enable-before-config ordering HAL hides."
sources:
  - https://www.st.com/resource/en/reference_manual/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STM32 register-level programming without HAL

**Goal:** know when and how to drop below HAL — to LL (Low-Layer) or raw
CMSIS register access — for the cases where HAL's abstraction cost (flash
size, call overhead, or hidden state) is the actual problem, building on
`computing-software.firmware-embedded-development.stm32.cubemx-hal-project-setup`'s
HAL-based workflow as the default this skill deviates from deliberately.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Why drop below HAL at all
- **Interrupt latency**: HAL's generic peripheral functions (`HAL_UART_Transmit`,
  interrupt callback dispatch through `HAL_UART_IRQHandler`) add function-call
  and state-checking overhead on a path that may need to be a handful of
  register writes for a tight real-time budget (e.g. a control loop ISR
  reading an ADC result and writing a PWM duty cycle every tick).
- **Flash size**: HAL links in generic error-checking and state-machine code
  for every feature of a peripheral even if the application uses one simple
  mode of it — on a flash-constrained part, LL or direct register access can
  meaningfully shrink the binary for a peripheral-heavy application.
- **Determinism/auditability**: some certification or safety-adjacent work
  wants exact knowledge of every register write with no library-internal
  state machine in between — register-level code is directly traceable to
  the reference manual, line for line.
ST's **LL (Low-Layer) API** is a middle ground: thin inline-function wrappers
around register bitfields (`LL_GPIO_SetPinMode`, not `HAL_GPIO_Init` with a
config struct) — much less overhead than HAL, still named/typed instead of
raw addresses. CubeMX can generate LL-based init code as an alternative to
HAL; consider it before dropping to fully raw CMSIS struct access, which has
the steepest manual-correctness burden of the three options.

## The ordering HAL hides: clock enable before peripheral config
HAL's `Init` functions call the peripheral clock-enable macro internally as
part of initialization, which can make it easy to forget, when writing
register-level code, that **every peripheral register write before its RCC
clock-enable bit is set is undefined behavior** — it may silently do nothing,
read back zero, or (on some parts/some peripherals) cause a bus fault,
depending on whether the bus even responds. Always:
```c
RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;   // clock on first
__NOP(); __NOP();                       // a couple of cycles' delay some errata recommend
GPIOA->MODER |= (1 << (5*2));           // then configure
```
Some STM32 families' errata explicitly call out needing a short delay (a few
dummy reads/NOPs) between enabling a peripheral clock and its first register
access, because of a pipelined/buffered bus write that hasn't actually landed
yet — check the specific family's errata sheet, this is a real documented
silicon behavior on more than one STM32 line, not folklore.

## Reading the reference manual instead of a header comment
Register-level code's correctness depends entirely on matching the reference
manual's bitfield definitions, reset values, and any "this bit must be set
before that bit" sequencing notes (common in clock/PLL configuration and
peripheral enable sequences) — CMSIS device headers give you the bit
positions as named constants (`RCC_AHB1ENR_GPIOAEN`), but the *sequencing
rules* live only in the reference manual's prose, not the header. Treat the
reference manual chapter for a given peripheral as required reading before
writing register-level init for it, not an occasional reference.

## Verify
- [ ] Every register access to a peripheral occurs only after its RCC clock-enable bit is confirmed set, with any errata-recommended delay included.
- [ ] Register-level init was checked against the reference manual's documented bit-sequencing rules for that peripheral, not just its register map.
- [ ] If LL was chosen over raw CMSIS, confirmed it actually reduces overhead/flash size versus HAL for the specific peripheral usage measured, not assumed.
- [ ] A register-level driver's output was verified against a known-good HAL-based reference implementation on the bench (same signal, same timing) before trusting it in the field.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
