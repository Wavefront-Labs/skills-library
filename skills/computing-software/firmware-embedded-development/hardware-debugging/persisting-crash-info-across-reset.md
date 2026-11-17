---
id: computing-software.firmware-embedded-development.hardware-debugging.persisting-crash-info-across-reset
name: persisting-crash-info-across-reset
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [fault-log-noinit, crash-log, hardfault-handler, reset-reason, noinit-ram, field-diagnostics, cfsr, watchdog-reset, cortex-m, firmware-embedded-development]
level: practitioner
status: draft
description: "Capture HardFault/watchdog/assert context into noinit RAM, reset, and report it on the next boot: record layout, a fault handler that works on a broken stack, and flash persistence."
sources:
  - https://developer.arm.com/documentation/ddi0403/latest
  - https://developer.arm.com/documentation/dui0552/a/cortex-m3-peripherals/system-control-block/configurable-fault-status-register
  - https://interrupt.memfault.com/blog/cortex-m-hardfault-debug
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Persisting crash info across reset

**Goal:** every unexpected reset in the field leaves a small record (what, where, why) that the
next boot reads, logs and uploads - without needing a debugger or a full core dump.

## Record (in a `.noinit` section, see `noinit-ram-sections`)
```c
typedef struct {
    uint32_t magic;            /* CRASH_MAGIC when valid */
    uint32_t type;             /* HARDFAULT, ASSERT, WDT_EARLY_WARN, STACK_OVF */
    uint32_t pc, lr, psr, sp;  /* from the stacked frame */
    uint32_t cfsr, hfsr, mmfar, bfar;
    uint32_t exc_return;
    uint32_t task_id;          /* current RTOS task, if any */
    uint32_t crc;
} crash_t;
__attribute__((section(".noinit"))) static crash_t g_crash;
```

## Fault handler that survives a corrupt stack
```c
__attribute__((naked)) void HardFault_Handler(void) {
    __asm volatile(
        "tst lr, #4      \n"
        "ite eq          \n"
        "mrseq r0, msp   \n"
        "mrsne r0, psp   \n"
        "mov r1, lr      \n"
        "ldr r2, =_crash_stack_top \n"   /* switch to a reserved stack: MSP may be overflowed */
        "mov sp, r2      \n"
        "b hardfault_c   \n");
}
void hardfault_c(uint32_t *frame, uint32_t exc_return) {
    g_crash.type = CRASH_HARDFAULT;
    g_crash.pc = frame[6]; g_crash.lr = frame[5]; g_crash.psr = frame[7]; g_crash.sp = (uint32_t)frame;
    g_crash.cfsr = SCB->CFSR; g_crash.hfsr = SCB->HFSR; g_crash.mmfar = SCB->MMFAR; g_crash.bfar = SCB->BFAR;
    g_crash.exc_return = exc_return;
    g_crash.magic = CRASH_MAGIC; g_crash.crc = crc32(&g_crash, offsetof(crash_t, crc));
    NVIC_SystemReset();
}
```
- If `frame` itself points to invalid memory (stack overflow past RAM), reading it faults again
  (lockup). Check the pointer is within RAM before dereferencing; put the main stack at the
  **bottom** of RAM so overflow hits an invalid address and faults instead of silently
  corrupting `.data`.
- Assert handler: record `__builtin_return_address(0)` and a file id/line, same path.
- Watchdog: use an early-warning interrupt (STM32 WWDG EWI, nRF WDT TIMEOUT event, Zephyr
  `wdt` callback) to record the PC of the stuck code before the reset.

## On boot
1. Read the hardware reset-cause register (RCC_CSR, POWER->RESETREAS, RSTC) and clear it.
2. If `g_crash` magic and CRC are valid: log it, copy it to flash/telemetry queue, then
   invalidate it (clear magic).
3. Decode PC/LR with `arm-none-eabi-addr2line -e app.elf -f -C 0x0800xxxx` on the host
   (keep ELFs per build id).

## Persist to flash (optional)
Never write flash from the fault handler (flash driver state may be corrupt). Save the record
from normal context after reboot, into a small ring of records, so repeated crashes are kept.

## Verify
- [ ] Deliberate null-pointer write: next boot reports HARDFAULT with the correct PC line.
- [ ] Deliberate stack overflow: record still captured (reserved crash stack works).
- [ ] Power cycle with no crash: no stale record reported.
