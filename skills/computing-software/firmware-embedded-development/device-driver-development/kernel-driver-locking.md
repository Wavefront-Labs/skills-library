---
id: computing-software.firmware-embedded-development.device-driver-development.kernel-driver-locking
name: kernel-driver-locking
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [kernel-spinlock, linux-kernel-module, mutex, spin-lock-irqsave, lockdep, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Choose and use Linux kernel locks in drivers: mutex vs spinlock vs spin_lock_irqsave by context, sleeping-in-atomic bugs, lockdep and CONFIG_DEBUG_ATOMIC_SLEEP."
sources:
  - https://docs.kernel.org/kernel-hacking/locking.html
  - https://docs.kernel.org/locking/spinlocks.html
  - https://docs.kernel.org/locking/lockdep-design.html
  - https://docs.kernel.org/locking/locktypes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spinlocks and mutexes in drivers

## Which lock
| Data shared between | Lock |
|---|---|
| process contexts only (file ops, sysfs, workqueues), may sleep while holding | `struct mutex` |
| process context and a hard IRQ handler | `spin_lock_irqsave` in process context, `spin_lock` in the IRQ handler |
| process context and softirq/tasklet/timer | `spin_lock_bh` |
| threaded IRQ handler (runs in a kthread) and process context | `mutex` is fine |
| simple counters/flags | `atomic_t`, `refcount_t`, `READ_ONCE/WRITE_ONCE` |
| read-mostly data | RCU or `rwlock`/`seqlock` |

```c
struct mydev { spinlock_t lock; struct mutex io_lock; u32 status; };
spin_lock_init(&d->lock); mutex_init(&d->io_lock);

static irqreturn_t my_irq(int irq, void *p) {          /* hard IRQ */
    struct mydev *d = p;
    spin_lock(&d->lock);
    d->status |= readl(d->base + STATUS);
    spin_unlock(&d->lock);
    return IRQ_WAKE_THREAD;
}
static ssize_t my_read(...) {
    unsigned long flags;
    spin_lock_irqsave(&d->lock, flags);
    u32 s = d->status; d->status = 0;
    spin_unlock_irqrestore(&d->lock, flags);
    mutex_lock(&d->io_lock);                           /* may sleep: I2C/SPI transfers */
    ...
}
```

## Rules
- **Never sleep with a spinlock held**: no `mutex_lock`, `kmalloc(GFP_KERNEL)`, `copy_to_user`,
  `msleep`, I2C/SPI transfers (`i2c_transfer` sleeps), `regmap` on slow buses. Results in
  "BUG: scheduling while atomic" or deadlocks.
- Keep spinlock sections short (no loops waiting for hardware).
- Consistent lock ordering across the driver; document it.
- Use `mutex_lock_interruptible` in syscall paths so signals can abort waits.
- `devm_mutex_init` (declared in `include/linux/mutex.h`) or `mutex_destroy` on remove for debug builds.
- On PREEMPT_RT kernels, `spinlock_t` and `rwlock_t` become sleeping locks while `raw_spinlock_t`
  keeps spinning; use `raw_spinlock_t` only for code that truly runs in hard-IRQ context with
  interrupts off (see the locktypes document).

## Debugging options
`CONFIG_PROVE_LOCKING` (lockdep: reports possible deadlocks and IRQ-safety violations the first
time the pattern occurs, without needing the actual deadlock), `CONFIG_DEBUG_ATOMIC_SLEEP`
("sleeping function called from invalid context"), `CONFIG_DEBUG_SPINLOCK`, `CONFIG_DEBUG_MUTEXES`.
Enable them in development kernels.

## Verify
- [ ] Driver exercised with lockdep and DEBUG_ATOMIC_SLEEP enabled: no splats in `dmesg`.
- [ ] Stress test with concurrent readers and interrupt load shows consistent state.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/locking/locktypes.rst: on PREEMPT_RT local_lock, spinlock_t and rwlock_t become sleeping locks, raw_spinlock_t stays a spinning lock. Confirmed in Documentation/kernel-hacking/locking.rst: spin_lock_bh, spin_lock_irqsave and mutex_lock_interruptible usage. Confirmed in lib/Kconfig.debug: PROVE_LOCKING, DEBUG_SPINLOCK, DEBUG_MUTEXES, DEBUG_ATOMIC_SLEEP exist. devm_mutex_init confirmed in include/linux/mutex.h; the unconfirmed "6.x" version gate was removed.

Method: documentation only; no commands were run.
