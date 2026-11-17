---
id: computing-software.firmware-embedded-development.bare-metal-programming.weak-default-handlers-and-aliases
name: weak-default-handlers-and-aliases
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [weak-handler-alias, startup-code, weak-symbol, default-handler, vector-table, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use weak symbols and aliases for Cortex-M interrupt handlers so unused vectors land in a default trap, and catch the typo'd handler name that silently never runs."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/Common-Attributes.html
  - https://sourceware.org/binutils/docs/ld/Options.html
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__intrinsic__CPU__gr.html
  - https://sourceware.org/binutils/docs/as/Weak.html
  - https://arm-software.github.io/CMSIS_6/latest/Core/startup_c_pg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Weak default handlers and handler aliasing

**Goal:** every vector table slot points at something valid, application code overrides a
handler just by defining a function with the right name, and misspelled handlers are caught.

## The pattern (C startup, CMSIS style)
```c
void Default_Handler(void) { __BKPT(0); for (;;) {} }      /* trap, not return */

void HardFault_Handler(void)   __attribute__((weak, alias("Default_Handler")));
void USART1_IRQHandler(void)   __attribute__((weak, alias("Default_Handler")));
void TIM2_IRQHandler(void)     __attribute__((weak, alias("Default_Handler")));

__attribute__((section(".isr_vector"), used))
void (* const g_vectors[])(void) = {
    (void (*)(void))&__StackTop, Reset_Handler, NMI_Handler, HardFault_Handler, /* ... */
    USART1_IRQHandler, TIM2_IRQHandler,
};
```
The alias target must be defined in the same translation unit as the alias, so keep
`Default_Handler` in the startup file. The `alias` attribute needs assembler and object-file
support. Assembly startup files mark a handler weak with the `.weak` directive.

The `weak` attribute emits the symbol as weak so user code can override it. The overriding
definition must have the same type as the weak symbol. The CMSIS-Core startup file works this
way: every exception and interrupt vector gets a weak default routine, and you extend the vector
table with the device's handler names (for example `NMI_Handler`, `HardFault_Handler`,
`SVC_Handler`, `PendSV_Handler`, `SysTick_Handler`). A strong definition of the same name in the
link replaces the weak alias; no registration call is needed.

## Failure modes
- **Typo or wrong name** (`USART1_IRQhandler`, `TIM2_IRQ_Handler`): the strong function is an
  unrelated symbol, the vector still points at `Default_Handler`, the IRQ fires and the CPU sits
  in the trap loop. Symptom: debugger halts in `Default_Handler` with no obvious cause.
  Compare your function names with the names in the device's startup file character by character.
- **C++ name mangling:** GCC notes that in C++ the mangled name must be used for an alias target,
  so a handler defined in a `.cpp` file needs `extern "C"` or its mangled name never matches the
  weak symbol.
- **Handler in a static library:** the linker searches an archive for the object files it needs
  to resolve undefined symbols, and a weak definition already satisfies the vector table
  reference, so a strong handler in an otherwise unreferenced archive member can go unused.
  Fix: link the object directly, or `-Wl,--whole-archive libdrivers.a -Wl,--no-whole-archive`
  (ld includes every object in archives listed after `--whole-archive`), or force it in with
  `-Wl,-u,USART1_IRQHandler`.
- **Default handler that returns:** if the peripheral's interrupt flag is never cleared it
  re-enters forever and starves main. Keep it as a trap (or log and reset).
- **Shared default handler hides which IRQ it was:** give each vector its own tiny stub in debug
  builds, or inspect the active exception number in the debugger.

## Finding unhandled vectors at build time
```sh
arm-none-eabi-nm -n app.elf | grep -i ' W '            # weak symbols that are still the weak definition
arm-none-eabi-objdump -s -j .isr_vector app.elf        # raw table: count entries equal to Default_Handler|1
```
A quick CI check: parse the vector table, list every IRQ that resolves to `Default_Handler`
and compare with the IRQs the code enables (`NVIC_EnableIRQ` calls).

## Verify
- [ ] `nm` shows your handler as `T` (strong) and its address appears in `.isr_vector` (with bit 0 set).
- [ ] Triggering the IRQ via `NVIC_SetPendingIRQ` lands in your function, not the trap.
- [ ] `.cpp` handlers are `extern "C"`.

## Checked
2026-11-08. Confirmed in the GCC manual (Common Attributes: `weak`, `alias`), the GNU as manual (`.weak`), the GNU
ld manual (`--whole-archive`, `-u`) and the CMSIS-Core startup page (weak default handlers, handler names, vector
table) plus the CMSIS intrinsics page (`__BKPT`). Removed: `.thumb_set` and the VECTACTIVE/ICSR recipe, which the cited pages do not cover. The nm, objdump
and `NVIC_SetPendingIRQ` checklist items were not checked against a manual.
Method: documentation only; no commands were run.
