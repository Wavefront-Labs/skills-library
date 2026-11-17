---
id: computing-software.software-engineering.java.thread-interruption-and-cancellation
name: thread-interruption-and-cancellation
category: computing-software
field: software-engineering
product: java
tags: [java, thread-interruption, interruptedexception, cancellation, future-cancel, shutdownnow, java-concurrency]
level: advanced
status: docs-checked
description: "Handle Java interruption correctly: what InterruptedException means, restoring the flag, cancellable loops, Future.cancel and shutdownNow, and non-interruptible blocking I/O."
sources: ["https://jcip.net/", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Thread.html#interrupt()", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ExecutorService.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread interruption and cancellation

**Goal:** tasks that stop promptly when cancelled, and code that never swallows the
cancellation signal.

## The model (JCIP ch7)
Interruption is a cooperative request: `t.interrupt()` sets a flag; blocking methods
(`sleep`, `wait`, `join`, `BlockingQueue.take`, `Future.get`, `lockInterruptibly`) throw
`InterruptedException` and **clear** the flag. Nothing forces a thread to stop.

## Never swallow it
```java
try {
    queue.take();
} catch (InterruptedException e) {
    // WRONG: empty catch or log-and-continue - the cancel request is lost
}
```
Either propagate (`throws InterruptedException`), or restore the flag and exit:
```java
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();     // let callers / the executor see it
    return;                                 // or throw a domain exception
}
```
Wrapping into an unchecked exception is fine **if** you restore the flag first.

## Cancellable loops
```java
public void run() {
    while (!Thread.currentThread().isInterrupted()) {
        doChunk();                           // keep chunks short
    }
    cleanup();
}
```
`Thread.interrupted()` (static) reads **and clears** the flag; `isInterrupted()` only reads.

## Cancelling via executors
```java
Future<?> f = pool.submit(task);
f.cancel(true);              // true = interrupt the running thread
pool.shutdown();             // stop accepting, finish queued
if (!pool.awaitTermination(30, SECONDS)) {
    List<Runnable> never = pool.shutdownNow();   // interrupt all, return queued tasks
}
```
`CompletableFuture.cancel(true)` does **not** interrupt the thread running it; the computation
continues. Use `Future` from an executor, structured concurrency, or check a cancel flag.

## Non-interruptible blocking
Blocking calls that do not respond to interruption need another cancellation path, such as closing the resource from another thread or setting a timeout.


## Verify
- [ ] grep for `catch (InterruptedException` - every block restores the flag or rethrows.
- [ ] Shutdown tests confirm tasks exit within the termination timeout.

## Checked

- Date: 2026-10-28
- Confirmed in the Java SE 21 Thread and ExecutorService Javadoc and CompletableFuture Javadoc: interrupt/interrupted/isInterrupted, interrupted status cleared when InterruptedException is thrown, shutdown/shutdownNow/awaitTermination, CompletableFuture.cancel(true) has no interrupt effect.
- Removed: SocketException/NIO channel claims, StructuredTaskScope preview section.
Method: documentation only; no commands were run.
