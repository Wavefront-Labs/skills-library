---
id: computing-software.software-engineering.concurrency.reducing-allocations-pooling-and-arenas
name: reducing-allocations-pooling-and-arenas
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, optimisation, object-pooling, arena-allocation, allocation-reduction, gc-pressure, buffer-reuse]
level: practitioner
status: draft
description: "Cut allocation cost and GC pressure in hot paths: measure allocation rate, reuse buffers, object pools (sync.Pool, ArrayPool), arenas, stack allocation, and when pooling backfires."
sources:
  - https://pkg.go.dev/sync#Pool
  - https://learn.microsoft.com/en-us/dotnet/api/system.buffers.arraypool-1
  - https://docs.rs/bumpalo/latest/bumpalo/
  - https://go.dev/doc/gc-guide
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reducing allocations: pooling, arenas and reuse

Allocations cost CPU (allocation itself, zeroing, GC tracing and pauses, cache misses on fresh memory). In hot paths, fewer allocations often beats any algorithmic tweak - but only after a profile shows allocation is the problem.

## Measure first
- Go: `go test -bench . -benchmem` (allocs/op, B/op), `go tool pprof -sample_index=alloc_space`, `GODEBUG=gctrace=1`.
- Java: JFR allocation events, async-profiler `-e alloc`, GC logs (`-Xlog:gc*`).
- .NET: BenchmarkDotNet `[MemoryDiagnoser]`, `dotnet-counters` (allocation rate, GC count), dotnet-trace.
- Python: `tracemalloc`; Rust/C++: heaptrack, `dhat`.

## Techniques, cheapest first
1. **Avoid the allocation:** preallocate capacity (`make([]T, 0, n)`, `new ArrayList<>(n)`, `Vec::with_capacity`, `List<T>(n)`); avoid boxing; avoid intermediate collections (stream/iterator fusion, `Span<T>` slicing, `strings.Builder`); reuse a buffer across loop iterations by resetting its length (`buf = buf[:0]`, `sb.setLength(0)`).
2. **Stack allocation / escape analysis:** keep values from escaping to the heap (Go `go build -gcflags=-m` shows escapes; C# `stackalloc` + `Span<T>`, `ref struct`; JVM scalar replacement for non-escaping objects).
3. **Pools for expensive or large objects:**
```go
var bufPool = sync.Pool{New: func() any { return new(bytes.Buffer) }}
func render(w io.Writer, v any) error {
    b := bufPool.Get().(*bytes.Buffer)
    b.Reset()                      // always reset before use
    defer bufPool.Put(b)
    if err := json.NewEncoder(b).Encode(v); err != nil { return err }
    _, err := w.Write(b.Bytes())
    return err
}
```
```csharp
byte[] buf = ArrayPool<byte>.Shared.Rent(minLength);   // may be larger than requested
try { int n = stream.Read(buf, 0, minLength); Process(buf.AsSpan(0, n)); }
finally { ArrayPool<byte>.Shared.Return(buf); }
```
Also: `Microsoft.Extensions.ObjectPool`, Netty `PooledByteBufAllocator`, Apache Commons Pool for heavy objects; connection pools are the classic case.
4. **Arenas / region allocation:** allocate many objects with the same lifetime from one block and free them all at once (per request, per frame, per compiler pass). Rust `bumpalo`, C++ `std::pmr::monotonic_buffer_resource`, Protobuf C++ arenas, Zig allocators. Go's experimental `arena` package is on hold - do not rely on it.

## When pooling backfires
- Pooled objects not reset leak data between requests (security bug: one user's buffer contents in another's response).
- Returning an object while still in use (use-after-return) corrupts data - harder to debug than a GC pause.
- Pools of small, cheap objects in generational-GC runtimes can be slower: young-gen allocation is very cheap and pooled objects get promoted to old gen, making GC more expensive.
- Unbounded pools retain memory after spikes; cap sizes or use pools that drop on GC (`sync.Pool` clears across GCs).
- Huge pooled buffers returned after one large request keep memory high; do not return oversize buffers.

## Verify
- [ ] Benchmark shows lower allocs/op and better throughput or tail latency, not just fewer allocations.
- [ ] Tests (or race detector/sanitisers) confirm pooled objects are reset and not used after return.
