---
id: computing-software.software-engineering.crystal.nil-guards-and-unless
name: nil-guards-and-unless
category: computing-software
field: software-engineering
product: crystal
tags: [nil-guards-and-unless, nil-and-nilable, guard-clause, early-return, unless-nil, raise-on-nil, flat-code, crystal]
level: practitioner
status: draft
description: "Use guard clauses with return, next, break and raise to narrow nilable locals and keep code flat."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nil guards and early returns

Goal: narrow after a guard.

```crystal
def render(user : User?)
  return "guest" unless user
  user.name   # user is User here
end
```
- Any branch that cannot fall through (return, raise, next, break, exit, NoReturn) narrows the variable afterwards.
- For hash lookup: `v = h["k"]? || return nil`.
- `raise ArgumentError.new("missing") if x.nil?` narrows x after the line.

Gotchas:
- Narrowing does not apply to `@ivar` or method calls; assign to a local first.
- A guard inside a block exits only the block when using `next`.
- Compound conditions `unless a && b` narrow only for the true side logic; test each separately if unsure.

Verify: compile; calling `user.name` before the guard must fail with the Nil error.
