---
id: computing-software.firmware-embedded-development.freertos.reader-writer-locks
name: reader-writer-locks
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [reader-writer-lock, rwlock, shared-exclusive-access, writer-starvation, freertos, firmware-embedded-development]
level: advanced
status: draft
description: "Build a reader-writer lock on FreeRTOS primitives (it has none built in): a writer-preferring design, priority-inversion limits, and when a plain mutex is the better choice."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes
  - https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reader-writer locks on FreeRTOS

FreeRTOS has no rwlock. Before building one, measure: on a single core, a mutex around a short
read is almost always cheaper than any rwlock. Use a rwlock only when reads are long (walking a
table, formatting a config dump) and frequent, and writes are rare.

## Writer-preferring implementation
```c
typedef struct {
    SemaphoreHandle_t mtx;        /* protects the counters, held briefly */
    SemaphoreHandle_t writeGate;  /* binary; held by a writer or by the reader group */
    uint32_t readers;
    uint32_t writersWaiting;
} rwlock_t;

void rw_init(rwlock_t *l) {
    l->mtx = xSemaphoreCreateMutex();
    l->writeGate = xSemaphoreCreateBinary();
    xSemaphoreGive(l->writeGate);
    l->readers = l->writersWaiting = 0;
}

void rw_read_lock(rwlock_t *l) {
    for (;;) {
        xSemaphoreTake(l->mtx, portMAX_DELAY);
        if (l->writersWaiting == 0) {
            if (l->readers++ == 0) xSemaphoreTake(l->writeGate, portMAX_DELAY); /* first reader locks out writers */
            xSemaphoreGive(l->mtx);
            return;
        }
        xSemaphoreGive(l->mtx);
        vTaskDelay(1);                       /* let the waiting writer in */
    }
}

void rw_read_unlock(rwlock_t *l) {
    xSemaphoreTake(l->mtx, portMAX_DELAY);
    if (--l->readers == 0) xSemaphoreGive(l->writeGate);   /* last reader releases */
    xSemaphoreGive(l->mtx);
}

void rw_write_lock(rwlock_t *l) {
    xSemaphoreTake(l->mtx, portMAX_DELAY); l->writersWaiting++; xSemaphoreGive(l->mtx);
    xSemaphoreTake(l->writeGate, portMAX_DELAY);
    xSemaphoreTake(l->mtx, portMAX_DELAY); l->writersWaiting--; xSemaphoreGive(l->mtx);
}

void rw_write_unlock(rwlock_t *l) { xSemaphoreGive(l->writeGate); }
```
`writeGate` is a **binary semaphore**, not a mutex, because the reader that takes it is often
not the reader that gives it; mutexes must be given by their holder.

## Limits
- No priority inheritance through `writeGate`: a high-priority writer waiting on low-priority
  readers can suffer unbounded inversion if medium-priority tasks run. Keep read sections short
  or run readers at the same priority.
- The `vTaskDelay(1)` back-off is a deliberate simplification; it costs a tick of latency for
  readers while a writer waits.
- Not usable from ISRs. Not recursive: a reader taking the read lock twice while a writer waits
  deadlocks.

## Alternatives
- Double buffering / seqlock: writer fills a shadow copy, then swaps a pointer inside a short
  critical section; readers never block.
- Single owner task (gatekeeper) that answers read requests from a queue.

## Verify
- [ ] Stress test: several readers plus a writer looping; invariants of the shared data hold.
- [ ] Writer latency under continuous reads is bounded (writer preference works).
