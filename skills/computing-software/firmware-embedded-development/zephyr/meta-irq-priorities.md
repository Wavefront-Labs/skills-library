---
id: computing-software.firmware-embedded-development.zephyr.meta-irq-priorities
name: meta-irq-priorities
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [meta-irq, config-num-metairq-priorities, cooperative-threads, interrupt-bottom-half, zephyr, firmware-embedded-development]
level: sme
status: docs-checked
description: "Use Zephyr meta-IRQ thread priorities as interrupt bottom halves that preempt even cooperative threads, with the rules that keep them from breaking the system."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/threads/index.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/kernel/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Meta-IRQ priorities

Zephyr thread priorities: negative = cooperative (never preempted by other threads), zero and
positive = preemptible. `CONFIG_NUM_METAIRQ_PRIORITIES=N` reserves the **N highest** cooperative
priorities as meta-IRQ priorities. A meta-IRQ thread preempts all threads at lower priorities, including
cooperative ones and ones that hold a scheduler lock, as soon as it becomes ready (it can also preempt meta-IRQ
threads of lower priority). It is still a thread: hardware interrupts can interrupt it, and it runs on its own
stack (not the interrupt stack).

```
CONFIG_NUM_COOP_PRIORITIES=16
CONFIG_NUM_METAIRQ_PRIORITIES=1
```
The meta-IRQ priorities are the numerically lowest end of the range, starting at `K_HIGHEST_THREAD_PRIO`
(= `-CONFIG_NUM_COOP_PRIORITIES`); the default for `CONFIG_NUM_METAIRQ_PRIORITIES` is 0 (disabled).

```c
K_THREAD_DEFINE(radio_bh, 1024, radio_bh_fn, NULL, NULL, NULL,
                K_HIGHEST_THREAD_PRIO, 0, 0);

static K_SEM_DEFINE(radio_sem, 0, 1);

void radio_isr(const void *arg) { k_sem_give(&radio_sem); }

void radio_bh_fn(void *a, void *b, void *c) {
    for (;;) {
        k_sem_take(&radio_sem, K_FOREVER);
        radio_process_event();      /* short: preempts cooperative code */
    }
}
```
The documentation's intent: interrupt "bottom half" or "tasklet" processing in driver subsystems. Unblocking
a meta-IRQ thread from a lower-priority thread acts like a synchronous system call; from interrupt context it
acts like an ARM-style pended IRQ. The thread is guaranteed to run before the current CPU returns into
application code.

## Rules
- Keep meta-IRQ work short and bounded. It breaks the "cooperative threads run until they yield"
  guarantee that cooperative code relies on; long meta-IRQ work causes latency everywhere.
- A cooperative (or schedule-locked) thread preempted by a meta-IRQ thread resumes on the same CPU, assuming it
  was neither suspended nor aborted.
- Cooperative code that assumed atomicity by not yielding is no longer atomic with respect to
  meta-IRQ threads: protect data shared with them (for example with a `k_spinlock`).
- The docs say the feature breaks the promise that other threads are not scheduled until the current cooperative
  thread blocks, so it should be used only with great care: these are not simply very high priority threads.

## When to use
Only when you need a thread-context bottom half that beats cooperative threads. For normal deferred ISR work, a high-priority preemptible
thread or a dedicated work queue is simpler.

## Verify
- [ ] Meta-IRQ thread execution time measured (thread runtime stats or GPIO) and bounded.
- [ ] Shared data between meta-IRQ and cooperative threads is lock-protected.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- Meta-IRQ semantics, own stack, same-CPU note, "synchronous system call" analogy and the warning (doc:
  kernel/services/threads/index, section Meta-IRQ Priorities); `CONFIG_NUM_METAIRQ_PRIORITIES` (default 0) and
  `CONFIG_NUM_COOP_PRIORITIES` (default 16) (`kernel/Kconfig`); `K_HIGHEST_THREAD_PRIO` (`kernel.h`).
- Wrong or removed: the claim that the scheduler returns to the preempted cooperative thread even when a
  higher-priority cooperative thread is ready, the Bluetooth/network driver usage, the priority-inheritance remark and
  the "one or two levels" rule (none documented).

Method: documentation only; no commands were run.
