---
id: computing-software.firmware-embedded-development.bare-metal-programming.tick-driven-timeout-lists
name: tick-driven-timeout-lists
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [software-timer-list, systick-timebase, timeout, delta-list, bare-metal-timers, firmware-embedded-development]
level: practitioner
status: draft
description: "Build bare-metal software timers on a millisecond tick: polled deadline structs, a sorted delta list for many timers, and wrap-safe expiry checks."
sources:
  - https://developer.arm.com/documentation/dui0553/latest/
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Timeout lists driven by a tick

## Level 1: polled deadlines (enough for most superloops)
```c
typedef struct { uint32_t start, period; } sw_timer_t;
static inline void tmr_start(sw_timer_t *t, uint32_t ms) { t->start = g_ticks; t->period = ms; }
static inline bool tmr_expired(const sw_timer_t *t) {
    return (uint32_t)(g_ticks - t->start) >= t->period;   /* wrap-safe unsigned subtraction */
}
/* main loop */
if (tmr_expired(&led_tmr)) { led_tmr.start += led_tmr.period; toggle_led(); }  /* += keeps phase, no drift */
```
`g_ticks` is a `volatile uint32_t` incremented in SysTick. 32-bit reads are atomic on Cortex-M.
Never compare `g_ticks >= deadline`: it breaks at the 49.7-day wrap.

## Level 2: callback timers in a sorted delta list
For dozens of timers with callbacks, keep them in a list sorted by expiry where each node
stores the delta to the previous one. The tick ISR decrements only the head.
```c
typedef struct tmr { struct tmr *next; uint32_t delta; void (*cb)(void *); void *arg; } tmr_t;
static tmr_t *head;

void tmr_add(tmr_t *t, uint32_t ms) {          /* call with tick IRQ masked */
    tmr_t **pp = &head;
    while (*pp && (*pp)->delta <= ms) { ms -= (*pp)->delta; pp = &(*pp)->next; }
    t->delta = ms; t->next = *pp;
    if (*pp) (*pp)->delta -= ms;
    *pp = t;
}
void SysTick_Handler(void) {
    g_ticks++;
    if (head && head->delta) head->delta--;
    if (head && head->delta == 0) g_timer_due = true;  /* run callbacks in main, not in the ISR */
}
```
In main: while the head has delta 0, unlink it (under a critical section) and call its callback.
Insertion is O(n), tick is O(1).

## Level 3: timer wheel
Hashed wheels (bucket = expiry % N) give O(1) insert for hundreds of timers; overkill for most MCUs.

## Gotchas
- Running callbacks in the SysTick ISR makes the tick jitter and forbids blocking work; set a
  flag or pend a low-priority interrupt.
- Modifying the list from main while the ISR touches the head needs the tick interrupt masked
  (BASEPRI or PRIMASK) during `tmr_add/remove`.
- A 1 ms tick costs wakeups in low-power designs: use a low-power timer compare set to the head
  timer's expiry (tickless) instead.
- Restarting a periodic timer with `start = g_ticks` after a late service drifts; `start += period`
  doesn't.

## Verify
- [ ] Set `g_ticks` to `0xFFFFF000` at boot and confirm timers fire correctly across the wrap.
- [ ] A 1000 ms periodic timer toggling a GPIO shows no cumulative drift on a scope over minutes.
