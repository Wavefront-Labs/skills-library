---
id: computing-software.firmware-embedded-development.bare-metal-programming.semihosting-hang-without-debugger
name: semihosting-hang-without-debugger
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [semihosting-hang, semihosting, bkpt-0xab, rdimon, debugger-detect, firmware-embedded-development]
level: practitioner
status: draft
description: "Fix firmware that runs under the debugger but hangs or HardFaults standalone because of semihosting BKPT 0xAB calls, and make semihosting safe when no probe is attached."
sources:
  - https://github.com/ARM-software/abi-aa/blob/main/semihosting/semihosting.rst
  - https://developer.arm.com/documentation/dui0553/latest/
  - https://openocd.org/doc/html/General-Commands.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Semihosting hang without a debugger

**Symptom:** the board works with the debugger attached; powered standalone it hangs at the first
`printf` or immediately at boot (HardFault with `HFSR.DEBUGEVT=1`).

## Why
Semihosting calls execute `BKPT 0xAB`. With a debugger attached and semihosting enabled, the
probe services the request. Without a debugger, a BKPT on Cortex-M escalates to **HardFault**
(DebugMonitor not enabled, halting debug not active). The HardFault handler loops forever.

Sources of semihosting you might not have asked for:
- Linking with `--specs=rdimon.specs` or `-lrdimon` (newlib's semihosting syscalls), often in
  vendor example projects.
- `initialise_monitor_handles()` in `main()`.
- Libraries calling `exit()` (`_exit` -> `SYS_EXIT` semihosting).

## Fix 1: don't ship semihosting
Use `--specs=nano.specs --specs=nosys.specs` and retarget `_write` to UART/RTT/ITM. Check the
binary:
```sh
arm-none-eabi-objdump -d app.elf | grep -n "bkpt.*0x00ab"
```

## Fix 2: make it conditional on a debugger
```c
static bool debugger_attached(void) {
    return (CoreDebug->DHCSR & CoreDebug_DHCSR_C_DEBUGEN_Msk) != 0;   /* only readable reliably on v7-M+; reads 0 on some v6-M parts from software */
}
int _write(int fd, const char *p, int n) {
    if (debugger_attached()) return semihost_write(fd, p, n);
    return uart_write(p, n);
}
```

## Fix 3: catch and skip in HardFault
Detect `BKPT 0xAB` in the HardFault handler: check `HFSR.DEBUGEVT`, read the stacked PC, check the
halfword is `0xBEAB`, set R0 (return value) to -1 in the stacked frame and advance the stacked PC
by 2. The program continues as if the call failed. Useful for test builds shared between bench
and debugger.

## Debugger side
Semihosting must be enabled in the probe: OpenOCD `arm semihosting enable`, J-Link GDB Server
`monitor semihosting enable`, pyOCD `-S`. Without it, the debugger halts at each BKPT and the
target looks frozen *with* the probe attached too. Semihosting is slow (each call halts the core
for milliseconds), so timing-sensitive code misbehaves while it runs.

## Verify
- [ ] `objdump` shows no `bkpt 0x00ab` in release builds.
- [ ] Power-cycle the board with the probe unplugged: it boots and logs on UART.
