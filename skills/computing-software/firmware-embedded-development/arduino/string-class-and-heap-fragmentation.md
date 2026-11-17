---
id: computing-software.firmware-embedded-development.arduino.string-class-and-heap-fragmentation
name: string-class-and-heap-fragmentation
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-string, heap-fragmentation, f-macro, progmem, snprintf, free-memory, char-array, arduino, firmware-embedded-development]
level: practitioner
status: draft
description: "Avoid Arduino String crashes on small RAM: how concatenation fragments the heap, reserve(), char buffers with snprintf, F() and PROGMEM strings, and measuring free memory."
sources:
  - https://docs.arduino.cc/language-reference/en/variables/data-types/stringObject/
  - https://docs.arduino.cc/learn/programming/memory-guide/
  - https://www.nongnu.org/avr-libc/user-manual/pgmspace.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# String class and heap fragmentation

An ATmega328P has 2 KB of SRAM shared by globals, heap and stack. `String` allocates on the heap
and reallocates on every growth; long-running sketches fragment the heap until an allocation
fails or the heap collides with the stack. The result is random resets, garbage output, or silent
truncation (failed concatenation leaves the String unchanged/invalid).

## Patterns that hurt
```cpp
String msg = "T=" + String(temp) + " H=" + String(hum);  // several temporaries per call
void loop() { String line; while (Serial.available()) line += (char)Serial.read(); }
```

## Safer options
1. **Fixed char buffers + snprintf:**
   ```cpp
   char msg[32];
   snprintf(msg, sizeof msg, "T=%d.%d H=%u", t10 / 10, abs(t10 % 10), hum);
   ```
   AVR `printf` family lacks `%f` by default; format integers (fixed-point) or use `dtostrf()`.
2. **If you keep String:** `reserve()` once to the maximum size so it never reallocates; avoid
   creating Strings inside loops and passing them by value (pass `const String&`).
3. **Constant strings in flash:** `Serial.println(F("Sensor init failed"));` keeps the literal out
   of RAM. Tables: `const char msg[] PROGMEM = "...";` read with `strcpy_P`, `pgm_read_byte`.
   On ARM/ESP cores flash constants are already not copied to RAM; `F()` is harmless there.
4. **Line input:** fixed buffer and index, terminate on `'\n'`, drop overflow:
   ```cpp
   static char buf[64]; static uint8_t n;
   while (Serial.available()) { char c = Serial.read();
     if (c == '\n') { buf[n] = 0; handle(buf); n = 0; } else if (n < sizeof buf - 1) buf[n++] = c; }
   ```

## Measuring free RAM (AVR)
```cpp
extern char *__brkval; extern char __heap_start;
int freeRam() { char top; return &top - (__brkval ? __brkval : &__heap_start); }
```
Log it periodically; a steady decline means leaks or fragmentation. The IDE's "Global variables use
X bytes" at compile time leaves the rest for heap+stack; stay below ~75% on AVR.
ESP32/ESP8266: `ESP.getFreeHeap()`, `ESP.getMaxAllocHeap()` (largest block, shows fragmentation).

## Verify
- [ ] Sketch runs 24 h with free RAM / largest block stable.
- [ ] No String concatenation in ISR or hot loop paths.
