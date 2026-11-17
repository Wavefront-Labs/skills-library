---
id: computing-software.firmware-embedded-development.device-driver-development.uart-error-flags-overrun-framing-noise
name: uart-error-flags-overrun-framing-noise
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [uart-overrun, uart, framing-error, noise-flag, parity-error, firmware-embedded-development]
level: practitioner
status: draft
description: "Handle UART receive errors (overrun, framing, noise, parity): what causes each, how to clear them, why an uncleared ORE silently stops reception, and how to count them."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/user_manual/um1884-description-of-stm32l4l4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Framing, noise and overrun errors

## The four errors
| Flag (STM32) | Meaning | Usual cause |
|---|---|---|
| ORE overrun | a byte arrived while RDR still held the previous one | ISR latency too high, interrupts masked too long, no DMA at high baud |
| FE framing | stop bit read as 0 | baud mismatch, line break, wrong data bits/parity setting, noise |
| NE noise | samples within a bit disagreed (3-sample majority) | noise, slow edges, ground issues |
| PE parity | parity mismatch | parity setting mismatch, noise |

## Overrun stops reception
On STM32 USART v2, when ORE is set **no new data is transferred to RDR** until ORE is cleared,
and with RXNEIE enabled ORE also triggers the interrupt (EIE for DMA). A handler that only checks
RXNE never clears ORE: the interrupt fires forever (if ORE is in the IRQ sources) or reception
stops dead. Clear it explicitly:
```c
void USART2_IRQHandler(void) {
    uint32_t isr = USART2->ISR;
    if (isr & (USART_ISR_ORE | USART_ISR_FE | USART_ISR_NE | USART_ISR_PE)) {
        USART2->ICR = USART_ICR_ORECF | USART_ICR_FECF | USART_ICR_NECF | USART_ICR_PECF;
        stats.ore += !!(isr & USART_ISR_ORE); stats.fe += !!(isr & USART_ISR_FE);
    }
    if (isr & USART_ISR_RXNE) { rb_put((uint8_t)USART2->RDR); }
}
```
On USART v1 (F1/F4) flags clear by reading SR then DR. If the protocol cannot tolerate overrun,
disable it with `CR3.OVRDIS` only if you have another way to detect loss (it then overwrites RDR).

## HAL behaviour
HAL treats any error as fatal for the current transfer: it calls `HAL_UART_ErrorCallback`, aborts
the reception, and you must restart `HAL_UART_Receive_IT/DMA` in the callback. Forgetting to
restart is the classic "UART stops receiving after a while". Check `huart->ErrorCode`.

## Reducing errors
- Overrun: move RX to DMA (circular + idle-line), raise UART IRQ priority, shorten critical
  sections, enable the RX FIFO (STM32 G4/H7/U5 `FIFOEN`).
- Framing at connect/disconnect: expected; ignore the first bytes after line activity starts.
- Framing persistently: verify baud error budget; check both ends' clock sources.
- Noise: enable `ONEBIT` sampling only for clean lines (higher tolerance to clock deviation but
  no noise detection); otherwise fix the hardware (RS-485/RS-232 transceivers, grounding).

## Verify
- [ ] Error counters exposed (CLI/telemetry); zero ORE under worst-case load at target baud.
- [ ] Injecting a line break or wrong-baud data recovers reception automatically.
