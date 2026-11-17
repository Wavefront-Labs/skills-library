---
id: computing-software.software-engineering.ruby.ruby-retry-backoff
name: ruby-retry-backoff
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, retry-backoff, resilience]
level: practitioner
status: docs-checked
description: "Retry flaky Ruby operations safely: rescue specific classes, retry semantics, re-raise, ensure and the infinite-loop risk."
sources: ["https://docs.ruby-lang.org/en/master/syntax/exceptions_rdoc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retry mechanics in Ruby

```ruby
def with_retries(max: 5)
  attempts = 0
  begin
    attempts += 1
    yield attempts
  rescue ArgumentError, NameError => e     # list only the classes you mean to retry
    raise if attempts >= max               # bare raise re-raises the current exception
    sleep(0.1 * 2**attempts)               # backoff choice is yours; the Ruby docs do not prescribe one
    retry                                  # resumes at the start of the begin block
  end
end
```
- `retry` is valid only inside a `rescue` block; any other use raises a SyntaxError. Execution resumes at the start of the `begin` block, so everything in that block, including side effects before the failing line, runs again. To retry a block iteration use `redo`.
- Without a retry cap the loop is infinite: Ruby's docs warn to be careful not to create one.
- A bare `rescue` handles StandardError and its subclasses; list specific classes after `rescue` to narrow it. The rescue clauses are matched from the top and match only once, so put specific classes before a bare `rescue`.
- `rescue => exception` assigns the exception; `raise` with no arguments inside the rescue re-raises it.
- A `begin/end`, method, class, module or block body can carry `rescue` without an explicit `begin`.
- `ensure` always runs, whether or not an exception was raised, and does not implicitly return a value. `else` runs only when no exception was raised.

## Gotchas
- Retrying anything that is not idempotent repeats its side effects; design the operation so a repeat is safe before wrapping it.
- Sleep, jitter, `Retry-After`, deadline handling and which errors are transient are application design: the page read covers only the language mechanics above.

## Checked

Date: 2026-11-08. Read in full: the Ruby syntax documentation for exceptions (the raw rdoc source on GitHub). The AWS Builders Library page was not read, so it was dropped from the sources and all backoff, jitter, status-code (429/502/503/504), idempotency-key, monotonic-clock and stacked-retry claims were removed, as were specific Net:: and Errno:: classes and `rescue Exception` claims.

Method: documentation only; no commands were run.
