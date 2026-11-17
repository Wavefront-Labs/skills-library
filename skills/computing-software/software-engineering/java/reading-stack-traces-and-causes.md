---
id: computing-software.software-engineering.java.reading-stack-traces-and-causes
name: reading-stack-traces-and-causes
category: computing-software
field: software-engineering
product: java
tags: [java, java-exceptions, stack-trace-reading, caused-by, suppressed, helpful-nullpointerexceptions]
level: practitioner
status: docs-checked
description: "Read a Java stack trace correctly: find the root Caused by, interpret '... N more', Suppressed entries and helpful NullPointerException messages."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Throwable.html", "https://openjdk.org/jeps/358"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading stack traces and cause chains

## Anatomy
```
Exception in thread "main" com.acme.ServiceException: load failed
    at com.acme.Service.load(Service.java:42)
    at com.acme.Main.main(Main.java:10)
Caused by: java.io.UncheckedIOException: read error
    at com.acme.Repo.read(Repo.java:77)
    ... 1 more
Caused by: java.nio.file.NoSuchFileException: data.json
    at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
    ...
```
1. The top is the outermost (wrapping) exception; each `Caused by:` is the cause of the one above, so the last one is the root cause. Read from the bottom up for the cause, from the top for the call site.
2. `... N more` means the remainder of that exception's stack trace matches N frames from the bottom of the enclosing exception's trace; they are omitted, not lost.
3. `Suppressed:` lists exceptions suppressed (for example while closing resources in try-with-resources) and attached to the primary exception.
4. The first frame in your own package under the cause is where to look.

## Helpful NullPointerException messages (JEP 358, JDK 14)
The JVM computes a null-detail message such as `Cannot invoke "String.length()" because "user.name" is null`, naming the action that failed and the expression that was null. Local variable names appear only if the class files carry debug information (`javac -g`); otherwise placeholders are shown. JEP 358 introduced `-XX:+ShowCodeDetailsInExceptionMessages` (off by default in JDK 14); check the option's default for your JDK. The message is computed on demand, so it is lost when the exception is serialized (for example over RMI). Long access paths can be cut with "..." placeholders.

## Programmatic access
Loop on `Throwable.getCause()` to reach the root; `Throwable.getSuppressed()` returns the suppressed exceptions.

## Verify
Throw a nested exception in a test, print it, and identify root cause and line; ensure the logging config emits `Caused by:` chains.

## Checked

Method: docs-checked 2026-11-09 against the Throwable class page (printStackTrace format, "... n more" explanation, Caused by example) in JDK 21 and JEP 358 (null-detail message, -g, option default, on-demand computation). Dropped unconfirmed claims (OmitStackTraceInFastThrow, StackWalker, logging truncation patterns) and the StackWalker source, which was not read.
