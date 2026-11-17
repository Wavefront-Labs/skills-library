---
id: computing-software.software-engineering.crystal.proc-literals-callbacks
name: proc-literals-callbacks
category: computing-software
field: software-engineering
product: crystal
tags: [proc-literals-callbacks, closures, callbacks, event-handler, observer, proc-array, handler-signature, crystal]
level: practitioner
status: draft
description: "Store lists of callbacks, pass them to other fibers and define typed handler signatures safely."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Proc callbacks and event handlers

Goal: build a simple observer.

```crystal
class Bus
  alias Handler = String -> Nil
  @handlers = [] of Handler
  def on(&h : Handler) : Nil
    @handlers << h
  end
  def emit(m : String)
    @handlers.each &.call(m)
  end
end
```
- Use `alias` to name the signature.
- Remove handlers by comparing proc identity (`==`) or return an id.

Gotchas:
- Proc with `Nil` return discards values only if declared `-> Nil`.
- Exceptions in one handler abort the loop; wrap and log.
- Cross-thread use with `-Dpreview_mt` needs a Mutex around the array.

Verify: spec that emit calls each handler in order.
