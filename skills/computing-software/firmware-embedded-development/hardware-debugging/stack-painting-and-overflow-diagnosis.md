---
id: computing-software.firmware-embedded-development.hardware-debugging.stack-painting-and-overflow-diagnosis
name: stack-painting-and-overflow-diagnosis
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [stack-painting, stack-overflow, high-water-mark, msplim, psplim, stack-usage, fstack-usage, mpu-guard, hardware-debugging, firmware-embedded-development]
level: practitioner
status: draft
description: "Size and police stacks: paint with a pattern and measure the high-water mark, -fstack-usage estimates, MSPLIM/PSPLIM on ARMv8-M, MPU guard regions and overflow symptoms."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html
  - https://developer.arm.com/documentation/100235/0100/The-Cortex-M33-Processor/Programmers-model/Core-registers
  - https://www.freertos.org/Stacks-and-stack-overflow-checking.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stack painting and overflow diagnosis

## Paint and measure
Fill the stack with a known pattern before use, then find the deepest overwritten word.
```c
extern uint32_t _sstack[], _estack[];          /* from the linker script */
#define PAINT 0xDEADBEEFu
void stack_paint(void) {                        /* call first thing in Reset_Handler, before main */
    uint32_t *sp; __asm volatile("mov %0, sp" : "=r"(sp));
    for (uint32_t *p = _sstack; p < sp - 8; ++p) *p = PAINT;
}
size_t stack_unused_bytes(void) {
    uint32_t *p = _sstack; while (p < _estack && *p == PAINT) ++p;
    return (size_t)((uint8_t*)p - (uint8_t*)_sstack);
}
```
Run the worst-case scenario (all ISRs nesting, longest paths, error handling, printf with floats),
then read the high-water mark. FreeRTOS does the same per task: `uxTaskGetStackHighWaterMark()`
(needs `INCLUDE_uxTaskGetStackHighWaterMark`); Zephyr `CONFIG_THREAD_ANALYZER`.
GDB one-off: `find /w _sstack, _estack, 0xDEADBEEF` is slow; dump and scan instead.

## Static estimate
`-fstack-usage` writes `.su` files per function (static/dynamic/bounded). Combine with a call graph
(`-fcallgraph-info=su` in GCC 10+, or tools like puncover / `avstack.pl`) to get worst-case depth.
Recursion, function pointers and VLAs make it unbounded; flag those.

## Catching overflow at runtime
- **ARMv8-M (M23/M33/M55):** set `MSPLIM`/`PSPLIM` (`__set_MSPLIM(( uint32_t)_sstack)`); overflow
  raises a UsageFault with `UFSR.STKOF`. Free and exact; use it.
- **ARMv7-M:** put the stack at the bottom of RAM so overflow hits invalid memory (HardFault on the
  stacking), or an MPU no-access region (32 bytes+) at the stack limit.
- **RTOS checks:** FreeRTOS `configCHECK_FOR_STACK_OVERFLOW 2` checks the last 16 bytes on context
  switch; it misses an overflow that jumps past the canary.
- GCC `-fstack-protector-strong` catches buffer overruns within a frame, not depth overflow.

## Symptoms of overflow without protection
Random corruption of the variables just below the stack (often `.bss` end or the heap), HardFault
with a garbage stacked PC, `IMPRECISERR`, a task that crashes only when an ISR nests.

## Sizing rule
Measured high-water mark + 25-50% margin; ISR stack (MSP) = deepest ISR nesting x frame sizes +
FPU context (extra 72 bytes per lazily stacked frame on M4F/M7).

## Verify
- [ ] Worst-case test leaves the documented margin unused.
- [ ] Deliberate recursion test trips the limit (STKOF / MPU fault), not silent corruption.
