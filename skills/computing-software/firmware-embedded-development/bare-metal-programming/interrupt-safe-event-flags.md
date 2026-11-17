---
id: computing-software.firmware-embedded-development.bare-metal-programming.interrupt-safe-event-flags
name: interrupt-safe-event-flags
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [event-flags-bitmask, bare-metal-concurrency, atomic-fetch-or, event-driven, superloop-events, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Signal events from ISRs to a bare-metal main loop with a bitmask set by atomic_fetch_or and taken with atomic_exchange, so no event is lost to a read-modify-write race."
sources:
  - https://en.cppreference.com/w/c/atomic/atomic_fetch_or
  - https://en.cppreference.com/w/c/atomic
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interrupt-safe event flag bitmasks

A common superloop pattern: ISRs set bits in a global word, `main` checks and clears them. The
naive version loses events.

## Naive version and its race
```c
volatile uint32_t g_events;
void UART_IRQHandler(void) { g_events |= EV_RX; }      /* load, OR, store */
void TIM_IRQHandler(void)  { g_events |= EV_TICK; }

/* main */
if (g_events & EV_RX) { g_events &= ~EV_RX; handle_rx(); }
```
`|=` and `&=` are separate load, modify and store steps. If the timer interrupt fires between
main's load and store of `g_events &= ~EV_RX`, main writes back the old value and `EV_TICK` is
lost. The same applies between two ISRs when one can preempt the other.

## Correct: atomic set, atomic take
```c
#include <stdatomic.h>
static atomic_uint g_events;

void UART_IRQHandler(void) { atomic_fetch_or_explicit(&g_events, EV_RX, memory_order_release); }

int main(void) {
    for (;;) {
        uint32_t ev = atomic_exchange_explicit(&g_events, 0, memory_order_acquire);
        if (ev == 0) { sleep_until_event(); continue; }
        if (ev & EV_RX)   handle_rx();
        if (ev & EV_TICK) handle_tick();
    }
}
```
- cppreference: `atomic_fetch_or` atomically replaces the value with the bitwise OR of the old
  value and the argument and returns the previous value; it is a read-modify-write operation. The
  plain form orders memory accesses as `memory_order_seq_cst`; the `_explicit` form takes the order
  and all values are permitted.
- `atomic_exchange` swaps a value with the atomic object, so reading all pending bits and clearing
  them is one step.
- Whether the compiler emits an inline sequence or a library call depends on the target; check
  the disassembly. Where no lock-free sequence exists, a fallback is to save the interrupt mask,
  read and clear the word, then restore the mask:
```c
uint32_t key = irq_save(); uint32_t ev = g_events; g_events = 0; irq_restore(key);
```

## Semantics to decide
- A bitmask coalesces: several interrupts of one kind before main runs give one bit. The handler
  must drain everything pending (read the whole ring buffer), not assume one event is one byte.
- If you need counts, use per-event atomic counters or a queue.
- Sleeping: checking for events and then sleeping has a window where an event arrives after the
  check and before the sleep instruction. Use a race-free superloop sleep pattern.

## Verify
- [ ] Stress test: two timers at high coprime rates set different bits; compare handled events with
  ISR counts over minutes; no deficit beyond coalescing.
- [ ] Disassembly shows an atomic sequence or an interrupt-masked section around every flag update.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on the cppreference pages: atomic_fetch_or and atomic_exchange semantics, seq_cst default, explicit-order form, the atomic operations library listing.
Removed because the cited pages do not state them: that these calls compile to LDREX/STREX loops on M3/M4/M7/M33 and to library calls on M0/M0+, and the Arm Compiler reference (dui0553) which could not be fetched.
