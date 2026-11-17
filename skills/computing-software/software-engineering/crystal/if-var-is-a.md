---
id: computing-software.software-engineering.crystal.if-var-is-a
name: if-var-is-a
category: computing-software
field: software-engineering
product: crystal
tags: [if-var-is-a, flow-typing-is-a, is-a, narrowing, type-test, flow-typing, negation, crystal]
level: practitioner
status: docs-checked
description: "Narrow Crystal types with if var.is_a?(Type): then and else branches, && conditions and the instance-variable limit."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/if_varis_a.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/if_var.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# if var.is_a?(Type) narrowing

Goal: use is_a? to narrow.

```crystal
a = some_condition ? 1 : "hello"   # Int32 | String
if a.is_a?(Number)
  # a : Int32
else
  # a : String
end
```
- In the `then` branch the variable is restricted to the tested type; in the `else` branch it is restricted to the types that do not match.
- Any type works as the test, including abstract classes and modules.
- It works with `&&`: `a.is_a?(String) && b.is_a?(Number)` restricts both in the body.
- Reassigning the variable in the branch gives it the assigned expression's type.

Gotchas:
- Works only for local variables, not instance variables, class variables, constants, variables bound in a closure, or method/getter calls. Copy first: `a = @a` or `if (a = @a).is_a?(String)`.

Verify: call a member-specific method inside the branch and outside; the second must fail to compile.

## Checked
Checked 2026-11-02 against the crystal-book `if var.is_a?` and `if var` pages. Removed: `unless`/`!` complement narrowing, `||` union narrowing, subclass/module truth remark.

Method: documentation only; no commands were run.
