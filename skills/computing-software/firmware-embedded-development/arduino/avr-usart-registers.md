---
id: computing-software.firmware-embedded-development.arduino.avr-usart-registers
name: avr-usart-registers
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [avr-usart, ubrr, u2x, baud-error, usart-rx-interrupt, ring-buffer, hardwareserial, avr, arduino, firmware-embedded-development]
level: advanced
status: draft
description: "Program the AVR USART without HardwareSerial: UBRR and U2X baud maths and error, frame format, interrupt-driven RX ring buffer, and why 115200 at 16 MHz is marginal."
sources:
  - https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf
  - https://www.nongnu.org/avr-libc/user-manual/group__util__setbaud.html
  - https://github.com/arduino/ArduinoCore-avr/blob/master/cores/arduino/HardwareSerial.cpp
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AVR USART registers

## Baud rate
`UBRR = F_CPU / (16 x baud) - 1` (normal) or `F_CPU / (8 x baud) - 1` with `U2X0 = 1`.
At 16 MHz:
| Baud | U2X=0 UBRR / error | U2X=1 UBRR / error |
|---|---|---|
| 9600 | 103 / 0.2% | 207 / 0.2% |
| 57600 | 16 / 2.1% | 34 / -0.8% |
| 115200 | 8 / -3.5% | 16 / 2.1% |
Keep total error (both sides) under ~2%. 115200 at 16 MHz is 2.1% even with U2X; it works with
FTDI/CH340 adapters (accurate clocks) but fails talking to another AVR or at temperature. Use
76800/250000/500000/1000000 (0% error at 16 MHz) between AVRs, or a 14.7456 MHz crystal.
avr-libc `<util/setbaud.h>` computes UBRR and U2X at compile time and warns about error.

## Init and polled I/O
```cpp
#define BAUD 250000
#include <util/setbaud.h>
void uartInit() {
  UBRR0H = UBRRH_VALUE; UBRR0L = UBRRL_VALUE;
#if USE_2X
  UCSR0A |= _BV(U2X0);
#else
  UCSR0A &= ~_BV(U2X0);
#endif
  UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);               // 8N1
  UCSR0B = _BV(RXEN0) | _BV(TXEN0) | _BV(RXCIE0);   // RX interrupt
}
void uartPut(uint8_t c) { while (!(UCSR0A & _BV(UDRE0))) {} UDR0 = c; }
```

## RX ring buffer
```cpp
volatile uint8_t rxb[64]; volatile uint8_t head, tail;   // size power of two
ISR(USART_RX_vect) {
  uint8_t st = UCSR0A, c = UDR0;                    // read status before data
  if (st & (_BV(FE0) | _BV(DOR0))) return;          // framing error or overrun
  uint8_t n = (head + 1) & 63; if (n != tail) { rxb[head] = c; head = n; }
}
int uartGet() { if (head == tail) return -1; uint8_t c = rxb[tail]; tail = (tail + 1) & 63; return c; }
```
Single-byte indices are atomic on AVR, so no interrupt masking is needed for this SPSC buffer.

## Conflicts with Arduino
`HardwareSerial` defines `USART_RX_vect` and `USART_UDRE_vect` if `Serial` is referenced anywhere
(including libraries). Defining them yourself then gives "multiple definition of `__vector_18`".
Don't use `Serial` in the same build, or build outside Arduino.

## Verify
- [ ] Loopback at the target baud for 1 MB of random data without errors.
- [ ] Overrun flag never set under worst-case ISR load.
