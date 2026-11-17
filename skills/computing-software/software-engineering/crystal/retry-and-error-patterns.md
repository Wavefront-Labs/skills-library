---
id: computing-software.software-engineering.crystal.retry-and-error-patterns
name: retry-and-error-patterns
category: computing-software
field: software-engineering
product: crystal
tags: [retry-and-error-patterns, exceptions, retry, backoff, resilience, error-patterns, timeout-error, cleanup, crystal]
level: practitioner
status: draft
description: "Implement retry loops with backoff using begin/rescue and loops, handle ensure cleanup and avoid swallowing errors."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# retry, timeouts and error handling patterns

Goal: bounded retries.

There is no `retry` keyword in Crystal (unlike Ruby); loop instead:
```crystal
attempts = 0
loop do
  attempts += 1
  begin
    call_api
    break
  rescue ex : IO::Error
    raise ex if attempts >= 3
    sleep (0.2 * 2 ** attempts).seconds
  end
end
```
Cleaner: wrap this in a helper `def with_retries(n, &)` that yields and re-raises on the last attempt.
- Use `IO::TimeoutError` / `read_timeout` on sockets; log failures with `Log`.
- Use `ensure` or block-form `File.open(...) { }` to release resources.

Gotchas:
- Retry only idempotent operations.
- Add jitter to avoid thundering herds.
- Don't rescue `Exception` blindly; it hides bugs like NilAssertionError.

Verify: spec a flaky lambda that fails twice then succeeds.
