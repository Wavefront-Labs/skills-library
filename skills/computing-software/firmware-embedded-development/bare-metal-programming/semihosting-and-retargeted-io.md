---
id: computing-software.firmware-embedded-development.bare-metal-programming.semihosting-and-retargeted-io
name: semihosting-and-retargeted-io
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [bare-metal, printf, semihosting, retarget, newlib, _write, syscalls-c, itm, segger-rtt, swo, semihosting-breakpoint, bkpt, no-semihosting-flag, nano-newlib, printf-float, firmware-embedded-development]
level: advanced
status: draft
description: "Get printf working on bare-metal Cortex-M without an OS: retarget newlib's _write to UART, choose semihosting vs ITM/SWO vs RTT, and avoid the float-printf and semihosting-hang traps."
sources:
  - https://developer.arm.com/documentation/dui0471/latest
  - https://sourceware.org/newlib/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# printf retargeting and semihosting on bare-metal

**Goal:** get text output from firmware with no OS underneath it, choosing the
right mechanism for bring-up vs field use, without `printf` silently doing
nothing or hanging the board.

## Why `printf` doesn't "just work"
Newlib (what arm-none-eabi-gcc links by default) implements `printf` on top of
low-level syscall stubs — `_write`, `_read`, `_sbrk`, etc. — that a bare-metal
target doesn't provide. Without retargeting them, `printf` either fails to link
(`undefined reference to _write`) or links against a stub that does nothing.

## Retargeting to UART
Implement `_write` to push bytes out your UART:
```c
int _write(int fd, char *ptr, int len) {
  for (int i = 0; i < len; i++) {
    while (!(USART2->ISR & USART_ISR_TXE));
    USART2->TDR = ptr[i];
  }
  return len;
}
```
This blocks per character — fine for bring-up/debug prints, wrong for a
time-critical path (an ISR, a control loop). Buffer through a ring buffer and
drain it in the UART TX-empty interrupt if `printf` must be called from
performance-sensitive code at all; better, don't call it there.

## Semihosting
ARM semihosting routes `printf`/file I/O through the debug probe via a special
`BKPT 0xAB` instruction that the debugger traps and services — no UART needed,
output appears in the debugger console. Link with `--specs=rdimon.specs` (or
`-specs=nano.specs` without semihosting) and call `initialise_monitor_handles()`.
**The trap:** if the debugger is disconnected and the firmware executes a
semihosting breakpoint, the core halts waiting for a debugger that isn't there —
indistinguishable from a hang. Never ship semihosting-enabled firmware; it's a
bring-up-only tool. Some vendor startup code adds a semihosting fault handler
that detects "no debugger" and returns instead of hanging — check for this if
you need semihosting prints that degrade gracefully when unplugged.

## ITM/SWO and SEGGER RTT as better field-safe alternatives
- **ITM (Instrumentation Trace Macrocell) over SWO**: a single pin, very low
  overhead, non-blocking if the debugger isn't capturing (writes are dropped if
  the FIFO is full and no debugger is draining it) — a safer choice than
  semihosting for sprinkle-and-remove debug prints that might ship by accident.
- **SEGGER RTT**: writes to a RAM ring buffer the host reads via J-Link over the
  existing SWD connection, no extra pin, no blocking, works even with no
  terminal attached, survives reset of the read side independently. Commonly the
  best choice for high-volume debug logging during development; requires a
  J-Link-compatible probe and the RTT library (`SEGGER_RTT.c`).

## nano.specs and float printf
`-specs=nano.specs` links newlib-nano, much smaller but by default built without
float/double format support in `printf`/`scanf` — `%f` silently prints garbage
or nothing. Add `-u _printf_float -u _scanf_float` to the linker flags to pull
the float-capable variants back in, at a flash-size cost; confirm this is worth
it versus formatting floats manually before reaching for it.

## Verify
- [ ] `_write` (or chosen alternative) is implemented and `printf` output is confirmed on real hardware, not just "it links."
- [ ] No semihosting call path can execute in firmware that will run without a debugger attached, or a documented fallback exists.
- [ ] If floats are printed, `-u _printf_float` is present and a float value prints correctly, not as `0.000000` or garbage.
- [ ] Blocking UART-based prints are confirmed absent from ISRs and hard-real-time loops.
