---
id: computing-software.firmware-embedded-development.zephyr.threading-and-work-queues
name: threading-and-work-queues
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr, k-thread, k-work, work-queue, system-workqueue, k-work-submit, k-mutex, k-sem, isr-safe-submit, thread-priority, cooperative-vs-preemptive, k-thread-create, stack-analyze, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Zephyr threading: cooperative vs preemptible priority ranges, k_work queues for ISR-to-thread handoff, and the system workqueue trap when one work item is slow or blocks."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/threads/index.html
  - https://docs.zephyrproject.org/latest/kernel/services/threads/workqueue.html
  - https://docs.zephyrproject.org/latest/kernel/services/synchronization/mutexes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zephyr threading and work queues

**Goal:** pick correct thread priorities and the right ISR-to-thread handoff mechanism, extending the
top-half/bottom-half model from
`computing-software.firmware-embedded-development.device-driver-development.interrupt-driven-driver-architecture`
with Zephyr's priority ranges and work queue semantics.

## Cooperative vs preemptible priority ranges
A thread priority is an integer; numerically lower values take precedence. **Negative** priorities are
cooperative: once such a thread is current it stays current until it does something that makes it unready.
**Non-negative** priorities are preemptible: they can be supplanted at any time when a cooperative thread,
or a preemptible thread of higher or equal priority, becomes ready. Usable ranges are
`-CONFIG_NUM_COOP_PRIORITIES` to -1 and 0 to `CONFIG_NUM_PREEMPT_PRIORITIES - 1` (5 and 10 give -5..-1 and
0..9). A thread's priority can be changed after it starts, so a thread can move between the classes;
the scheduler never re-prioritises on its own.

Use cooperative priorities deliberately, for short latency-critical work that other threads must not
interrupt (hardware interrupts still can). Do not use them as the default. A cooperative thread that never
blocks starves every preemptible thread.

## k_work: ISR-safe handoff to a thread context
A work item is queued with `k_work_submit()` (system workqueue) or `k_work_submit_to_queue()` (a specific
queue) and its handler later runs in the work queue's thread. Both may be called from an ISR or a thread,
and the documentation's example has an ISR offloading its error printing to the system workqueue. If an item
that is already queued is submitted again it is not affected and runs once. A handler may re-submit its own
work item to process in stages. Handlers must not block on things that can take long (taking a semaphore is
the docs' example of a potentially blocking operation).

## The system workqueue trap
`k_work_submit()` uses the **system workqueue**, a single shared thread that kernel and driver code may also
use. The documentation says to define extra work queues only when needed, because each one costs memory, and
justifies one when blocking work items would delay other system workqueue processing unacceptably. Note that
the system workqueue has the lowest cooperative priority by default, so draining it takes precedence over all
preemptible threads, and making it preemptible is risky because drivers may rely on cooperative execution; a
separate lower-priority queue suits low-priority work. A dedicated queue is created with a
`K_THREAD_STACK_DEFINE` stack, `k_work_queue_init()` and `k_work_queue_start()` (stack, size, priority,
optional config). The work queue thread yields between submitted items regardless of its priority.

## Stack sizing
`CONFIG_THREAD_STACK_INFO` plus `k_thread_stack_space_get()`, the thread analyzer or the kernel shell
(`kernel thread list`, `kernel stacks`, with `CONFIG_KERNEL_SHELL`) report actual stack usage. Size stacks from
measured high-water marks under worst-case call depth, including work handler frames, not a guessed constant.

## Synchronization primitives
`k_mutex` (supports priority inheritance), `k_sem` (counting semaphore) and `k_poll` (wait on several
objects or signals at once; see the k-poll skill) cover most needs; use `k_event` when only flags are needed.

## Verify
- [ ] Priorities were chosen against the cooperative/preemptible split and the configured range.
- [ ] Work items on the system workqueue were checked for execution time; slow or blocking work uses its own queue.
- [ ] Stack sizes come from measured usage under worst-case nesting.
- [ ] A deliberately slow work item on the system workqueue was used to check for starvation of other users.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- Priority classes and ranges, runtime priority changes (doc: kernel/services/threads/index).
- ISR submission, resubmission semantics, system workqueue wording and default cooperative priority, `k_work_queue_init` /
  `k_work_queue_start`, workqueue yield, blocking-handler warning (doc: kernel/services/threads/workqueue); mutex priority
  inheritance (doc: kernel/services/synchronization/mutexes).
- Removed: every FreeRTOS comparison (not checkable here), the `k_work_submit_from_isr` aside (no such API is documented),
  the claim that the system workqueue is "single point of contention" in the way of FreeRTOS timers, the `kernel threads`
  shell spelling (now `kernel thread list`) and the claim that `k_poll` has no equivalent elsewhere.

Method: documentation only; no commands were run.
