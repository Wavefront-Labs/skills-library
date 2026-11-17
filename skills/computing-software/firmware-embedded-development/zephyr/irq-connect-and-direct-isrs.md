---
id: computing-software.firmware-embedded-development.zephyr.irq-connect-and-direct-isrs
name: irq-connect-and-direct-isrs
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [irq-connect, irq-direct-connect, irq-enable, zero-latency-irq, dynamic-interrupts, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Hook interrupts in Zephyr with IRQ_CONNECT, IRQ_DIRECT_CONNECT, zero-latency IRQs and dynamic connection: priorities from devicetree, ISR rules, and the generated ISR table."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/interrupts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IRQ_CONNECT and direct ISRs

## Regular ISR
```c
#define MYDEV_NODE DT_NODELABEL(timer2)

static void timer2_isr(const void *arg)
{
    const struct device *dev = arg;
    clear_flags(dev);
    k_sem_give(&tick_sem);         /* ISR-safe kernel calls only */
}

static int mydev_init(const struct device *dev)
{
    IRQ_CONNECT(DT_IRQN(MYDEV_NODE), DT_IRQ(MYDEV_NODE, priority),
                timer2_isr, DEVICE_DT_GET(MYDEV_NODE), 0);
    irq_enable(DT_IRQN(MYDEV_NODE));
    return 0;
}
```
- `IRQ_CONNECT` is not a C function and does inline assembly magic: **all its arguments must be known at build
  time** (IRQ line, priority, ISR, argument, flags). The `gen_isr_tables.py` script generates the vector table and
  software ISR table (`isr_tables.c`, `isr_tables_swi.ld`, `isr_tables_vt.ld`).
- The interrupt must then be enabled with `irq_enable`. The unprefixed `irq_enable` / `irq_lock` are the legacy
  spelling on main; `k_irq_enable` / `k_irq_lock` are the namespaced equivalents (docs: both remain supported).
- Take IRQ and priority from devicetree so boards can change them.
- Drivers with several instances define a per-instance config function that calls `IRQ_CONNECT`.

## Direct ISR (lower latency)
```c
ISR_DIRECT_DECLARE(fast_isr)
{
    handle_fast_thing();
    ISR_DIRECT_PM();          /* PM done after servicing, for best latency; not for zero-latency IRQs */
    return 1;                 /* 1 = ask the kernel to check for a scheduling decision, 0 = no */
}

IRQ_DIRECT_CONNECT(FAST_IRQ, 0, fast_isr, 0);
irq_enable(FAST_IRQ);
```
Regular ISRs pay for fetching and passing the argument, resuming hardware from low-power state before the ISR
runs (with PM), switching to the interrupt stack in code on some architectures, and a scheduling check on exit;
direct ISRs avoid these. Direct ISRs exist only on architectures that select `CONFIG_ARCH_HAS_DIRECT_INTERRUPTS`;
elsewhere `IRQ_DIRECT_CONNECT` / `ISR_DIRECT_DECLARE` fail the build.

## Zero-latency IRQs (Cortex-M)
```
CONFIG_ZERO_LATENCY_IRQS=y
```
(Cortex-M only today.)
```c
IRQ_DIRECT_CONNECT(MOTOR_IRQ, 0, motor_isr, IRQ_ZERO_LATENCY);
```
A zero-latency interrupt runs at a priority level that interrupt locking cannot block. It must be a direct
ISR, must not use `ISR_DIRECT_PM`, and must return 0. The docs treat all kernel APIs as undefined behaviour
there: no kernel APIs, no modifying data that kernel APIs inspect, no synchronous exceptions such as kernel panic.
It is currently implemented for Arm Cortex-M. With power management that keeps interrupts locked across resume,
such an ISR can run during PM suspend/resume and must be PM-wake-safe or have its source masked.

## Dynamic interrupts
`CONFIG_DYNAMIC_INTERRUPTS=y` enables `irq_connect_dynamic(irq, prio, isr, arg, flags)` at runtime
at runtime; removing or re-configuring a dynamic interrupt is unsupported. Dynamic direct interrupts exist
only on some architectures (Cortex-M: `ARM_IRQ_DIRECT_DYNAMIC_CONNECT`).
`CONFIG_SHARED_INTERRUPTS=y` lets several ISR/argument pairs share a line (limit
`CONFIG_SHARED_IRQ_MAX_NUM_CLIENTS`) at a non-negligible binary size cost; with dynamic interrupts it also
enables `irq_disconnect_dynamic`.

## ISR rules
- An ISR may call only functions marked isr-ok, and must not wait (use `K_NO_WAIT`).
- `k_is_in_isr()` tells shared code whether it runs in an ISR.
- Priority semantics are architecture-specific; some architectures have no interrupt priorities. The priority is
  not stored in the ISR tables but programmed into the interrupt controller. On Cortex-M the zero-latency levels
  are set by `CONFIG_ZERO_LATENCY_LEVELS`.

## Verify
- [ ] IRQ number and priority come from devicetree macros.
- [ ] Zero-latency ISRs contain no kernel calls.
- [ ] The generated `isr_tables.c` in the build directory shows the handler on the right line.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- `IRQ_CONNECT` build-time arguments, `irq_enable`, direct ISR overheads and `CONFIG_ARCH_HAS_DIRECT_INTERRUPTS`,
  `ISR_DIRECT_PM` and return value, zero-latency rules and PM caveat, dynamic and shared interrupt options,
  generated table files (doc: kernel/services/interrupts).
- Removed: the `_isr_wrapper` description, the `BASEPRI` statement, the architecture list for direct ISRs, the
  "kernel calls allowed only if you return 1" claim, the specific ISR-safe call list and the "lower = more urgent"
  Cortex-M remark (not in the Zephyr docs).

Method: documentation only; no commands were run.
