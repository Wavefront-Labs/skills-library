---
id: computing-software.software-engineering.objective-c.kvc-collection-operators
name: kvc-collection-operators
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-kvc-kvo, kvc-collection-operators]
level: advanced
status: docs-checked
description: "Use @avg, @count, @max, @min, @sum, @distinctUnionOfObjects and the other collection operators in valueForKeyPath: to aggregate collections."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueCoding/CollectionOperators.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KVC collection operators
**Goal:** aggregate collections with key paths instead of loops.

```objc
NSNumber *transactionAverage = [self.transactions valueForKeyPath:@"@avg.amount"];
NSNumber *numberOfTransactions = [self.transactions valueForKeyPath:@"@count"];
NSDate *latestDate = [self.transactions valueForKeyPath:@"@max.date"];
NSNumber *amountSum = [self.transactions valueForKeyPath:@"@sum.amount"];
NSArray *distinctPayees = [self.transactions valueForKeyPath:@"@distinctUnionOfObjects.payee"];
```
- An operator is a keyword preceded by `@` inside a key path passed to `valueForKeyPath:`. The part before it is the left key path (the collection); the part after is the right key path (the property to operate on). Every operator except `@count` needs a right key path. When sent to a collection directly, the left key path may be omitted.
- Aggregation operators return one value: `@avg`, `@count`, `@max`, `@min`, `@sum`. `@avg` and `@sum` convert each value to a double (nil counts as 0) and return an `NSNumber`. `@count` takes no right key path (it is ignored if given) and returns an `NSNumber`. `@max` and `@min` compare with `compare:`, so the property must respond to it.
- Array operators return an `NSArray` of objects for the right key path: `@distinctUnionOfObjects` removes duplicates, `@unionOfObjects` keeps them. They raise an exception if any leaf object is nil.
- Nesting operators work on collections of collections and return an `NSArray` or `NSSet`: `@distinctUnionOfArrays`, `@unionOfArrays`, `@distinctUnionOfSets`. They also raise an exception for a nil leaf object.

## Gotchas
- A nil leaf in an array or nesting operator path raises an exception rather than being skipped.

## Self-check
Compare `@sum.amount` with a hand-written loop in a unit test, including a case with a nil amount.

## Checked
2026-11-03. Confirmed against Apple's Key-Value Coding Programming Guide, "Collection Operators" (operator format, aggregation, array and nesting operators, nil behaviour). Removed: the claim that operators are not extensible, the result-type summary, the empty-collection `@sum` / `@avg` figures and the undefined-key exception remark (not on the page).
Method: documentation only; no commands were run.
