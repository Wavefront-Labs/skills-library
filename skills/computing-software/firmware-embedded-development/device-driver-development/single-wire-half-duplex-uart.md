---
id: computing-software.firmware-embedded-development.device-driver-development.single-wire-half-duplex-uart
name: single-wire-half-duplex-uart
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [half-duplex-uart, uart, single-wire, hdsel, smart-servo, firmware-embedded-development]
level: practitioner
status: draft
description: "Use one-wire half-duplex UART (STM32 HDSEL, open-drain TX) for smart servos, 1-wire-like sensors and UPDI: echo handling, turnaround timing, and pull-up choice."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://emanual.robotis.com/docs/en/dxl/protocol2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Single-wire half-duplex UART

TX and RX share one pin. Used by Dynamixel and other smart servos (TTL variants), some battery
and ESC telemetry links, Microchip UPDI programming, and SmartPort/F.Port in RC gear.

## STM32 configuration
```c
USART1->CR1 &= ~USART_CR1_UE;
USART1->CR3 |= USART_CR3_HDSEL;          /* RX internally connected to TX pin; RX pin unused */
USART1->CR1 |= USART_CR1_TE | USART_CR1_RE | USART_CR1_UE;
```
GPIO: TX pin as alternate function. For multi-drop buses, configure it **open-drain with a
pull-up** (internal ~40k for short wires, external 1-10k for longer ones) so a slave can drive
the line low while the MCU idles; push-pull fights the other device during its reply.
HAL: `HAL_HalfDuplex_Init()`, then `HAL_HalfDuplex_EnableTransmitter()` /
`HAL_HalfDuplex_EnableReceiver()` to switch direction.

## Echo
In half-duplex the receiver hears your own transmission unless you disable RE while sending.
Two approaches:
1. Disable RE during TX, re-enable after TC (transfer complete, last stop bit sent).
2. Keep RE on, read back each byte and compare (detects collisions and bus faults), then discard
   the echo before parsing the reply.

## Turnaround timing
The slave may start replying very soon after the request (Dynamixel's Return Delay Time defaults
to 250 us, can be 0). Switch to receive on the **TC** interrupt, not TXE, and do it in the ISR,
not the main loop. With DMA TX, enable the TC interrupt for the switch.

## Without HDSEL
- Tie TX and RX pins together through a resistor (1k on TX) and use normal full-duplex mode with
  echo handling.
- Use a tri-state buffer (74LVC1G125) driven by a direction GPIO, like RS-485 DE.

## Baud rates
Smart servo buses run at 1-4.5 Mbaud: oversampling by 8 (`CR1.OVER8`) helps reach high rates with
low clock frequencies; check the baud error budget at those rates.

## Verify
- [ ] Logic analyser: no contention (intermediate voltage levels) at the turnaround.
- [ ] Ping/response to each servo ID at the configured return delay works 10k times with zero timeouts.
