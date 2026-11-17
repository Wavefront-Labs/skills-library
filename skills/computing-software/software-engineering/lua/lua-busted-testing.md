---
id: computing-software.software-engineering.lua.lua-busted-testing
name: lua-busted-testing
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-testing, busted-testing]
level: practitioner
status: docs-checked
description: "Write BDD tests with busted and luassert, mock with spies and stubs and run in CI."
sources:
  - https://lunarmodules.github.io/busted/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# busted specs, assertions, spies and luassert
- `describe("name", function() it("works", function() assert.same(expected, actual) end) end)`; `before_each` / `after_each` run around each child test, `setup` / `teardown` run once per `describe` block (lazy and strict variants exist).
- luassert: `assert.same(a, b)` is deep equality; `assert.has_error(function() ... end, "msg")` checks the error message.
- Spies, stubs and mocks: `local s = spy.on(obj, "method")` wraps in place, `assert.spy(s).was.called_with(1)`; `stub(obj, "method")` replaces without calling the function; `mock(obj)` spies on a table's functions and `mock(obj, true)` stubs them. `match.is_ref(obj)` matches the self argument.
- Run `busted [OPTIONS] [ROOT...]`; `-o` picks the output library (TAP-compatible output is available), `-p` sets the file pattern (default `_spec`, so name files `*_spec.lua`), `-c` / `--coverage` runs code coverage and needs LuaCov installed.
Verify: break the function under test and see the failing spec.

## Checked
2026-11-08. Confirmed in the busted documentation page (lunarmodules.github.io/busted), read via targeted searches across usage, hooks, assertions, spies/stubs/mocks. Removed: unverified luassert helpers (`assert.is_true`, `assert.near`), the `busted -o TAP spec/` form, `luacov` report step and the `spec/` directory convention.
Method: documentation only; no commands were run.
