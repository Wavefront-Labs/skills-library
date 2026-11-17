---
id: computing-software.software-engineering.ada.loops-exit
name: loops-exit
category: computing-software
field: software-engineering
product: ada
tags: [ada, loops-exit]
level: intro
status: draft
description: "Ada loop forms: while, for with 'reverse', for-of iteration, plain loop with exit when, and named loops."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Loops, exit and labels
```ada
for I in 1 .. 10 loop ... end loop;
for I in reverse 1 .. 10 loop ... end loop;
for E of Arr loop E := E + 1; end loop;       -- element iterator
Outer : while True loop
   loop exit Outer when Done; end loop;
end loop Outer;
```
- The loop variable is a constant local to the loop.
- Empty range (`1 .. 0`) runs zero times.
## Gotchas
- No continue statement; use an `if` or a nested block.
- `reverse 10 .. 1` loops zero times: reverse the range, not the bounds.
## Self-check
Print 5 downto 1 with `reverse 1 .. 5`.
