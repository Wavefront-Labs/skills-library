---
id: computing-software.firmware-embedded-development.arduino.avr-pin-change-interrupts
name: avr-pin-change-interrupts
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [pin-change-interrupt, pcint, pcicr, pcmsk, attachinterrupt-limits, enableinterrupt-library, avr, arduino, firmware-embedded-development]
level: practitioner
status: draft
description: "Interrupt on any AVR pin with pin-change interrupts: PCICR/PCMSK setup, one vector per port, finding which pin changed, edge detection in software, and wake from sleep."
sources:
  - https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf
  - https://docs.arduino.cc/language-reference/en/functions/external-interrupts/attachInterrupt/
  - https://github.com/GreyGnome/EnableInterrupt
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pin change interrupts (AVR)

`attachInterrupt()` on an Uno only works on pins 2 and 3 (INT0/INT1). Every other pin can raise a
**pin change interrupt** (PCINT): any edge, grouped per port.

## Groups on ATmega328P
| Vector | Enable bit | Mask reg | Arduino pins |
|---|---|---|---|
| `PCINT0_vect` | PCICR.PCIE0 | PCMSK0 | D8-D13 (PB0-PB5) |
| `PCINT1_vect` | PCICR.PCIE1 | PCMSK1 | A0-A5 (PC0-PC5) |
| `PCINT2_vect` | PCICR.PCIE2 | PCMSK2 | D0-D7 (PD0-PD7) |
Use `digitalPinToPCICR(pin)`, `digitalPinToPCICRbit(pin)`, `digitalPinToPCMSK(pin)`,
`digitalPinToPCMSKbit(pin)` macros for portable code across AVR boards.

## Setup and edge detection
```cpp
volatile uint8_t lastB; volatile uint16_t pulses;
void setup() {
  pinMode(8, INPUT_PULLUP); pinMode(9, INPUT_PULLUP);
  lastB = PINB;
  PCMSK0 |= _BV(PCINT0) | _BV(PCINT1);   // D8, D9
  PCIFR  |= _BV(PCIF0);                   // clear stale flag
  PCICR  |= _BV(PCIE0);
}
ISR(PCINT0_vect) {
  uint8_t now = PINB, changed = now ^ lastB; lastB = now;
  if ((changed & _BV(0)) && !(now & _BV(0))) pulses++;   // D8 falling edge
  if (changed & _BV(1)) { /* D9 changed either way */ }
}
```
Read the port once at the start of the ISR; compare with the previous snapshot to find which pins
changed and in which direction.

## Pitfalls
- A short pulse (shorter than ISR latency, a few us) can toggle and return before the ISR reads the
  port: the change is seen but both levels look equal. Use INT0/INT1 or input capture for narrow
  pulses.
- Multiple pins in one group share a vector; heavy ISRs delay all of them.
- Libraries define PCINT vectors too (SoftwareSerial defines all three on AVR): "multiple definition
  of `__vector_3`" link errors. Use EnableInterrupt/PinChangeInterrupt libraries that coexist, or
  avoid SoftwareSerial.
- Variables shared with `loop()` must be `volatile`; read multi-byte ones with interrupts disabled
  (`noInterrupts(); uint16_t p = pulses; interrupts();`).

## Wake from sleep
Pin change interrupts wake the 328P from power-down (they are asynchronous), unlike INT0/INT1 edge
modes which need a clock (only LOW level wakes from power-down on INT0/1). Good for button wake on
any pin.

## Verify
- [ ] Edge counting matches a function generator up to the intended rate.
- [ ] No link conflicts with other libraries' PCINT vectors.
