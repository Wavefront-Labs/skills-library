---
id: computing-software.firmware-embedded-development.bare-metal-programming.tick-counter-wraparound-arithmetic
name: tick-counter-wraparound-arithmetic
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [systick-timebase, tick-wraparound, timer-rollover, unsigned-arithmetic, timeout, 49-day-bug, deadline, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write timeout and elapsed-time checks that survive 32-bit tick counter rollover (the 49.7-day bug): unsigned subtraction, signed deadline compare, and testing it."
sources:
  - https://github.com/torvalds/linux/blob/master/include/linux/jiffies.h
  - https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tick counter wraparound arithmetic

**Goal:** time comparisons that keep working when a free-running counter wraps
(a 32-bit millisecond counter wraps after 2^32 ms = 49.7 days; a 16-bit timer every
65.5 ms at 1 MHz).

## The one correct idiom: elapsed = now - start (unsigned)
```c
uint32_t start = g_ms;
while ((uint32_t)(g_ms - start) < TIMEOUT_MS) { /* poll */ }
```
Unsigned subtraction is defined modulo 2^N in C (C11 6.2.5p9), so `now - start` is the true
elapsed ticks as long as the interval is shorter than one full wrap.

## The bug to grep for
```c
if (g_ms > start + TIMEOUT_MS)          // WRONG: start + TIMEOUT wraps, compare fails
uint32_t deadline = g_ms + 500;
if (g_ms >= deadline)                    // WRONG near the wrap: fires immediately
```
Both pass every bench test and fail once in the field after 49 days, which is why fleets see
"device locks up after about seven weeks".

## Deadlines (absolute times) need a signed compare
When you must store a deadline (timer lists, schedulers):
```c
static inline bool time_reached(uint32_t now, uint32_t deadline) {
    return (int32_t)(now - deadline) >= 0;   // valid while |now - deadline| < 2^31
}
```
This is how Linux `time_after()` works. The conversion of an out-of-range unsigned value to
`int32_t` is implementation-defined (C11 6.3.1.3); check your compiler's documentation for the
modulo behaviour this relies on, and record it as a MISRA deviation if you need compliance.

## Narrow counters and integer promotion
For `uint16_t` or `uint8_t` counters, `a - b` promotes to `int` first, so a wrap gives a
negative number. Cast the result back:
```c
uint16_t dt = (uint16_t)(TIM->CNT - start);
```

## Test it without waiting 49 days
- Initialise the tick counter to `0xFFFFFFFF - 5000` at boot in a test build
  (Linux does the same with `INITIAL_JIFFIES`). Any wrap bug shows up 5 s after boot.
- Unit-test the helper on host with `start = 0xFFFFFF00, now = 0x00000010`.

## Verify
- [ ] No `+` on tick values in comparisons anywhere (`grep -n "ms *+\|tick *+"`).
- [ ] Test build with near-wrap initial tick passes all timeout paths.
- [ ] Narrow counter differences are cast back to their width.

## Checked
2026-11-01. Confirmed: C11 draft N1570 6.2.5 (unsigned arithmetic reduced modulo 2^N); Linux include/linux/jiffies.h
(`time_after()` signed-difference compare, `INITIAL_JIFFIES` starting the counter shortly before wrap); the
49.7-day and 65.5 ms figures follow from 2^32 ms and 2^16 us. Removed: the claim that every named compiler does
modulo conversion.
Method: documentation only; no commands were run.

