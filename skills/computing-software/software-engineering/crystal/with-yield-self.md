---
id: computing-software.software-engineering.crystal.with-yield-self
name: with-yield-self
category: computing-software
field: software-engineering
product: crystal
tags: [with-yield-self, closures, with-yield, dsl, builder, implicit-receiver, instance-eval, crystal]
level: advanced
status: draft
description: "Build DSL-style blocks using with obj yield to evaluate a block in another receiver's scope."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# with ... yield and DSL blocks

Goal: write builder DSLs.

```crystal
class Html
  def p(t); @buf << "<p>#{t}</p>"; end
  def build
    with self yield self
    @buf.to_s
  end
end
```
- `with obj yield` makes unqualified calls in the block resolve against `obj` first, then self; passing `self` as the argument too lets users write `|h|` explicitly.
- Used by Crystal's `Spec` DSL style helpers and `HTTP::Server` route libs.

Gotchas:
- Name collisions between the block's outer scope and obj resolve to obj.
- Type errors show up inside the block site; keep DSL methods small and annotated.
- Not available for procs, only for `yield` in a method.

Verify: spec output string equals the expected HTML.
