---
id: computing-software.software-engineering.debugging.reading-stack-traces
name: reading-stack-traces
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, stack-traces, exceptions, error-messages, caused-by, async-stack-traces]
level: intro
status: docs-checked
description: "Read stack traces and error messages in Java, Python, JS and .NET: find the first frame in your code, follow Caused-by chains, handle async frames."
sources: ["https://docs.python.org/3/library/traceback.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Throwable.html#printStackTrace()", "https://v8.dev/docs/stack-trace-api", "https://learn.microsoft.com/en-us/dotnet/api/system.exception.stacktrace"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading stack traces and error messages

## Read the message first, fully
Java's `printStackTrace` output starts with the throwable's `toString()` (type and message), followed by the
frames recorded when the exception was created. Copy the type and message exactly before searching.

## Direction by language
| Language | Order | Your starting point |
|---|---|---|
| Python | printed under the header `Traceback (most recent call last):`, so the raise point is last | read from the bottom up |
| Java | message line first, then frames (the Javadoc example lists the throwing frame first) | read from the top down |

Find the **first frame in your code** (skip framework and library frames); that is usually where to look,
though the bug may be in what you passed to the library.

## Chained exceptions
- Java: `Caused by:` sections follow the main trace, one per cause; the Javadoc example shows `... n more`
  lines abbreviating frames. An exception can also carry suppressed exceptions, a separate relationship from its cause.
- Python: an unhandled exception prints chained exceptions (`__cause__` or `__context__`), for example
  "During handling of the above exception, another exception occurred:". `traceback.print_exception`
  prints the chain by default (`chain=True`).
- Preserve the original cause when rethrowing in your language's own way (chain/cause argument) so these
  sections still appear.

## Hard cases
- **Async JS**: V8's `--async-stack-traces` flag (on by default since V8 v7.3) adds async frames (await
  locations) to an Error's `stack`, shown as `at async foo (...)`.
- **Truncated JS stacks**: `Error.stackTraceLimit` controls how many frames V8 captures; it only has an effect
  when your code runs in V8.
- **.NET**: `Exception.StackTrace` is a string of the frames on the call stack at the time of the throw.
- Check the deployed build matches the source you are reading before trusting line numbers.

## Checked
2026-11-09. Confirmed against the Python traceback module docs, the Java 21 `Throwable.printStackTrace`
Javadoc, the V8 stack trace API page and the `Exception.StackTrace` reference. Removed as not stated in the
pages: the Go panic row, the .NET `InnerException` text and `throw;` versus `throw ex;` advice, Java 14 helpful
NPE messages, JVM `-XX:-OmitStackTraceInFastThrow`, source-map and debug-symbol tooling, the claim that
the last `Caused by` is always the root, the meaning of `... n more`, and the .NET/asyncio async remarks.
Method: documentation only; no commands were run.
