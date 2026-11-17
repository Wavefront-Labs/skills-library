---
id: computing-software.software-engineering.ada.bareboard-runtimes
name: bareboard-runtimes
category: computing-software
field: software-engineering
product: ada
tags: [ada, bareboard-runtimes, ada-embedded]
level: advanced
status: draft
description: "Cross-compile Ada for MCUs with Alire toolchains (gnat_arm_elf), Runtime attribute, light and light-tasking runtimes."
sources:
  - https://learn.adacore.com/courses/Ada_For_The_Embedded_C_Developer/
  - https://alire.ada.dev/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bare-board runtimes and cross toolchains
```
alr toolchain --select gnat_arm_elf gprbuild
```
```
project Blink is
   for Target use "arm-eabi";
   for Runtime ("Ada") use "embedded-stm32f4";   -- name varies, see Ada_Drivers_Library
end Blink;
```
- Runtimes: `light` (no tasking), `light-tasking` (Ravenscar), `embedded`; availability per board.
- Use Ada_Drivers_Library (AdaCore) for STM32 and other boards.
## Gotchas
- Exceptions and secondary stack depend on runtime; check `-fstack-usage`.
## Self-check
Build an LED blink image and verify the ELF section sizes.
