---
id: computing-software.firmware-embedded-development.arduino.tone-and-timer-conflicts
name: tone-and-timer-conflicts
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-tone, tone, notone, timer2, timer-conflict, buzzer, ir-remote-conflict, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use tone() without breaking other features: which timer it takes per board, PWM pins and libraries it conflicts with (IRremote, Servo), one-tone-at-a-time, and alternatives."
sources:
  - https://github.com/arduino/reference-en/blob/master/Language/Functions/Advanced%20IO/tone.adoc
  - https://github.com/arduino/ArduinoCore-avr/blob/master/cores/arduino/Tone.cpp
  - https://github.com/Arduino-IRremote/Arduino-IRremote/blob/master/src/private/IRTimer.hpp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tone() and timer conflicts

`tone(pin, freq[, duration])` generates a 50% square wave by toggling the pin in a timer ISR.
`noTone(pin)` stops it.

## Which timer
Per the Arduino AVR core's `Tone.cpp`:
- **Uno/Nano (the default branch):** Timer2. The reference says `tone()` interferes with PWM output on
  pins 3 and 11 (on boards other than the Mega).
- **Mega 2560:** Timer2, one tone pin.
- **Leonardo/32U4:** Timer3.
Other cores are not covered here; check their `tone()` implementation.

## Conflicts
- **IRremote** defaults to Timer2 on the AVR boards in its timer file, the same timer `tone()` uses, and its
  source says the receive timer interrupt must be disabled before using the timer for `tone()`. It lets you
  select another timer (`IR_USE_AVR_TIMER1`) before including the library.
- Any library that configures the timer `tone()` uses will conflict with it.
- It is not possible to generate tones lower than 31 Hz.

## Practical rules
- One tone at a time. Calling `tone()` on a second pin while one plays has no effect; call `noTone()` on the
  first pin before using another. Calling it on the same pin sets the frequency.
- `tone(pin, f, ms)` is non-blocking even with a duration, so schedule melodies with `millis()`, not `delay()`.

## Alternatives
- Generate the tone with a hardware timer output on a timer nothing else needs (see the AVR timer register skill).
- On the ESP32 core, `ledcWriteTone(pin, freq)` is documented in the LEDC API.

## Verify
- [ ] Tone frequency measured on a scope; other timer-based features tested while it plays.

## Checked

Date: 2026-10-25. Documentation release: Arduino language reference (reference-en, last commit 2025-04-11); ArduinoCore-avr Tone.cpp (latest commit 2026-07-01); Arduino-IRremote IRTimer.hpp on master.

Confirmed: `tone()` makes a 50% duty square wave, only one tone at a time (a call on a different pin while one plays has no effect; call `noTone()` first), interferes with PWM on pins 3 and 11 (boards other than the Mega), cannot go below 31 Hz, and is non-blocking when a duration is given; the AVR core uses Timer2 by default (Uno class), Timer2 on the ATmega1280/2560 with a single tone pin (the extra timers in the code are commented out), and Timer3 on the ATmega32U4; IRremote selects Timer2 by default on the AVR boards in its timer file and offers `IR_USE_AVR_TIMER1`, and its source notes the receive timer must be disabled before using the timer for `tone()`. Fixed: the Mega can only use one tone pin through the core (Timers 3, 4 and 5 are not allocated). Removed unconfirmed claims: SAMD, ESP32 and RP2040 timer details, the Servo, LED matrix and NewPing conflicts, prescaler granularity, buzzer and resistor advice, the register-level alternative and the toneAC library.

Method: documentation only; no commands were run.
