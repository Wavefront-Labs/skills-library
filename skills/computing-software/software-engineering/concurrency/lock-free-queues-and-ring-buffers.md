---
id: computing-software.software-engineering.concurrency.lock-free-queues-and-ring-buffers
name: lock-free-queues-and-ring-buffers
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, lock-free, ring-buffer, spsc-queue, mpmc-queue, disruptor, memory-ordering]
level: sme
status: draft
description: "Implement and choose lock-free queues: SPSC ring buffers with acquire/release indices, cache-line padding, MPMC options like the Disruptor, and when a mutex queue is fine."
sources: ["https://rigtorp.se/ringbuffer/", "https://lmax-exchange.github.io/disruptor/disruptor.html", "https://www.1024cores.net/", "https://en.cppreference.com/w/cpp/atomic/memory_order"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lock-free queues and SPSC ring buffers

## SPSC ring buffer (single producer, single consumer)
The simplest and fastest lock-free queue: a fixed array, a write index owned by the producer, a read
index owned by the consumer.
```cpp
template<class T, size_t N>            // N power of two
class Spsc {
  std::array<T, N> buf;
  alignas(64) std::atomic<size_t> head{0};   // written by consumer
  alignas(64) std::atomic<size_t> tail{0};   // written by producer
  alignas(64) size_t cachedHead = 0;         // producer's cached copy of head
  alignas(64) size_t cachedTail = 0;         // consumer's cached copy of tail
public:
  bool push(const T& v) {
    size_t t = tail.load(std::memory_order_relaxed);
    if (t - cachedHead == N) { cachedHead = head.load(std::memory_order_acquire); if (t - cachedHead == N) return false; }
    buf[t & (N - 1)] = v;
    tail.store(t + 1, std::memory_order_release);   // publish the element
    return true;
  }
  bool pop(T& out) {
    size_t h = head.load(std::memory_order_relaxed);
    if (h == cachedTail) { cachedTail = tail.load(std::memory_order_acquire); if (h == cachedTail) return false; }
    out = buf[h & (N - 1)];
    head.store(h + 1, std::memory_order_release);   // free the slot
    return true;
  }
};
```
Key points: release on publish, acquire on observe; indices on separate cache lines (false sharing
otherwise halves throughput); cached opposite index cuts cross-core traffic (Rigtorp); free-running
indices with power-of-two masking avoid the full/empty ambiguity.

## MPMC and MPSC
Much harder (ABA, memory reclamation, contention). Use proven implementations:
- C++: `boost::lockfree::spsc_queue`/`queue`, `moodycamel::ConcurrentQueue`, `folly::MPMCQueue`, Vyukov's
  bounded MPMC queue (per-slot sequence numbers).
- Java: LMAX **Disruptor** (pre-allocated ring, sequence barriers, wait strategies), JCTools
  (`SpscArrayQueue`, `MpscArrayQueue`) used by Netty; `ConcurrentLinkedQueue` (Michael-Scott).
- Rust: `crossbeam::queue::ArrayQueue`, `rtrb` (SPSC), `crossbeam-channel`.
- Go: channels (mutex-based but well optimised) are usually enough.

## When lock-free pays off
Low-latency pipelines (audio, trading, telemetry ingest), threads that must never block (real-time
audio callbacks, signal handlers). Otherwise a mutex + condition variable queue is simpler and,
under moderate contention, competitive.

## Waiting strategy
Lock-free push/pop don't block; consumers must spin, yield, or park when empty. Busy-spinning burns a
core (Disruptor `BusySpinWaitStrategy`); blocking strategies add latency. Choose per latency budget.

## Testing
Run under ThreadSanitizer, stress tests on weakly ordered hardware (ARM), and model checkers (loom,
CDSChecker, Relacy) for custom code.
