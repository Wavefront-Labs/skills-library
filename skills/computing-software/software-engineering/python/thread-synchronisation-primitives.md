---
id: computing-software.software-engineering.python.thread-synchronisation-primitives
name: thread-synchronisation-primitives
category: computing-software
field: software-engineering
product: python
tags: [python, threading-lock, python-queue, threading-event, condition, rlock, python-threading]
level: practitioner
status: verified
description: "Coordinate Python threads: Lock/RLock for shared state, queue.Queue handoff, Event for shutdown, Condition and Barrier, and what the GIL does not protect."
sources: ["https://docs.python.org/3/library/threading.html", "https://docs.python.org/3/library/queue.html", "https://docs.python.org/3/howto/free-threading-python.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread synchronisation primitives

**Goal:** threaded code with no lost updates, no deadlocks and a clean shutdown path.

## The GIL is not a lock for your code
`counter += 1` is several bytecodes (load, add, store); threads can interleave between
them and lose updates (4 threads x 1M increments lost none on the GIL build of 3.14.0 in one run, so a passing test proves nothing, but lost about 75% on the free-threaded 3.14.8 build). On free-threaded CPython (3.13t+) even more races surface. Protect
every read-modify-write of shared state.

## Lock / RLock
```python
import threading
class Stats:
    def __init__(self):
        self._lock = threading.Lock()
        self._counts = {}
    def incr(self, key):
        with self._lock:                         # always via `with`: released on exceptions
            self._counts[key] = self._counts.get(key, 0) + 1
    def snapshot(self):
        with self._lock:
            return dict(self._counts)            # copy out; never return the guarded object
```
`RLock` lets the same thread re-acquire (recursive helper calls); needing it is often a
design smell. `lock.acquire(timeout=5)` returns False on timeout - useful for deadlock
diagnosis.

## queue.Queue: prefer message passing
```python
import queue
q = queue.Queue(maxsize=1000)
SENTINEL = object()
def consumer():
    while (item := q.get()) is not SENTINEL:
        try: handle(item)
        finally: q.task_done()
    q.task_done()
t = threading.Thread(target=consumer, daemon=False); t.start()
for x in items: q.put(x)        # blocks when full: backpressure
q.put(SENTINEL); q.join(); t.join()
```
Queue does its own locking; threads share nothing else. 3.13 adds `q.shutdown()`.

## Event: signals and graceful stop
```python
stop = threading.Event()
def poller():
    while not stop.is_set():
        poll_once()
        stop.wait(5)            # sleeps 5 s but wakes immediately on stop.set()
# on SIGTERM / exit:
stop.set(); t.join(timeout=10)
```

## Condition and Barrier
`Condition` = lock + wait/notify for "wait until state X" (always wait in a `while` loop
re-checking the predicate, or use `cond.wait_for(pred)`). `Barrier(n)` makes n threads meet
before continuing (phased simulations, tests). `Semaphore(n)` limits concurrent access to a
resource.

## Deadlock avoidance
- Acquire multiple locks in one global order.
- Never call unknown code (callbacks, logging handlers that lock) while holding a lock.
- Diagnose hangs: `faulthandler.dump_traceback_later(30)` or `py-spy dump --pid <pid>`.

## Daemon threads
`daemon=True` threads are killed abruptly at interpreter exit (no finally blocks, partial
writes). Use non-daemon threads plus an Event for anything that writes data.

## Verify
- [ ] Every shared mutable object has one documented lock (or is only touched via a Queue).
- [ ] Shutdown test: set the stop event, all threads join within the timeout.

## Checked
- Python 3.14.0 and free-threaded 3.14.8: `counter += 1` disassembles to load, add, store; 4 threads x 1M unlocked increments gave 4,000,000 on the GIL build but 1,042,756 on the free-threaded build; the `Stats` lock class gave 400000; `acquire(timeout)` returned False; `RLock` re-entry; Queue with sentinel and `task_done`/`join`; `queue.Queue.shutdown` exists and raises `queue.ShutDown`; `Event.wait` woke at once on `set()`; `Condition.wait_for`, `Barrier(3)`, `Semaphore(2)` (max 2 concurrent); a daemon thread's `finally` did not run at exit; `faulthandler.dump_traceback_later(1)` dumped stacks. `py-spy dump` is covered in the profiling skill.
