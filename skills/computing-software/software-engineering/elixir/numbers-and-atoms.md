---
id: computing-software.software-engineering.elixir.numbers-and-atoms
name: numbers-and-atoms
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, integer, float, atom, division, rem, div, numbers-atoms, elixir-basic-types]
level: intro
status: docs-checked
description: "Atoms are constants named by themselves; know / versus div/rem, ==/===, truthiness operators and the atom limit."
sources: ["https://hexdocs.pm/elixir/basic-types.html", "https://hexdocs.pm/elixir/Kernel.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integers, floats and atoms

**Goal:** pick the right numeric operator and understand atoms before using them as keys and tags.

```elixir
10 / 2            #=> 5.0   `/` always returns a float
div(10, 2)        #=> 5     integer division
rem(5, 2)         #=> 1     truncated division, sign of the dividend
rem(6, -4)        #=> 2
Integer.mod(5, 2) #=> 1     floored division, sign of the divisor
Integer.mod(6, -4) #=> -2
round(3.58)       #=> 4     closest integer
trunc(3.58)       #=> 3     integer part
1 == 1.0          #=> true  ;  1 === 1.0  #=> false (strict)
:apple == :apple  #=> true  (atoms are equal if their names are equal)
```

## Rules
- Atoms are constants whose value is their own name, often used for states such as `:ok` and `:error`; `true`, `false` and `nil` are atoms.
- Atoms are not garbage collected and the VM limits them (default 1 048 576). Do not convert uncontrolled strings to atoms; use `String.to_existing_atom/1` (or `/2` with an allowed list) or keep strings.
- `or`, `and`, `not` are strict: they expect booleans (at least the first argument). `||`, `&&`, `!` accept any value; only `false` and `nil` are falsy (`0` and `""` are truthy). Use the strict ones when you expect booleans.
- `==` treats integers and floats with the same value as equal; use `===`/`!==` to distinguish them.
- `rem/2` and `Integer.mod/2` raise `ArithmeticError` for a zero divisor or non-integer arguments.
- Comparison operators work across data types (structural comparison); see the `Kernel` docs on structural vs semantic comparison before relying on it.

## Self-check
`div(7, 2)` is `3`, `rem(7, 2)` is `1`, `7 / 2` is `3.5`.

## Checked
Date: 2026-11-02. Confirmed against the Elixir basic-types guide and Kernel.rem/2, Integer.mod/2, round, trunc docs (/ returns float, div, rem sign, Integer.mod sign, ==/===, atoms equal by name, truthiness operators, atom limit via the anti-patterns page). Removed: bignum claim, 0.1+0.2, round(2.5), Decimal advice, module-name atom, cross-type term order claim.
Method: documentation only; no commands were run.
