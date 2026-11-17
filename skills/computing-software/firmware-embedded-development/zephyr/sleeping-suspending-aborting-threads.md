---
id: computing-software.firmware-embedded-development.zephyr.sleeping-suspending-aborting-threads
name: sleeping-suspending-aborting-threads
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [k-sleep, k-msleep, k-usleep, k-wakeup, k-thread-suspend, k-thread-abort, k-thread-join, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Control Zephyr thread execution with k_sleep/k_msleep/k_usleep, k_wakeup, k_thread_suspend/resume, k_thread_abort and k_thread_join, including timeout and tick rounding."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/threads/index.html
  - https://docs.zephyrproject.org/latest/kernel/services/timing/clocks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sleeping, suspending and aborting threads

## Sleep
```c
k_msleep(100);                 /* ms */
k_usleep(250);                 /* us; the docs warn to read the k_usleep notes before using it */
k_sleep(K_SECONDS(2));         /* k_timeout_t form */
int32_t left = k_msleep(500);  /* returns ms remaining if woken early by k_wakeup */
```
- Sleep granularity is the system tick (`CONFIG_SYS_CLOCK_TICKS_PER_SEC`, default 10000 with
  `CONFIG_TICKLESS_KERNEL`, else 100); the sleeps return the time left rounded up to the
  millisecond. For short delays use `k_busy_wait(us)` (spins, does not yield; its clock may be
  skewed relative to `k_sleep`, and it may not work with `CONFIG_SYSTEM_CLOCK_SLOPPY_IDLE` plus
  `CONFIG_PM`).
- Periodic loop without drift: compute absolute deadlines with `K_TIMEOUT_ABS_MS()` or use a
  `k_timer` with `k_timer_status_sync`.
```c
int64_t next = k_uptime_get();
for (;;) {
    next += 10;
    k_sleep(K_TIMEOUT_ABS_MS(next));   /* absolute timeouts need CONFIG_TIMEOUT_64BIT (default y) */
    sample();
}
```
- `k_yield()` gives the CPU to other ready threads of the **same or higher** priority; with none
  ready it returns immediately.

## Wake early
`k_wakeup(tid)` ends a `k_sleep` immediately (the sleep returns the time left); if the thread is
not sleeping it has no effect.

## Suspend / resume
`k_thread_suspend(tid)` stops the scheduler from running a thread (kernel objects it waits on are
still handed to it, and a timeout that expires while suspended does not resume it);
`k_thread_resume(tid)` removes the suspension. Suspending an already suspended thread has no
additional effect, so suspensions do not count. Do not use suspend/resume for synchronisation; use
a semaphore. Threads created with a `K_FOREVER` delay are started with `k_thread_start`.

## Abort and join
```c
k_thread_abort(tid);              /* thread stops; shared resources it owns are NOT reclaimed */
int rc = k_thread_join(tid, K_MSEC(100));   /* 0 = exited, -EBUSY (K_NO_WAIT), -EAGAIN (timeout), -EDEADLK */
```
- A thread function returning is equivalent to self-abort.
- After abort/exit, a `K_THREAD_STACK_DEFINE`d stack and `struct k_thread` can be reused for a new
  `k_thread_create` once join has returned.
- Aborting a thread holding a mutex or partway through updating shared data leaves it
  inconsistent. Prefer asking the thread to exit (flag + `k_wakeup`/`k_sem_give`) and joining.
- Termination or abort of a thread created with `K_ESSENTIAL` is treated as a fatal error.

## Verify
- [ ] Delay values reviewed against tick rate; short waits use `k_busy_wait` deliberately.
- [ ] Periodic threads use absolute deadlines or `k_timer`, not repeated `k_msleep(period)`.
- [ ] Thread shutdown uses cooperative exit + `k_thread_join`, not bare abort.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- `k_msleep` / `k_usleep` / `k_sleep` return values (`include/zephyr/sleep.h`); `k_busy_wait`, `k_yield`, `k_wakeup`,
  `k_thread_suspend`, `k_thread_join` return codes (`kernel.h`); abort, suspend and `K_ESSENTIAL` wording (doc:
  kernel/services/threads/index).
- `CONFIG_SYS_CLOCK_TICKS_PER_SEC` and `CONFIG_TIMEOUT_64BIT` defaults (`kernel/Kconfig`).
- Wrong or removed: "k_yield only to equal or higher" reworded to "same or higher"; the `k_usleep` rounding claim and
  the "kernel panic" wording for essential threads were replaced with documented statements.

Method: documentation only; no commands were run.
