---
id: computing-software.firmware-embedded-development.arduino.non-blocking-sketch-structure
name: non-blocking-sketch-structure
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino, arduino-ide, sketch, millis, micros, delay, non-blocking, state-machine, cooperative-multitasking, timer-rollover, unsigned-arithmetic, volatile, isr, attachinterrupt, nointerrupts, serial-debugging, f-macro, progmem, sram, avr, atmega328p, string-fragmentation, heap, debounce, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Structure Arduino sketches around millis() state machines instead of delay(): rollover-safe timing, ISR-safe volatile data, Serial debugging and AVR RAM hygiene (F(), no String)."
sources:
  - https://docs.arduino.cc/language-reference/
  - https://docs.arduino.cc/built-in-examples/digital/BlinkWithoutDelay/
  - https://docs.arduino.cc/learn/programming/memory-guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
updated: 2026-10-14
---

# Non-blocking sketch structure — many jobs, one loop(), no delay()

**Goal:** a sketch that blinks, reads sensors, debounces buttons and talks Serial at the
same time, keeps timing correct across the `millis()` rollover, and does not run out of
RAM on a 2 KB AVR.

## 1. Why delay() has to go
`delay(500)` spins the CPU for 500 ms; nothing else in `loop()` runs, buttons are missed
and Serial input piles up (the AVR core's RX buffer is 64 bytes by default). Rule: `loop()`
must return quickly (aim for well under 1 ms per pass) and every job checks "is it my
time yet?" instead of waiting.

## 2. The rollover-safe timing pattern
`millis()` is an `unsigned long` (32-bit) and wraps after about 49.7 days. Always compare
an *elapsed* interval, computed by unsigned subtraction, never an absolute deadline:

```cpp
unsigned long lastBlink = 0;
const unsigned long BLINK_MS = 250;

void loop() {
  unsigned long now = millis();
  if (now - lastBlink >= BLINK_MS) {   // correct across wrap
    lastBlink += BLINK_MS;              // += keeps cadence; = now drifts
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  }
  pollButton(now);
  pollSerial();
}
```

Gotchas:
- `if (millis() > deadline)` breaks at the wrap. `now - last >= interval` does not, because
  unsigned subtraction is modulo 2^32.
- Keep the variables `unsigned long`. Storing `millis()` in `int` (16-bit on AVR) wraps after
  about 32 s and goes negative.
- `micros()` wraps after about 70 minutes and on 16 MHz boards has 4 µs resolution.

## 3. Turn sequences into state machines
A sequence such as "valve on 2 s, wait 5 s, read sensor" becomes an `enum` plus a switch:

```cpp
enum class Pump : uint8_t { Idle, Running, Settling };
Pump state = Pump::Idle; unsigned long t0;

void pumpTask(unsigned long now) {
  switch (state) {
    case Pump::Idle:     if (startRequested) { digitalWrite(PUMP, HIGH); t0 = now; state = Pump::Running; } break;
    case Pump::Running:  if (now - t0 >= 2000) { digitalWrite(PUMP, LOW); t0 = now; state = Pump::Settling; } break;
    case Pump::Settling: if (now - t0 >= 5000) { readSensor(); state = Pump::Idle; } break;
  }
}
```

Each task owns its state and timestamps; `loop()` just calls every task. Debounce buttons the
same way: accept a new level only after it has been stable for ~20–50 ms.

## 4. Interrupts and volatile
- Variables shared between an ISR (`attachInterrupt(digitalPinToInterrupt(pin), isr, FALLING)`)
  and `loop()` must be `volatile`, or the compiler may cache them in a register.
- On 8-bit AVR, reading a multi-byte variable (e.g. a `volatile unsigned long` counter) is not
  atomic. Copy it with interrupts off: `noInterrupts(); unsigned long c = count; interrupts();`.
- Keep ISRs tiny: set a flag or bump a counter. No `Serial.print`, no `delay()`; `millis()`
  does not advance inside an ISR on AVR.

## 5. Serial debugging without wrecking timing
- `Serial.begin(115200);` — slower baud means `print` blocks once the TX buffer is full. Heavy logging changes timing; gate it with a `#define DEBUG 1` macro.
- On native-USB boards (Leonardo, many SAMD/RP2040 boards) `while (!Serial) {}` waits forever
  without a host. Add a timeout or remove it for field builds.
- Read input non-blockingly: `while (Serial.available()) { char c = Serial.read(); ... }`
  and assemble lines into a fixed `char` buffer.

## 6. RAM hygiene on AVR (ATmega328P has 2 KB SRAM)
- String literals are copied into SRAM at startup. Wrap print-only literals in `F("...")` to
  keep them in flash; use `PROGMEM` for large constant tables.
- Avoid the `String` class in long-running sketches: repeated concatenation fragments the
  small heap, and failures surface as random resets days later. Use a fixed `char buf[32]` with `snprintf`.

On ESP32/RP2040 cores RAM is far larger, but the timing pattern is identical. For a sketch
that outgrows one loop, see computing-software.firmware-embedded-development.freertos.task-and-queue-design;
for multi-board builds, computing-software.firmware-embedded-development.platformio.multi-environment-builds-and-ci.

## Verify
- [ ] `grep -n "delay(" ` finds no calls in `loop()` paths (setup-only is acceptable).
- [ ] Every timing comparison has the form `now - last >= interval` with `unsigned long` operands.
- [ ] Every ISR-shared variable is `volatile` and multi-byte reads are wrapped in `noInterrupts()`.
- [ ] Measured `loop()` pass time (toggle a pin, view on a scope or log `micros()` deltas) stays under your tightest deadline.
- [ ] AVR build reports enough free SRAM and no `String` objects are built in `loop()`.
- [ ] The board boots and runs with no USB host attached.

## Checked
2026-11-01. Confirmed in the arduino/reference-en repo: `millis()` overflow after about 50 days, `micros()` overflow after
about 70 minutes with 4 µs resolution on 16 MHz boards, the 64-byte serial receive buffer, `millis()` not incrementing and
`delay()` not working inside an ISR, `volatile` for ISR-shared variables. Removed the TX buffer size, the `snprintf` `%f` note
and the IDE memory-line claim (not confirmed). `F()`, `PROGMEM` and `String` fragmentation are standard Arduino guidance
not re-verified here.
Method: documentation only; no commands were run.
