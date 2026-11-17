---
id: computing-software.software-engineering.crystal.custom-exceptions
name: custom-exceptions
category: computing-software
field: software-engineering
product: crystal
tags: [custom-exceptions, exceptions, custom-exception, exception-class, error-hierarchy, cause, message, domain-error, crystal]
level: practitioner
status: draft
description: "Define exception hierarchies with context fields and messages, chain causes and map error types at API boundaries."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom exception classes

Goal: expressive error types.

```crystal
class AppError < Exception; end
class NotFound < AppError
  getter id : Int32
  def initialize(@id)
    super("record #{@id} not found")
  end
end
raise NotFound.new(7)
```
- Inherit `Exception` (not `Error`, no such class); keep one root class per library for easy rescue.
- Chain: `raise Wrapped.new("ctx", cause: ex)` or `Exception.new(msg, cause)`.
- Translate low-level errors at module boundaries, not deep inside.

Gotchas:
- Default `message` is the class name if no message is given.
- Exceptions carry backtraces captured at raise time; large objects in fields stay alive.
- Uncaught exceptions exit with status 1 and print the backtrace to stderr.

Verify: `expect_raises(NotFound, /7/)` in a spec.
