---
id: computing-software.firmware-embedded-development.device-driver-development.uart-auto-baud-detection
name: uart-auto-baud-detection
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [auto-baud, uart, abr, baud-detection, bootloader-sync, firmware-embedded-development]
level: practitioner
status: draft
description: "Detect an unknown UART baud rate with hardware auto-baud (STM32 ABR modes, 0x7F/0x55 sync chars) or timer input capture, and validate the result before use."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Auto-baud detection

Used by bootloaders (the host picks the baud rate), LIN slaves, and devices that must talk to
legacy equipment configured at unknown rates.

## Hardware auto-baud (STM32 USART v2)
```c
USART1->CR1 &= ~USART_CR1_UE;
USART1->CR2 |= USART_CR2_ABREN | (mode << USART_CR2_ABRMODE_Pos);
USART1->CR1 |= USART_CR1_UE | USART_CR1_RE;
while (!(USART1->ISR & (USART_ISR_ABRF | USART_ISR_ABRE))) {}
if (USART1->ISR & USART_ISR_ABRE) { /* failed: request again */ USART1->RQR = USART_RQR_ABRRQ; }
/* BRR now holds the measured divisor */
```
| ABRMODE | Measures | Host must send |
|---|---|---|
| 0 | start bit length | any character whose first data bit (LSB) is 1 |
| 1 | falling edge to falling edge (start + first bit) | any character starting with the bit pattern 10 |
| 2 | 0x7F frame | 0x7F |
| 3 | 0x55 frame | 0x55 |
Mode 2 with 0x7F is what the STM32 ROM bootloader expects (AN2606). Mode 3 (0x55 has many
edges) is most accurate. The measuring character is consumed; it appears in RDR in some modes.

Range is limited by the USART clock: at fCK = 80 MHz and oversampling 16, rates from about
1.2 kbaud up to fCK/16. Low rates may overflow BRR (16 bits).

## Software method (timer input capture)
Route RX to a timer channel (or use EXTI + free-running timer), capture falling edges of a known
sync character, take the **shortest** interval between edges as one bit time (0x55 gives
alternating bits), then snap to the nearest standard rate:
```c
static const uint32_t std[] = { 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600 };
uint32_t measured = timer_hz / min_bit_ticks;
/* pick the standard rate within 3%; reject otherwise */
```

## Validate
After detection, require a second known byte (or a protocol ACK exchange) at the detected rate
before trusting it; noise on RX during detection produces a confident wrong answer. Re-run
detection after framing errors or long idle (host may have changed rates).

## Verify
- [ ] Detection succeeds at every supported rate, with host clock tolerance +-2%.
- [ ] Garbage before the sync character yields ABRE/retry, not a wrong baud rate.
