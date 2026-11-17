---
id: computing-software.firmware-embedded-development.stm32.cubemx-hal-project-setup
name: cubemx-hal-project-setup
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32, stm32cubemx, stm32cubeide, ioc, hal, ll-drivers, clock-tree, hse, hsi, pll, systick, hal-timebase, tim6, freertos, cmsis-rtos, user-code-begin, code-regeneration, hal-uart-receive-it, hal-uart-receive-dma, idle-line, swd, serial-wire-debug, nvic, cortex-m, firmware-embedded-development]
level: practitioner
status: draft
description: "Set up an STM32 project in CubeMX/CubeIDE that survives regeneration: clock tree from HSE/PLL, HAL timebase off SysTick with an RTOS, USER CODE blocks, interrupt/DMA UART and SWD kept."
sources:
  - https://www.st.com/en/development-tools/stm32cubemx.html
  - https://www.st.com/en/development-tools/stm32cubeide.html
  - https://wiki.st.com/stm32mcu/wiki/Main_Page
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# STM32 CubeMX/HAL project setup — a generated project you can keep regenerating

**Goal:** a CubeMX (`.ioc`) project whose clocks are right, whose debug link never gets
locked out, whose UART receives without polling, and whose hand-written code survives every
"Generate Code".

## 1. Pinout first: protect the debug port
In **Pinout & Configuration › System Core › SYS**, set **Debug = Serial Wire**. If it is left
at "No Debug", CubeMX may hand PA13/PA14 (SWDIO/SWCLK) to other functions, and after flashing,
the debugger cannot attach. Recovery: connect under reset ("Connect under reset" in
STM32CubeProgrammer, or hold NRST while attaching). Never assign PA13/PA14 as GPIO unless you
mean it.

## 2. Clock tree
- **RCC**: set HSE to "Crystal/Ceramic Resonator" if the board has one (Nucleo boards often
  feed HSE from the ST-LINK's MCO — "BYPASS Clock Source"; check the board manual).
- In the **Clock Configuration** tab, select PLL source HSE, type the target HCLK and let the
  solver pick M/N/P/Q. Watch for red fields: APB1 maximum, USB needing exactly 48 MHz, and
  flash wait states (CubeMX sets `FLASH_LATENCY_x` in `SystemClock_Config()` for you).
- A wrong `HSE_VALUE` (in `stm32xxxx_hal_conf.h`) makes every baud rate wrong while the code
  "works". If UART output is garbage, check this first.

## 3. HAL timebase vs SysTick when using an RTOS
HAL uses a 1 ms tick for `HAL_Delay()` and timeouts. FreeRTOS (via the CMSIS-RTOS wrapper)
wants SysTick for its own tick. In **SYS › Timebase Source**, choose a basic timer such as
**TIM6** (or TIM7) when the RTOS is enabled; CubeMX warns if you don't. The HAL tick then comes
from `HAL_TIM_PeriodElapsedCallback()` in `main.c`. Keep that timer's NVIC priority high enough
(numerically low) that `HAL_Delay()` works inside other interrupts if you must call it there —
better, don't. See computing-software.firmware-embedded-development.freertos.task-and-queue-design
for interrupt priority rules against `configMAX_SYSCALL_INTERRUPT_PRIORITY`.

## 4. Code that survives regeneration
CubeMX rewrites generated files on every generate. Only text between matching markers is kept:
```c
/* USER CODE BEGIN 2 */
  HAL_UARTEx_ReceiveToIdle_DMA(&huart2, rx_buf, sizeof rx_buf);
/* USER CODE END 2 */
```
Rules that avoid lost work:
- Put substantial code in your own files (`app.c`, `app.h`) and call `app_init()` / `app_loop()`
  from the USER CODE blocks in `main.c`.
- Don't rename or delete the markers. Code outside them is silently discarded.
- In **Project Manager › Code Generator**, enable "Generate peripheral initialization as a
  pair of .c/.h files per peripheral" for cleaner diffs, and commit the `.ioc` alongside the
  generated sources so reviewers can diff both.
- Pin the CubeMX version and the STM32Cube MCU package (firmware package) version in the
  project notes; regenerating with a newer package can change HAL code underneath you.

## 5. UART reception without polling
- `HAL_UART_Receive(&huart2, buf, n, timeout)` blocks — fine for bring-up only.
- `HAL_UART_Receive_IT(&huart2, &byte, 1)` and re-arm inside `HAL_UART_RxCpltCallback()` —
  simple, one interrupt per byte, works for low rates.
- For variable-length packets use DMA with idle-line detection: `HAL_UARTEx_ReceiveToIdle_DMA()`
  and handle `HAL_UARTEx_RxEventCallback(huart, Size)`. Available in newer HAL packages only;
  on older families/versions check whether it exists. Set the DMA channel to circular mode and
  disable the half-transfer interrupt if you don't want callbacks at half-buffer.
- Enable the USART global interrupt in the NVIC tab, or callbacks never fire.
- Callbacks run in interrupt context: copy data into a ring buffer or queue; don't parse there.
- After an overrun (ORE) error, HAL aborts reception; implement `HAL_UART_ErrorCallback()` to
  re-arm.

## 6. Build and flash
CubeIDE builds with arm-none-eabi-gcc; alternatively choose "Makefile" or "CMake" as the
toolchain in Project Manager for command-line/CI builds (CMake output depends on CubeMX
version). Check `arm-none-eabi-size` output after each change.

## Verify
- [ ] SYS Debug = Serial Wire; the debugger attaches after flashing without connect-under-reset.
- [ ] A 1 s `HAL_Delay()` blink measures 1 s on a scope; UART at 115200 prints clean text.
- [ ] With an RTOS, the timebase is TIMx and SysTick is owned by the RTOS.
- [ ] Regenerating code from the `.ioc` produces no loss of hand-written code (git diff clean in USER CODE blocks).
- [ ] UART receives a burst of variable-length frames without overrun errors.
