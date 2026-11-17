---
id: computing-software.firmware-embedded-development.zephyr.event-objects-k-event
name: event-objects-k-event
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [k-event, k-event-post, k-event-wait, k-event-wait-all, event-flags, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Signal multiple conditions with Zephyr k_event bit flags: post vs set vs clear, wait any or all, the reset option, ISR posting, and multi-waiter behaviour."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/synchronization/events.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event objects (k_event)

A `k_event` holds 32 event bits. Producers (threads or ISRs) set bits; threads wait for any or
all of a mask. All waiters whose condition is met wake together.

```
CONFIG_EVENTS=y
```
```c
#define EV_RX    BIT(0)
#define EV_TX    BIT(1)
#define EV_ERR   BIT(2)

K_EVENT_DEFINE(comms_ev);

void uart_isr(const struct device *d, void *u) {
    k_event_post(&comms_ev, EV_RX);           /* ISR-safe */
}

void comms_thread(void *a, void *b, void *c) {
    for (;;) {
        uint32_t ev = k_event_wait(&comms_ev, EV_RX | EV_TX | EV_ERR,
                                   false /*don't reset first*/, K_FOREVER);
        k_event_clear(&comms_ev, ev);         /* consume what we saw */
        if (ev & EV_ERR) recover();
        if (ev & EV_RX)  handle_rx();
        if (ev & EV_TX)  handle_tx();
    }
}
```

## Setting bits
| Call | Effect |
|---|---|
| `k_event_post(&e, bits)` | OR bits in |
| `k_event_set(&e, bits)` | replace all bits with `bits` |
| `k_event_set_masked(&e, bits, mask)` | replace only bits in mask |
| `k_event_clear(&e, bits)` | clear bits |

`k_event_post` returns the bits of the posted mask that were already set; `k_event_set` and
`k_event_clear` return the previous state of the events (see the header comments in `kernel.h`).

## Waiting
- `k_event_wait(&e, mask, reset, timeout)`: any bit in mask. Returns the matching bits, or 0 on
  timeout.
- `k_event_wait_all(&e, mask, reset, timeout)`: all bits in mask.
- `reset = true` clears **all** event bits before waiting, discarding anything already set. Usually
  you want `false` plus an explicit clear after waking, or events posted just before the wait are
  lost.
- `k_event_wait_safe` / `k_event_wait_all_safe` atomically clear the matched bits on return, which
  avoids the lost-event window of a separate `k_event_clear` or of `reset = true`.
- A mask of zero returns 0 immediately.
- From an ISR, waiting is allowed only with `K_NO_WAIT`.
- `k_event_test(&e, mask)` reads without blocking.

## Multiple waiters
Bits are not consumed by waking, so several threads can wait on the same bit (broadcast style).
That is the main difference from a semaphore. Decide who clears.

## vs alternatives
- One waiter, counted events: `k_sem`.
- Need a rendezvous of several threads: wait_all with each thread posting its bit.
- Wait on events plus queues together: `k_poll`.

## Verify
- [ ] Each bit has one owner responsible for clearing it.
- [ ] No `reset = true` unless discarding earlier events is intended.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- 32-bit event word; delivery by thread or ISR; wake of all waiters whose condition is met; the reset option and the
  warning about several waiters (doc: kernel/services/synchronization/events).
- `k_event_post/set/set_masked/clear/wait/wait_all/wait_safe/wait_all_safe/test` signatures and return values, ISR rule
  for waiting, zero-mask behaviour (`include/zephyr/kernel.h`).
- Removed: the FreeRTOS comparison (no source).

Method: documentation only; no commands were run.
