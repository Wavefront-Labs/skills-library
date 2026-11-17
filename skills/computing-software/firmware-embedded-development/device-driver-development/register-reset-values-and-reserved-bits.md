---
id: computing-software.firmware-embedded-development.device-driver-development.register-reset-values-and-reserved-bits
name: register-reset-values-and-reserved-bits
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [reserved-bits, datasheet, reset-value, must-be-kept, register-initialisation, firmware-embedded-development]
level: practitioner
status: draft
description: "Respect register reset values and reserved bits: 'must be kept at reset value' fields, read-modify-write vs full writes, and why writing 0 to reserved bits can break hardware."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://developer.arm.com/documentation/ddi0403/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reset values and reserved bits

## Reserved bit conventions
Reference manuals mark unused fields with phrases that have specific meanings:
| Wording | Meaning | Correct handling |
|---|---|---|
| "Reserved, must be kept at reset value" | the bit may do something (test modes, future features) | read-modify-write, preserving the bit |
| "Reserved, must be kept cleared" / "set" | write that value | include it in your full write |
| "Reserved" (Arm ARM: RES0 / RES1) | software should write 0 (RES0) or 1 (RES1); reads are unknown | mask on read, write the defined value |
| "Reserved, read as 0" | safe to write 0 | full write fine |

Writing a whole register with a constant that zeroes "must be kept at reset value" bits that
reset to 1 is a real bug source: e.g. STM32 RCC and PWR registers have reserved bits with reset
value 1 on some families; FLASH_ACR and option byte registers contain factory-set bits.

## Reset values matter for
- **Full-register writes**: `TIM2->CR1 = TIM_CR1_CEN;` assumes all other bits should be 0. Fine
  for CR1, wrong for registers with non-zero reset defaults (e.g. GPIO `MODER` resets to analog
  `0xFFFFFFFF` on STM32L4, `0xABFFFFFF` for port A with SWD pins in AF mode). Writing
  `GPIOA->MODER = 0;` turns SWD pins into inputs and disconnects the debugger.
- **Reinitialisation without reset**: a bootloader leaves peripherals configured; the application
  assumes reset values. Either reset peripherals via `RCC->APBxRSTR` (assert then release) before
  init, or write every relevant field explicitly.
- **Debug comparisons**: compare live register dumps against reset values to spot what has been
  configured.

## Patterns
```c
/* RMW preserving unknown/reserved bits */
GPIOA->MODER = (GPIOA->MODER & ~GPIO_MODER_MODE5_Msk) | (1U << GPIO_MODER_MODE5_Pos);
/* MODIFY_REG from CMSIS/ST: same thing */
MODIFY_REG(GPIOA->MODER, GPIO_MODER_MODE5_Msk, GPIO_MODER_MODE5_0);
/* peripheral reset before (re)init */
RCC->APB1RSTR1 |=  RCC_APB1RSTR1_USART2RST;
RCC->APB1RSTR1 &= ~RCC_APB1RSTR1_USART2RST;
```

## Verify
- [ ] No full-register writes to registers documenting "must be kept at reset value" fields (grep `->REG =` and review).
- [ ] Application init produces the same register state whether started from reset or from the bootloader (dump and diff).
