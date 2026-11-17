---
id: computing-software.firmware-embedded-development.low-power-design.lpuart-wakeup-on-receive
name: lpuart-wakeup-on-receive
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [wake-source, lpuart-wakeup, lpuart, usart-wakeup-from-stop, uesm, wufie, start-bit-detection, address-match-wake, lse-uart-clock, firmware-embedded-development]
level: advanced
status: draft
description: "Wake from stop mode when a UART byte arrives without losing it: LPUART/USART UESM, wake-up event selection, kernel clock choice and the first-byte problem."
sources:
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LPUART wake-up on receive

**Goal:** a device that sleeps in Stop mode at microamps but still answers a host or modem
that sends serial data at any time.

## Options
1. **LPUART clocked from LSE** (32.768 kHz): keeps receiving in Stop 2 at up to 9600 baud
   (LSE allows <= 9600). Data is received normally; the RXNE/wake-up interrupt wakes the core.
2. **USART/LPUART clocked from HSI16 with UESM**: in Stop mode the HSI is started on demand
   when a start bit is detected (wake-up from Stop). Higher baud rates; HSI wake-up time adds
   a few microseconds.
3. **Sacrifice the first byte**: EXTI on the RX pin, wake, then enable the UART. Any protocol
   must then start with a wake-up preamble byte (common with modems).

## STM32L4 LPUART + LSE setup
```c
/* RCC: LPUART1 kernel clock = LSE */
__HAL_RCC_LPUART1_CONFIG(RCC_LPUART1CLKSOURCE_LSE);
huart.Init.BaudRate = 9600;
HAL_UART_Init(&hlpuart1);
UART_WakeUpTypeDef wk = { .WakeUpEvent = UART_WAKEUP_ON_READDATA_NONEMPTY };
HAL_UARTEx_StopModeWakeUpSourceConfig(&hlpuart1, wk);
__HAL_UART_ENABLE_IT(&hlpuart1, UART_IT_WUF);
HAL_UARTEx_EnableStopMode(&hlpuart1);          /* sets UESM */
HAL_UART_Receive_IT(&hlpuart1, &rx, 1);
HAL_PWREx_EnterSTOP2Mode(PWR_STOPENTRY_WFI);
```
Wake-up events: on start bit, on RXNE (byte complete, recommended: no byte lost), or on
address match (multi-drop: only wake when addressed).

## Gotchas
- **Not every USART supports wake-up from Stop** on every part, and some only from Stop 0/1.
  Check the "USART/LPUART features" table in the reference manual.
- **Baud rate limits** with LSE: 9600 max; mismatch shows as framing errors only after sleep.
- **After wake, restore the system clock** but don't reconfigure the UART kernel clock if it
  must keep receiving the rest of the frame.
- **Clear WUF** (`__HAL_UART_CLEAR_FLAG(huart, UART_CLEAR_WUF)`) in the handler or the core
  re-wakes immediately.
- Bursty input: a 2nd byte arrives while you restore clocks; use DMA or a FIFO-equipped
  LPUART and process after the clock is stable.

## Verify
- [ ] Send a 20-byte command to a sleeping device 1000 times: no lost first byte, all answered.
- [ ] Idle current in Stop 2 with LPUART armed within ~1 uA of plain Stop 2.
