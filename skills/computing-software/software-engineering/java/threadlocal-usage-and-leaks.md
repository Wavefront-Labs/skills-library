---
id: computing-software.software-engineering.java.threadlocal-usage-and-leaks
name: threadlocal-usage-and-leaks
category: computing-software
field: software-engineering
product: java
tags: [java, threadlocal, thread-pools, memory-leak, scoped-values, concurrency]
level: practitioner
status: gated
description: "Use Java ThreadLocal safely: always remove in thread pools, avoid classloader leaks, understand InheritableThreadLocal and alternatives such as ScopedValue."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ThreadLocal.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ThreadLocal usage and leaks

## Use
```java
private static final ThreadLocal<SimpleDateFormat> FMT =
    ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));
```
Typical legitimate uses: non-thread-safe helper objects (prefer thread-safe `DateTimeFormatter`), request context (user id, trace id) carried through a call chain.

## The leak
Each thread holds a reference to its copy as long as the thread is alive and the `ThreadLocal` instance is accessible, so pool threads that live as long as the application keep a value you never removed. If the value (or its class) references your webapp classloader, undeploy/redeploy can leak the whole classloader (a general JVM behaviour, not stated on the API page) (gated: unconfirmed, source is paywalled or blocked). `remove()` drops the current thread's value; a later `get()` re-runs `initialValue()`. Always:
```java
try { CTX.set(ctx); work(); } finally { CTX.remove(); }
```
Make the ThreadLocal `static final` (the API docs say instances are typically private static fields) and wrap in a servlet filter / executor decorator that clears it.

## Pitfalls
- Reused pool threads leak data between requests when not cleared: a security issue (wrong user).
- `InheritableThreadLocal` gives a child thread initial values when the child is created (customisable via `childValue`), so values do not follow tasks into already-created pooled threads; use executor decorators to propagate context (or libraries such as the context-propagation support in your framework).
- Virtual threads support ThreadLocal but millions of threads mean millions of copies; prefer `ScopedValue` for immutable per-call context (finalized in JDK 25 by JEP 506; preview in earlier releases, so check your version). The per-thread copy cost for virtual threads is general reasoning, not stated on the ThreadLocal API page (gated: unconfirmed, source is paywalled or blocked).
- Values hold heap: large buffers per thread multiply by pool size.

## Diagnose
Heap dump: dominator tree on `Thread` objects and their thread-local maps; look for entries retaining app classes (internal class names: gated: unconfirmed, source is paywalled or blocked).

## Verify
After a request completes, `get()` on the pool thread returns the initial value/null; heap stays flat across redeploys.

## Checked

2026-11-02. Checked against the Java SE 21 ThreadLocal and InheritableThreadLocal API pages and JEP 506. Confirmed: `withInitial`, `remove()` semantics, copies live as long as the thread is alive and the ThreadLocal accessible, typical private static field, InheritableThreadLocal child initial values and `childValue`, ScopedValue final in JDK 25. Gated: classloader-leak mechanics, virtual-thread cost and heap-dump internal class names, none of which the API pages state.

Method: documentation only; no commands were run.
