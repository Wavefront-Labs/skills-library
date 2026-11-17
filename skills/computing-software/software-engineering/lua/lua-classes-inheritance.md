---
id: computing-software.software-engineering.lua.lua-classes-inheritance
name: lua-classes-inheritance
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-oop, classes-inheritance]
level: practitioner
status: docs-checked
description: "Build classes with metatables, the colon call syntax, inheritance and avoid shared-state bugs."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prototype classes, inheritance and the colon syntax
- `local Account = {}; Account.__index = Account; function Account.new(b) return setmetatable({balance = b}, Account) end; function Account:deposit(v) self.balance = self.balance + v end`.
- The `__index` event fires when the key is absent from the table; its metavalue may be a function (called with table and key) or a table (indexed with the key, a regular non-raw index that can trigger another `__index`). That chain is what makes inheritance work.
- Inheritance: `setmetatable(Savings, {__index = Account})`; call parent with `Account.deposit(self, v)`.
- Putting a mutable table in the class (not in `new`) shares it across instances, because instances find it through `__index` instead of owning a copy.
- `v:name(args)` is sugar for `v.name(v, args)`, so calling `obj.method()` instead of `obj:method()` leaves `self` nil.
- Private state via closures or upvalues; there are no access modifiers.
Verify: create two instances and mutate one; the other must be unaffected.

## Checked
2026-11-08. Confirmed in the Lua 5.4 Reference Manual: section 2.4 (`__index` metamethod behaviour) and section 3.4.10 (the `v:name(args)` sugar), read via targeted searches rather than a full read of the manual. Removed nothing of substance; added the manual's wording for the `__index` chain.
Method: documentation only; no commands were run.
