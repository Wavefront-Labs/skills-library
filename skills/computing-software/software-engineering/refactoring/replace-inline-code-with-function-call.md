---
id: computing-software.software-engineering.refactoring.replace-inline-code-with-function-call
name: replace-inline-code-with-function-call
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, replace-inline-code-with-function-call, duplication, standard-library, moving-features]
level: practitioner
status: draft
description: "Replace inline code that duplicates an existing function (often a library or standard-library call) with a call to it, checking the semantics really match."
sources: ["https://refactoring.com/catalog/replaceInlineCodeWithFunctionCall.html", "https://martinfowler.com/books/refactoring.html", "https://docs.python.org/3/library/functions.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Replace Inline Code with Function Call

**Motivation:** functions name behaviour and centralise it. When you see code doing what an
existing function already does, call the function: you gain a name and one place to fix bugs.
Especially valuable when the function is in the standard library or a well-known library.

```js
// before
let appliesToMass = false;
for (const s of states) { if (s === "MA") appliesToMass = true; }
// after
const appliesToMass = states.includes("MA");
```

## Mechanics
1. Replace the inline code with a call to the existing function.
2. Test.

## Check semantics before swapping
Library functions often differ at the edges from hand-written code:
- Null/empty handling (`StringUtils.isBlank` vs your `s.trim().isEmpty()` on null).
- Rounding modes (`Math.round` half-up vs `BigDecimal.setScale(HALF_EVEN)`; Python `round()` is
  banker's rounding).
- Locale and case (`toLowerCase()` without `Locale.ROOT` and the Turkish dotless i).
- Equality semantics (`includes` uses SameValueZero, so `NaN` matches; `indexOf` uses `===`, so it doesn't).
- Stable vs unstable sorting, inclusive/exclusive ranges, character vs code point counting.
Characterisation tests over the edge cases make these differences visible.

## Common targets
Hand-rolled loops replaceable by `any/all/sum/min/max/sorted`, `Collections.max`, LINQ, `Array.prototype.some`;
date arithmetic replaced by `java.time`/`datetime`; string padding/joining; path joining
(`os.path.join`, `Path.of`); URL building (`URLSearchParams`, `urllib.parse.urlencode`) which also fixes
escaping bugs.

## Difference from Extract Function
Extract Function creates a new function from the code; this refactoring applies when the function
already exists. If several snippets duplicate each other but no function exists, extract first,
then replace the others with calls.
