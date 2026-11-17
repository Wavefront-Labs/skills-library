---
id: computing-software.software-engineering.lua.lua-math-random-library
name: lua-math-random-library
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-math, math-random-library]
level: practitioner
status: docs-checked
description: "Use the math library correctly including seeding, integer conversion and range pitfalls."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# math.random seeding, floor, tointeger and ranges
- Lua 5.4 initialises the generator with the equivalent of `math.randomseed()` with no arguments, so sequences differ per run; call `math.randomseed(42)` for a reproducible sequence (`x` and `y` form a 128-bit seed, equal seeds give equal sequences). `math.randomseed` returns the two seed components used.
- `math.random()` gives a float in [0, 1); `math.random(m, n)` an integer in [m, n]; `math.random(n)` is `math.random(1, n)`; `math.random(0)` gives an integer with all bits random. The algorithm is xoshiro256**.
- `math.tointeger(x)` returns an integer if `x` is convertible, otherwise fail; `math.floor(x)` returns the largest integral value not above `x`.
- `math.huge`, `math.maxinteger`, `math.mininteger`, `math.ult(m, n)` (unsigned comparison); `x ~= x` is true only for NaN.
- The generator is not documented as cryptographically secure; use an OS source or a vetted library for secrets.
Verify: with a fixed seed two runs print identical values.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: math.random, math.randomseed, math.tointeger, math.floor, math.huge, math.maxinteger, math.mininteger, math.ult, section 3.4.4 (NaN), section 8.2 (new seeding and algorithm). Removed: 5.1/5.2 seeding advice with `os.time()`, the 'empty interval error' wording and the `/dev/urandom` suggestion.
Method: documentation only; no commands were run.
