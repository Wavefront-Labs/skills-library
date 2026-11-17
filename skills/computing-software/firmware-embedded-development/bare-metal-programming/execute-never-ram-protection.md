---
id: computing-software.firmware-embedded-development.bare-metal-programming.execute-never-ram-protection
name: execute-never-ram-protection
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [mpu, execute-never, xn, w-xor-x, iaccviol, code-injection, ramfunc-exception, null-pointer-guard, firmware-embedded-development]
level: advanced
status: draft
description: "Apply execute-never (XN) to SRAM and peripheral space and read-only to flash (W^X) with the MPU, keep RAM functions working, and trap NULL-pointer accesses."
sources:
  - https://developer.arm.com/documentation/dui0553/latest/Cortex-M4-Peripherals/Optional-Memory-Protection-Unit
  - https://docs.zephyrproject.org/latest/kernel/usermode/memory_domain.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Execute-never and W^X with the MPU

**Goal:** memory is writable or executable, never both, so a buffer overflow can't run
injected code and a corrupted function pointer into RAM faults immediately.

## Default map
The ARMv7-M default memory map already makes the peripheral (0x40000000) and system
(0xE0000000) regions XN, but **SRAM (0x20000000) is executable** by default. Add regions:

| Region | Access | XN |
|---|---|---|
| Flash | read-only | no |
| SRAM (whole) | read-write | **yes** |
| `.ramfunc` area (if any) | read-only after copy, or RW | no |
| Peripherals / external device memory | RW | yes |

## RAM functions
Flash-programming routines and time-critical code often run from RAM. Place them in a
dedicated, aligned section and give that section a higher-numbered region with XN off:
```ld
.ramfunc : ALIGN(32) { _sramfunc = .; *(.ramfunc*) . = ALIGN(32); _eramfunc = .; } > RAM AT > FLASH
```
After startup copies it, make the region **read-only + executable**, so it isn't a writable
executable area. Region size must be a power of two and aligned: pad the section.

## Trapping NULL dereferences
Address 0 is usually the flash alias (vector table) and readable, so `*(uint32_t*)0` returns
the initial SP instead of faulting. Add a small no-access region at 0x00000000 (e.g. 256 bytes)
after boot, once the core no longer needs the alias (VTOR points elsewhere). On STM32 the
vector table is still fetched via VTOR at the flash address, so this is safe if VTOR is set.
Zephyr: `CONFIG_NULL_POINTER_EXCEPTION_DETECTION_MPU=y`.

## Faults to expect
- `IACCVIOL` (CFSR bit 0): instruction fetch from XN memory; `MMFAR` not valid, use the
  stacked PC.
- `DACCVIOL` (bit 1): write to read-only/no-access; `MMFAR` valid.

## Verify
- [ ] Jumping to a function pointer in SRAM (outside `.ramfunc`) faults with IACCVIOL.
- [ ] Flash writes through the controller still work (they go via FLASH registers, not stores
      to flash addresses, and those routines run from the executable RAM function region).
- [ ] `*(volatile uint32_t*)0` faults in a test build.
