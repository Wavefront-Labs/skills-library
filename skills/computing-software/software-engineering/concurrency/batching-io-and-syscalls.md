---
id: computing-software.software-engineering.concurrency.batching-io-and-syscalls
name: batching-io-and-syscalls
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, optimisation, io-batching, syscalls, buffered-io, write-coalescing, nagle]
level: practitioner
status: draft
description: "Improve throughput by batching I/O: buffered readers/writers, vectored and batched syscalls, DB batch inserts and pipelining, message batching, and latency trade-offs."
sources:
  - https://man7.org/linux/man-pages/man2/writev.2.html
  - https://redis.io/docs/latest/develop/use/pipelining/
  - https://jdbc.postgresql.org/documentation/use/
  - https://kafka.apache.org/documentation/#producerconfigs_linger.ms
  - https://www.brendangregg.com/blog/2014-05-11/strace-wow-much-syscall.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Batching I/O and syscalls

Each syscall, network round trip, or DB statement has a fixed cost (microseconds for a syscall, a full RTT for a network call). Doing many small operations multiplies that overhead; batching amortises it.

## Find the problem
- `strace -c -f -p <pid>` summarises syscall counts; thousands of tiny `write`/`read` calls per second is the signature. `perf trace -s` is lower overhead.
- APM/DB logs: one INSERT per row, one Redis call per key, high request rate with small payloads.

## Techniques
**Buffered I/O**
- Wrap streams: Java `BufferedOutputStream`/`BufferedWriter`, Go `bufio.NewWriterSize(w, 64<<10)` (remember `Flush()`), Python files are buffered by default (avoid `buffering=0`/flush per line), C `setvbuf`. Logging frameworks: async appenders with batching.
- Read in large chunks (64 KB-1 MB) instead of byte-by-byte.

**Vectored and batched syscalls**
- `writev`/`readv` write several buffers in one call (Go `net.Buffers`, Java NIO gathering writes).
- `sendmmsg`/`recvmmsg` for UDP batches; `io_uring` submits many operations per syscall; `sendfile`/`splice` for zero-copy file-to-socket.

**Database**
- Multi-row inserts or batch APIs: JDBC `addBatch()`/`executeBatch()` with PostgreSQL `reWriteBatchedInserts=true`; `COPY` for bulk loads (fastest in Postgres); Python `executemany` / `psycopg` `copy`; EF Core batches SaveChanges.
- Fetch by sets (`WHERE id = ANY($1)`) instead of loops; tune fetch size for large result sets.
- Wrap batches in one transaction (one fsync at commit instead of per row).

**Network protocols**
- Redis pipelining (send many commands without waiting for each reply) or `MGET/MSET`; HTTP/2 multiplexing and keep-alive connection reuse.
- Message producers: Kafka `linger.ms` (5-20 ms) + `batch.size` + compression; SQS `SendMessageBatch` (up to 10); consumers process in batches and commit offsets per batch.

**Application-level coalescing**
- Micro-batching: collect requests for up to N items or T ms, then issue one call (DataLoader in GraphQL, write-behind buffers). Keep T small and bounded.

## Trade-offs
- Latency vs throughput: waiting to fill a batch adds latency; cap by both size and time.
- Bigger failure blast radius: one bad row can fail a whole batch - decide on per-item error reporting or splitting and retrying.
- Memory: unbounded buffers under load; bound them and apply backpressure.
- Durability: buffered data is lost on crash until flushed; flush on shutdown and at transaction boundaries.
- Nagle's algorithm + delayed ACK can add ~40 ms to small request/response writes; set `TCP_NODELAY` for latency-sensitive protocols and do your own write coalescing.

## Verify
- [ ] `strace -c` / DB statement counts drop by the expected factor.
- [ ] Throughput improves at target load and p99 latency stays within budget (batch time cap honoured).
