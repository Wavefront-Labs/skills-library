---
id: computing-software.software-engineering.debugging.stack-overflows-and-deep-recursion
name: stack-overflows-and-deep-recursion
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, stack-overflow, recursion, stack-size, tail-calls, ulimit]
level: practitioner
status: gated
description: "Diagnose and fix stack overflows: recognise them per runtime, find the recursive cycle, raise stack limits safely, and convert deep recursion to iteration."
sources: ["https://docs.python.org/3/library/sys.html#sys.setrecursionlimit", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html", "https://man7.org/linux/man-pages/man2/getrlimit.2.html", "https://learn.microsoft.com/en-us/dotnet/api/system.stackoverflowexception"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stack overflows and deep recursion

## Recognise it
| Runtime | Symptom |
|---|---|
| Java | `java.lang.StackOverflowError`, trace with repeating frames (truncated to 1024 by default (gated: unconfirmed, source is paywalled or blocked)) |
| Python | `RecursionError: maximum recursion depth exceeded` (default limit 1000, run on 3.14.0 with `sys.getrecursionlimit()`) |
| Node/JS | `RangeError: Maximum call stack size exceeded` (run on Node 20) |
| .NET | process terminates ("Stack overflow." on stderr); can't be caught (gated: unconfirmed, source is paywalled or blocked) |
| C/C++/Rust/Go native threads | SIGSEGV near stack guard page; Rust prints "thread 'main' has overflowed its stack" (run on rustc 1.99.1); Go prints "runtime: goroutine stack exceeds 1000000000-byte limit" (64-bit; the runtime source uses 250000000 on 32-bit) |

## Find the cycle
- Look for the repeating frame pattern in the trace; the cycle may span several functions
  (A -> B -> C -> A), e.g. `toString()`/`equals()`/`hashCode()` on bidirectional relations, JSON
  serializers walking parent<->child references, property getters calling themselves, event handlers
  that trigger themselves, mutual recursion in visitors.
- Java: `-XX:MaxJavaStackTraceDepth=` to see more frames (gated: unconfirmed, source is paywalled or blocked). Native: gdb `bt -20` on the core.
- Unbounded recursion = missing/incorrect base case; deep but finite = input bigger than expected
  (deeply nested JSON/XML, long linked lists, degenerate trees).

## Fixes
1. Fix the cycle (exclude back-references from `toString`/serialization: `@JsonManagedReference`/
   `@JsonBackReference`, `@ToString.Exclude`, `__repr__` that prints ids).
2. **Convert recursion to iteration** with an explicit stack/queue for deep traversals:
   ```python
   def walk(root):
       stack = [root]
       while stack:
           n = stack.pop(); visit(n); stack.extend(reversed(n.children))
   ```
3. Bound input depth at trust boundaries (parsers: max nesting depth) to avoid DoS.
4. Raising limits is a last resort: Java `-Xss4m` (or `new Thread(group, r, name, stackSize)`),
   Python `sys.setrecursionlimit(10000)` plus `threading.stack_size()` for a worker thread (the docs warn a too-high limit can crash the interpreter; on 3.14.0 a limit of 200000 ran pure-Python recursion to depth 150000, while C-level recursion such as `repr` of a 300000-deep nested list raised `RecursionError: Stack overflow (used 2912 kB)` instead of crashing), `ulimit -s` for the main thread on Linux, linker
   `/STACK` on Windows, `RUST_MIN_STACK` for spawned threads (run: a 20000-deep recursion overflowed a default spawned thread and passed with `RUST_MIN_STACK=67108864`).
5. Tail-call elimination isn't guaranteed in Java, Python, JS (except Safari), C# or Go; don't rely
   on it. Scala `@tailrec`, Kotlin `tailrec` and most functional languages do it.

## Also check
Large stack-allocated arrays/structs in C/C++/Rust (`char buf[1<<20]` in a function) overflow small
thread stacks (musl defaults to 128 KB); allocate on the heap.
