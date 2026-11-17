---
id: computing-software.firmware-embedded-development.bare-metal-programming.noinit-ram-sections
name: noinit-ram-sections
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [noinit-section, noinit-ram, linker-script, noload, warm-reset, reset-survival, magic-word, gnu-ld, cortex-m, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Keep variables alive across a warm reset with a NOLOAD .noinit section: linker script, validation with magic and CRC, and why you must check your part's reset behaviour."
sources:
  - https://sourceware.org/binutils/docs/ld/Output-Section-Type.html
  - https://gcc.gnu.org/onlinedocs/gcc/Common-Variable-Attributes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# No-init RAM sections surviving reset

**Goal:** a small block of RAM (reset reason, crash record, boot counter, bootloader request)
that the startup code does not zero or initialise, so its contents can survive a warm reset.

## Linker script
```ld
.noinit (NOLOAD) : ALIGN(4)
{
    _snoinit = .;
    *(.noinit .noinit.*)
    . = ALIGN(4);
    _enoinit = .;
} > RAM
```
- `NOLOAD`: the section is marked not loadable, so it is not loaded into memory when the program
  runs. For ELF output ld still allocates the memory space at run time (the ld manual calls this
  ELF behaviour a bug that may change, so check your ld version).
- Place it **outside** `.bss` and outside any region your startup code or RTOS clears.
- If a bootloader and an application share the record, put it at a fixed address in both
  linker scripts and shrink both `RAM` regions accordingly.

## Declaring
GCC has a `noinit` variable attribute: data with it is not initialised by the C runtime startup
code or the program loader. It is specific to ELF targets and relies on the linker script to
place sections with the `.noinit` prefix. The `section` attribute with `.noinit` works the same way:
```c
typedef struct { uint32_t magic; uint32_t boot_count; uint32_t reason; uint32_t crc; } persist_t;
__attribute__((section(".noinit"))) static persist_t g_persist;
```
Do not give it an initialiser.

## Validate before trusting
After a power-on the contents are undefined. Always check:
```c
if (g_persist.magic != PERSIST_MAGIC || crc32(&g_persist, offsetof(persist_t, crc)) != g_persist.crc) {
    memset(&g_persist, 0, sizeof g_persist);   /* cold boot */
    g_persist.magic = PERSIST_MAGIC;
}
```
Update the CRC after every write. Combine with the part's reset-cause register and clear its
flags once read.

## Which resets preserve RAM
This depends on the part: look up in its reference manual which reset sources (software,
watchdog, pin, power-on, brown-out, low-power exits) clear SRAM, and whether SRAM ECC/parity
init or option bytes erase it. See `retention-ram-in-deep-sleep` for retention RAM.

## Gotchas
- The debugger "load" step may zero RAM, and some IDEs run init scripts that clear SRAM.
- C++ static constructors and a `memset` of all RAM in a custom startup kill it.

## Verify
- [ ] `nm` shows the variable inside the `.noinit` address range.
- [ ] Write a counter, trigger a warm reset, confirm it incremented; power-cycle,
      confirm the magic check resets it.

## Checked
2026-10-31. Confirmed in the GNU ld manual (Output Section Type): `NOLOAD` semantics and the ELF
note. Confirmed in the GCC Common Variable Attributes page: the `noinit` attribute and the `.noinit` prefix.
Removed: per-reset-source retention claims (software, watchdog, power-on, STM32 SRAM2 and option bytes), the
GCC `.data`/section-conflict warning claim, and the Zephyr and ESP-IDF attribute names (sources unreadable).
Method: documentation only; no commands were run.
