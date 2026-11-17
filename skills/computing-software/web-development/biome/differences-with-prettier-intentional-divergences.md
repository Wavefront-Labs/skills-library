---
id: computing-software.web-development.biome.differences-with-prettier-intentional-divergences
name: differences-with-prettier-intentional-divergences
category: computing-software
field: web-development
product: biome
tags: [biome, prettier-differences, unquote-properties, bogus-nodes, parser-strictness, computed-keys, non-null-assertion, trailing-comma-type-parameters]
level: advanced
status: docs-checked
description: "Intentional output differences from Prettier: unquoting ES2015 identifiers, computed-key assignments, type-parameter commas, non-null chains."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/formatter/differences-with-prettier.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Biome matches Prettier closely but diverges in a few documented places. Language coverage gaps are on the language support page.

1. **Property unquoting.** Both unquote object and class property names that are valid identifiers, but Prettier only unquotes valid ES5 identifiers (a legacy limit). Biome unquotes all valid identifiers in ES2015+, so `"𐊧": true` becomes `𐊧: true`. A possible future workaround is a configured ECMAScript version where `ES5` would match Prettier.
2. **Assignments in computed keys.** Both parenthesise some assignment expressions (so a comparison typo is visible). Prettier is inconsistent: it adds parentheses for an object computed key `[x = 0]` but not for a class property. Biome omits the parentheses in both for consistency.
3. **Trailing comma in arrow type parameters.** A comma is needed in `<T,>() => {}` to distinguish from JSX, but not when a default type is given. Prettier still adds it to `<T = unknown,>() => {}`; Biome prints `<T = unknown>() => {}`, matching the original intent of adding commas only when required.
4. **Parenthesised non-null-asserted optional chains.** In TypeScript `(a?.b)!` and `a?.b!` are equivalent. Prettier keeps whichever you wrote (and moves the operator outside parentheses); Biome normalises.
5. **Invalid syntax.** Prettier's loose Babel-based parsing ignores many errors and formats the tree; Biome's parser is stricter and reports them: duplicate modifiers, invalid modifier order, function declarations with bodies, abstract properties in non-abstract classes, assigning to an optional chain, `const` on an interface type parameter in the wrong order, top-level `return`. Such code becomes **bogus nodes** printed verbatim, with no formatting, so nothing is changed that could alter semantics. Prettier tracks modifiers as booleans (one of each kind) while Biome keeps a list, which is why duplicates are detected and preserved.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the 'Practical effect' paragraph and the invented Verify step. The page's example in item 4 reads `a.?.b!` (a typo); the skill writes `?.`.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
