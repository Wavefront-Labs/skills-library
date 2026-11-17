---
id: computing-software.firmware-embedded-development.zephyr.k-poll-multiple-object-wait
name: k-poll-multiple-object-wait
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-data-passing, k-poll, k-poll-event, k-poll-signal, config-poll, wait-multiple-objects, event-loop-thread, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Wait on several Zephyr kernel objects at once with k_poll (semaphores, FIFOs, msgqs, signals): event setup, state reset rules and when k_event is simpler."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/polling.html
  - https://docs.zephyrproject.org/latest/kernel/services/synchronization/events.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Waiting on multiple objects with k_poll

**Goal:** one thread that reacts to whichever of several sources becomes ready first (a
command FIFO, a data semaphore, a shutdown signal), without one thread per source.

## Setup
```c
/* prj.conf: CONFIG_POLL=y */
K_SEM_DEFINE(data_sem, 0, 1);
K_FIFO_DEFINE(cmd_fifo);
static struct k_poll_signal stop_sig = K_POLL_SIGNAL_INITIALIZER(stop_sig);

struct k_poll_event events[] = {
    K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_SEM_AVAILABLE, K_POLL_MODE_NOTIFY_ONLY, &data_sem, 0),
    K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_FIFO_DATA_AVAILABLE, K_POLL_MODE_NOTIFY_ONLY, &cmd_fifo, 0),
    K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_SIGNAL, K_POLL_MODE_NOTIFY_ONLY, &stop_sig, 0),
};

for (;;) {
    k_poll(events, ARRAY_SIZE(events), K_FOREVER);
    if (events[0].state == K_POLL_STATE_SEM_AVAILABLE) {
        k_sem_take(&data_sem, K_NO_WAIT);          /* poll does NOT take it for you */
        handle_data();
    }
    if (events[1].state == K_POLL_STATE_FIFO_DATA_AVAILABLE) {
        struct cmd *c = k_fifo_get(&cmd_fifo, K_NO_WAIT);
        if (c) handle_cmd(c);
    }
    if (events[2].state == K_POLL_STATE_SIGNALED) {
        k_poll_signal_reset(&stop_sig);
        break;
    }
    for (size_t i = 0; i < ARRAY_SIZE(events); i++)
        events[i].state = K_POLL_STATE_NOT_READY;  /* must reset before next k_poll */
}
```

## Rules
- `k_poll` only **reports readiness**; you still take/get the object with `K_NO_WAIT`, and it
  may already be gone if another thread got there first (handle NULL / -EBUSY).
- Reset every event's `state` to `K_POLL_STATE_NOT_READY` before polling again, or the next
  call returns immediately.
- Several events can be ready at once: check all of them each iteration.
- Signals (`k_poll_signal_raise(&sig, result)`) carry an int result. Reset both the event state and
  the signal (`k_poll_signal_reset`) on each loop iteration, or the next poll returns at once.
- Only one thread can poll a specific object. The docs recommend polling when a single "dispatcher"
  thread is the only one acquiring the objects, because an object is signalled only if no other
  thread is waiting for it.
- `k_poll` returns 0 on success and `-EAGAIN` on timeout. A closed `k_pipe` counts as ready
  (`K_POLL_TYPE_PIPE_DATA_AVAILABLE`), so read it to get `-EPIPE` and stop polling it.

## Simpler alternative: k_event
If the sources are just flags (no data object), `k_event` (CONFIG_EVENTS) is lighter:
`k_event_post(&ev, BIT(0))` from anywhere, and `k_event_wait(&ev, BIT(0)|BIT(1), false,
K_FOREVER)` returns the set bits. Use `k_event_clear` to consume.

## Verify
- [ ] All sources are serviced under simultaneous load (no starvation of later events).
- [ ] No busy-looping: thread CPU usage near zero when idle (`thread analyzer` / tracing).

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- Event types and initialisers, state reset rule in loops, signal reset rule, single-poller note, `-EAGAIN` on timeout
  (doc: kernel/services/polling).
- Removed: the "-EADDRINUSE in some versions" sentence (the docs only mention it in a comment) and the unsourced
  ISR-safe claim for `k_poll_signal_raise`.

Method: documentation only; no commands were run.
