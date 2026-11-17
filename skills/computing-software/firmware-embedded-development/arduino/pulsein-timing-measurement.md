---
id: computing-software.firmware-embedded-development.arduino.pulsein-timing-measurement
name: pulsein-timing-measurement
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [pulsein, pulseinlong, hc-sr04, rc-receiver-pwm, input-capture, micros, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Measure pulse widths with pulseIn/pulseInLong: timeouts, blocking cost, accuracy with interrupts on, HC-SR04 and RC receiver examples, and when to switch to input capture."
sources:
  - https://github.com/arduino/reference-en/blob/master/Language/Functions/Advanced%20IO/pulseIn.adoc
  - https://github.com/arduino/reference-en/blob/master/Language/Functions/Advanced%20IO/pulseInLong.adoc
  - https://github.com/arduino/reference-en/blob/master/Language/Functions/Time/micros.adoc
  - https://github.com/arduino/ArduinoCore-avr/blob/master/cores/arduino/wiring_pulse.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pulseIn timing measurement

`pulseIn(pin, HIGH, timeout_us)` waits for the pin to go HIGH, times until it goes LOW, and returns
the width in microseconds, or 0 on timeout (default 1 s).

## Basics
```cpp
// HC-SR04 ultrasonic
digitalWrite(TRIG, LOW); delayMicroseconds(2);
digitalWrite(TRIG, HIGH); delayMicroseconds(10); digitalWrite(TRIG, LOW);
unsigned long us = pulseIn(ECHO, HIGH, 30000UL);   // timeout: microseconds to wait for the pulse to start
// convert us to distance with the formula in the sensor's datasheet
```
```cpp
// RC receiver channel
unsigned long w = pulseIn(CH1, HIGH, 25000UL);
if (w == 0) failsafe();
```

## pulseIn vs pulseInLong
- `pulseIn` times by counting loop iterations (about 16 clock cycles each on AVR); the reference says its
  timing was determined empirically, works from 10 microseconds to 3 minutes and will probably show errors
  in longer pulses. The AVR source notes it performs better with interrupts disabled.
- `pulseInLong` relies on `micros()` (4 microsecond resolution on 16 MHz boards), can only be used with
  interrupts enabled, and is better for long pulses and interrupt-affected scenarios.

## Costs and pitfalls
- **Blocking:** the call waits for the pulse; with the default one-second timeout a disconnected
  sensor stalls `loop()`. Always pass a timeout.
- Interrupts (Serial, the millis tick, other libraries) disturb the measured width of `pulseIn`;
  use `pulseInLong` or an interrupt-based method when that matters.
- Several channels measured in sequence miss frames; each call waits for its own pulse.

## Better: interrupts or input capture
- **Pin-change / attachInterrupt:** record `micros()` on CHANGE and compute widths in the handler; reads
  many channels at once and does not block (resolution is that of `micros()`, 4 microseconds on 16 MHz boards).
- **Hardware input capture** on a timer, where the chip has it, latches the timer on the edge and is not
  affected by interrupt latency (see the chip's datasheet).

## Verify
- [ ] Width measured against a function generator at the expected range.
- [ ] Sketch stays responsive with the sensor unplugged (timeout path).

## Checked

Date: 2026-10-25. Documentation release: Arduino language reference (reference-en, last commit 2025-04-11); ArduinoCore-avr wiring_pulse.c (latest commit 2026-07-01).

Confirmed: `pulseIn(pin, value, timeout)` returns the pulse length in microseconds or 0, the timeout is the time to wait for the pulse to start with a default of one second, timing was determined empirically and works for 10 microseconds to 3 minutes; the AVR implementation counts loop iterations of about 16 clock cycles and the source says it performs better with interrupts disabled; `pulseInLong()` is better for long pulses and interrupt-affected cases, relies on `micros()` and can be used only with interrupts enabled; `micros()` has 4 microsecond resolution on 16 MHz boards. Removed unconfirmed claims: the HC-SR04 range and conversion factor, RC receiver pulse widths, the "2 x timeout" figure, Timer1 input capture resolution and register recipe, and the ESP32 and RP2040 peripherals.

Method: documentation only; no commands were run.
