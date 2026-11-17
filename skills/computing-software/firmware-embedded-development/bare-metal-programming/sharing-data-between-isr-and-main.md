---
id: computing-software.firmware-embedded-development.bare-metal-programming.sharing-data-between-isr-and-main
name: sharing-data-between-isr-and-main
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [bare-metal-concurrency, isr-shared-data, torn-read, primask-save-restore, primask, critical-section, double-buffer-swap, sequence-counter, firmware-embedded-development]
level: practitioner
status: draft
description: "Share multi-byte state between interrupt handlers and the main loop without torn reads: choose between atomics, short critical sections, double buffering and sequence counters."
sources:
  - https://www.embedded.com/introduction-to-the-volatile-keyword/
  - https://arm-software.github.io/CMSIS_5/Core/html/group__Core__Register__gr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharing data between ISR and main loop

**Goal:** the main loop never sees a half-updated struct, 64-bit value or multi-field state
written by an ISR, and vice versa.

## The problem
An ISR updating `{x, y, z}` (or a 64-bit timestamp) can preempt the main loop between reading
`x` and `y`: main gets `x` from the new sample and `y` from the old one (a torn read). Bugs are
rare, load-dependent and nearly impossible to reproduce on the bench.

## Options
| Data | Technique |
|---|---|
| single aligned 8/16/32-bit value, write-only by ISR | `volatile` (or atomic) is enough: Cortex-M reads/writes of aligned words are single-copy atomic |
| counters updated by both sides | C11 atomic fetch_add (LDREX/STREX) |
| small struct, infrequent read | critical section with PRIMASK save/restore |
| large struct, high-rate ISR | double buffer with index swap |
| read-mostly struct, ISR must never wait | sequence counter (seqlock) |

## Critical section done right
```c
static inline uint32_t irq_save(void) { uint32_t p = __get_PRIMASK(); __disable_irq(); return p; }
static inline void irq_restore(uint32_t p) { __set_PRIMASK(p); }

sample_t snapshot(void) {
    uint32_t s = irq_save();
    sample_t copy = g_sample;          /* copy, then release quickly */
    irq_restore(s);
    return copy;
}
```
Save/restore (not plain enable) so nested use and calls from already-masked code are correct.
Use `BASEPRI` instead of PRIMASK to keep top-priority interrupts unmasked.

## Double buffer
ISR writes `buf[w]`, then flips `ready_idx = w` (single word store), and next time writes the
other buffer. Main reads `buf[ready_idx]`. Needs care that main finishes reading before the ISR
comes back to that buffer (use 3 buffers if main can be slow).

## Sequence counter (writer never blocks)
```c
/* ISR (writer) */            /* main (reader) */
g_seq++;                      do { s1 = g_seq; while (s1 & 1) s1 = g_seq;
g_data = new;                      copy = g_data;
g_seq++;                           s2 = g_seq; } while (s1 != s2);
```
Odd = write in progress; reader retries if the counter changed. Needs compiler barriers
(`atomic_signal_fence(memory_order_seq_cst)` or `__DMB()`) around the data copy.

## Verify
- [ ] Every ISR-shared variable is listed with its protection technique (code review checklist).
- [ ] Stress test with ISR at max rate and an invariant check in main (e.g. x+y+z checksum
      field) runs for hours without a violation.
