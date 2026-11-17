---
id: computing-software.firmware-embedded-development.stm32.alternate-function-pin-mapping
name: alternate-function-pin-mapping
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-gpio, alternate-function, afr, af-mapping, pin-muxing, gpio-moder, remap, pinout-planning, datasheet-af-table, firmware-embedded-development]
level: practitioner
status: gated
description: "Route STM32 peripherals to pins with the alternate-function (AF) table: AFRL/AFRH setup, conflict planning in CubeMX, and why a peripheral is silent on the wrong AF."
sources:
  - https://www.st.com/resource/en/datasheet/stm32f401re.pdf
  - https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-for-stm32-configuration-and-initialization-c-code-generation-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alternate-function pin mapping

**Goal:** each peripheral signal on a pin that supports it, with the right AF number,
decided before the PCB is laid out.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Where the truth is
The **datasheet** (not the reference manual) has the "Alternate function mapping" table:
rows = pins, columns AF0..AF15, cells = signal (e.g. PA9 AF7 = USART1_TX). The reference
manual describes the mechanism; the datasheet has the per-package mapping. Packages differ:
a pin on the 100-pin part may not exist on the 48-pin one.

## Register setup (what HAL does)
```c
RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
/* PA9 = USART1_TX, AF7 */
GPIOA->MODER   = (GPIOA->MODER & ~(3u << (9*2))) | (2u << (9*2));     /* 10 = AF */
GPIOA->OTYPER &= ~(1u << 9);                                           /* push-pull */
GPIOA->OSPEEDR |= (2u << (9*2));                                       /* high speed */
GPIOA->AFR[1]  = (GPIOA->AFR[1] & ~(0xFu << ((9-8)*4))) | (7u << ((9-8)*4)); /* AFRH */
```
Pins 0-7 use `AFR[0]` (AFRL), pins 8-15 `AFR[1]` (AFRH). HAL: `GPIO_InitStruct.Alternate =
GPIO_AF7_USART1`.

## Planning
- Do the pinout in **CubeMX first** (even if you won't use generated code): it knows the AF
  table and flags conflicts (a timer channel and SPI wanting the same pin).
- Reserve SWDIO/SWCLK (PA13/PA14), BOOT0, NRST, and the HSE/LSE oscillator pins.
- Pick pins for peripherals that need **specific features**: timer channels with
  complementary outputs (TIMx_CHxN), ADC channels on 5 V-tolerant vs not, I2C on pins with
  "FT_f" (Fm+ capable), USB on its fixed pins.
- Prefer one pin per signal; some signals appear on several pins, keep alternates for rework.
- STM32F1 is different: no per-pin AF; uses **AFIO remap** registers (`__HAL_AFIO_REMAP_*`)
  with fixed pin groups.

## Symptoms of a wrong mapping
- Peripheral registers look right, scope shows nothing: AF number wrong or MODER not `10`.
- I2C pins stuck: missing open-drain (`OTYPER=1`) for I2C AF.
- Two peripherals fighting: both configured on the same pin; the last AF written wins.

## Verify
- [ ] Every signal's AF checked against the datasheet table for the exact package.
- [ ] Readback of `MODER`/`AFR` for the pins at run time matches the plan (debugger
      peripheral view / SVD).
- [ ] Scope shows activity on the pin when the peripheral transmits.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
