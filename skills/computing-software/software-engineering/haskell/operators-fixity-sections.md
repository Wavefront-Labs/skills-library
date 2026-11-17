---
id: computing-software.software-engineering.haskell.operators-fixity-sections
name: operators-fixity-sections
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, operators, fixity, infixl, infixr, sections, backtick, operators-fixity-sections]
level: practitioner
status: docs-checked
description: "Define and use Haskell operators, set infixl/infixr/infix precedence 0-9, use operator sections and backtick infix functions, and avoid the minus-section trap."
sources: ["https://www.haskell.org/onlinereport/haskell2010/haskellch3.html", "https://www.haskell.org/onlinereport/haskell2010/haskellch4.html", "https://www.haskell.org/onlinereport/haskell2010/haskellch9.html", "https://www.haskell.org/onlinereport/haskell2010/haskellch10.html", "https://hackage.haskell.org/package/base/docs/Prelude.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operators, fixity and sections

**Goal:** define readable operators with correct precedence and use sections without surprises.

## Declaring
```haskell
infixr 5 +++            -- right associative, precedence 5 (0 lowest, 9 highest)
(+++) :: [a] -> [a] -> [a]
xs +++ ys = foldr (:) ys xs

infixl 6 `plus`         -- backticks make any function infix
plus :: Int -> Int -> Int
plus = (+)
```
Without a declaration an operator is `infixl 9`. A fixity declaration must be in the same declaration list as the
operator's definition (class methods may also be declared at top level), and an operator gets at most one. Prelude:
`$` is `infixr 0`, `.` is `infixr 9`, `++` is `infixr 5`, `==` is `infix 4`, `&&` is `infixr 3`, `||` is `infixr 2`,
`>>=` is `infixl 1`.

## Sections
`(`div` 2)`, `(2 ^)`, `(^ 2)` are sections: the operator with one argument supplied.
```haskell
map (* 2) [1,2,3]        -- [2,4,6]
map (`div` 2) [10,20]    -- [5,10]
```

## Gotchas
- `(- 1)` is the number negative one, not a section. Write `(subtract 1)` or `(\x -> x - 1)`.
- `infix` (non-associative) operators cannot chain: `a == b == c` is rejected.
- Unary minus has precedence 6 (the same as binary `-`): `- 2 ^ 2` is `-(2^2)` = -4, and `a + -b` is illegal.
- `$` is `infixr 0`, so `f $ g $ h x` is `f (g (h x))`.
- Always declare fixity for operators a library exports, or users get infixl 9 surprises.

## Self-check
- [ ] Mixed-operator expressions are parenthesised where precedence is not obvious.
- [ ] No `(- n)` used where a section was intended.

## Checked

2026-11-08. Confirmed against the Haskell 2010 Report (section 4.4.2 fixity declarations and Table 4.1, section 3.4 operator applications and negation, section 3.5 sections, section 10.6 fixity resolution, Prelude source for `.`, `&&`, `$`) and the base Prelude page for `||` (`infixr 2`). Removed: the NegativeLiterals and LexicalNegation line and the GHCi `:i` self-check (not in the pages read).
Method: documentation only; no commands were run.
