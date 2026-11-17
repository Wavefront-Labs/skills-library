---
id: computing-software.software-engineering.java.exceptions-and-try-with-resources
name: exceptions-and-try-with-resources
category: computing-software
field: software-engineering
product: java
tags: [java, java-exceptions, try-with-resources, autocloseable, checked-exceptions, suppressed-exceptions, exception-chaining, error-handling]
level: practitioner
status: docs-checked
description: "Handle Java exceptions well: checked vs unchecked design, chaining causes, try-with-resources and suppressed exceptions, and the swallow/log-and-rethrow anti-patterns."
sources: ["https://dev.java/learn/exceptions/", "https://docs.oracle.com/javase/tutorial/essential/exceptions/tryResourceClose.html", "https://docs.oracle.com/javase/specs/jls/se21/html/jls-14.html#jls-14.20.3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exceptions and try-with-resources

**Goal:** resources always closed, failures carry their root cause, and each exception
is handled exactly once at a level that can do something about it.

## try-with-resources
```java
try (var in = Files.newInputStream(src);
     var out = Files.newOutputStream(dst)) {
    in.transferTo(out);
}   // closed in reverse order, even on exception
```
- Works with any `AutoCloseable`. Effectively final variables can also be used:
  `try (conn) { ... }`.
- If the body throws AND `close()` throws, the close exception is attached as
  SUPPRESSED (`e.getSuppressed()`), not lost. A manual `finally { close(); }` instead
  masks the original exception with the close one.
- JDBC: Connection, PreparedStatement and ResultSet each in the header.

## Chaining
```java
catch (SQLException e) {
    throw new RepositoryException("loading order " + id, e);   // keep cause!
}
```
Losing the cause (`new X(e.getMessage())`) deletes the stack trace you need.

## Checked vs unchecked
- Checked: caller can reasonably recover (file missing, remote temporarily unavailable)
  and it is part of the contract.
- Unchecked (`RuntimeException`): programming errors (`IllegalArgumentException`,
  `IllegalStateException`) and failures nobody in the call chain can fix.
- Modern practice (Spring, most libraries) leans unchecked plus translation at layer
  boundaries; lambdas and streams cannot propagate checked exceptions anyway.

## Anti-patterns
- `catch (Exception e) {}` - swallowing. At minimum log with the exception object.
- Log AND rethrow at every layer: same stack trace 5 times in logs. Log once at the
  boundary (request handler, job runner).
- `catch (Throwable)` - catches `OutOfMemoryError`/`StackOverflowError`; let Errors propagate.
- Catching `InterruptedException` and continuing: restore the flag with
  `Thread.currentThread().interrupt()` or rethrow.
- Exceptions for control flow in hot paths: stack capture is costly.
- `log.error("failed: " + e)` loses the stack; use `log.error("failed", e)`.

## Verify
- [ ] Static analysis (SpotBugs, Error Prone, Sonar) has no "resource leak" or "swallowed exception" findings.
- [ ] A forced failure in tests shows the full cause chain in the log once.

## Checked

- Date: 2026-10-28
- Confirmed in the Java tutorial (try-with-resources) and Throwable Javadoc: suppressed exceptions and getSuppressed, finally-block exception suppressing the try-block exception, JLS 14.20.3 effectively final resource variables.
- Removed: Java 9 version tag.
Method: documentation only; no commands were run.
