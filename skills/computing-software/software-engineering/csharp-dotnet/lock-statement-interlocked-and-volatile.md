---
id: computing-software.software-engineering.csharp-dotnet.lock-statement-interlocked-and-volatile
name: lock-statement-interlocked-and-volatile
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-concurrency, lock, interlocked, volatile, monitor, thread-safety]
level: practitioner
status: docs-checked
description: "Use the C# lock statement with a dedicated System.Threading.Lock or object, what not to lock on, no await in lock, and why Microsoft prefers Interlocked and lock over volatile."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/lock", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/volatile"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lock, Interlocked and volatile

## lock
```csharp
private readonly Lock _gate = new();       // System.Threading.Lock, .NET 9 / C# 13
private int _balance;

public void Deposit(int x) { lock (_gate) { _balance += x; } }
```
- `lock (x)` acquires a mutual-exclusion lock, runs the block and releases it; the holding thread can acquire it multiple times (re-entrant); other threads block. At most one thread executes the body at a time.
- With a `System.Threading.Lock` the compiler treats `lock (x)` as `using (x.EnterScope())`; otherwise it is `Monitor.Enter`/`Monitor.Exit` in a `try`/`finally`. Either way the lock is released if an exception is thrown in the body (the data it protects may be half-updated).
- Starting with .NET 9 and C# 13, lock a dedicated `Lock` instance for best performance. On older versions lock a dedicated `object` instance used for nothing else. The compiler warns if you cast a known `Lock` to another type and lock it.
- Do not lock on `this` (callers may lock it too), on `Type` instances (obtainable via `typeof` or reflection) or on strings (literals may be interned). Do not share one lock object between different shared resources: it risks deadlock or contention.
- Hold the lock for as short a time as possible.
- You cannot use `await` in the body of a `lock` statement.

## Interlocked and volatile
Microsoft's `volatile` documentation carries a caution: the keyword is often misunderstood and misused, and for most scenarios you should use `Interlocked`, the `lock` statement or higher-level synchronization primitives instead.
- `volatile` excludes a field from certain compiler/runtime/hardware reordering optimisations, but there is no guarantee of a single total ordering of volatile writes as seen by all threads, and a volatile read is not guaranteed to see the latest value written by any processor.
- It applies only to fields of a class or struct (not locals), of reference types, simple types such as `int`, `bool` and `char`, certain enums, pointers and `IntPtr`/`UIntPtr`. It cannot be applied to `double` or `long`, because their reads and writes cannot be guaranteed atomic; protect those with `Interlocked` members or `lock`.
- See `System.Threading.Volatile` for explicit volatile reads and writes.

## Verify
A test with many threads each incrementing a shared counter many times, asserting the exact total, for both a locked version and an `Interlocked` version.

## Checked
2026-11-03. Confirmed against dotnet/docs: "The lock statement" and "volatile keyword" pages. Removed because not found there: the claim that `volatile` gives acquire/release semantics and that a stop flag is a typical valid use (the page cautions against it), `volatile int n; n++` remarks, specific `Interlocked` method examples, the compiler error number for `await` in `lock`, `Monitor.TryEnter` ordering advice, double-checked locking and `Lazy<T>` mode advice, `ReaderWriterLockSlim` performance, 32-bit tearing, diagnostic tools.
Method: documentation only; no commands were run.
