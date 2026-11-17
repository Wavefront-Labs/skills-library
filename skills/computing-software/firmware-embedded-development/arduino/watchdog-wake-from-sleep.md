---
id: computing-software.firmware-embedded-development.arduino.watchdog-wake-from-sleep
name: watchdog-wake-from-sleep
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [wdt-sleep-wake, wdt-interrupt-mode, power-down-sleep, wdie, low-power-library, avr-sleep, arduino, firmware-embedded-development]
level: practitioner
status: draft
description: "Use the AVR watchdog as a periodic wake timer from power-down sleep: WDT interrupt mode, 8 s maximum and drift, multi-cycle sleeps, the LowPower library, and current figures."
sources:
  - https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf
  - https://www.nongnu.org/avr-libc/user-manual/group__avr__watchdog.html
  - https://github.com/rocketscream/Low-Power
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Watchdog wake from sleep (AVR)

In power-down mode the ATmega328P stops all clocks except the watchdog's 128 kHz oscillator. Using
the WDT in **interrupt mode** gives a wake timer at ~4-6 uA total (bare chip, BOD off).

## Register setup
```cpp
#include <avr/sleep.h>
#include <avr/wdt.h>
#include <avr/interrupt.h>
volatile bool wdt_fired;
ISR(WDT_vect) { wdt_fired = true; }

void wdtInterrupt8s() {
  cli();
  MCUSR &= ~_BV(WDRF);
  WDTCSR = _BV(WDCE) | _BV(WDE);                    // timed sequence: 4 cycles to change
  WDTCSR = _BV(WDIE) | _BV(WDP3) | _BV(WDP0);       // interrupt only, ~8 s
  sei();
}
void sleep8s() {
  wdtInterrupt8s();
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  ADCSRA &= ~_BV(ADEN);                              // ADC off saves ~100+ uA
  cli(); sleep_enable();
  sleep_bod_disable();                               // BOD off during sleep (328P picoPower)
  sei(); sleep_cpu();                                // must follow bod_disable within 3 cycles
  sleep_disable();
}
```
Prescaler options: 16 ms to 8 s (WDP bits). For longer intervals, loop: sleep 8 s N times and
count in the ISR, doing real work only every Nth wake.

## Accuracy
The 128 kHz WDT oscillator varies with voltage and temperature (datasheet: about +/-10% or worse).
An "8 s" sleep can be 7-9 s. For accurate timekeeping use an external RTC (DS3231 alarm on INT0)
or a 32 kHz crystal on Timer2 asynchronous mode (power-save).

## LowPower library
`LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);` wraps the same steps. Rocketscream Low-Power
supports AVR and some SAMD; check for your board.

## Reducing current further
- Disable the ADC (above), analog comparator (`ACSR = _BV(ACD)`), and peripherals via `PRR`.
- On an Arduino Uno board, the USB-serial chip, regulator and power LED draw ~30-50 mA total; sleep
  only pays off on bare ATmega or Pro Mini with LED and regulator removed.
- Set unused pins as INPUT_PULLUP or OUTPUT LOW to avoid floating inputs.

## Gotchas
- WDIE alone: interrupt. WDE + WDIE: interrupt then reset on the next timeout (unless WDIE re-set
  in the ISR). WDE alone: reset. Mixing these up gives unexpected resets.
- After a reset caused by WDT, the WDT stays enabled with the shortest timeout; clear `WDRF` and
  disable early in setup (old bootloaders loop otherwise).

## Verify
- [ ] Measured sleep current matches expectation with all peripherals off.
- [ ] Wake interval measured over an hour to calibrate the N-loop count.
