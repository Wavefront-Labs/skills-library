---
id: computing-software.firmware-embedded-development.arduino.watchdog-interrupt-hang-diagnosis
name: watchdog-interrupt-hang-diagnosis
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [wdt-interrupt-diagnosis, wdt-interrupt-then-reset, hang-location, return-address, noinit-section, avr-crash-log, arduino, firmware-embedded-development]
level: advanced
status: draft
description: "Find where an AVR sketch hangs: WDT interrupt-then-reset mode, grabbing the return address in WDT_vect, saving it in .noinit or EEPROM, and mapping it with addr2line."
sources:
  - https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf
  - https://www.nongnu.org/avr-libc/user-manual/mem_sections.html
  - https://github.com/Megunolink/ArduinoCrashMonitor
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Watchdog interrupt hang diagnosis

AVR has no fault registers or debugger on most boards. The watchdog's **interrupt + system reset**
mode gives you one interrupt just before the reset: enough to record where the code was stuck.

## Configure interrupt-then-reset
```cpp
#include <avr/wdt.h>
void wdtStart2s() {
  cli(); wdt_reset();
  WDTCSR = _BV(WDCE) | _BV(WDE);
  WDTCSR = _BV(WDIE) | _BV(WDE) | _BV(WDP2) | _BV(WDP1) | _BV(WDP0);   // ~2 s, interrupt then reset
  sei();
}
```
The hardware clears WDIE when the interrupt fires; if nothing re-arms it, the next timeout resets.

## Capture the address
On AVR the interrupt pushes the return address (the PC of the interrupted code) onto the stack;
GCC's ISR prologue then pushes registers. A naked ISR reads it before anything else is pushed:
```cpp
struct Crash { uint16_t magic; uint32_t addr; } __attribute__((section(".noinit")));
Crash crash __attribute__((section(".noinit")));

ISR(WDT_vect, ISR_NAKED) {
  uint8_t *sp = (uint8_t *)SP;              // SP points one below the last pushed byte
  // 328P (16-bit PC): sp[1] = PC high byte, sp[2] = PC low byte. Mega2560 (3-byte PC): sp[1..3].
  crash.addr = ((uint16_t)sp[1] << 8) | sp[2];
  crash.magic = 0xDEAD;
  while (1) {}                               // wait for the reset
}
```
The stacked value is a **word** address; multiply by 2 for the byte address used by tools.
Reading SP via the `SP` macro in a naked ISR is safe because nothing has been pushed.

## Report on next boot
```cpp
void setup() {
  Serial.begin(115200);
  if (crash.magic == 0xDEAD) {
    Serial.print(F("WDT hang at 0x")); Serial.println(crash.addr * 2, HEX);
    crash.magic = 0;                         // .noinit survives reset, not power loss
  }
  wdtStart2s();
}
```
For power-loss survival, write to EEPROM in the ISR instead (a few ms; fine before reset).

## Map to source
```sh
avr-addr2line -f -C -e build/sketch.ino.elf 0x1a2c
avr-objdump -d -S build/sketch.ino.elf | less     # look around the address
```
Get the ELF with `arduino-cli compile --output-dir` or the IDE's temp build folder (verbose).

## Interpreting
Address in `twi_*` / `Wire` = I2C bus hang (lockup waiting on TWINT); in `HardwareSerial::write` =
TX buffer full with interrupts disabled; in your loop = infinite loop or blocking wait. The
ArduinoCrashMonitor library packages this approach.

## Verify
- [ ] Deliberate `while(1)` in a known function reports that function after reset.
