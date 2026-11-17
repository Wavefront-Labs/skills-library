---
id: computing-software.software-engineering.java.custom-exception-design
name: custom-exception-design
category: computing-software
field: software-engineering
product: java
tags: [java, java-exceptions, custom-exception-design, domain-exceptions, exception-hierarchy, checked-vs-unchecked, error-codes, fail-fast]
level: practitioner
status: docs-checked
description: "Design custom Java exceptions: one base per module, carry data not just a message, keep the cause, and avoid stack-trace cost for control flow."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Throwable.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Designing custom exceptions

## Shape
```java
public class OrderException extends RuntimeException {          // module base type
    private final String orderId;
    public OrderException(String orderId, String message, Throwable cause) {
        super(message + " [order=" + orderId + "]", cause);
        this.orderId = orderId;
    }
    public String orderId() { return orderId; }
}
public final class OrderNotFoundException extends OrderException { ... }
```
- By convention (Throwable API) subclasses likely to have a cause offer constructors taking a `Throwable` cause and a `String` message plus cause. Always allow passing a cause so root causes are not lost.
- Add typed fields (ids, error codes) so handlers branch on data, not on message strings.
- Keep fields immutable.

## Checked or unchecked? (design judgement, not from the docs)
Prefer unchecked (`RuntimeException`) for programming errors and failures a caller cannot sensibly recover from. Use checked only when the immediate caller can realistically recover and you want the compiler to force a decision.

## Translation at layer boundaries
Catch the low-level exception in the lowest layer and rethrow a domain exception **with the cause** so the persistence or transport type does not leak upward. Translate domain exceptions to a response in one place.

## Gotchas
- Do not use exceptions for ordinary control flow. If you must, the Throwable constructor `Throwable(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace)` can disable the writable stack trace (pass `false` for the last two), and `fillInStackTrace()` is the method that fills it in.
- Never catch `Exception`/`Throwable` just to log and rethrow; log once at the boundary.
- Do not put secrets or PII in messages; they end up in logs.
- Avoid generic custom exceptions (`MyException`); name by condition.

## Verify
For each custom exception a test asserts `getCause()` is preserved and the typed field is readable.

## Checked
2026-11-09. Confirmed against the Java 21 Throwable API page: the cause-taking constructor convention, the four-argument constructor with enableSuppression and writableStackTrace, fillInStackTrace.
Removed: the Spring ControllerAdvice/ProblemDetail, UncheckedIOException and SQLException specifics, the Serializable/serialVersionUID advice, and the dev.java source (returned no content). The checked-versus-unchecked guidance is labelled as judgement.
Method: documentation only; no commands were run.
