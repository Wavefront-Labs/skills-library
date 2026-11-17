---
id: computing-software.firmware-embedded-development.device-driver-development.threaded-irq-handlers
name: threaded-irq-handlers
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [platform-driver, request-threaded-irq, irqf-oneshot, hard-irq-handler, irq-wake-thread, sleeping-bus-in-irq, level-triggered-irq, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Handle interrupts from I2C/SPI devices in Linux with threaded IRQs: hard vs thread handler, IRQF_ONESHOT for level IRQs, shared lines and avoiding interrupt storms."
sources:
  - https://docs.kernel.org/core-api/genericirq.html
  - https://github.com/torvalds/linux/blob/master/include/linux/interrupt.h
  - https://github.com/torvalds/linux/blob/master/kernel/irq/manage.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Threaded IRQ handlers

**Goal:** service device interrupts whose handling needs to sleep (bus transfers over I2C/SPI,
mutexes) without blocking the system, and without interrupt storms on level-triggered lines.

## The split
```c
ret = devm_request_threaded_irq(dev, irq,
        acme_hardirq,          /* may be NULL; runs in hard-IRQ context, can't sleep */
        acme_irq_thread,       /* runs in a kernel thread, can sleep (i2c, mutex) */
        IRQF_ONESHOT,          /* keep line masked until the thread finishes */
        dev_name(dev), a);

static irqreturn_t acme_hardirq(int irq, void *data) {
    struct acme *a = data;
    a->ts = ktime_get_boottime_ns();   /* timestamp while it's fresh */
    return IRQ_WAKE_THREAD;
}
static irqreturn_t acme_irq_thread(int irq, void *data) {
    struct acme *a = data;
    int st = i2c_smbus_read_byte_data(a->client, ACME_REG_INT_STATUS);  /* clears source */
    if (st <= 0) return IRQ_NONE;
    if (st & ACME_INT_DRDY) acme_push_sample(a);
    return IRQ_HANDLED;
}
```
With a NULL hard handler, `IRQF_ONESHOT` is **mandatory** (the core refuses otherwise): the line
stays masked until the thread clears the device's interrupt, so a level-triggered line doesn't
refire endlessly.

## Trigger type
Take it from DT (`interrupts = <17 IRQ_TYPE_LEVEL_LOW>` or `interrupts-extended`); don't
hard-code `IRQF_TRIGGER_*` unless the device dictates it. For level-triggered lines use
`IRQF_ONESHOT` so the line stays masked until the thread has cleared the source.

## Return values
- `IRQ_NONE` when your device didn't interrupt (important for shared IRQs and for the kernel's
  spurious-IRQ detector, which reports "irq N: nobody cared" and can disable the line after
  repeated unhandled interrupts, evaluated every 100000 interrupts).
- `IRQ_HANDLED` after clearing the source.

## Shared lines
`IRQF_SHARED` must be set by every sharer and the trigger-type bits must match (a handler using
`IRQF_COND_ONESHOT` agrees to ONESHOT if already set); every handler must check its own
device's status.

## Wake-up
For a device that wakes the system: `device_init_wakeup(dev, true)` and
`enable_irq_wake(irq)` in suspend (or `dev_pm_set_wake_irq`, declared in `pm_wakeirq.h`).

## Verify
- [ ] `/proc/interrupts` count matches expected event rate; no "nobody cared" messages.
- [ ] Under load the thread (named `irq/<n>-<name>`) keeps up; adjust its scheduling priority if latency matters.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in kernel/irq/manage.c: error "Threaded irq requested with handler=NULL and !ONESHOT" (so ONESHOT is mandatory with a NULL hard handler), thread name format irq/%d-%s, shared-line rule (both need IRQF_SHARED and matching trigger type bits; IRQF_COND_ONESHOT adopts ONESHOT if already set), irq_set_irq_wake. Confirmed in kernel/irq/spurious.c: message "irq %d: nobody cared" and the 100000-interrupt counting window. Confirmed in include/linux/interrupt.h: IRQF_SHARED, IRQF_ONESHOT, IRQF_COND_ONESHOT, devm_request_threaded_irq, enable_irq_wake. Confirmed in include/linux/pm_wakeirq.h and pm_wakeup.h: dev_pm_set_wake_irq, device_init_wakeup. Removed as unconfirmed: the edge-trigger event-loss explanation and the "level-low is the robust choice" statement, and the chrt tool reference.

Method: documentation only; no commands were run.
