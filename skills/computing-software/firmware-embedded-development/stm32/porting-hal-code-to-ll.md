---
id: computing-software.firmware-embedded-development.stm32.porting-hal-code-to-ll
name: porting-hal-code-to-ll
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-ll, hal-to-ll-porting, hal-overhead, ll-migration, code-size-reduction, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Port STM32 HAL code to LL for speed or size: what to keep in HAL, mapping HAL calls to LL, CubeMX per-peripheral driver switch, and verifying behaviour stays identical."
sources:
  - https://www.st.com/resource/en/user_manual/um1884-description-of-stm32l4l4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-for-stm32-configuration-and-initialization-c-code-generation-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Porting HAL code to LL

## Decide what to port
Port where HAL costs too much:
- ISR-heavy paths: UART byte reception, timer update ISRs at tens of kHz, GPIO toggling (HAL
  callbacks add hundreds of cycles per interrupt through `HAL_xxx_IRQHandler` dispatch).
- Flash-constrained parts (16-32 KB): HAL UART + I2C + TIM easily take several KB.
Keep HAL for complex stacks: USB, SDMMC, Ethernet, FDCAN message RAM, crypto.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

Measure first: `arm-none-eabi-size` per object and cycle counts (`DWT->CYCCNT`) around the ISR.

## CubeMX switch
Project Manager > Advanced Settings > driver selector: set the peripheral to LL. Regenerate:
`MX_USART2_UART_Init` becomes LL init code (`LL_USART_Init` with an init struct). The HAL module
for that peripheral can then be disabled in `stm32xxxx_hal_conf.h` (`#define HAL_UART_MODULE_ENABLED` removed)
if nothing else uses it.

## Mapping table
| HAL | LL |
|---|---|
| `HAL_GPIO_WritePin(P, pin, SET)` | `LL_GPIO_SetOutputPin(P, pin)` (BSRR) |
| `HAL_GPIO_TogglePin` | `LL_GPIO_TogglePin` |
| `HAL_UART_Transmit(...)` polling | loop: wait `LL_USART_IsActiveFlag_TXE`, `LL_USART_TransmitData8`; then wait TC |
| `HAL_UART_Receive_IT` + `RxCpltCallback` | `LL_USART_EnableIT_RXNE` + own ISR + ring buffer |
| `HAL_TIM_Base_Start_IT` + `PeriodElapsedCallback` | `LL_TIM_EnableIT_UPDATE`, `LL_TIM_EnableCounter`; ISR: `LL_TIM_ClearFlag_UPDATE` |
| `__HAL_TIM_SET_COMPARE` | `LL_TIM_OC_SetCompareCH1` |
| `HAL_ADC_Start` / `PollForConversion` / `GetValue` | `LL_ADC_REG_StartConversion`, wait `LL_ADC_IsActiveFlag_EOC`, `LL_ADC_REG_ReadConversionData12` |
| `HAL_Delay` | own SysTick ms counter, or `LL_mDelay` (no SysTick ISR) |

## Things HAL did silently
- Clock enables (`__HAL_RCC_xxx_CLK_ENABLE` inside MspInit): LL init does not enable clocks.
- GPIO AF config in MspInit.
- Timeouts on every blocking call: add your own or you get infinite loops on a dead bus.
- Error flag clearing (ORE on UART, ARLO/BERR on I2C).
- Lock/state checks against concurrent use.
- Calibration (`HAL_ADCEx_Calibration_Start` vs `LL_ADC_StartCalibration` + wait + required delays
  `LL_ADC_DELAY_CALIB_ENABLE_ADC_CYCLES`).
- ADC voltage regulator startup delay on L4/G4 (`LL_ADC_EnableInternalRegulator` + `LL_ADC_DELAY_INTERNAL_REGUL_STAB_US`).

## Mixing
HAL and LL coexist per peripheral instance, but not on the same instance at once (HAL's state
machine won't know about LL changes).

## Verify
- [ ] Behavioural tests pass identically before and after (same logic analyser traces).
- [ ] Flash and ISR cycle savings measured and recorded.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
