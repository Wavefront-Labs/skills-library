---
id: computing-software.software-engineering.concurrency.seqlocks-and-versioned-reads
name: seqlocks-and-versioned-reads
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, seqlock, versioned-reads, optimistic-reads, memory-ordering, stampedlock]
level: sme
status: docs-checked
description: "Use seqlocks and versioned optimistic reads for read-mostly data: sequence counter protocol, Java StampedLock, and when seqlocks are the wrong tool."
sources: ["https://www.kernel.org/doc/html/latest/locking/seqlock.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/StampedLock.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Seqlocks and versioned reads

## Idea (Linux kernel documentation)
Sequence counters are a reader-writer consistency mechanism with lockless readers (read-only retry loops) and no writer starvation. They suit data that is rarely written (for example system time), where the reader wants a consistent set of information and will retry if it changes.
- Writers increment the sequence count at the start and the end of their critical section. While it is odd, an update is in progress; at the end it is even again.
- A data set is consistent when the count at the start of the read section is even and the same value is read again at the end. The data must be copied out inside the read section; if the count changed, the reader must retry.
- Kernel API: `read_seqbegin` / `read_seqretry` for `seqlock_t`; `read_seqcount_begin` / `read_seqcount_retry` for bare `seqcount_t`.
- Normal readers never block a writer and writers do not wait for readers.

## Constraints
- Cannot be used if the protected data contains pointers: the writer can invalidate a pointer the reader is following.
- A write-side critical section must never be preempted or interrupted by read-side sections; otherwise the reader spins for the scheduler tick on the odd count, and a real-time reader can spin forever and livelock the kernel.
- Readers can see inconsistent data before validation: copy first, use only after the count check.
- Under a sharp spike in write activity lockless readers can retry too much; the kernel offers a conditional form (`read_seqbegin_or_lock`) that retries lockless once and then takes the lock.

## Java: StampedLock optimistic reads
```java
long stamp = lock.tryOptimisticRead();
double cx = x, cy = y;
if (!lock.validate(stamp)) {
    stamp = lock.readLock();
    try { cx = x; cy = y; } finally { lock.unlockRead(stamp); }
}
```
- `tryOptimisticRead()` returns a stamp, or zero if exclusively locked; `validate(stamp)` returns true if the lock has not been acquired in write mode since the stamp was issued, and always false for a zero stamp.
- Javadoc: optimistic mode is an extremely weak read lock that a writer can break at any time; for short read-only sections it often reduces contention and improves throughput, but is inherently fragile. Read fields into local variables and use them only after validation; fields read before validation may be wildly inconsistent.
- Reading an object or array reference and then dereferencing it needs extra consistency checks or repeated `validate`.
- Without a successful `validate` there is no guarantee that reads between `tryOptimisticRead` and `validate` form a consistent snapshot.
- Not reentrant; no notion of ownership (a lock acquired in one thread can be released in another); scheduling does not consistently prefer readers or writers.
- Intended as an internal utility for building thread-safe components.

## Checked
2026-11-08. Confirmed against the Linux kernel seqlock documentation and the Java 21 StampedLock Javadoc. Removed: the C++ writer/reader fence code and the claim about C++/Rust undefined behaviour with Boehm's paper (not on the cited pages and the HP report did not load), the `jiffies` claim (the kernel page says system time), and the RCU / copy-on-write alternatives line. The HP Labs PDF was unreadable and was dropped from sources.
Method: documentation only; no commands were run.
