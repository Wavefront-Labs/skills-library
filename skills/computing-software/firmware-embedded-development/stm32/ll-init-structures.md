---
id: computing-software.firmware-embedded-development.stm32.ll-init-structures
name: ll-init-structures
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-ll, ll-init, use-full-ll-driver, ll-gpio-init, ll-usart-init, ll-structinit, stm32, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Initialise STM32 peripherals with the LL init structures (LL_xxx_Init/StructInit) under USE_FULL_LL_DRIVER, versus inline LL register calls, with clock and ordering rules."
sources:
  - https://www.st.com/resource/en/user_manual/um1884-description-of-stm32l4l4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
  - https://github.com/STMicroelectronics/STM32CubeL4/tree/master/Projects/NUCLEO-L476RG/Examples_LL
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LL init structures

The LL (low-layer) driver has two layers:
- **Inline register functions** in `stm32xxxx_ll_<ppp>.h` (`LL_GPIO_SetPinMode`,
  `LL_USART_Enable`): one or two register accesses, always available, no init structs.
- **Init functions** in `stm32xxxx_ll_<ppp>.c` (`LL_GPIO_Init`, `LL_USART_Init`) that take a
  struct and configure everything at once. Compiled only with `USE_FULL_LL_DRIVER` defined.

## Enabling
Define `USE_FULL_LL_DRIVER` globally (CubeMX does this when any peripheral is set to LL in
*Project Manager > Advanced Settings*), and compile the `ll_*.c` files you use.

## Pattern
```c
#include "stm32l4xx_ll_bus.h"
#include "stm32l4xx_ll_gpio.h"
#include "stm32l4xx_ll_usart.h"

void uart2_init(void)
{
    LL_AHB2_GRP1_EnableClock(LL_AHB2_GRP1_PERIPH_GPIOA);       /* clocks first */
    LL_APB1_GRP1_EnableClock(LL_APB1_GRP1_PERIPH_USART2);

    LL_GPIO_InitTypeDef g;
    LL_GPIO_StructInit(&g);                                    /* defaults for every field */
    g.Pin        = LL_GPIO_PIN_2 | LL_GPIO_PIN_3;
    g.Mode       = LL_GPIO_MODE_ALTERNATE;
    g.Alternate  = LL_GPIO_AF_7;
    g.Speed      = LL_GPIO_SPEED_FREQ_HIGH;
    g.Pull       = LL_GPIO_PULL_UP;
    LL_GPIO_Init(GPIOA, &g);

    LL_USART_InitTypeDef u;
    LL_USART_StructInit(&u);
    u.BaudRate = 115200;
    u.DataWidth = LL_USART_DATAWIDTH_8B;
    u.StopBits = LL_USART_STOPBITS_1;
    u.Parity = LL_USART_PARITY_NONE;
    u.TransferDirection = LL_USART_DIRECTION_TX_RX;
    if (LL_USART_Init(USART2, &u) != SUCCESS) { init_fault(); }   /* fails if UE is set */
    LL_USART_ConfigAsyncMode(USART2);
    LL_USART_Enable(USART2);
    while (!LL_USART_IsActiveFlag_TEACK(USART2) || !LL_USART_IsActiveFlag_REACK(USART2)) {}
}
```

## Rules that bite
- Always `StructInit` first; uninitialised stack fields configure random modes.
- Init functions return `ERROR` when preconditions fail: USART enabled (`UE=1`), invalid
  parameter, or clock not ready. Check the return.
- `LL_USART_Init` computes BRR from the **current** kernel clock (`LL_RCC_GetUSARTClockFreq`);
  initialise peripherals **after** the final system clock configuration, or re-init after
  clock changes.
- LL doesn't enable NVIC lines or clocks for you (unlike HAL MSP callbacks). Do it explicitly.
- No timeouts or state machines: LL init doesn't wait for anything except where noted; add
  bounded waits yourself for ready flags.
- Timebase: LL projects use `LL_Init1msTick(SystemCoreClock)` and `LL_mDelay`, which configure
  SysTick without interrupts. Don't combine with HAL's SysTick tick (see mixing-hal-and-ll).

## When to use which
- Init structs: readable one-shot setup, close to HAL style, small code.
- Inline functions: runtime changes and ISRs (switch pin mode, change baud, toggle enables).
- Many teams init with LL structs and run with inline calls, never touching HAL.

## Verify
- [ ] Every `LL_*_Init` return value checked.
- [ ] Peripheral init happens after `SystemClock_Config` (baud rate verified on a scope/terminal).
- [ ] `USE_FULL_LL_DRIVER` defined in all build configurations that use init functions.

## Checked

2026-10-31: Confirmed the LL layer split (inline functions vs `USE_FULL_LL_DRIVER`-guarded init functions, both present in stm32l4xx_ll_usart.h), `LL_USART_Init`/`LL_USART_StructInit` (ErrorStatus), `LL_USART_DATAWIDTH_8B`, `LL_USART_STOPBITS_1`, `LL_USART_PARITY_NONE`, `LL_USART_DIRECTION_TX_RX`, `LL_USART_ConfigAsyncMode`, the `TEACK`/`REACK` flags, `LL_AHB2_GRP1_PERIPH_GPIOA` and `LL_APB1_GRP1_PERIPH_USART2` clock enables (stm32l4xx_ll_bus.h), the LL_GPIO init structure fields and `LL_Init1msTick`/`LL_mDelay` (stm32l4xx_ll_utils.h).

Method: documentation only; no commands were run.
