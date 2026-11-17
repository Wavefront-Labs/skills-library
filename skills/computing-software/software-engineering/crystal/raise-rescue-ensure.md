---
id: computing-software.software-engineering.crystal.raise-rescue-ensure
name: raise-rescue-ensure
category: computing-software
field: software-engineering
product: crystal
tags: [raise-rescue-ensure, exceptions, raise, rescue, ensure, else, begin, exception-handling, reraise, try-catch, crystal]
level: intro
status: draft
description: "Raise exceptions, rescue by type with variable binding, use else and ensure, method-level rescue and re-raise."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# raise, rescue, else and ensure

Goal: handle errors predictably.

```crystal
begin
  risky
rescue ex : ArgumentError | KeyError
  puts ex.message
rescue ex
  raise ex          # re-raise
else
  puts "ok"
ensure
  cleanup
end
```
- `raise "msg"` raises `Exception`; `raise MyError.new("msg")`; `ex.message`, `ex.cause`, `ex.backtrace`, `ex.inspect_with_backtrace`.
- Method-level: `def f ... rescue ... ensure ... end` without begin.
- A rescue-free `begin/end` can be an expression returning a value.
- Common: `IndexError`, `KeyError`, `ArgumentError`, `TypeCastError`, `NilAssertionError`, `IO::Error`, `File::NotFoundError`, `JSON::ParseException`.

Gotchas:
- Exceptions are not for control flow in hot paths (costly).
- `ensure` runs on `return`, `break`, `next` too.
- A bare `rescue` catches `Exception` subclasses, not process signals.

Verify: spec with `expect_raises(KeyError) { h["x"] }`.
