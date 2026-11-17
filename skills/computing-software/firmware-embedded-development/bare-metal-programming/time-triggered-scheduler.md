---
id: computing-software.firmware-embedded-development.bare-metal-programming.time-triggered-scheduler
name: time-triggered-scheduler
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [time-triggered-scheduler, ttc-scheduler, static-schedule, major-cycle, minor-cycle, task-overrun, safety-critical, pont, firmware-embedded-development]
level: advanced
status: draft
description: "Implement a time-triggered co-operative scheduler: tick-driven task table with periods and offsets, major/minor cycle planning, overrun detection, and a single timer interrupt."
sources:
  - https://www.safetty.net/publications/pttes
  - https://www.safetty.net/publications/the-engineering-of-reliable-embedded-systems-second-edition
  - https://developer.arm.com/documentation/ddi0403/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Time-triggered scheduler

**Goal:** a highly predictable architecture (Pont's TTC) where the only interrupt is a
periodic tick and every task runs at a statically planned time, so timing can be analysed
and tested exhaustively. Common in safety-related and automotive bare-metal designs.

## Structure
```c
typedef struct { void (*fn)(void); uint16_t period; uint16_t delay; uint16_t wcet_us; } tt_task_t;
static tt_task_t sched[] = {
    { sensor_read, 1, 0 },   /* every tick (1 ms) */
    { control,     5, 1 },   /* every 5 ms, offset 1 ms */
    { comms,      10, 2 },
    { ui,        100, 3 },
};
static volatile uint32_t tick_pending;
void SysTick_Handler(void) { tick_pending++; }   /* the ONLY enabled interrupt */

void tt_dispatch(void) {
    while (tick_pending) {
        __disable_irq(); tick_pending--; __enable_irq();
        for (unsigned i = 0; i < ARRAY_SIZE(sched); i++)
            if (sched[i].delay == 0) { sched[i].fn(); sched[i].delay = sched[i].period - 1; }
            else sched[i].delay--;
    }
    __WFI();   /* wait for next tick */
}
```

## Planning the schedule
- **Minor cycle** = tick period; **major cycle** = LCM of all task periods (here 100 ms).
- Use **offsets** to spread tasks so the sum of WCETs in any single tick < tick period
  (with margin, e.g. 70 %). Draw the major cycle as a table tick by tick.
- Peripherals are **polled** by tasks rather than interrupt-driven; UART RX uses DMA or a
  hardware FIFO deep enough to cover one polling period.
- Choose the tick from the tightest period; a faster tick wastes CPU on dispatch.

## Overrun detection
- `tick_pending > 1` at dispatch means a tick's tasks overran into the next: log it, and in
  safety designs move to a safe state.
- Measure each task's WCET with the DWT cycle counter; check against the budget in the
  table. A watchdog kicked once per major cycle catches lock-ups.

## Variants
- **TTH (time-triggered hybrid)**: one short pre-emptive task in the tick ISR itself for a
  hard deadline, rest co-operative.
- Replace the countdown with a precomputed table indexed by `tick % major_cycle` for
  cheaper, fully static dispatch.

## Gotchas
- Any extra enabled interrupt breaks the timing analysis; review vector enables.
- Long tasks must be split into state-machine steps that fit in one slot.
- Jitter of a task = variation of the WCETs of tasks run before it in the same tick;
  order the table to put jitter-sensitive tasks first.

## Verify
- [ ] GPIO per task on a logic analyser over a full major cycle matches the planned table.
- [ ] Overrun counter stays at zero under worst-case input.
