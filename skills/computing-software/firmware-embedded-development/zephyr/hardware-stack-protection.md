---
id: computing-software.firmware-embedded-development.zephyr.hardware-stack-protection
name: hardware-stack-protection
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-userspace, hw-stack-protection, mpu-stack-guard, psplim, stack-sentinel, stack-canaries, thread-analyzer, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Catch Zephyr thread stack overflows deterministically with CONFIG_HW_STACK_PROTECTION (MPU guards or ARMv8-M stack limit registers), plus canaries and sizing tools."
sources:
  - https://docs.zephyrproject.org/latest/kernel/usermode/memory_domain.html
  - https://docs.zephyrproject.org/latest/kernel/services/other/fatal.html
  - https://docs.zephyrproject.org/latest/hardware/arch/arm_cortex_m.html
  - https://docs.zephyrproject.org/latest/services/debugging/thread-analyzer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardware stack protection

A silent stack overflow corrupts whatever lies below the stack and crashes much later
somewhere unrelated. Hardware protection turns it into an immediate, attributable fault.

## Enable
```
CONFIG_HW_STACK_PROTECTION=y
```
The arch picks the mechanism:
- **Arm v8-M and v8.1-M**: stack limit checking with the `MSPLIM` / `PSPLIM` registers
  (`CONFIG_BUILTIN_STACK_GUARD`). No memory areas reserved, no MPU regions used; an overflow raises
  the v8-M UsageFault. With `CONFIG_HW_STACK_PROTECTION` this is used by default instead of the MPU guard.
- **Cortex-M with an MPU**: a guard region at the lowest address of the stack
  (`CONFIG_MPU_STACK_GUARD`) that normally reserves one MPU region (two in some v8-M setups with
  `CONFIG_MPU_GAP_FILLING`). Guards are reprogrammed at every context switch, and the stack alignment
  requirement grows (`CONFIG_ARM_MPU_REGION_MIN_ALIGN_AND_SIZE`).
- Other architectures implement this with their own CPU features or read-only MMU/MPU guard regions.
- `CONFIG_BUILTIN_STACK_GUARD` and `CONFIG_MPU_STACK_GUARD` are mutually exclusive mechanisms; set
  `CONFIG_HW_STACK_PROTECTION` and let the architecture choose.
- In user mode, overflows are always caught by the memory protection hardware, whatever this option says.

## What you see
On Cortex-M the fault handler prints lines such as `***** MPU FAULT *****` or
`***** USAGE FAULT *****`, then the kernel prints `>>> ZEPHYR FATAL ERROR <n>: Stack overflow on CPU <n>`
(fatal reason `K_ERR_STACK_CHK_FAIL`) and `Current thread: <ptr> (<name>)`. The thread name tells
you whose stack to grow. Detection does not guarantee that nothing was corrupted: treat any
supervisor-mode overflow as a serious error.

## Complementary software checks
| Option | Catches | Cost |
|---|---|---|
| `CONFIG_STACK_CANARIES` | corruption of a single stack frame (compiler canary), not whole-buffer overflow | compiler checks per function |
| `CONFIG_STACK_SENTINEL` | software-only periodic check of a sentinel at the end of the stack | no hardware needed |
| `CONFIG_THREAD_ANALYZER` | measures peak usage per thread | debug aid |
| `CONFIG_INIT_STACKS` + `k_thread_stack_space_get()` | unused bytes per thread | stacks filled with 0xaa |

## Sizing workflow
1. Enable `CONFIG_THREAD_ANALYZER=y`, `CONFIG_THREAD_ANALYZER_AUTO=y`, `CONFIG_THREAD_NAME=y`.
2. Run the worst-case scenario (all features, error paths, max payloads).
3. Read the report (`thread_analyzer_print()` or shell `kernel stacks`) and size each stack from the measured peak with margin.
4. Keep HW protection on in production; analyser and `INIT_STACKS` can go.

Also covered: ISR stack (`CONFIG_ISR_STACK_SIZE`), main (`CONFIG_MAIN_STACK_SIZE`), system
workqueue (`CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE`) and logging thread. Overflows there are common
because people forget they exist.

## Verify
- [ ] A test thread with deliberate deep recursion faults immediately with the stack overflow reason.
- [ ] Thread analyzer margins recorded for every thread, including system threads.
- [ ] Production config keeps `CONFIG_HW_STACK_PROTECTION=y` (check `hardenconfig`).

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- Stack-protection mechanisms, their cost, exclusivity and the default on v8-M (doc: hardware/arch/arm_cortex_m);
  user-mode overflows always caught, `CONFIG_STACK_SENTINEL`, `CONFIG_STACK_CANARIES`, `K_ERR_STACK_CHK_FAIL` (doc:
  kernel/services/other/fatal); migration-guide-4.5 note that `HW_STACK_PROTECTION` is the recommended switch.
- Printed text: `***** MPU FAULT *****` / `***** USAGE FAULT *****` (`arch/arm/core/cortex_m/fault.c`), `Stack overflow` reason
  string and `Current thread:` line (`kernel/fatal.c`).
- Wrong or removed: the invented `***** Stack overflow *****` / `Stacking error` log block, the Cortex-M33/M55/M85 list, the
  "32 bytes / FPU lazy stacking" guard-size claim, the x1.25-1.5 sizing factor and the RISC-V PMP statement.

Method: documentation only; no commands were run.
