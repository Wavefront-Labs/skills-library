---
id: computing-software.firmware-embedded-development.zephyr.cpu-affinity-masks-smp
name: cpu-affinity-masks-smp
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [cpu-mask, k-thread-cpu-pin, k-thread-cpu-mask-enable, config-sched-cpu-mask, zephyr-smp, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Pin Zephyr threads to CPUs on SMP with CONFIG_SCHED_CPU_MASK: k_thread_cpu_pin and mask APIs, the must-be-stopped rule, and when to pin versus let threads float."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/smp/smp.html#cpu-mask
  - https://docs.zephyrproject.org/latest/kernel/services/scheduling/index.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/kernel.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPU affinity masks on SMP

```
CONFIG_SMP=y
CONFIG_MP_MAX_NUM_CPUS=2
CONFIG_SCHED_CPU_MASK=y
```

## API
```c
#define STACK 2048
K_THREAD_STACK_DEFINE(rx_stack, STACK);
static struct k_thread rx_thread;

k_tid_t t = k_thread_create(&rx_thread, rx_stack, STACK, rx_fn, NULL, NULL, NULL,
                            5, 0, K_FOREVER);          /* create NOT started */
k_thread_cpu_pin(t, 1);                                 /* only CPU 1 */
/* or build a mask: */
k_thread_cpu_mask_clear(t);
k_thread_cpu_mask_enable(t, 0);
k_thread_cpu_mask_enable(t, 1);
k_thread_start(t);
```
- Mask changes are only allowed while the thread is **not runnable** (blocked or suspended,
  for example created with `K_FOREVER` and not yet started); otherwise `-EINVAL` is returned.
- `k_thread_cpu_pin(t, cpu)` clears the mask and enables the one CPU. `k_thread_cpu_mask_enable_all`
  and `k_thread_cpu_mask_disable` are also available.
- A thread with an empty mask is not schedulable on any CPU.
- `CONFIG_SCHED_CPU_MASK_PIN_ONLY=y` requires every thread to carry exactly one CPU bit; each CPU
  then keeps its own run queue, so the scheduler needs no mask filtering. In that mode
  `k_thread_cpu_mask_clear`, `_enable_all` and `_disable` are not permitted (they can produce a
  mask that is not exactly one bit and trigger an assertion), so use `k_thread_cpu_pin` only.

## When to pin
- Thread that touches per-CPU hardware or must not migrate (per-core timers, cache-sensitive
  DSP loops).
- Isolating a latency-critical thread on a core with nothing else, leaving the other core for
  bulk work.
- Debugging SMP races: pin everything to one CPU to see if a bug disappears.

## When not to
Most threads should float; pinning defeats load balancing and can leave one core idle while
the other is saturated.

## Related
- The SMP documentation says CPU mask filtering is supported with all three scheduler backends
  (simple, scalable, multiq) at different cost, while the scheduling documentation says the
  multi-queue backend is incompatible with SMP affinity; prefer the simple or scalable backend.
- On SMP use spinlocks (`k_spin_lock`) for critical sections: they mask interrupts locally and
  guard a shared lock variable so only one CPU enters at a time. `irq_lock()` still works through
  an emulation built on a single global spinlock with a nesting count.

## Verify
- [ ] Threads are pinned before start; return codes from mask calls checked.
- [ ] `kernel threads` shell output or tracing shows the thread only on its CPU.

## Checked

Checked 2026-10-25 against the Zephyr source (main, post-4.4; latest release v4.4.2): doc/kernel/services/smp/smp.rst and include/zephyr/kernel.h.
Confirmed: `CONFIG_SMP`, `CONFIG_MP_MAX_NUM_CPUS`, `CONFIG_SCHED_CPU_MASK`, `CONFIG_SCHED_CPU_MASK_PIN_ONLY`; `k_thread_cpu_mask_clear/enable/disable/enable_all` and `k_thread_cpu_pin`; the not-runnable requirement and `-EINVAL`; behaviour under PIN_ONLY; backend support (the two pages disagree about multiq, as noted in the skill); spinlock and irq_lock emulation semantics.

Method: documentation only; no commands were run.
