---
id: computing-software.firmware-embedded-development.bare-metal-programming.startup-code-and-linker-script
name: startup-code-and-linker-script
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [bare-metal, cortex-m, arm, startup-code, reset-handler, vector-table, linker-script, ld, memory-regions, sections, lma, vma, data-section, bss-section, volatile, mmio, rcc, clock-enable, arm-none-eabi-gcc, arm-none-eabi-size, arm-none-eabi-objdump, arm-none-eabi-nm, map-file, cmsis, firmware-embedded-development]
level: advanced
status: draft
description: "Write and debug Cortex-M startup code and GNU linker scripts: vector table, Reset_Handler copying .data and zeroing .bss, LMA vs VMA, volatile MMIO, clock enables, and size/objdump/nm checks."
sources:
  - https://developer.arm.com/documentation/
  - https://sourceware.org/binutils/docs/ld/
  - https://gcc.gnu.org/onlinedocs/
  - https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Startup code and linker script — from reset vector to main() on Cortex-M

**Goal:** understand and own everything that happens before `main()`, so you can bring up a
new part, place code/data in specific memories, and diagnose "globals are garbage" or "it
crashes before main".

## 1. What the core does at reset
A Cortex-M reads two words from the vector table (at address 0 or wherever the boot remap /
`VTOR` points, typically flash at `0x08000000` on STM32): word 0 is the initial **MSP**, word 1
is the address of **Reset_Handler** (with bit 0 set for Thumb). Nothing else is initialised:
`.data` holds garbage, `.bss` is not zeroed, clocks run from the internal RC oscillator.

## 2. The linker script
```ld
MEMORY {
  FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
  RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}
_estack = ORIGIN(RAM) + LENGTH(RAM);
SECTIONS {
  .isr_vector : { KEEP(*(.isr_vector)) } > FLASH
  .text   : { *(.text*) *(.rodata*) . = ALIGN(4); _etext = .; } > FLASH
  .data   : { _sdata = .; *(.data*) . = ALIGN(4); _edata = .; } > RAM AT > FLASH
  _sidata = LOADADDR(.data);
  .bss (NOLOAD) : { _sbss = .; *(.bss*) *(COMMON) . = ALIGN(4); _ebss = .; } > RAM
}
```
(Simplified: real scripts also keep `.init_array`, `.ARM.exidx`, heap/stack reservations.)
- **VMA** (run address) vs **LMA** (load address): `.data` runs in RAM but its initial values
  are stored in flash. `> RAM AT > FLASH` sets that; `LOADADDR(.data)` gives the flash copy.
- `KEEP()` stops `--gc-sections` discarding the vector table, which nothing references.
- Take MEMORY sizes from the exact part number's reference manual; some parts split RAM into
  non-contiguous banks (e.g. CCM RAM that DMA cannot reach).

## 3. Reset_Handler
```c
extern uint32_t _sidata, _sdata, _edata, _sbss, _ebss, _estack;
void Reset_Handler(void) {
    uint32_t *src = &_sidata, *dst = &_sdata;
    while (dst < &_edata) *dst++ = *src++;      // copy .data LMA -> VMA
    for (dst = &_sbss; dst < &_ebss; ) *dst++ = 0;  // zero .bss
    SystemInit();                               // clocks/FPU, vendor CMSIS
    __libc_init_array();                        // C++ constructors, if any
    main();
    for (;;) {}
}
__attribute__((section(".isr_vector"), used))
const void *vectors[] = { &_estack, Reset_Handler, NMI_Handler, HardFault_Handler, /* ... */ };
```
Gotchas:
- Linker symbols are addresses, not variables: use `&_sdata`, never `_sdata`.
- On M4F/M7 with hard-float ABI, enable the FPU (`SCB->CPACR |= 0xF << 20`) before any float code
  runs — including in `SystemInit` or constructors — or you get a UsageFault (NOCP).
- If a bootloader starts you, set `SCB->VTOR` to your vector table address (aligned per the
  architecture; at least 128 bytes, more with many vectors).
- Default handlers should be weak aliases to an infinite loop so a missing ISR is obvious in
  the debugger rather than a jump into nowhere.

## 4. Touching peripherals
- Registers are memory-mapped: access through `volatile` pointers
  (`#define GPIOA_ODR (*(volatile uint32_t *)0x40020014)`) or CMSIS device headers. Without
  `volatile` the compiler may merge, reorder or delete accesses — busy-wait loops on status flags
  become infinite or vanish at `-O2`.
- **Enable the peripheral clock first** (e.g. `RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;`). Writes to
  an unclocked peripheral are ignored or bus-fault. Some parts need a dummy read-back or a couple
  of cycles before the first access (errata); a `(void)RCC->AHB1ENR;` read is a common fix.
- Use read-modify-write carefully for registers with write-1-to-clear bits; prefer set/reset
  registers (`BSRR`) for GPIO.

## 5. Inspect the output
```bash
arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -nostartfiles -T app.ld -Wl,--gc-sections \
    -Wl,-Map=app.map -o app.elf startup.c main.c
arm-none-eabi-size -A app.elf        # per-section; flash = text+data, RAM = data+bss
arm-none-eabi-objdump -h app.elf     # VMA and LMA columns per section
arm-none-eabi-objdump -d app.elf | less
arm-none-eabi-nm -S --size-sort -C app.elf | tail -20   # biggest symbols
arm-none-eabi-objcopy -O binary app.elf app.bin
```
Check that `.isr_vector` VMA equals flash origin and `.data` LMA sits in flash right after
`.text`. A `.bin` hundreds of MB large means some section got an LMA in RAM.

Faults during bring-up: computing-software.firmware-embedded-development.hardware-debugging.cortex-m-hardfault-analysis.

## Verify
- [ ] `objdump -h` shows `.data` with VMA in RAM and LMA in flash; `.bss` has no file contents.
- [ ] The first two words of the `.bin` are a RAM address (stack top) and an odd flash address.
- [ ] A global `int x = 42;` reads 42 and a global `int y;` reads 0 at the start of `main()`.
- [ ] `arm-none-eabi-size` totals fit the part's flash and RAM with margin for stack.
- [ ] The map file shows no unexpected large symbols (e.g. pulled-in `printf` float support).
