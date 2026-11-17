---
id: computing-software.firmware-embedded-development.arduino.avr-timer-registers
name: avr-timer-registers
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [avr-registers, avr-timer-registers, tccr1a, tccr1b, ocr1a, ctc-mode, fast-pwm, timer0-millis, timer-conflicts, firmware-embedded-development]
level: advanced
status: draft
description: "Program ATmega328P timers directly (CTC interrupts, custom-frequency PWM, input capture) without breaking millis(), Servo, tone() or analogWrite that the Arduino core already owns."
sources:
  - https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf
  - https://github.com/arduino/ArduinoCore-avr/blob/master/cores/arduino/wiring.c
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AVR timer registers

**Goal:** precise periodic interrupts and PWM frequencies on Uno-class boards, knowing which
timer each Arduino feature already uses.

## Who owns what (ATmega328P)
| Timer | Bits | Used by core/libraries | PWM pins |
|---|---|---|---|
| Timer0 | 8 | `millis()`, `micros()`, `delay()` (overflow ISR, fast PWM, /64) | D5, D6 |
| Timer1 | 16 | `Servo` library, many libraries (TimerOne) | D9, D10 |
| Timer2 | 8 | `tone()` | D3, D11 |
**Don't reconfigure Timer0** unless you give up millis/delay. Changing Timer1 breaks Servo and
analogWrite on D9/D10; Timer2 conflicts with tone() and D3/D11 PWM.

## 1 kHz interrupt with Timer1 in CTC mode
```cpp
void setup() {
  noInterrupts();
  TCCR1A = 0;
  TCCR1B = _BV(WGM12) | _BV(CS11) | _BV(CS10);   // CTC (TOP = OCR1A), prescaler 64
  OCR1A = 249;                                   // 16 MHz / 64 / (249+1) = 1000 Hz
  TCNT1 = 0;
  TIMSK1 = _BV(OCIE1A);
  interrupts();
}
ISR(TIMER1_COMPA_vect) { tick++; }
```
Formula: `f = F_CPU / (prescaler * (OCR + 1))`. Reset `TCCR1A` explicitly: the core's
`init()` pre-configures timers for analogWrite, so leftover bits give wrong modes.

## Custom PWM frequency (Timer1, mode 14: fast PWM, TOP = ICR1)
```cpp
TCCR1A = _BV(COM1A1) | _BV(WGM11);
TCCR1B = _BV(WGM13) | _BV(WGM12) | _BV(CS10);   // no prescale
ICR1 = 799;                                     // 16 MHz / 800 = 20 kHz
OCR1A = 400;                                    // 50 % on D9
```

## 16-bit register access
16-bit registers (TCNT1, OCR1A, ICR1) use a shared TEMP byte: reading/writing them from both
main code and an ISR without disabling interrupts can corrupt values. Access inside
`ATOMIC_BLOCK` when an ISR also touches any 16-bit timer register.

## Input capture (Timer1, ICP1 = D8)
`TCCR1B |= _BV(ICES1)` (rising edge), `TIMSK1 |= _BV(ICIE1)`, read `ICR1` in
`ISR(TIMER1_CAPT_vect)`: hardware timestamps with 62.5 ns resolution at 16 MHz.

## Verify
- [ ] Scope confirms frequency; `millis()` still correct after your changes (Timer0 untouched).
- [ ] Libraries in use checked for timer ownership (grep for `TCCR1`, `TIMER1_` in their sources).
