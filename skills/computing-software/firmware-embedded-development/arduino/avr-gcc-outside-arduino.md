---
id: computing-software.firmware-embedded-development.arduino.avr-gcc-outside-arduino
name: avr-gcc-outside-arduino
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [avr-gcc, avr-libc, makefile, avr-objcopy, avr-size, bare-metal-avr, mmcu, avr, arduino, firmware-embedded-development]
level: practitioner
status: draft
description: "Build AVR firmware with avr-gcc and avr-libc directly: -mmcu and F_CPU, compile/link flags, objcopy to hex, avr-size, a minimal Makefile, and avrdude flashing."
sources:
  - https://www.nongnu.org/avr-libc/user-manual/using_tools.html
  - https://gcc.gnu.org/onlinedocs/gcc/AVR-Options.html
  - https://github.com/avrdudes/avrdude
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# avr-gcc outside Arduino

## Toolchain
Linux: `apt install gcc-avr avr-libc binutils-avr avrdude`. macOS: `brew tap osx-cross/avr && brew
install avr-gcc avrdude`. Windows: Microchip AVR 8-bit toolchain, or reuse the one inside the
Arduino data dir (`packages/arduino/tools/avr-gcc/<ver>/bin`). Newer GCC (12+) generates warnings
for some old avr-libc idioms; Microchip's builds include device packs for new parts (AVR-DA/DB).

## Minimal program
```c
// main.c
#include <avr/io.h>
#include <util/delay.h>
int main(void) {
    DDRB |= _BV(PB5);                    // Uno LED D13
    for (;;) { PORTB ^= _BV(PB5); _delay_ms(500); }
}
```
`_delay_ms` needs `F_CPU` defined and optimisation on, otherwise delays are wrong and large.

## Build
```sh
avr-gcc -mmcu=atmega328p -DF_CPU=16000000UL -Os -std=gnu11 -Wall -Wextra \
  -ffunction-sections -fdata-sections -c main.c -o main.o
avr-gcc -mmcu=atmega328p -Wl,--gc-sections -Wl,-Map,app.map main.o -o app.elf
avr-objcopy -O ihex -R .eeprom app.elf app.hex
avr-objcopy -O ihex -j .eeprom --change-section-lma .eeprom=0 app.elf app.eep
avr-size --mcu=atmega328p -C app.elf      # older binutils; newer: avr-size -A app.elf
```
Add `-flto` for size; Arduino uses it too.

## Minimal Makefile
```make
MCU=atmega328p
F_CPU=16000000UL
CFLAGS=-mmcu=$(MCU) -DF_CPU=$(F_CPU) -Os -Wall -ffunction-sections -fdata-sections
SRC=$(wildcard *.c)
app.hex: app.elf ; avr-objcopy -O ihex -R .eeprom $< $@
app.elf: $(SRC:.c=.o) ; avr-gcc -mmcu=$(MCU) -Wl,--gc-sections $^ -o $@
flash: app.hex ; avrdude -p m328p -c arduino -P $(PORT) -b 115200 -U flash:w:$<:i
clean: ; rm -f *.o app.elf app.hex
```

## Flashing an Arduino board
- Uno (optiboot): `avrdude -p m328p -c arduino -P /dev/ttyACM0 -b 115200 -U flash:w:app.hex:i`.
- Old Nano bootloader: `-b 57600`. Mega 2560: `-p m2560 -c wiring -b 115200 -D`.
- With an ISP programmer the bootloader is erased; set fuses (`BOOTRST`) accordingly.

## Using Arduino libraries anyway
Compile the Arduino core (`cores/arduino/*.c*`) with the same flags plus `-DARDUINO=10819
-DARDUINO_AVR_UNO -DARDUINO_ARCH_AVR` and the variant include path, or use PlatformIO/CMake
toolchains (avr-cmake) instead of a hand Makefile for larger projects.

## Verify
- [ ] `avr-size` reports flash/RAM use under limits.
- [ ] LED blinks at the right rate (F_CPU matches the real clock).
