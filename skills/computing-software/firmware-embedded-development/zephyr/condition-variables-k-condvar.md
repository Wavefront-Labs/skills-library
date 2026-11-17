---
id: computing-software.firmware-embedded-development.zephyr.condition-variables-k-condvar
name: condition-variables-k-condvar
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [k-condvar, k-condvar-wait, k-condvar-signal, k-condvar-broadcast, predicate-loop, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Wait for a shared-state condition in Zephyr with k_condvar and k_mutex: the predicate loop, signal vs broadcast, timeouts, and why ISRs cannot participate."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/synchronization/condvar.html
  - https://docs.zephyrproject.org/latest/kernel/services/synchronization/mutexes.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/kernel.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Condition variables (k_condvar)

Use when threads must wait for a **predicate over shared state** ("queue has at least N items",
"all workers idle"), protected by a mutex.

```c
K_MUTEX_DEFINE(lock);
K_CONDVAR_DEFINE(changed);
static int free_slots = 4;

void acquire_slot(void) {
    k_mutex_lock(&lock, K_FOREVER);
    while (free_slots == 0) {                       /* ALWAYS a loop */
        k_condvar_wait(&changed, &lock, K_FOREVER); /* atomically unlocks, sleeps, relocks */
    }
    free_slots--;
    k_mutex_unlock(&lock);
}

void release_slot(void) {
    k_mutex_lock(&lock, K_FOREVER);
    free_slots++;
    k_condvar_signal(&changed);                    /* wake one waiter */
    k_mutex_unlock(&lock);
}
```

## Rules
- **Predicate loop:** after waking, re-check the condition. Another thread may have consumed the
  state between the signal and this thread reacquiring the mutex.
- Modify the shared state and signal while holding the mutex.
- `k_condvar_signal` wakes one waiting thread; `k_condvar_broadcast` wakes all and returns the
  number of woken threads; use broadcast when different waiters wait on different predicates over
  the same state.
- Timed wait: `k_condvar_wait(&cv, &m, K_MSEC(50))` returns `-EAGAIN` on timeout. Whether the wait
  was signalled, timed out or was non-blocking, it returns with the mutex locked by the caller.
  Compute remaining time across loop iterations if a total deadline matters.

## Limitations
- Mutexes are not designed for use by ISRs, so an ISR can't take the mutex to change the
  predicate state and signal. For ISR producers, use a semaphore, `k_event`, or `k_poll_signal`
  instead.
- The loop is required for the reason above regardless of whether a particular implementation
  produces spurious wake-ups.

## When not to
- Pure counting: `k_sem`.
- Waiting for bit flags: `k_event`.
- Passing data: `k_msgq`/`k_fifo`.

## Verify
- [ ] Every `k_condvar_wait` sits inside a `while (!predicate)` loop.
- [ ] State changes and signals happen with the mutex held.
- [ ] No ISR touches the predicate state.

## Checked

Checked 2026-10-25 against the Zephyr source (main, post-4.4; latest release v4.4.2): doc/kernel/services/synchronization/condvar.rst, mutexes.rst and include/zephyr/kernel.h.
Confirmed: `K_CONDVAR_DEFINE`, `k_condvar_wait` (atomically releases the mutex, re-locks it on every return, `-EAGAIN` on timeout), `k_condvar_signal` (one thread), `k_condvar_broadcast` (all threads, returns the count), mutexes not designed for ISRs.

Method: documentation only; no commands were run.
