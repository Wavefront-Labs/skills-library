---
id: computing-software.firmware-embedded-development.arduino.analogread-and-analogwrite
name: analogread-and-analogwrite
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [analogwrite, analogread, analogreference, analogreadresolution, pwm-frequency, adc-reference, arduino, firmware-embedded-development]
level: intro
status: docs-checked
description: "Use analogRead and analogWrite correctly across Arduino cores: reference voltages, resolution, PWM-capable pins and frequencies, timer conflicts, and ESP32/RP2040 differences."
sources:
  - https://github.com/arduino/reference-en/blob/master/Language/Functions/Analog%20IO/analogRead.adoc
  - https://github.com/arduino/reference-en/blob/master/Language/Functions/Analog%20IO/analogWrite.adoc
  - https://github.com/arduino/reference-en/blob/master/Language/Functions/Analog%20IO/analogReference.adoc
  - https://github.com/arduino/reference-en/blob/master/Language/Functions/Analog%20IO/analogWriteResolution.adoc
  - https://github.com/espressif/arduino-esp32/blob/master/docs/en/api/adc.rst
  - https://github.com/espressif/arduino-esp32/blob/master/docs/en/api/ledc.rst
  - https://github.com/arduino/docs-content/blob/main/content/learn/02.microcontrollers/01.digital-pins/digital-pins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# analogRead and analogWrite

## analogRead
- Uno/Nano (ATmega328P): 10-bit (0-1023), ~100 us per read, reference = AVcc (5 V) by default.
  `value * 5.0 / 1023.0` is the usual conversion (or `/1024` with the datasheet's definition; the
  difference is below one LSB).
- `analogReference(INTERNAL)` = 1.1 V on the ATmega168/328P; `INTERNAL2V56` is a Mega-only option (2.56 V);
  `EXTERNAL` uses the voltage on the AREF pin (0 to 5 V only). **If you apply an external voltage to AREF,
  call `analogReference(EXTERNAL)` before any `analogRead()`**; otherwise the active internal reference is
  shorted to the AREF voltage (the reference suggests a 5 k series resistor if you need to switch).
- Boards with more than 10-bit ADCs (Zero, Due, MKR family, Nano 33, Portenta) keep 10 bits by default;
  call `analogReadResolution(bits)` for more.
- ESP32 core: default ADC resolution is 12 bits; set attenuation per pin with
  `analogSetPinAttenuation(pin, ADC_11db)`; `analogReadMilliVolts()` returns a calibrated value in millivolts
  while `analogRead()` is raw (non-calibrated).

## analogWrite (PWM)
- Only on PWM pins (Uno, Nano and Mini: 3, 5, 6, 9, 10, 11). Value 0-255 by default.
- Frequencies on those boards: 490 Hz, with pins 5 and 6 at 980 Hz; other boards differ (see the reference table).
- Pins 5 and 6 share the timer used by `millis()` and `delay()`, so low duty cycles on them are higher than
  expected. `tone()` interferes with PWM on pins 3 and 11.
- `analogWriteResolution(bits)` is an extension for the Due, Zero and MKR family (default 8 bits).
- ESP32 core: `analogWrite()` exists (documented under the LEDC API); for control use
  `ledcAttach(pin, freq, resolution)` and `ledcWrite(pin, duty)`.
- PWM is not an analog voltage: add an RC filter for DC, and drive motors and LEDs through a transistor or
  driver; ATmega pins can source or sink up to 40 mA.

## Changing PWM frequency on AVR
Done through the timer registers of the pin's timer; see the AVR timer register skill. Changing the timer
that `millis()` uses affects timekeeping.

## Verify
- [ ] Measured voltage at a known divider matches `analogRead` conversion within 1-2 LSB.
- [ ] PWM frequency checked on a scope after adding libraries that use timers.

## Checked

Date: 2026-10-25. Documentation release: Arduino language reference (reference-en, last commit 2025-04-11); arduino-esp32 API docs (latest commit 2026-10-20); Arduino digital pins tutorial.

Confirmed: analogRead is 10-bit on the ATmega boards, takes about 100 microseconds, and the default `analogRead()` resolution of 12-bit capable boards stays 10 bits (`analogReadResolution()` for Zero, Due, MKR, Nano 33 and Portenta); `analogReference` options (DEFAULT, INTERNAL 1.1 V on ATmega168/328P, INTERNAL2V56 on the Mega only, EXTERNAL) and the AREF warning (use EXTERNAL before `analogRead()` when an external voltage is applied, otherwise the active reference is shorted); PWM pins and frequencies (Uno class 3, 5, 6, 9, 10, 11 at 490 Hz, pins 5 and 6 at 980 Hz; pins 5 and 6 share the `millis()`/`delay()` timer); `tone()` interferes with PWM on pins 3 and 11; ATmega pins source or sink up to 40 mA; ESP32 `analogReadMilliVolts()` returns a calibrated value, `analogSetPinAttenuation`, `ADC_11db`, default 12-bit ADC resolution, `ledcAttach(pin, freq, resolution)`, `ledcWrite(pin, duty)` and an `analogWrite()` in the LEDC API. Removed unconfirmed claims: the AREF settling remark, source-impedance limits, ESP32 ADC non-linearity and ADC2 and Wi-Fi remarks, the ESP32 2.x function names, Servo timer use, RP2040 and ESP8266 resolution and frequency functions, the 20 mA figure and the register example for changing PWM frequency.

Method: documentation only; no commands were run.
