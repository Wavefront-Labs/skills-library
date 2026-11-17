---
id: computing-software.software-engineering.refactoring.replace-loop-with-pipeline
name: replace-loop-with-pipeline
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, moving-features, replace-loop-with-pipeline, collection-pipeline, map-filter-reduce, streams, fowler-catalog]
level: practitioner
status: verified
description: "Replace Loop with Pipeline: rewrite accumulation loops as map/filter/reduce chains (streams, LINQ, comprehensions), including laziness, debugging and when loops stay clearer."
sources:
  - https://refactoring.com/catalog/replaceLoopWithPipeline.html
  - https://martinfowler.com/articles/collection-pipeline/
  - https://martinfowler.com/articles/refactoring-pipelines.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replace Loop with Pipeline

## Before / after
```javascript
const names = [];
for (const i of input) {
  if (i.job === "programmer") names.push(i.name);
}
// after
const names = input.filter(i => i.job === "programmer").map(i => i.name);
```
(Run in Node: the loop and the `filter`/`map` chain produce identical arrays.) Java `stream().filter().map().toList()`, C# LINQ `Where().Select()`, Python comprehension `[i.name for i in input if i.job == "programmer"]`, Kotlin `filter{}.map{}`, Rust iterator adapters.

## Mechanics
1. Create a variable for the loop's source collection.
2. Starting from the top of the loop body, replace each piece of behaviour with a pipeline operation: guard clauses become `filter`, transformations `map`, accumulation `reduce`/`sum`/`groupBy`, early exit `find`/`any`/`takeWhile`, skipping a header `slice(1)`/`skip(1)`.
3. Test after each operation.
4. Remove the loop; inline the source variable if it no longer helps.

## Laziness gotchas
- Java streams, LINQ, Python generators, Rust iterators are lazy: nothing runs until a terminal operation. Side effects inside `map` run late, maybe never, maybe twice if enumerated twice (LINQ `IEnumerable` re-enumeration hits the database again; materialise with `ToList()`).
- Java streams are single-use (Javadoc: operate on a stream only once); Python and JavaScript generators are exhausted after one pass (run on Python 3.14 and Node 20: a second `list(gen)` / `[...gen]` returned an empty list). LINQ queries defer execution until enumerated (Microsoft Learn).
- Do not put side effects in `map`/`filter`; use `forEach` at the end or keep a loop.

## When a loop stays
- Complex multi-accumulator state machines (a reduce with a tuple of five values is less readable).
- Need to `break` with partial results plus side effects.
- Hot inner loops where the language's pipeline allocates (benchmark; JIT/rustc usually optimise well).

## Debugging pipelines
Java `peek()`, IntelliJ Stream Trace debugger, splitting a chain across named intermediate variables temporarily.

## Verify
- [ ] Tests green after each converted step.
- [ ] No side effects inside map/filter lambdas; materialised once where re-enumeration would repeat work.
