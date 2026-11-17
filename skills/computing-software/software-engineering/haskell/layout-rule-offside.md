---
id: computing-software.software-engineering.haskell.layout-rule-offside
name: layout-rule-offside
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, layout, indentation, where, let, do-block, parse-error, layout-rule-offside, haskell-syntax]
level: practitioner
status: docs-checked
description: "Haskell layout rule: how indentation opens and closes blocks after where, let, do and of, the parse-error(t) rule and common indentation errors."
sources: ["https://www.haskell.org/onlinereport/haskell2010/haskellch2.html", "https://www.haskell.org/onlinereport/haskell2010/haskellch3.html", "https://www.haskell.org/onlinereport/haskell2010/haskellch10.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/using-warnings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The layout rule

**Goal:** write indentation that the parser reads as intended, and decode "parse error on input" messages.

## How it works
After the keywords `where`, `let`, `do`, `of` the next token's column
opens an implicit block. Each following line at the same column starts a new item; a line indented further
continues the previous item; a line indented less closes the block.

```haskell
main :: IO ()
main = do
  let x = 1
      y = 2          -- aligns with x: same let block
  print (x + y)      -- dedent closes the let block, new do statement
  where
    helper = ()      -- where block, separate from do block
```

## Explicit braces
Layout is optional: `do { a; b }` and `let { x = 1; y = 2 } in x + y` are valid. Useful for one-liners in GHCi:
`let { f 0 = 1; f n = n * f (n-1) }`. An explicit open brace must be matched by an explicit close brace, and no layout
processing happens inside it for constructs outside the braces.

## parse-error(t) rule
An implicit block also closes when the next token would be a parse error. That is why `let x = 1 in x` on one
line works, and why `(case x of A -> 1)` closes at `)`. The report defines it as: the tokens so far plus the next
token t are an invalid prefix of the grammar, but the tokens so far plus a close brace are a valid prefix.

## Failure modes
- Tabs: the report puts tab stops 8 characters apart, so mixed tabs and spaces misalign. Use spaces only;
  `-Wtabs` warns about tabs and is on by default.
- An operator at line start inside `do` at the statement column is read as a new statement; indent continuation lines more.
- `where` scopes over all guards of one equation only, not across equations.
- `if exp [;] then exp [;] else exp` is the Haskell 2010 grammar, so inside `do` the `then` and `else` lines may sit at the
  same column as `if`.

## Self-check
- [ ] No tab characters in the file (no `-Wtabs` warnings).
- [ ] Every continuation line is indented strictly more than the start of its statement.
- [ ] The module compiles with no layout parse errors.

## Checked

2026-11-08. Confirmed against the Haskell 2010 Report (section 2.7 Layout, section 3 conditional grammar, section 10.3 layout algorithm): the four layout keywords, same, greater and lesser indentation, explicit braces, the parse-error(t) definition, tab stops 8 characters apart, optional semicolons in if/then/else; and the GHC User's Guide warnings page for `-Wtabs` (in the default warning set). Removed: the `\case` layout claim, the DoAndIfThenElse extension name, and the grep and `ghc -fno-code` self-checks.
Method: documentation only; no commands were run.
