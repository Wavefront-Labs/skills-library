---
id: computing-software.firmware-embedded-development.arduino.avr-sleep-modes
name: avr-sleep-modes
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [avr-registers, avr-sleep, power-down, set-sleep-mode, watchdog-wake, adc-disable, prr, bod-disable-in-sleep, pro-mini-low-power, firmware-embedded-development]
level: practitioner
status: draft
description: "Get ATmega328P boards down to microamps: power-down sleep, wake by watchdog or pin interrupt, ADC/BOD/peripheral shutdown, and the board-level parts that ruin it."
sources:
  - https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf
  - https://www.nongnu.org/avr-libc/user-manual/group__avr__sleep.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AVR sleep modes

**Goal:** a battery-powered ATmega328P sensor that sleeps at ~1-5 uA and wakes on a timer or
an external event.

## Modes (ATmega328P)
| Mode | Running | Typical current (3 V) |
|---|---|---|
| Idle | timers, UART, ADC | mA |
| ADC noise reduction | ADC, async timer2, WDT | |
| Power-save | Timer2 async (32 kHz crystal) + WDT | ~1 uA + timer |
| **Power-down** | WDT, pin change/INT0/INT1, TWI address match | ~0.1-0.5 uA (+ WDT ~4-6 uA if on) |

## Sleep with watchdog wake (~8 s max per cycle)
```cpp
#include <avr/sleep.h>
#include <avr/wdt.h>
#include <avr/power.h>
ISR(WDT_vect) { }                         // just wake
void sleep_8s() {
  ADCSRA &= ~_BV(ADEN);                   // ADC off (saves ~200 uA)
  MCUSR &= ~_BV(WDRF);
  WDTCSR = _BV(WDCE) | _BV(WDE);          // timed sequence
  WDTCSR = _BV(WDIE) | _BV(WDP3) | _BV(WDP0);   // interrupt mode, 8 s
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  noInterrupts();
  sleep_enable();
  sleep_bod_disable();                    // BOD off during sleep (picoPower parts), must be just before sleep
  interrupts();
  sleep_cpu();
  sleep_disable();
  ADCSRA |= _BV(ADEN);
}
```
Wake on a button with `attachInterrupt(digitalPinToInterrupt(2), isr, LOW)` (power-down only
wakes on **level** for INT0/INT1, or pin-change interrupts on any pin).

## Board parts that dominate current
Arduino Uno/Nano boards never get below ~10-40 mA in sleep because of the USB-serial chip,
power LED and linear regulator. For low power: a Pro Mini (3.3 V/8 MHz) with the power LED and
regulator removed, or a bare ATmega328P on your own board; then the MCU numbers apply.

## Other savings
- `power_all_disable()` / `PRR` bits off for unused peripherals while awake.
- Set unused pins as inputs with pull-ups (or outputs low) to avoid floating-input current.
- Run at 8 MHz or lower and lower voltage (1.8-3.3 V within the speed grade).
- WDT timing is +/-10 % or worse over temperature; for accurate time use Timer2 asynchronously
  with a 32.768 kHz crystal in power-save mode.

## Verify
- [ ] Measure sleep current with a uCurrent/PPK2: < 10 uA with WDT on (bare MCU).
- [ ] Wake reliably from WDT and the button for 1000 cycles.
