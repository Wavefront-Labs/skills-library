---
id: computing-software.software-engineering.concurrency.double-checked-locking
name: double-checked-locking
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, double-checked-locking, lazy-initialization, memory-model, volatile, safe-publication]
level: advanced
status: docs-checked
description: "Get lazy initialisation right: why naive double-checked locking is broken, the volatile fix, and simpler idioms (static holder class, Lazy<T>, sync.Once, OnceLock)."
sources: ["https://www.cs.umd.edu/~pugh/java/memoryModel/DoubleCheckedLocking.html", "https://pkg.go.dev/sync#Once", "https://learn.microsoft.com/en-us/dotnet/api/system.lazy-1", "https://doc.rust-lang.org/std/sync/struct.OnceLock.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Double-checked locking and lazy initialisation races

## The broken version
```java
class Foo {
  private Helper helper = null;
  public Helper getHelper() {
    if (helper == null) {                  // 1st check, no lock
      synchronized (this) {
        if (helper == null) helper = new Helper();   // 2nd check
      }
    }
    return helper;
  }
}
```
Per "The Double-Checked Locking is Broken" declaration, this does not work reliably in a platform-independent way in Java without additional synchronization: the assignment of the reference can happen before the constructor has run, which the old Java memory model allows (and C and C++, which had no memory model, also allow). In C++ it depends on the processor's memory model, compiler reordering and the synchronisation library; explicit memory barriers can make it work in C++ but are not available in Java.
- Putting construction in an inner synchronized block does not help: a monitor exit only requires earlier actions to finish before the release; later actions can be moved inside the block.
- Forcing a full barrier in the writer is still not enough on some systems, because the reading thread also needs barriers (stale locally cached copies).

## Correct options
- JDK 5 and later: declare the field `volatile`; the volatile semantics were extended so a volatile write cannot be reordered with earlier reads or writes and a volatile read cannot be reordered with later ones. This does not work under JDK 4 and earlier.
- If `Helper` is immutable (all fields final), double-checked locking works without `volatile`.
- It also works for 32-bit primitives (not `long` or `double`, whose unsynchronised reads and writes are not guaranteed atomic).
- For a static singleton, define it as a static field in a separate class: Java guarantees the field is not initialised until referenced and that every thread sees all writes from initialisation.
- Is it worth it? For most applications a synchronized `getHelper()` is not costly; optimise only if it is a measured overhead.

## Prefer the library idioms
| Language | Idiom (from the docs) |
|---|---|
| Go | `sync.Once`: `Do(f)` calls `f` only on the first call for that instance; use a function literal to capture arguments. Go 1.21 added `OnceFunc`, `OnceValue`, `OnceValues`; the returned function may be called concurrently, and if `f` panics it panics with the same value on every call. |
| .NET | `Lazy<T>`: the simple constructors are fully thread safe; `LazyThreadSafetyMode.ExecutionAndPublication` locks so one thread initialises, `PublicationOnly` lets threads race and discards extra copies, `None` is not thread safe. With a factory method exceptions are cached and rethrown on every access (not with `PublicationOnly`); build retry logic into the factory if failure is recoverable. |
| Rust | `OnceLock<T>`: a thread-safe once-cell usable in statics, written at most once; `LazyLock` is the simpler choice when initialisation needs no extra inputs. |

## Checked
2026-11-08. Confirmed against the Pugh et al. Double-Checked Locking declaration, the Go sync package page (Once, OnceFunc, OnceValue), the .NET Lazy<T> page and the Rust OnceLock page. Removed (not on those pages): the local-variable `volatile` variant, the C++, C#, Python and Kotlin rows, the language-version claims for `LazyLock`, the lazy-map race advice, and the detection tools list (ThreadSanitizer, jcstress, SpotBugs).
Method: documentation only; no commands were run.
