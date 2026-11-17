---
id: computing-software.software-engineering.debugging.diagnostic-logging-and-assertions
name: diagnostic-logging-and-assertions
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, observing-execution, diagnostic-logging, assertions, log-levels, printf-debugging, structured-logging, dynamic-log-levels]
level: practitioner
status: verified
description: "Use logging and assertions as debugging instruments: what to log at which level, temporary vs permanent diagnostics, dynamic log levels and assertions that localise faults."
sources: ["Why Programs Fail, 2nd ed. (Zeller), chapters on observing facts and asserting expectations (confirm chapter numbers in your edition)", "https://www.debuggingbook.org/html/Assertions.html", "https://docs.spring.io/spring-boot/api/rest/actuator/loggers.html", "https://docs.python.org/3/howto/logging.html", "https://opentelemetry.io/docs/concepts/signals/logs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnostic logging and assertions

**Goal:** observe what the program actually did, and make it stop at the first point
where state goes wrong instead of far downstream.

## Printf debugging, done well
Quick prints are legitimate (Zeller: "observing facts"), but:
- Print the evidence for a specific hypothesis, not everything.
- Include identity and values: `print(f"[DBG cart={cart.id}] total={total!r} items={len(items)}")`.
  `!r`/`%q`/`{:?}` reveal whitespace, None vs "None", types.
- Tag with a unique marker (`DBG`) so they are trivially found and removed before commit
  (or a pre-commit hook rejects them).
- Flush/stderr for crashing programs: buffered stdout is lost on a crash (run on Python 3.14: with stdout piped, `print("x")` then `os._exit(1)` printed nothing, while `print(..., flush=True)` and stderr output survived). `!r` is Python, `%q` is Go and `{:?}` is Rust (all three run: they separate `None` from the string `"None"` and show a trailing space inside quotes).

## Permanent diagnostic logging
| Level | Use |
|---|---|
| ERROR | operation failed, needs attention |
| WARN | unexpected but handled (retry, fallback) |
| INFO | business events at low volume (startup config, job started/finished) |
| DEBUG | decision points and inputs useful for diagnosing, off in prod by default |
| TRACE | per-iteration detail |
- Log decisions with their inputs: "using fallback pricing because region=null".
- Structured fields (`log.info("charge failed", order_id=..., code=...)`) make logs
  searchable; carry a request/trace id on every line.
- Never log secrets, tokens, full card numbers or personal data.
- Make levels changeable at runtime per logger (Spring Boot actuator `/loggers`, which reports `configuredLevel` and `effectiveLevel` per logger,
  log4j2 JMX, env var + SIGHUP reload) so you can turn on DEBUG for one module in
  production without redeploying.

## Assertions as fault localisers
An assertion turns a silent corruption into an immediate failure close to the cause:
```python
def apply_payment(account, amount):
    assert amount > 0, f"amount={amount}"
    before = account.balance
    account.balance -= amount
    assert account.balance == before - amount   # postcondition
```
- Assert invariants of data structures in a `check_rep()` / `invariant()` method and
  call it after each mutation while debugging (Zeller's representation invariants).
- Debug-only asserts can be expensive; always-on checks must be cheap.
- See computing-software.software-engineering.refactoring.introduce-assertion for
  language specifics (disabled in Python -O (run: `assert` skipped), Java without -ea, C NDEBUG).

## Verify
- [ ] No `DBG` prints left in committed code (pre-commit grep).
- [ ] Production can switch one logger to DEBUG at runtime and back.
